# Product Requirements Document (PRD)

## Product Name
**NestEgg Compass**  
*Tagline: Smart money tracking for students, expats, and shared trips.*

## 1. Product Overview
NestEgg Compass is a web-first money management system (with mobile app readiness) built for:
- Students managing limited budgets.
- New families living away from their support system.
- Friends/teams sharing travel or group expenses.

The product helps users track income and expenses, plan budgets, and split group costs transparently.

## 2. Problem Statement
People living away from family (e.g., abroad) often struggle with:
- Unclear monthly spending patterns.
- Difficulty balancing income vs. essentials.
- Stress around shared costs during trips or group activities.
- Lack of simple, stylish, and reliable tools focused on both personal and group finance.

## 3. Goals & Objectives
### Primary Goals
1. Enable easy daily income/expense tracking.
2. Provide meaningful insights into spending behavior.
3. Simplify group money split with clear settlement recommendations.
4. Offer an attractive, intuitive interface suitable for frequent use.

### Success Criteria (First 6 months)
- 70% of active users log at least 3 transactions/week.
- 50% of active users set monthly budgets.
- 40% of group users complete at least 1 trip split without manual recalculation.
- NPS > 35 for usability and visual design.

## 4. Target Users
### Persona A: International Student
- Lives on fixed allowance/part-time income.
- Needs strict budget control and visibility of essentials.

### Persona B: New Family Abroad
- Tracks household bills, groceries, child expenses, and savings.
- Needs joint planning and category-wise monitoring.

### Persona C: Group Trip Organizer
- Handles shared costs for travel, dining, transport.
- Needs fair split and low-friction settlement process.

## 5. Scope
### In Scope (MVP)
- User authentication and profile setup.
- Personal income and expense logging.
- Category and subcategory management.
- Monthly budget setup with alerts.
- Dashboard with summaries and trends.
- Group creation and expense splitting.
- Settlement calculator (“who owes whom”).
- Multi-currency display support (base + transaction currency).

### Out of Scope (MVP)
- Direct bank account integration.
- Crypto/stock portfolio tracking.
- Tax filing automation.
- Full offline-first sync engine.

## 6. Core Features
1. **Income Tracking**
   - Add one-time/recurring income.
   - Track by source (salary, freelance, allowance, etc.).

2. **Expense Tracking**
   - Quick add transaction with amount, category, note, date, payment mode.
   - Smart categories for student/family needs.

3. **Budget Planning**
   - Monthly category budgets.
   - Overspend alerts and progress indicators.

4. **Money Split (Flagship Feature)**
   - Create groups (trip/flatmates/events).
   - Add shared expenses with split methods:
     - Equal split.
     - Unequal/manual share.
     - Percentage share.
   - Automatic settlement graph and net balances.

5. **Reports & Insights**
   - Weekly/monthly spend charts.
   - Category-wise heatmap.
   - Savings trend.

6. **Family/Partner Collaboration (Phase-ready in MVP design)**
   - Shared household wallet view (optional).
   - Role-based visibility.

## 7. User Stories
- As a student, I want to log every meal and commute expense quickly so that I can stay in budget.
- As a new family user, I want to compare planned vs actual household spending each month.
- As a trip organizer, I want to split hotel and food bills among friends and see who should pay whom.
- As an expat, I want to record expenses in local currency and view totals in my home currency.

## 8. Functional Requirements
- FR1: System must allow users to create/edit/delete income entries.
- FR2: System must allow users to create/edit/delete expense entries.
- FR3: System must allow custom categories and default templates.
- FR4: System must support recurring transactions.
- FR5: System must generate monthly summaries and category totals.
- FR6: System must allow group creation and member management.
- FR7: System must support split logic (equal, unequal, percentage).
- FR8: System must compute minimal settlement recommendations.
- FR9: System must provide notifications for budget limits and reminders.
- FR10: System must include export to CSV/PDF for reports.

## 9. Non-Functional Requirements
- NFR1: Mobile-responsive UI (progressive web app friendly).
- NFR2: Page load target < 2.5s on standard 4G.
- NFR3: Data encryption in transit (HTTPS) and secure password storage.
- NFR4: 99.5% monthly uptime target.
- NFR5: Accessibility baseline (WCAG 2.1 AA for key workflows).

## 10. UX & Design Principles
- Clean, modern visual style with high readability.
- Color-coded categories (income, expenses, savings, group dues).
- One-tap transaction entry on mobile.
- Clear empty states and guided onboarding.

## 11. Metrics & Analytics
- Daily active users (DAU), weekly retention.
- Avg. transactions per user/week.
- Budget creation and completion rate.
- Group split completion rate.
- Settlement conversion (recommended settlements marked paid).

## 12. Risks & Mitigations
- **Risk:** Users forget to log transactions.  
  **Mitigation:** Smart reminders + quick-add widgets.
- **Risk:** Split logic confusion.  
  **Mitigation:** Visual breakdown and real-time preview before saving.
- **Risk:** Multi-currency inaccuracies.  
  **Mitigation:** Timestamped exchange rates and manual override.

## 13. Rollout Plan
### Phase 1 (MVP)
- Auth, personal tracking, dashboards, split basics.

### Phase 2
- Shared household wallets, recurring rules improvements, richer analytics.

### Phase 3
- Mobile app, bank sync, AI spending insights.

## 14. Open Questions
- Should household shared wallets be free or premium?
- Which currencies should be pre-supported at launch?
- Should settlement payments support integration with payment providers?

