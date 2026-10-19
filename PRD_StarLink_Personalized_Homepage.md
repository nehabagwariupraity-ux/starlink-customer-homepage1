# Product Requirements Document

## StarLink Personalized Customer Homepage

**Status:** Draft  
**Version:** 1.0  
**Date:** 20 October 2026  
**Product:** StarLink customer self-service portal

## 1. Overview

StarLink customers should be able to sign in to one homepage to view their current data plan, usage, remaining allowance, billing summary, and personalized recommendations.

The homepage must make recommendations visible in the primary account experience. Customers should not need to open a separate analytics or offers screen.

The first release will support three demo customers—Neha, Rahul, and Vivaan—whose plan and usage data is stored in `customer_usage.csv`.

## 2. Problem statement

Customers often discover that they have reached their data limit only after service is throttled or an add-on is needed. Existing account pages typically show usage and offers separately, making it difficult to understand what action is best.

StarLink needs a clear, personalized homepage that answers three questions immediately:

1. What plan am I currently on?
2. How much data have I used and how much remains?
3. What plan or offer should I consider next?

## 3. Goals and success metrics

### Goals

- Provide a simple customer sign-in experience.
- Show customer-specific allocated, used, and remaining data.
- Recommend a larger data plan when the customer has reached their allocation.
- Persist a selected add-on so the next visit reflects the updated plan.
- Keep recommendations inline on the homepage.

### Success metrics

- 100% of authenticated customers see their own usage data.
- 0 instances of one customer seeing another customer’s data.
- Recommendation appears when remaining data equals zero.
- Add-on selection updates the customer record successfully.
- At least 80% of test users can understand the recommended action without assistance.

## 4. Users and personas

### Primary user: StarLink customer

A mobile or broadband customer who wants to check usage, pay a bill, and decide whether to upgrade or purchase an add-on.

### Demo users

| Customer | Allocated data | Used data | Remaining data | Expected behavior |
|---|---:|---:|---:|---|
| Neha | 10 GB | 10 GB | 0 GB | Recommend a larger data plan |
| Rahul | 20 GB | 8 GB | 12 GB | Recommend keeping the current plan |
| Vivaan | 5 GB | 4.5 GB | 0.5 GB | Show remaining data and monitor usage |

## 5. User stories

- As a customer, I want to sign in with my profile and PIN so that I can securely view my account.
- As a customer, I want to see my allocated data so that I understand my plan limit.
- As a customer, I want to see data used till date so that I can monitor consumption.
- As a customer, I want to see remaining data so that I know whether I need an add-on.
- As a customer who reaches the limit, I want to see a recommended plan immediately on the homepage.
- As a customer, I want to select the recommended add-on so that my plan allocation is updated.
- As a returning customer, I want to see my updated plan and recommendation state after my previous selection.
- As a customer, I want to sign out so that the next user cannot access my account view.

## 6. Functional requirements

### FR-1: Customer sign-in

- The app must show a sign-in screen before displaying account information.
- The customer must select their profile and enter a four-digit PIN.
- The app must validate the PIN against the customer record.
- Incorrect credentials must show an error without exposing account details.
- A successful sign-in must store the authenticated customer in the active session.

### FR-2: Customer-specific homepage

After sign-in, the homepage must display the selected customer’s name and corresponding data from the customer record. The app must not use hard-coded customer usage values.

### FR-3: Usage summary

The homepage must display:

- Allocated data in GB.
- Data used till date in GB.
- Remaining data in GB.
- Usage percentage.
- Current plan name.

Remaining data is calculated as:

```text
remaining_data = max(0, allocated_data - data_used)
```

Usage percentage is calculated as:

```text
usage_percentage = min(100, data_used / allocated_data * 100)
```

### FR-4: Recommendation logic

- If remaining data equals zero, recommend a larger plan.
- The recommended plan must provide more data than the current allocation.
- The recommendation must explain why it was shown.
- If remaining data is greater than zero, the app should recommend keeping the current plan rather than showing an unnecessary upgrade.
- The recommendation must be shown on the same homepage as usage and billing information.

Initial demo rule:

