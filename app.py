import json
import logging
import time

import streamlit as st
from openai import OpenAI

from validator import validate, build_repair_prompt, Finding
from backend.envelope import extract_envelope, find_envelope

st.set_page_config(page_title="Ontology Assistant", layout="wide")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

LOG_DELTA_EVERY_N_EVENTS = 250


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def check_password() -> bool:
    if st.session_state.get("authenticated"):
        return True
    pw = st.text_input("Password", type="password")
    if pw and pw == st.secrets["app_password"]:
        st.session_state["authenticated"] = True
        st.rerun()
    elif pw:
        st.error("Wrong password.")
    return False


if not check_password():
    st.stop()


# ---------------------------------------------------------------------------
# Startup validation — fail loudly if secrets are missing
# ---------------------------------------------------------------------------

for _k in ("openai_api_key", "vector_store_id", "model"):
    if _k not in st.secrets:
        st.error(f"Missing required secret: {_k!r}. Add it to .streamlit/secrets.toml.")
        st.stop()

MODEL: str = st.secrets["model"]
VECTOR_STORE_ID: str = st.secrets["vector_store_id"]


# ---------------------------------------------------------------------------
# Cached resources
# ---------------------------------------------------------------------------

@st.cache_resource
def get_client() -> OpenAI:
    return OpenAI(api_key=st.secrets["openai_api_key"])


