# Test Cases: Ordering a Taxi (Basic Scenario)

## Preconditions for All Test Cases:
- Yandex Go app is installed and opened
- User is logged in
- GPS is enabled
- Internet connection is available

---

### TC-001: Successful "Right Now" Taxi Order

| Field | Value |
|-------|-------|
| **ID** | TC-001 |
| **Title** | Order a taxi from "Pickup" to "Destination" address |
| **Priority** | Critical |
| **Precondition** | Sufficient funds on the account |
| **Steps** | 1. Enter "Moscow, Tverskaya 1" in the pickup field <br> 2. Enter "Moscow, Kremlin" in the destination field <br> 3. Tap the "Order" button |
| **Expected Result** | 1. The route is displayed on the map <br> 2. Driver information appears (name, car model, rating) <br> 3. The estimated amount is pre-authorized (hold) |
| **Postcondition** | Ride is active, status: "Finding a driver" |

---

### TC-002: Negative Scenario — Empty Destination Field

| Field | Value |
|-------|-------|
| **ID** | TC-002 |
| **Title** | Attempt to order without specifying a destination |
| **Priority** | High |
| **Steps** | 1. Enter an address in the pickup field <br> 2. Leave the destination field empty <br> 3. Tap "Order" |
| **Expected Result** | An error message appears: "Specify your destination". The "Order" button is disabled or shows a warning. |

---

### TC-003: Changing the Tariff During Driver Search

| Field | Value |
|-------|-------|
| **ID** | TC-003 |
| **Title** | Switch tariff from "Economy" to "Comfort" after search has started |
| **Priority** | Medium |
| **Steps** | 1. Start searching for a taxi with the "Economy" tariff <br> 2. While searching (status: "Finding driver"), tap on the tariff and select "Comfort" |
| **Expected Result** | The search restarts with the new tariff. The price is recalculated. The previous hold is canceled. |
