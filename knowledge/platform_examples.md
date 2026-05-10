# Platform Example Ontologies

This document contains complete ontology examples for real and fictional digital platforms,
extracted from the DPO Visual Paradigm project. Each example shows the **full** platform-specific
ontology as it appears on the VP diagram — including both DPO base classes (KEEP) and
platform-specific NEW classes.

Each class is annotated with its source module (the DPO module it originated from). Classes from the
platform's own package are platform-specific (NEW). This shows the pattern of how DPO modules are
adapted and extended for a specific platform.

These examples serve as few-shot references: they show what a good platform ontology looks like,
how many classes are typical, and how domain-specific concepts relate to DPO patterns.

---
## SafaRide

> A digital marketplace for sharing safari jeep rides. Providers list available seats in their vehicles for specific parks and departure times. Travelers can search listings by park and number of seats, then book seats. Price is set per seat by the provider. Payment is handled externally via Stripe/PayPal. The platform takes a commission on each booking. After the trip, both customers and providers can leave reviews. Listing and transaction conversations are supported.

**Taxonomy selections:** multi_sided, registration, transaction, p2p, c2c, decentralized, listing_kind_service, listing_type_offline_service, frequency_one_time, quantity_many, price_discovery_set_by_provider, price_calculation_by_quantity, conversation_listing, conversation_transaction, review_by_customer, review_by_provider, review_of_provider, review_of_customer, revenue_stream_commission, revenue_source_customer, payment_system_external, under_utilized

**Summary:** 28 classes, 27 relations, 8 generalizations

**Classes (28):**

*From Commission:*
- `«subkind»` **Commission Fee**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Search**

*From External Payment:*
- `«event»` **External Payment**
- `«subkind»` **Payment Provider**

*From General: User Actions:*
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From General: User Roles:*
- `«roleMixin»` **Platform Visitor**

*From Registration:*
- `«roleMixin»` **Logged In User**
- `«event»` **Login** [checkEmail, checkPassword]
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]

*From Review By:*
- `«relator»` **Review** [score, comment]
- `«event»` **Review Creation** [setScore, givesComment]

*From Review by Customer:*
- `«event»` **Review Creation by Customer**

*From Review by Provider:*
- `«event»` **Review Creation by Provider**

*From SafaRide:*
- `«type»` **Car Type** [carTypeName, carTypeImage]
- `«subkind»` **Offered Price per Seat**
- `«kind»` **Park** [parkName, parkLocation]
- `«event»` **Set Filter**
- `«event»` **Set Price per Seat**
- `«roleMixin»` **Trip Customer**
- `«roleMixin»` **Trip Provider**

*From Service:*
- `«subkind»` **Booking** [personsBooked]

*From Transaction:*
- `«roleMixin»` **Customer**
- `«roleMixin»` **Listing Creator**
- `«roleMixin»` **Provider**
- `«roleMixin»` **Target Customer**

*From Transaction Conversation:*
- `«event»` **Transaction Conversation** [sendMessage]

**Relations (27):**