@st.cache_data
def load_system_prompt() -> str:
    with open("prompts/system_prompt.md", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

def _init_state() -> None:
    defaults = {
        "messages": [],
        "last_proposal": None,
        "last_report": None,
        # stream_pending: set to True whenever a user message has just been
        # appended and the assistant reply hasn't been fetched yet.
        "stream_pending": False,
        "chk_count": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_state()


# ---------------------------------------------------------------------------
# Report helpers
# ---------------------------------------------------------------------------

def _set_report(report) -> None:
    """Store a new validation report and unconditionally reset all chk_* state."""
    for key in list(st.session_state.keys()):
        if key.startswith("chk_"):
            del st.session_state[key]
    n = len(report.findings)
    st.session_state.chk_count = n
    for i in range(n):
        st.session_state[f"chk_{i}"] = True
    st.session_state.last_report = report


# ---------------------------------------------------------------------------
# Envelope element counting
# ---------------------------------------------------------------------------

def _count_elements(envelope: dict) -> tuple[int, int, int]:
    """Return (n_classes, n_relations, n_generalizations) from a flat contents list."""
    contents = envelope.get("model", {}).get("contents", [])
    classes = sum(1 for e in contents if e.get("type") == "Class")
    relations = sum(1 for e in contents if e.get("type") == "Relation")
    generalizations = sum(1 for e in contents if e.get("type") == "Generalization")
    return classes, relations, generalizations


# ---------------------------------------------------------------------------
# Message rendering
# ---------------------------------------------------------------------------

def _render_assistant_message(text: str, ts: str, idx: int) -> None:
    """Render an assistant message, replacing any JSON envelope with download UI.

    The original text in session_state is never modified — this is render-only.
    """
    result = find_envelope(text)
    if result is None:
        st.markdown(text)
        return

    envelope, start, end = result

    prose_before = text[:start].strip()
    prose_after = text[end:].strip()

    if prose_before:
        st.markdown(prose_before)

    n_classes, n_relations, n_gens = _count_elements(envelope)
    json_str = json.dumps(envelope, indent=2)
    filename = f"proposal_{ts if ts else idx}.json"

    st.download_button(
        label="Download JSON",
        data=json_str,
        file_name=filename,
        mime="application/json",
        key=f"dl_{idx}",
    )
    st.caption(f"{n_classes} classes, {n_relations} relations, {n_gens} generalizations")

    with st.expander("View JSON"):
        st.code(json_str, language="json")

    if prose_after:
        st.markdown(prose_after)


# ---------------------------------------------------------------------------
# Assistant generation
# ---------------------------------------------------------------------------

def _event_detail(event) -> str:
    """Return compact diagnostic info for non-delta Responses stream events."""
    parts = []
    sequence_number = getattr(event, "sequence_number", None)
    if sequence_number is not None:
        parts.append(f"seq={sequence_number}")

    response = getattr(event, "response", None)
    if response is not None:
        parts.append(f"response_id={getattr(response, 'id', None)}")
        parts.append(f"status={getattr(response, 'status', None)}")
        incomplete = getattr(response, "incomplete_details", None)
        if incomplete is not None:
            parts.append(f"incomplete={incomplete}")
        error = getattr(response, "error", None)
        if error is not None:
            parts.append(f"error={error}")

    item = getattr(event, "item", None)
    if item is not None:
        parts.append(f"item_type={getattr(item, 'type', None)}")

    error_code = getattr(event, "code", None)
    error_message = getattr(event, "message", None)
    if error_code is not None:
        parts.append(f"code={error_code}")
    if error_message is not None:
        parts.append(f"message={error_message}")

    return " ".join(parts)


def _log_response_summary(response, elapsed: float, output_chars: int) -> None:
    if response is None:
        logger.warning(
            "OpenAI response stream ended without a terminal response event "
            "elapsed=%.1fs output_chars=%d",
            elapsed,
            output_chars,
        )
        return

    usage = getattr(response, "usage", None)
    if hasattr(usage, "model_dump"):
        usage = usage.model_dump()

    logger.info(
        "OpenAI response finished id=%s status=%s elapsed=%.1fs output_chars=%d "
        "incomplete=%s error=%s usage=%s",
        getattr(response, "id", None),
        getattr(response, "status", None),
        elapsed,
        output_chars,
        getattr(response, "incomplete_details", None),
        getattr(response, "error", None),
        usage,
    )


def _collect_reply(messages: list[dict]) -> tuple[str, object | None]:
    """Collect a full streamed response without live-rendering every delta."""
    api_input = [{"role": m["role"], "content": m["content"]} for m in messages]
    chunks: list[str] = []
    delta_events = 0
    output_chars = 0
    final_response = None
    started_at = time.monotonic()

    logger.info(
        "Starting OpenAI response model=%s messages=%d input_chars=%d",
        MODEL,
        len(api_input),
        sum(len(m["content"]) for m in api_input),
    )

    with get_client().responses.stream(
        model=MODEL,
        input=api_input,
        instructions=load_system_prompt(),
        tools=[{"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]}],
    ) as stream:
        for event in stream:
            event_type = getattr(event, "type", "<unknown>")
            if event.type == "response.output_text.delta":
                chunks.append(event.delta)
                delta_events += 1
                output_chars += len(event.delta)
                if delta_events % LOG_DELTA_EVERY_N_EVENTS == 0:
                    logger.info(
                        "OpenAI stream event type=%s delta_events=%d output_chars=%d",
                        event_type,
                        delta_events,
                        output_chars,
                    )
                continue

            logger.info("OpenAI stream event type=%s %s", event_type, _event_detail(event))

            if event_type in {"response.completed", "response.incomplete", "response.failed"}:
                final_response = getattr(event, "response", None)

    reply = "".join(chunks)
    _log_response_summary(final_response, time.monotonic() - started_at, len(reply))
    return reply, final_response


def _format_generation_notice(response) -> str:
    if response is None:
        return (
            "Generation ended without a terminal Responses API event. "
            "Check the terminal logs for stream diagnostics."
        )

    status = getattr(response, "status", None)
    if status in (None, "completed"):
        return ""

    details = getattr(response, "incomplete_details", None) or getattr(response, "error", None)
    if details:
        return f"Generation status: {status}. Details: {details}"
    return f"Generation status: {status}."


def _run_assistant(messages: list[dict]) -> tuple[str, str]:
    """Generate a reply, then render it after completion."""
    with st.chat_message("assistant"):
        with st.spinner("Generating complete response..."):
            try:
                reply, response = _collect_reply(messages)
            except Exception as e:
                logger.exception("OpenAI response generation failed")
                notice = f"Generation failed: {type(e).__name__}: {e}"
                st.error(notice)
                return "", notice

        notice = _format_generation_notice(response)
        _render_assistant_message(reply, time.strftime("%H%M%S"), -1)
        if notice:
            st.warning(notice)
        return reply, notice


def _process_reply(reply: str) -> None:
    """Detect an OntoUML envelope in the reply and validate it if found."""
    envelope = extract_envelope(reply)
    if envelope is not None:
        st.session_state.last_proposal = envelope
        _set_report(validate(envelope))


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

col_chat, col_panel = st.columns([2, 1])

# ---- Chat column -----------------------------------------------------------

with col_chat:
    st.title("Ontology Assistant")

    with st.container(height=600):
        # Render conversation history inside the scrollable container.
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant":
                    _render_assistant_message(msg["content"], msg.get("ts", ""), i)
                    if msg.get("notice"):
                        st.warning(msg["notice"])
                else:
                    st.markdown(msg["content"])

        # Generate the next assistant turn inside the container.
        # stream_pending is set (with st.rerun()) by both the chat input handler
        # below and the repair button in the side panel, so the user message is
        # always in history and visible before generation begins.
        if st.session_state.stream_pending:
            st.session_state.stream_pending = False
            reply, notice = _run_assistant(st.session_state.messages)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply,
                    "notice": notice,
                    "ts": time.strftime("%H%M%S"),
                }
            )
            _process_reply(reply)
            st.rerun()

    # Chat input docks to the bottom of col_chat. On submit it appends the user
    # message and sets stream_pending, then reruns so the message appears in the
    # scrollable container before streaming starts.
    if user_input := st.chat_input("Message…"):
        st.session_state.messages.append(
            {"role": "user", "content": user_input, "ts": time.strftime("%H%M%S")}
        )
        st.session_state.stream_pending = True
        st.rerun()

# ---- Validation panel ------------------------------------------------------

with col_panel:
    st.subheader("Validation")
    report = st.session_state.last_report

    if report is None:
        st.caption("No proposal validated yet.")

    elif not report.has_findings():
        st.success("No issues found — proposal is valid.")

    else:
        errors = report.errors()
        warnings = report.warnings()

        count_parts: list[str] = []
        if errors:
            count_parts.append(f"{len(errors)} error{'s' if len(errors) != 1 else ''}")
        if warnings:
            count_parts.append(f"{len(warnings)} warning{'s' if len(warnings) != 1 else ''}")
        st.write(", ".join(count_parts))

        chk_count: int = st.session_state.chk_count

        for i, f in enumerate(report.findings):
            is_error = f.severity.value == "error"
            prefix = "🔴" if is_error else "🟡"
            header = f"{prefix} [{f.code}] {f.message}"
            if f.entity_name:
                header += f" ({f.entity_name})"
            with st.expander(header, expanded=is_error):
                if is_error:
                    st.error(f.message)
                else:
                    st.warning(f.message)
                st.checkbox("Include in repair", key=f"chk_{i}")
                if f.repair_hint:
                    st.info(f"Hint: {f.repair_hint}")

        additional: str = st.text_area(
            "Additional instructions (optional)",
            key="additional_instructions",
        )

        any_checked = any(
            st.session_state.get(f"chk_{i}", True) for i in range(chk_count)
        )
        repair_disabled = not (any_checked or bool(additional.strip()))

        if st.button("Send repair to assistant", type="primary", disabled=repair_disabled):
            selected: list[Finding] = [
                f
                for i, f in enumerate(report.findings)
                if st.session_state.get(f"chk_{i}", True)
            ]
            prompt = build_repair_prompt(selected, additional.strip())
            st.session_state.messages.append(
                {"role": "user", "content": prompt, "ts": time.strftime("%H%M%S")}
            )
            st.session_state.stream_pending = True
            st.rerun()

    # Clear conversation — always shown at the bottom of the panel
    st.divider()
    if st.button("Clear conversation", type="secondary"):
        st.session_state.messages = []
        st.session_state.last_proposal = None
        st.session_state.last_report = None
        st.session_state.stream_pending = False
        for key in list(st.session_state.keys()):
            if key.startswith("chk_") or key.startswith("dl_"):
                del st.session_state[key]
        st.session_state.chk_count = 0
        st.session_state["additional_instructions"] = ""
        st.rerun()
