import streamlit as st
from openai import OpenAI

from validator import validate, build_repair_prompt, Finding
from backend.envelope import extract_envelope

st.set_page_config(page_title="Ontology Assistant", layout="wide")


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
        "repair_pending": False,
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
# Assistant streaming
# ---------------------------------------------------------------------------

def _stream_reply(messages: list[dict]):
    """Generator that yields text deltas from the Responses API stream."""
    with get_client().responses.stream(
        model=MODEL,
        input=messages,
        instructions=load_system_prompt(),
        tools=[{"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]}],
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta


def _run_assistant(messages: list[dict]) -> str:
    """Stream an assistant reply into a chat bubble; return the full text."""
    with st.chat_message("assistant"):
        return st.write_stream(_stream_reply(messages))


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

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Repair takes precedence over chat input if both fire in the same rerun.
    # (repair_pending is set by the side-panel button, which triggers st.rerun()
    # before the chat input can be processed.)
    if st.session_state.repair_pending:
        st.session_state.repair_pending = False
        reply = _run_assistant(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        _process_reply(reply)

    elif user_input := st.chat_input("Message…"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        reply = _run_assistant(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        _process_reply(reply)

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
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.repair_pending = True
            st.rerun()