```text
if remaining_data == 0:
    recommended_allocation = max(current_allocation * 2, data_used + 5)
else:
    recommended_allocation = current_allocation
```

### FR-5: Add-on selection

- A customer at zero remaining data must be able to select the recommended add-on.
- Selecting the add-on must update the customer’s allocated data in `customer_usage.csv`.
- The customer’s used data must remain unchanged when an add-on is selected.
- The app must show a confirmation message after a successful update.
- The next session must load the updated allocation from the CSV.
- When the customer has remaining data, the add-on action should be disabled or replaced by a “Keep current plan” state.

### FR-6: Sign out

- The customer must be able to sign out from the homepage.
- After sign-out, account information must no longer be visible.
- The next customer must authenticate before seeing account data.

### FR-7: Billing and offers

- The homepage should provide a visible current bill summary and payment CTA.
- The homepage may show additional offers such as auto-pay discounts.
- Offers must be clearly separated from plan recommendations so customers understand the difference.

## 7. Data requirements

The current demo data source is [customer_usage.csv](./customer_usage.csv).

### CSV schema

| Field | Type | Required | Description |
|---|---|---:|---|
| `name` | string | Yes | Customer display name |
| `pin` | string | Yes | Demo four-digit sign-in PIN |
| `allocated_data_gb` | decimal | Yes | Current plan data allowance |
| `data_used_gb` | decimal | Yes | Data used till date |
| `plan_name` | string | Yes | Current plan name |
| `last_action` | string | No | Last plan or add-on action |

### Data validation rules

- `name` must be unique.
- `pin` must contain exactly four digits for the demo.
- `allocated_data_gb` must be greater than zero.
- `data_used_gb` must be greater than or equal to zero.
- `data_used_gb` should not exceed `allocated_data_gb` in the prototype.
- A plan update must preserve the customer name and used-data value.

## 8. Homepage information architecture

1. StarLink navigation and signed-in customer identity.
2. Greeting and account overview.
3. Current bill card.
4. Current plan card.
5. Usage card with allocated, used, and remaining data.
6. Connection status card.
7. Inline smart recommendation cards.
8. Support entry point.

## 9. Acceptance criteria

### Sign-in

- Given a valid customer and PIN, when the user selects “Sign in,” then the matching customer homepage is displayed.
- Given an invalid PIN, when the user selects “Sign in,” then an error is shown and no account data is displayed.

### Personalization

- Given Neha signs in, then the page shows 10GB allocated, 10GB used, and 0GB remaining.
- Given Rahul signs in, then the page shows 20GB allocated, 8GB used, and 12GB remaining.
- Given Vivaan signs in, then the page shows 5GB allocated, 4.5GB used, and 0.5GB remaining.

### Recommendation

- Given a customer has 0GB remaining, then a larger data plan is shown inline on the homepage.
- Given a customer has data remaining, then the current plan is presented as the recommended fit.

### Add-on persistence

- Given Neha selects the recommended add-on, then her allocation is updated from 10GB to 20GB.
- Given Neha signs out and signs in again, then the page shows the updated 20GB allocation.
- Neha’s used data remains 10GB after the allocation update.

## 10. Non-functional requirements

- The app should load the customer homepage within three seconds in a local demo environment.
- Customer records must be isolated by authenticated session.
- The interface must be usable on desktop and mobile-sized screens.
- Buttons and recommendation actions must provide visible feedback.
- CSV write operations must preserve the file header and all customer records.
- The prototype must fail safely if the CSV file is missing or malformed.

## 11. Out of scope for version 1

- Production-grade authentication and password hashing.
- Real payment processing.
- Live telecom usage APIs.
- Multiple devices or family plans.
- Proration and billing-cycle calculations.
- Inventory, tax, or regional pricing rules.
- Machine-learning recommendation models.

## 12. Future enhancements

- Replace CSV storage with a secure database.
- Add OTP-based authentication.
- Add billing history and payment receipts.
- Add real-time data usage refresh.
- Add recommendation explanations based on historical usage trends.
- Add plan comparison and checkout flow.
- Add broadband and bundled-service recommendations.
