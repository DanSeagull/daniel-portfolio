# Test Plan: Yandex Go Mobile App (Passenger Version)

## 1. Test Object

**Product Name:** Yandex Go — a superapp for urban services (taxi, carsharing, delivery, scooter rental).

**Platforms:** iOS (last 2 versions), Android (last 3 versions).

**Key Functionality (Scope):**
- **Core Scenario:** Order a taxi "right now" (Select pickup point A → Select destination B → Driver matching → Real-time tracking → Payment → Rate the ride).
- **Payments:** Cashless payment (card/Apple Pay/Google Pay), cash payment, promo codes.
- **AI Feature (new):** Chat with "Alice AI" to order a taxi via voice or text.
- **User Profile:** Ride history, profile settings, payment methods.
- **Safety & Security:** Phone number verification (SMS), matching car/driver details in the app.

*Out of scope for this plan:* Backend load testing, dark mode testing, driver/courier app testing.

---

## 2. Types of Testing

| Testing Type | Why It Matters for Yandex Go | Tools |
|--------------|------------------------------|-------|
| **Functional** | The user must get from A to B without failures. | Manual, Checklists |
| **UI/UX** | The map is the main screen. Critical to display cars, zoom, and taxi positioning correctly. | Figma, DevTools (Remote Debugging) |
| **Integration** | The app depends on 3 things: Maps (GPS), Payment Gateway, SMS provider. | Charles Proxy (sniffer) |
| **Location/GPS Testing** | The heart of the app. How it behaves with weak signal, in the subway, under bridges. | Charles (Location mocking), Android Studio Emulator |
| **AI Testing (Alice)** | Verify accuracy of voice command recognition (noise, accents) and text intents. | Mobile logs, Manual testing |
| **Regression** | Any map or Alice update must not break payments. | Automated tests (UI tests for critical path) |
| **Cross-Platform** | Different behavior of the Back button on Android vs swipe gestures on iOS. | Xcode Simulator, Android Studio |

---

## 3. Testing Approach

**Manual Testing:**
- **Exploratory:** Simulating real rides in different city areas (downtown, residential district, industrial zone).
- **Negative:** Trying to order a taxi without internet, with a zero card balance, canceling a ride at different stages.

**Tools for Emulation (Important for portfolio):**
- **Charles / Proxyman:** To mock server responses (e.g., make the app think no cars are nearby).
- **Android Studio / Xcode:** To simulate weak GPS signal or poor network conditions (Network Link Conditioner).
- **Postman:** For API endpoint testing (e.g., getting the list of available tariffs).

---

## 4. Quality Criteria (Exit Criteria)

We complete testing when:

1.  **P0 (Blockers):** No bugs that prevent placing an order or paying for a ride.
2.  **Geolocation Accuracy:** Address A location error does not exceed 50 meters.
3.  **Alice:** Alice recognizes the command "Take me home" and builds a route in 95% of cases.
4.  **Memory:** The app does not crash (no Crashlytics errors) while running in the background for 10 minutes.

---

## 5. Resources & Test Data

**Test Environment:**
- **Devices:** iPhone 15 (iOS 17), Pixel 6 (Android 14), iPhone SE emulator (small screen).
- **Accounts:**
    - User with a linked Visa card.
    - User with a linked Mastercard card (with 3D Secure).
    - User with a zero balance.
    - User with an active promo code ("TEST2025").
- **Geo Data:** Test location (Moscow, Tverskaya Street).

---

## 6. Risks (Taxi Testing Risks)

| Risk | Probability | Mitigation (What I will do) |
|------|-------------|------------------------------|
| **Financial risks** (incorrect charges) | Medium | Focus on payment API tests and verifying the final amount in ride history. |
| **AI "surprise"** (Alice sends the user to the wrong place) | High | Cover not only logical inputs but also slang ("Floor it", "Step on it", "Hurry up"). |
| **Real GPS issues** (indoors) | Low | Use "poor signal" emulation in Charles/Android Studio. |

---

## 7. Schedule (Example for 1 sprint)

- **Day 1:** Requirements analysis for the new "Children" tariff + preparing checklists.
- **Day 2:** Functional testing (manual) + Logging bugs in the bug-tracking system (simulating Jira, Yandex Tracker).
- **Day 3:** API & Integration testing (Postman, Charles).
- **Day 4:** Regression (verify that old payment functionality is not broken).
- **Day 5:** Report generation and demo.

---

## 8. Checklist / Artifacts

1.  **`/test-cases`** : Test case "Order a taxi via Alice voice assistant".
2.  **`/api-testing`** : Postman collection for `POST /api/order/create` (order creation).
3.  **`/sql-queries`** : Query to find duplicate rides (if there is suspicion of a double-charge bug).
4.  **`/screenshots`** : Screenshot where Alice misunderstood the address (visual bug).
5.  **`/bug-reports`** : Bug report: "When the screen rotates, the route on the map resets to the center of Moscow."
