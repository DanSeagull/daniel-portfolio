# Regression Checklist: Yandex Go (Pre-Release)

## 1. Authorization & Profile
- [ ] Login by phone number (SMS code)
- [ ] Login with invalid number → error
- [ ] Change payment method (card → cash)
- [ ] View ride history (last 5 rides are displayed)

## 2. Ordering a Taxi (Core Scenario)
- [ ] Auto-detection of current address (error < 50 m)
- [ ] Manual address entry for "Pickup" and "Destination"
- [ ] Tariff selection (Economy, Comfort, Business, Children)
- [ ] "Order" button is enabled only when fields are filled
- [ ] Driver card appears after confirmation

## 3. Payments
- [ ] Charge from linked card
- [ ] Cash payment (no pre-authorization hold)
- [ ] Promo code: apply and display discount
- [ ] Promo code: expired → error

## 4. Alice (AI Chat)
- [ ] Voice input "Take me home" → route to home address is built
- [ ] Voice input with background noise (emulated) → at least 70% accuracy
- [ ] Text input "Take me to the train station" → suggests a list of train stations

## 5. Background & Network Handling
- [ ] App does not crash when minimized during a ride
- [ ] Internet loss for 10 seconds → ride is not canceled
- [ ] Internet restored → ride status updates