- Add Listing [1] --creates «creation»--> Listing [1]
- Set Price per Seat [1] --sets--> Offered Price per Seat [1..*]
- Trip Provider [1] --participates--> Set Price per Seat [1..*]
- Review [0..*] --linked to--> Trip Customer [1]
- Add Listing [1] --(unnamed) «participational»--> Set Price per Seat [1..*]
- Register [1..*] --performed by «participation»--> User [1]
- Park [1] --includes--> Listing [0..*]
- Listing Search [*] --for--> Listing [*]
- Listing Search [1] --includes--> Set Filter [*]
- Car Type [1] --includes--> Listing [0..*]
- Customer [1] --does--> Review Creation by Customer [0..*]
- Listing [1] --has--> Offered Price per Seat [1]
- External Payment [1..*] --intermediates--> Payment Provider [1]
- Listing [1] --conforms to--> Booking [0..*]
- Register [1] --followed by--> Login [0..*]
- Review [0..*] --linked to--> Trip Provider [1]
- Logged In User [1] --participates--> Login [1]
- Set Filter [0..*] --(unnamed)--> Target Customer [1]
- Transaction Conversation [0..*] --concerns--> Booking [1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Transaction Conversation [0..*] --participates--> Provider [1]
- Provider [1] --does--> Review Creation by Provider [0..*]
- Transaction Conversation [0..*] --participates--> Customer [1]
- Booking [1] --concerning--> Review [0..2]
- Booking [1..*] --from--> Trip Customer [1]
- External Payment [0..*] --(unnamed)--> Trip Customer [1]
- Review Creation [1] --creates--> Review [1]

**Generalizations (8):**

- Review Creation by Customer --|> Review Creation
- Logged In User --|> User
- Trip Provider --|> Logged In User
- Review Creation by Provider --|> Review Creation
- Trip Customer --|> Logged In User
- Target Customer --|> Platform Visitor
- Trip Customer --|> Target Customer
- User --|> Platform Visitor

---
## Airbnb

> A global accommodation marketplace. Homeowners list their properties (rooms, apartments, houses) with descriptions, photos, availability calendars, and pricing. Travelers search listings by location, dates, and guest count. Booking involves a transaction with internal payment processing. The platform takes a commission from both hosts and guests. Reviews are bidirectional. Hosts and guests can message before and during bookings.

**Taxonomy selections:** multi_sided, registration, transaction, decentralized, user_type_person, listing_kind_service, listing_type_offline_service, frequency_one_time, quantity_one, price_discovery_set_by_provider, price_calculation_by_quantity, conversation_listing, conversation_transaction, review_by_customer, review_by_provider, revenue_stream_commission, revenue_source_customer, payment_system_internal, under_utilized

**Summary:** 34 classes, 23 relations, 19 generalizations

**Classes (34):**

*From Airbnb:*
- `«subkind»` **Accommodation**
- `«subkind»` **Airbnb Booking**
- `«role»` **Airbnb Customer**
- `«roleMixin»` **Airbnb Home Seeker**
- `«roleMixin»` **Airbnb Host**
- `«roleMixin»` **Airbnb User**
- `«event»` **Book an accomodation**
- `«role»` **Private Airbnb Homeowner**
- `«event»` **Register on Airbnb**
- `«event»` **Rent Accomodation**
- `«event»` **Rent Out Own Home**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«event»` **Decentralized Transaction Creation**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«subkind»` **Listing Description**
- `«collective»` **Listing Overview**
- `«event»` **Listing Search**

*From General: User Actions:*
- `«roleMixin»` **Platform Company** [name]
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From General: User Roles:*
- `«roleMixin»` **Platform Visitor**

*From Good Transfer:*
- `«kind»` **Good**

*From Multi-Sided:*
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

*From P2P:*
- `«event»` **Automated Affiliation Action**
- `«roleMixin»` **Peer User**

*From Product-oriented:*
- `«event»` **Product-Oriented Delivery**

*From Registration:*
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Transaction:*
- `«event»` **Create Transaction**
- `«event»` **Delivery**
- `«event»` **Offering Creation**
- `«relator»` **Offering On The Platform** [attribute]

*From UFO-C:*
- `«kind»` **Person** [firstName, lastName, email, birthDate]

*From Under-Utilized:*
- `«subkind»` **Physical Good**

*From User-oriented :*
- `«event»` **User-Oriented Delivery**

**Relations (23):**

- Register [1] --creates «creation»--> Registration [1]
- Airbnb Host [1] --accepted by «participation»--> Create Transaction [1..*]
- Rent Accomodation [0..*] --by «participation»--> Airbnb Customer [1]
- Rent Out Own Home [0..*] --rented--> Accommodation [1]
- Listing Search [1..*] --uses «participation»--> Listing Overview [1]
- Listing Search [1..*] --performed by «participation»--> Airbnb Home Seeker [0..1]
- Automated Affiliation Action [1..*] --performed by «participation»--> Peer User [1]
- Listing Description [1..*] --is part of «memberOf»--> Listing Overview [1]
- Register [1..*] --performed by «participation»--> User [1]
- Listing [1] --described by «mediation»--> Listing Description [1]
- Transaction [1] --partially fulfills--> Delivery [0..*]
- Rent Accomodation [0..*] --rented «participation»--> Accommodation [1]
- Platform Company [1] --bounds «mediation»--> Registration [1..*]
- Listing Search [1..*] --results in «historicalDependence»--> Decentralized Transaction Creation [0..1]
- Platform Visitor [1] --performed by--> Listing Search [0..*]
- Offering Creation [1..*] --performed by «participation»--> Airbnb Host [1]
- Rent Accomodation [0..*] --made possible by «participation»--> Airbnb Host [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Create Transaction [1..*] --performed by «participation»--> Airbnb Customer [1]
- Private Airbnb Homeowner [1] --made possible by--> Rent Out Own Home [0..*]
- Create Transaction [1] --creates «creation»--> Transaction [1]
- Add Listing [1] --creates «creation»--> Listing [1]
- Accommodation [0..*] --personally uses «material»--> Private Airbnb Homeowner [0..1]

**Generalizations (19):**

- Rent Accomodation --|> User-Oriented Delivery
- Register on Airbnb --|> Register
- Private Airbnb Homeowner --|> Person
- Accommodation --|> Physical Good
- Private Airbnb Homeowner --|> Airbnb Host
- Product-Oriented Delivery --|> Delivery
- Airbnb Host --|> Peer User
- Rent Out Own Home --|> Rent Accomodation
- User-Oriented Delivery --|> Delivery
- Airbnb Home Seeker --|> Person
- Airbnb Home Seeker --|> Airbnb User
- Register on Airbnb --|> Automated Affiliation Action
- Airbnb Booking --|> Transaction
- Physical Good --|> Good
- Airbnb Host --|> Airbnb User
- Airbnb User --|> Peer User
- Book an accomodation --|> Create Transaction
- Listing --|> Offering On The Platform
- Airbnb Customer --|> Airbnb Home Seeker

---
## BlaBlaCar

> A carpooling/ride-sharing platform. Drivers list planned trips with departure/arrival locations, times, and available seats. Passengers search for matching trips and book seats. The driver sets the price per seat. Payment is handled through the platform. The car is personally used by the driver (under-utilized good). After the trip, passengers can review drivers.

**Taxonomy selections:** multi_sided, registration, transaction, p2p, c2c, decentralized, listing_kind_service, listing_type_offline_service, frequency_one_time, quantity_many, price_discovery_set_by_provider, price_calculation_by_quantity, review_by_customer, revenue_stream_commission, revenue_source_customer, payment_system_internal, under_utilized

**Summary:** 50 classes, 38 relations, 28 generalizations

**Classes (50):**

*From Auction:*
- `«subkind»` **Bid Price**

*From BlaBlaCar:*
- `«role»` **BlaBlaCar Driver**
- `«subkind»` **BlaBlaCar Listing** [point of time, start location, end  location, comment]
- `«role»` **BlaBlaCar Passenger**
- `«subkind»` **Booked Seat**
- `«subkind»` **Car**
- `«event»` **Drive Passengers**
- `«subkind»` **Free Seat**
- `«subkind»` **PayPal**
- `«kind»` **Seats**

*From C2C:*
- `«role»` **Person Platform Customer**
- `«role»` **Person Platform Provider**
- `«role»` **Registered C2C User** [name, email]

*From Commission:*
- `«subkind»` **Commission Fee**

*From Customer:*
- `«subkind»` **Revenue Stream Payed by Customer**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Search**

*From External Payment:*
- `«event»` **External Payment**
- `«subkind»` **Payment Provider**

*From General: User Actions:*
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From Good Transfer:*
- `«kind»` **Good**

*From Listing Conversation:*
- `«event»` **Listing Conversation**

*From Multi-Sided:*
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

*From Price Calculation:*
- `«subkind»` **Transaction Price**

*From Price Discovery:*
- `«quality»` **Price**

*From Product-oriented:*
- `«event»` **Product-Oriented Delivery**

*From Provider:*
- `«subkind»` **Revenue Stream Payed by Provider**

*From Quantity-based:*
- `«subkind»` **Price per Item**

*From Registration:*
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Result-oriented:*
- `«event»` **Result-Oriented Delivery**

*From Review By:*
- `«relator»` **Review** [score, comment]

*From Review by Customer:*
- `«subkind»` **Customer Review**
- `«event»` **Review Creation by Customer**

*From Review by Provider:*
- `«subkind»` **Provider Review**
- `«event»` **Review Creation by Provider**

*From Service:*
- `«subkind»` **Booking** [personsBooked]

*From Set by Provider:*
- `«subkind»` **Price set by Provider**

*From Transaction:*
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«event»` **Delivery**
- `«roleMixin»` **Listing Creator**
- `«roleMixin»` **Provider**
- `«roleMixin»` **Target Customer**

*From Transaction Conversation:*
- `«event»` **Transaction Conversation** [sendMessage]

*From UFO-C:*
- `«kind»` **Person** [firstName, lastName, email, birthDate]

*From Under-Utilized:*
- `«subkind»` **Physical Good**
- `«subkind»` **Under-Utilized Good**

*From User-oriented :*
- `«event»` **User-Oriented Delivery**

**Relations (38):**

- Bid Price [0..*] --has--> Listing [1]
- Listing Search [*] --for--> Listing [*]
- Registration [1..*] --bounds user «mediation»--> User [1]
- Transaction Conversation [0..*] --participates--> Provider [1]
- Review Creation by Provider [1] --by--> Provider Review [1]
- Add Listing [1] --sets--> Price set by Provider [0..*]
- Transaction Conversation [0..*] --participates--> Customer [1]
- Price per Item [1] --(unnamed)--> Free Seat [1..4]
- Register [1] --creates «creation»--> Registration [1]
- Booking [1] --(unnamed)--> External Payment [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Customer [1] --by--> Revenue Stream Payed by Customer [0..*]
- Listing [1] --concerns--> Listing Conversation [0..*]
- Review Creation by Customer [1] --By--> Customer Review [1]
- Register [1..*] --performed by «participation»--> User [1]
- Create Transaction [1..*] --accepted by «participation»--> Provider [1]
- Customer [1] --does--> Review Creation by Customer [0..*]
- Booked Seat [1..4] --(unnamed)--> Booking [1]
- Provider [1] --does--> Review Creation by Provider [0..*]
- Add Listing [1] --creates «creation»--> Listing [1]
- Target Customer [1] --initiates--> Listing Conversation [0..*]
- Create Transaction [1] --creates «creation»--> Transaction [1]
- External Payment [0..*] --(unnamed)--> BlaBlaCar Passenger [1]
- Customer Review [None] --(unnamed)--> BlaBlaCar Driver [None]
- Price per Item [1] --used for--> Transaction Price [0..*]
- Provider [1] --by--> Revenue Stream Payed by Provider [0..*]
- Product-Oriented Delivery [0..*] --involves «participation»--> Good [1..*]
- Review [0..2] --concerning--> Transaction [1]
- Transaction [1] --partially fulfills--> Delivery [0..*]
- Transaction Conversation [0..*] --concerns--> Booking [1]
- Provider Review [None] --(unnamed)--> BlaBlaCar Passenger [None]
- Result-Oriented Delivery [1..*] --performed by «participation»--> Provider [1..*]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Listing Conversation [0..*] --participates in--> Listing Creator [1]
- Delivery [0..*] --received by «participation»--> Customer [1..*]
- External Payment [1..*] --intermediates--> Payment Provider [1]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]

**Generalizations (28):**

- Price per Item --|> Bid Price
- Physical Good --|> Good
- Car --|> Under-Utilized Good
- User-Oriented Delivery --|> Result-Oriented Delivery
- Free Seat --|> Seats
- Price set by Provider --|> Bid Price
- Bid Price --|> Price
- Customer --|> User
- Customer --|> Target Customer
- User-Oriented Delivery --|> Product-Oriented Delivery
- Drive Passengers --|> Result-Oriented Delivery
- Booking --|> Transaction
- Provider --|> Listing Creator
- BlaBlaCar Passenger --|> Person Platform Customer
- BlaBlaCar Driver --|> Person Platform Provider
- Product-Oriented Delivery --|> Delivery
- Provider Review --|> Review
- Registered C2C User --|> User
- BlaBlaCar Listing --|> Listing
- Person Platform Provider --|> Provider
- Customer Review --|> Review
- Result-Oriented Delivery --|> Delivery
- Person Platform Customer --|> Customer
- Booked Seat --|> Seats
- User-Oriented Delivery --|> Delivery
- Under-Utilized Good --|> Physical Good
- PayPal --|> Payment Provider
- Listing Creator --|> User

---
## Couchsurfing

> A hospitality exchange platform where homeowners offer free accommodation to travelers. There is no payment — the platform operates on a gift economy model. Hosts list their homes with descriptions. Travelers search listings and send requests. Reviews are bidirectional. The platform monetizes through optional subscriptions.

**Taxonomy selections:** multi_sided, registration, decentralized, user_type_person, p2p, c2c, listing_kind_service, listing_type_offline_service, frequency_one_time, quantity_one, conversation_transaction, review_by_customer, review_by_provider, revenue_stream_subscription, under_utilized

**Summary:** 36 classes, 31 relations, 14 generalizations

**Classes (36):**

*From C2C:*
- `«role»` **Registered C2C User** [name, email]

*From Couchsurfing:*
- `«roleMixin»` **Couchsurfing Home Searcher**
- `«roleMixin»` **Couchsurfing Homeowner**
- `«subkind»` **Couchsurfing Listing** [description]
- `«roleMixin»` **Couchsurfing Lodger**
- `«event»` **Free Stay**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Search**

*From External Payment:*
- `«event»` **External Payment**
- `«subkind»` **Payment Provider**

*From General: User Actions:*
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From Listing Conversation:*
- `«event»` **Listing Conversation**

*From Multi-Sided:*
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

*From Offline Service:*
- `«mode»` **Listing Location**

*From Payment System:*
- `«event»` **Payment Action**

*From Recurring:*
- `«phase»` **Available time slot**
- `«phase»` **Booked Time Slot**

*From Registration:*
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Review By:*
- `«relator»` **Review** [score, comment]
- `«event»` **Review Creation** [setScore, givesComment]

*From Review by Customer:*
- `«event»` **Review Creation by Customer**

*From Review by Provider:*
- `«event»` **Review Creation by Provider**

*From Service:*
- `«subkind»` **Booking** [personsBooked]

*From Subscription:*
- `«roleMixin»` **Subscribed Platform User**
- `«event»` **Subscription Action**
- `«subkind»` **Subscription Fee**
- `«event»` **Subscription Payment Plan**

*From Transaction:*
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«roleMixin»` **Listing Creator**
- `«roleMixin»` **Provider**
- `«roleMixin»` **Target Customer**

*From Transaction Conversation:*
- `«event»` **Transaction Conversation** [sendMessage]

*From UFO-C:*
- `«kind»` **Person** [firstName, lastName, email, birthDate]

**Relations (31):**

- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Listing Search [0..*] --(unnamed)--> Couchsurfing Listing [0..*]
- Subscription Action [0..1] --Followed by «historicalDependence»--> Register [1]
- Booking [1] --captures--> Booked Time Slot [1..*]
- Review Creation [1] --creates--> Review [1]
- Free Stay [0..*] --for--> Couchsurfing Lodger [1]
- Transaction Conversation [0..*] --concerns--> Booking [1]
- Registration [1..*] --bounds user «mediation»--> User [1]
- Subscription Payment Plan [1] --includes «participational»--> Subscription Action [1]
- Listing [1] --conforms to--> Booking [0..*]
- Subscription Action [1..*] --performed by «participation»--> Subscribed Platform User [1]
- Provider [1] --does--> Review Creation by Provider [0..*]
- Subscription Fee [1..*] --of--> Subscription Payment Plan [1]
- Transaction Conversation [0..*] --participates--> Customer [1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Couchsurfing Homeowner [1] --organized by--> Free Stay [0..*]
- Listing Conversation [0..*] --participates in--> Listing Creator [1]
- Listing [1] --concerns--> Listing Conversation [0..*]
- Available time slot [1] --becomes «historicalDependence»--> Booked Time Slot [0..1]
- Booking [1] --concerning--> Review [0..2]
- Customer [1] --does--> Review Creation by Customer [0..*]
- Create Transaction [1..*] --accepted by «participation»--> Provider [1]
- Listing Location [1] --at--> Free Stay [0..*]
- External Payment [1..*] --intermediates--> Payment Provider [1]
- Couchsurfing Listing [0..*] --captures--> Listing Location [1]
- Transaction Conversation [0..*] --participates--> Provider [1]
- Target Customer [1] --initiates--> Listing Conversation [0..*]
- Add Listing [1] --creates «creation»--> Listing [1]
- Register [1..*] --performed by «participation»--> User [1]
- Register [1] --creates «creation»--> Registration [1]

**Generalizations (14):**

- Listing Creator --|> User
- Booking --|> Transaction
- Subscription Payment Plan --|> Payment Action
- Couchsurfing Homeowner --|> Provider
- Couchsurfing Lodger --|> Customer
- Couchsurfing Home Searcher --|> Target Customer
- Couchsurfing Home Searcher --|> Subscribed Platform User
- Couchsurfing Homeowner --|> Subscribed Platform User
- Registered C2C User --|> User
- External Payment --|> Payment Action
- Couchsurfing Listing --|> Listing
- Review Creation by Provider --|> Review Creation
- Review Creation by Customer --|> Review Creation
- Customer --|> Target Customer

---
## Uber Eats

> A meal delivery platform connecting restaurants, riders, and customers. Restaurants upload menus and dashboards. Customers order meals. The platform matches orders with available riders for delivery. Restaurants prepare meals, riders pick up and deliver. Customers can review restaurants, and rate riders. The platform takes a commission and handles payment internally.

**Taxonomy selections:** multi_sided, registration, transaction, centralized, listing_kind_service, listing_type_offline_service, frequency_one_time, quantity_one, price_discovery_set_by_provider, immediate_access, review_by_customer, revenue_stream_commission, revenue_source_customer, payment_system_internal

**Summary:** 46 classes, 34 relations, 25 generalizations

**Classes (46):**

*From Airbnb:*
- `«kind»` **Product**

*From Centralized:*
- `«subkind»` **Centralized Offering**
- `«subkind»` **Centralized Transaction**
- `«event»` **Centralized Transaction Creation**
- `«event»` **Match Target Customer To Offering**

*From Decentralized:*
- `«subkind»` **Decentralized Transaction**
- `«event»` **Decentralized Transaction Creation**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«subkind»` **Listing Description**
- `«collective»` **Listing Overview**
- `«event»` **Listing Search**

*From General: User Actions:*
- `«roleMixin»` **Platform Company** [name]
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From Immediate Access:*
- `«subkind»` **Immediate Acces Transaction**
- `«subkind»` **Immediate Access Claim**
- `«subkind»` **Immediate Access Commitment**
- `«roleMixin»` **Immediate Access Customer**
- `«roleMixin»` **immediate Access Provider**

*From Organisation:*
- `«kind»` **Organization** [name, location, description]

*From P2P:*
- `«event»` **Automated Affiliation Action**
- `«event»` **Manually-Checked Affiliation Action**
- `«roleMixin»` **Peer User**

*From Registration:*
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Transaction:*
- `«event»` **Create Transaction**
- `«event»` **Delivery**
- `«event»` **Offering Creation**
- `«relator»` **Offering On The Platform** [attribute]

*From UFO-C:*
- `«kind»` **Person** [firstName, lastName, email, birthDate]

*From Uber eats:*
- `«event»` **Accepts Ride**
- `«event»` **Deliver Meal**
- `«subkind»` **Delivering Obligation**
- `«event»` **Match Rider to Meal Order**
- `«subkind»` **Meal**
- `«subkind»` **Meal Order**
- `«event»` **Meal Preparation**
- `«subkind»` **Offers to Deliver**
- `«event»` **Order a Meal**
- `«event»` **Sign Up to Deliver**
- `«role»` **Uber Eats Customer**
- `«event»` **Uber Eats Customer Registers**
- `«role»` **Uber Eats Restaurant**
- `«event»` **Uber Eats Restaurant Registers**
- `«role»` **Uber Eats Rider**
- `«roleMixin»` **Uber Eats User**
- `«event»` **Upload Menu and Install Dashboard**

**Relations (34):**

- Centralized Transaction [1] --partially fulfills--> Deliver Meal [1]
- Deliver Meal [0..*] --performed by «participation»--> Uber Eats Rider [1]
- Decentralized Transaction [0..*] --bound to «mediation»--> Uber Eats Customer [1]
- Centralized Offering [1..*] --towards--> Match Target Customer To Offering [0..*]
- Platform Company [1] --bounds «mediation»--> Registration [1..*]
- Listing Description [1..*] --is part of «memberOf»--> Listing Overview [1]
- Decentralized Transaction Creation [1] --results in «creation»--> Decentralized Transaction [1]
- Offering Creation [1] --created «creation»--> Offering On The Platform [1]
- Match Target Customer To Offering [1..*] --is part of--> Centralized Transaction Creation [1]
- Meal [1..*] --includes--> Deliver Meal [1]
- Listing Search [1..*] --uses «participation»--> Listing Overview [1]
- Deliver Meal [0..*] --delivered to «participation»--> Uber Eats Customer [1]
- Register [1..*] --performed by «participation»--> User [1]
- Offering Creation [0..*] --performed by «participation»--> Uber Eats Rider [1]
- immediate Access Provider [1..*] --inheres in «characterization»--> Immediate Access Commitment [1..*]
- Listing [1] --described by «mediation»--> Listing Description [1]
- Accepts Ride [0..*] --followed by «historicalDependence»--> Match Target Customer To Offering [1]
- Accepts Ride [1] --creates--> Delivering Obligation [1]
- Immediate Access Claim [1..*] --is part of--> Immediate Acces Transaction [1]
- Listing Search [0..*] --performed by «participation»--> Uber Eats Customer [1]
- Decentralized Transaction [1] --partially fulfills--> Meal Preparation [1]
- Uber Eats Customer [1] --participates--> Uber Eats Customer Registers [1]
- Offering Creation [0..*] --performed by «participation»--> Uber Eats Restaurant [1]
- Immediate Acces Transaction [1] --is part of--> Immediate Access Commitment [0..*]
- Listing Search [1..*] --results in «historicalDependence»--> Decentralized Transaction Creation [0..1]
- Uber Eats Restaurant Registers [1] --participates--> Uber Eats Restaurant [1]
- Meal Preparation [1..*] --performed by «participation»--> Uber Eats Restaurant [1]
- Create Transaction [0..*] --performed by «participation»--> Uber Eats Customer [1]
- Decentralized Transaction Creation [0..*] --performed by «participation»--> Uber Eats Restaurant [1]
- Immediate Access Customer [1] --inheres in  «characterization»--> Immediate Access Claim [1..*]
- Accepts Ride [0..*] --performed by «participation»--> Uber Eats Rider [1]
- Register [1] --creates «creation»--> Registration [1]
- Meal Preparation [1] --created «creation»--> Meal [1..*]
- Centralized Transaction [0..*] --conforms to «mediation»--> Offering On The Platform [1]

**Generalizations (25):**

- Uber Eats Restaurant --|> Organization
- Listing --|> Offering On The Platform
- Uber Eats Rider --|> Person
- Upload Menu and Install Dashboard --|> Offering Creation
- Uber Eats Customer --|> Person
- Uber Eats Customer Registers --|> Automated Affiliation Action
- Uber Eats Customer --|> Peer User
- Meal --|> Product
- Uber Eats Restaurant Registers --|> Manually-Checked Affiliation Action
- Uber Eats Customer --|> Uber Eats User
- Sign Up to Deliver --|> Automated Affiliation Action
- Uber Eats Rider --|> Peer User
- Decentralized Transaction Creation --|> Create Transaction
- Offers to Deliver --|> Centralized Offering
- Uber Eats Rider --|> Uber Eats User
- Centralized Offering --|> Offering On The Platform
- Order a Meal --|> Create Transaction
- Match Rider to Meal Order --|> Match Target Customer To Offering
- Delivering Obligation --|> Centralized Transaction
- Sign Up to Deliver --|> Offering Creation
- Uber Eats Customer Registers --|> Register
- Uber Eats Restaurant Registers --|> Register
- Delivering Obligation --|> Immediate Acces Transaction
- Uber Eats Restaurant --|> Uber Eats User
- Meal Order --|> Decentralized Transaction

---
## Uber Eats (simplified)

> (Simplified version of Uber Eats with fewer classes, useful as a more concise reference)

**Summary:** 25 classes, 23 relations, 9 generalizations

**Classes (25):**

*From Centralized:*
- `«subkind»` **Centralized Transaction**
- `«event»` **Centralized Transaction Creation**
- `«event»` **Match Target Customer To Offering**

*From Decentralized:*
- `«subkind»` **Decentralized Transaction**
- `«event»` **Decentralized Transaction Creation**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«subkind»` **Listing Description**
- `«collective»` **Listing Overview**
- `«event»` **Listing Search**

*From General: User Actions:*
- `«event»` **Platform Software Action**

*From Organisation:*
- `«kind»` **Organization** [name, location, description]

*From Registration:*
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]

*From Transaction:*
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«roleMixin»` **Listing Creator**
- `«event»` **Offering Creation**
- `«relator»` **Offering On The Platform** [attribute]

*From UFO-C:*
- `«kind»` **Person** [firstName, lastName, email, birthDate]

*From Uber eats:*
- `«event»` **Accepts Ride**
- `«event»` **Deliver Meal**
- `«subkind»` **Meal**
- `«event»` **Meal Preparation**
- `«role»` **Uber Eats Customer**
- `«role»` **Uber Eats Restaurant**
- `«role»` **Uber Eats Rider**

**Relations (23):**

- Centralized Transaction Creation [1] --creates «creation»--> Centralized Transaction [1]
- Offering Creation [0..*] --performed by «participation»--> Uber Eats Restaurant [1]
- Accepts Ride [0..*] --followed by «historicalDependence»--> Match Target Customer To Offering [1]
- Listing [1] --described by «mediation»--> Listing Description [1]
- Decentralized Transaction [1] --relates to--> Meal Preparation [0..*]
- Decentralized Transaction Creation [1] --results in «creation»--> Decentralized Transaction [1]
- Decentralized Transaction [0..*] --conforms to «historicalDependence»--> Listing [1]
- Offering Creation [1] --created «creation»--> Offering On The Platform [1]
- Meal [1..*] --includes--> Deliver Meal [1]
- Deliver Meal [0..*] --delivered to «participation»--> Uber Eats Customer [1]
- Listing Description [1..*] --is part of «memberOf»--> Listing Overview [1]
- Create Transaction [0..*] --performed by «participation»--> Uber Eats Customer [1]
- Deliver Meal [0..*] --performed by «participation»--> Uber Eats Rider [1]
- Meal Preparation [1] --created «creation»--> Meal [1..*]
- Meal Preparation [1..*] --performed by «participation»--> Uber Eats Restaurant [1]
- Listing Search [0..*] --performed by «participation»--> Uber Eats Customer [1]
- Match Target Customer To Offering [1..*] --is part of--> Centralized Transaction Creation [1]
- Listing Search [1..*] --uses «participation»--> Listing Overview [1]
- Centralized Transaction [1] --partially fulfills--> Deliver Meal [1]
- Register [1] --performed by «participation»--> Uber Eats Customer [1]
- Register [1] --performed by «participation»--> Uber Eats Restaurant [1]
- Accepts Ride [1..*] --part of--> Centralized Transaction Creation [1]
- Accepts Ride [0..*] --performed by «participation»--> Uber Eats Rider [1]

**Generalizations (9):**

- Uber Eats Customer --|> Customer
- Uber Eats Customer --|> Person
- Match Target Customer To Offering --|> Platform Software Action
- Uber Eats Restaurant --|> Organization
- Centralized Transaction Creation --|> Create Transaction
- Listing --|> Offering On The Platform
- Uber Eats Restaurant --|> Listing Creator
- Uber Eats Rider --|> Person
- Decentralized Transaction Creation --|> Create Transaction

---
## Pooly

> A pool-sharing platform where pool owners list their pools for temporary access by swimmers. Owners set availability and pricing. Swimmers search and book pool sessions. Payment handled through the platform with a commission model.

**Taxonomy selections:** multi_sided, registration, transaction, decentralized, user_type_person, c2c, listing_kind_service, listing_type_offline_service, frequency_one_time, quantity_many, price_discovery_set_by_provider, price_calculation_by_quantity, review_by_customer, revenue_stream_commission, revenue_source_customer, payment_system_internal, under_utilized

**Summary:** 35 classes, 44 relations, 9 generalizations

**Classes (35):**

*From Commission:*
- `«subkind»` **Commission Fee**

*From Conversation System:*
- `«subkind»` **Message**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Search**

*From General:*
- `«type»` **Category** [name]
- `«event»` **Change Status** [setStatus]
- `«enumeration»` **Listing Status**
- `«kind»` **Notification** [notificationID, viewed, receiverID]
- `«enumeration»` **Transaction Status**

*From General: User Actions:*
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From General: User Roles:*
- `«roleMixin»` **Platform Visitor**

*From Multi-Sided:*
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

*From Offline Service:*
- `«mode»` **Listing Location**

*From Price Calculation:*
- `«subkind»` **Transaction Price**

*From Recurring:*
- `«phase»` **Available time slot**
- `«phase»` **Booked Time Slot**

*From Registration:*
- `«event»` **Login** [checkEmail, checkPassword]
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Review By:*
- `«relator»` **Review** [score, comment]

*From Review by Customer:*
- `«subkind»` **Customer Review**
- `«event»` **Review Creation by Customer**

*From Review by Provider:*
- `«subkind»` **Provider Review**
- `«event»` **Review Creation by Provider**

*From Service:*
- `«subkind»` **Booking** [personsBooked]
- `«mode»` **Time**

*From Set by Provider:*
- `«event»` **Price Setting action by Provider** [setPricePerSeat]
- `«subkind»` **Price set by Provider**

*From Transaction:*
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«roleMixin»` **Listing Creator**
- `«roleMixin»` **Provider**

*From Transaction Conversation:*
- `«event»` **Transaction Conversation** [sendMessage]
- `«subkind»` **Transaction Message**

**Relations (44):**

- Booking [0..*] --according--> Time [1]
- Listing Search [*] --for--> Listing [*]
- Create Transaction [1..*] --accepted by «participation»--> Provider [1]
- Register [1..*] --performed by «participation»--> User [1]
- Listing [*] --has--> Category [*]
- Platform Visitor [1] --performed by--> Listing Search [0..*]
- Listing [1] --captures--> Available time slot [0..*]
- Listing [0..*] --indicated--> Time [1]
- Create Transaction [1..*] --initiates «participation»--> Customer [1]
- Available time slot [1] --becomes «historicalDependence»--> Booked Time Slot [0..1]
- Transaction [1] --generates--> Notification [0..*]
- User [None] --(unnamed)--> Message [0..*]
- Listing Creator [1] --(unnamed)--> Change Status [1..*]
- Customer [1] --participates--> Transaction Conversation [1..*]
- Booking [1] --concerning--> Review [0..2]
- Add Listing [1] --sets--> Price set by Provider [0..*]
- User [1] --performed by «participation»--> Login [0..*]
- Register [1] --creates «creation»--> Registration [1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Customer [1] --does--> Review Creation by Customer [0..*]
- Commission Fee [None] --(unnamed)--> Create Transaction [None]
- Register [1] --followed by--> Login [0..*]
- Listing [1] --conforms to--> Booking [0..*]
- Transaction Conversation [0..*] --participates--> Provider [1]
- User [1] --to--> Notification [0..*]
- Transaction [1] --(unnamed)--> Transaction Conversation [0..*]
- Transaction [1] --(unnamed)--> Transaction Message [0..*]
- Transaction Conversation [0..*] --concerns--> Booking [1]
- Transaction Price [1] --adds--> Commission Fee [0..1]
- Listing [1..*] --(unnamed)--> Price set by Provider [1..*]
- Listing Creator [1] --changes--> Price Setting action by Provider [0..*]
- Registration [1] --has--> User [1]
- Listing [0..*] --captures--> Listing Location [1..*]
- Review Creation by Customer [1] --By--> Customer Review [1]
- Booking [1] --captures--> Booked Time Slot [1..*]
- Add Listing [1] --includes «participational»--> Price Setting action by Provider [1..*]
- Review Creation by Provider [1] --by--> Provider Review [1]
- Transaction [1] --(unnamed)--> Transaction Price [1]
- Add Listing [1] --creates «creation»--> Listing [1]
- Review [0..2] --concerning--> Transaction [1]
- Price Setting action by Provider [1] --sets--> Price set by Provider [1..*]
- Transaction [1..*] --(unnamed)--> Customer Review [0..1]
- Provider [1] --does--> Review Creation by Provider [0..*]
- Change Status [0..*] --(unnamed)--> Listing [1]

**Generalizations (9):**

- User --|> Platform Visitor
- Customer --|> Platform Visitor
- Customer --|> User
- Provider --|> Listing Creator
- Transaction Message --|> Message
- Listing Creator --|> User
- Booking --|> Transaction
- Provider Review --|> Review
- Customer Review --|> Review

---
## RetroKicks

> A marketplace for buying and selling vintage/retro sneakers. Sellers list sneakers with photos, size, brand, condition, and price. Buyers search and purchase. Payment handled through the platform with a commission model. Product-oriented (physical good transfer).

**Taxonomy selections:** multi_sided, registration, transaction, decentralized, user_type_person, c2c, listing_kind_good, listing_type_physical_good, frequency_one_time, quantity_one, price_discovery_set_by_provider, review_by_customer, revenue_stream_commission, revenue_source_customer, payment_system_internal

**Summary:** 33 classes, 39 relations, 8 generalizations

**Classes (33):**

*From Auction:*
- `«event»` **Bid**
- `«subkind»` **Bid Price**
- `«subkind»` **Highest Bid Price**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Search**

*From General:*
- `«type»` **Category** [name]
- `«event»` **Change Status** [setStatus]
- `«enumeration»` **Listing Status**
- `«kind»` **Notification** [notificationID, viewed, receiverID]
- `«enumeration»` **Transaction Status**

*From General: User Actions:*
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From General: User Roles:*
- `«roleMixin»` **Platform Visitor**

*From Good Transfer:*
- `«kind»` **Good**

*From Listing Fee:*
- `«subkind»` **Listing Fee**
- `«event»` **Listing Fee Payment**

*From Multi-Sided:*
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

*From Organisation:*
- `«relator»` **Member**
- `«kind»` **Organization** [name, location, description]
- `«roleMixin»` **Professional User**
- `«event»` **Registers Organisation**

*From Physical Good:*
- `«mode»` **Delivery Location**
- `«event»` **Physical Delivery**
- `«subkind»` **Physical Good**

*From Registration:*
- `«event»` **Login** [checkEmail, checkPassword]
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Set by Provider:*
- `«event»` **Price Setting action by Provider** [setPricePerSeat]
- `«subkind»` **Price set by Provider**

*From Transaction:*
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«roleMixin»` **Listing Creator**
- `«roleMixin»` **Provider**

**Relations (39):**

- Physical Delivery [0..*] --(unnamed)--> Provider [None]
- Listing Fee [None] --(unnamed)--> Listing Fee Payment [None]
- Register [1] --creates «creation»--> Registration [1]
- Professional User [1] --participates in--> Registers Organisation [0..*]
- User [1] --does--> Bid [0..*]
- Physical Delivery [0..1] --(unnamed)--> Physical Good [1..*]
- Register [1..*] --performed by «participation»--> User [1]
- Transaction [1] --(unnamed)--> Highest Bid Price [1]
- Bid Price [1] --(unnamed)--> Bid [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Transaction [0..1] --confirm the--> Good [1..*]
- User [1] --performed by «participation»--> Login [0..*]
- Listing Search [*] --for--> Listing [*]
- User [1] --to--> Notification [0..*]
- Add Listing [1] --includes «participational»--> Price Setting action by Provider [1..*]
- Registers Organisation [1] --to create--> Organization [1]
- Listing [1] --involves--> Good [1..*]
- Listing Creator [1] --changes--> Price Setting action by Provider [0..*]
- Create Transaction [1] --creates «creation»--> Transaction [1]
- Member [1..*] --of a--> Organization [1]
- Add Listing [1] --sets--> Price set by Provider [0..*]
- Registration [1] --has--> User [1]
- Bid Price [0..*] --has--> Listing [1]
- Listing Creator [1] --(unnamed)--> Change Status [1..*]
- Delivery Location [0..*] --(unnamed)--> Physical Delivery [0..*]
- Create Transaction [1..*] --accepted by «participation»--> Provider [1]
- Create Transaction [1..*] --initiates «participation»--> Customer [1]
- Listing [*] --has--> Category [*]
- Change Status [0..*] --(unnamed)--> Listing [1]
- Listing [1..*] --(unnamed)--> Price set by Provider [1..*]
- Register [1] --followed by--> Login [0..*]
- Listing Fee [1] --includes--> Add Listing [1]
- Listing Fee Payment [0..1] --includes--> Add Listing [1]
- Add Listing [1] --creates «creation»--> Listing [1]
- Price Setting action by Provider [1] --sets--> Price set by Provider [1..*]
- Physical Delivery [1..*] --(unnamed)--> Customer [1]
- Platform Visitor [1] --performed by--> Listing Search [0..*]
- Member [1..*] --is a--> Professional User [1]

**Generalizations (8):**

- Price set by Provider --|> Bid Price
- Listing Creator --|> User
- Physical Good --|> Good
- User --|> Platform Visitor
- Customer --|> User
- Customer --|> Platform Visitor
- Provider --|> Listing Creator
- Highest Bid Price --|> Bid Price

---
## SmartLearn

> An online tutoring/learning platform where teachers offer courses or tutoring sessions. Students search for courses, book sessions, and attend online. Recurring subscription model possible. Reviews by students.

**Taxonomy selections:** multi_sided, registration, transaction, decentralized, user_type_person, listing_kind_service, listing_type_digital_service, frequency_recurring, quantity_one, price_discovery_set_by_provider, conversation_transaction, review_by_customer, revenue_stream_commission, revenue_source_customer, payment_system_internal

**Summary:** 36 classes, 39 relations, 9 generalizations

**Classes (36):**

*From By Feature:*
- `«mode»` **Feature**
- `«type»` **Feature Type**
- `«subkind»` **Feature-Based Price**

*From Decentralized:*
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Search**

*From General:*
- `«type»` **Category** [name]
- `«event»` **Change Status** [setStatus]
- `«enumeration»` **Listing Status**
- `«kind»` **Notification** [notificationID, viewed, receiverID]
- `«enumeration»` **Transaction Status**

*From General: User Actions:*
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

*From General: User Roles:*
- `«roleMixin»` **Platform Visitor**

*From Listing Frequency:*
- `«quality»` **Time Slot**

*From Multi-Sided:*
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

*From Online Service:*
- `«mode»` **Meeting link**

*From Organisation:*
- `«relator»` **Member**
- `«kind»` **Organization** [name, location, description]
- `«roleMixin»` **Professional User**
- `«event»` **Registers Organisation**

*From Recurring:*
- `«phase»` **Available time slot**
- `«phase»` **Booked Time Slot**

*From Registration:*
- `«event»` **Login** [checkEmail, checkPassword]
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**

*From Service:*
- `«subkind»` **Booking** [personsBooked]

*From Set by Customer:*
- `«event»` **Price Setting Action by Customer**
- `«subkind»` **Suggested Price**

*From Subscription:*
- `«roleMixin»` **Subscribed Platform User**
- `«event»` **Subscription Action**
- `«subkind»` **Subscription Fee**
- `«event»` **Subscription Payment Plan**

*From Transaction:*
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«roleMixin»` **Listing Creator**
- `«roleMixin»` **Provider**

**Relations (39):**

- Subscription Payment Plan [1] --includes «participational»--> Subscription Action [1]
- Meeting link [0..*] --captures--> Listing [0..*]
- Price Setting Action by Customer [1] --of--> Suggested Price [1]
- Create Transaction [1..*] --initiates «participation»--> Customer [1]
- Register [1..*] --performed by «participation»--> User [1]
- Feature Type [1] --instantiates--> Feature [0..*]
- Professional User [1] --participates in--> Registers Organisation [0..*]
- Available time slot [1] --becomes «historicalDependence»--> Booked Time Slot [0..1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Add Listing [1] --creates «creation»--> Listing [1]
- Subscription Action [1..*] --performed by «participation»--> Subscribed Platform User [1]
- User [1] --does--> Price Setting Action by Customer [0..*]
- User [1] --performed by «participation»--> Login [0..*]
- Listing Search [*] --for--> Listing [*]
- Registration [1] --has--> User [1]
- Create Transaction [1..*] --accepted by «participation»--> Provider [1]
- Member [1..*] --is a--> Professional User [1]
- Listing [1] --captures--> Available time slot [0..*]
- Platform Visitor [1] --performed by--> Listing Search [0..*]
- Member [1..*] --of a--> Organization [1]
- Suggested Price [0..*] --(unnamed)--> Listing [1]
- Transaction [1] --generates--> Notification [0..*]
- Booking [1] --captures--> Booked Time Slot [1..*]
- User [1] --to--> Notification [0..*]
- Create Transaction [1] --creates «creation»--> Transaction [1]
- Register [1] --creates «creation»--> Registration [1]
- Listing [*] --has--> Category [*]
- Listing [1] --conforms to--> Booking [0..*]
- Feature Type [0..*] --sets--> Add Listing [0..*]
- Registers Organisation [1] --to create--> Organization [1]
- Listing Creator [1] --(unnamed)--> Change Status [1..*]
- Feature-Based Price [0..*] --(unnamed)--> Feature Type [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Meeting link [1] --includes--> Booking [1]
- Change Status [0..*] --(unnamed)--> Listing [1]
- Feature [1] --has--> Transaction [0..*]
- Subscription Action [0..1] --Followed by «historicalDependence»--> Register [1]
- Register [1] --followed by--> Login [0..*]
- Subscription Fee [1..*] --of--> Subscription Payment Plan [1]

**Generalizations (9):**

- User --|> Platform Visitor
- Listing Creator --|> User
- Professional User --|> User
- Subscribed Platform User --|> User
- Provider --|> Listing Creator
- Booked Time Slot --|> Time Slot
- Customer --|> User
- Available time slot --|> Time Slot
- Booking --|> Transaction
