## Taxonomy Confirmation Format

The taxonomy classification has two parts that must be presented
separately. Do not merge them, and do not invent dimensions.

### Part 1: Platform type

Platform type is a higher-level classification that situates the platform
within the broader DPO category structure. Possible values:

- One-sided platform | Two-sided platform | Multi-sided platform
- Centralization: Centralized | Decentralized
- User affiliation: Registration | Transaction | Investment
- Participation: P2P | B2C | B2B | C2C

Most digital marketplaces are multi-sided, decentralized, registration +
transaction, P2P. Confirm by reading the platform description.

### Part 2: Marketplace taxonomy

When the platform is a digital marketplace, classify it according to the
eleven taxonomy dimensions from Derave et al. Use exactly the dimensions
and value names below. Do not invent dimensions or values. If a dimension
genuinely does not apply, mark it "Not applicable" rather than skipping it.

| Dimension              | Allowed values                                                  | Notes                                                |
| ---------------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| User Type              | Person, Organization                                            | Mandatory. Indicate provider type and customer type. |
| Listing Type           | Good Transfer, Service                                          | Mandatory.                                           |
| Listing Kind           | Physical Good, Digital Good, Offline Service, Online Service    | Mandatory. Dependent on Listing Type.                |
| Frequency              | One-Time, Recurring                                             | Exclusive. Dependent on Service.                     |
| Quantity               | One, Many                                                       | Mandatory. Exclusive.                                |
| Price Discovery        | Set by Provider, Set by Customer, Set by Market                 | Exclusive.                                           |
| Price Calculation      | By Quantity, By Feature, Auction, Quote                         | Dependent.                                           |
| Conversation System    | Listing Conversation, Booking Conversation                      | Either, both, or neither.                            |
| Review System          | By Customer, By Provider                                        | Either, both, or neither.                            |
| Revenue Stream         | Subscription, Commission, Fixed Fee, Listing Fee                | Multiple values allowed.                             |
| Revenue Source         | Customer, Provider                                              | Dependent on Revenue Stream.                         |

### Output template

Present the taxonomy classification using this exact structure:

Platform type

One-sided / Two-sided / Multi-sided [pick one]
Centralization: Centralized / Decentralized [pick one]
User affiliation: Registration + Transaction
Participation: P2P

Marketplace taxonomy 

User Type: [Person | Organization] (Provider) and [Person | Organization] (Customer)
Listing Type: [Good Transfer | Service]
Listing Kind: [Physical Good | Digital Good | Offline Service | Online Service]
Frequency: [One-Time | Recurring | both]
Quantity: [One | Many]
Price Discovery: [Set by Provider | Set by Customer | Set by Market]
Price Calculation: [By Quantity | By Feature | Auction | Quote]
Conversation System: [Listing Conversation | Booking Conversation | both | none]
Review System: [By Customer | By Provider | both | none]
Revenue Stream: [Subscription | Commission | Fixed Fee | Listing Fee]
Revenue Source: [Customer | Provider]

After presenting the classification, ask the user to confirm or adjust any
of the dimensions before generating the ontology. Use a short closing
prompt such as: "Does this classification look right? Anything you'd
change before I generate the ontology?"

### What not to include

Do not add ad-hoc dimensions like "Discovery model," "Community structure,"
"Exchange object," or any other free-form characterization of the platform.
Those belong in the design narrative, not the taxonomy classification. The
taxonomy is fixed at eleven dimensions; descriptive narrative comes
separately.