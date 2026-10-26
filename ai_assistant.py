
def get_spending_advice(expenses):
    if not expenses:
        return "Add some expenses first to analyze your spending."

    category_totals = {}
    total = 0

    for expense in expenses:
        amount = float(expense[2])
        category = expense[3]

        total += amount
        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    highest_category = max(category_totals, key=category_totals.get)
    highest_amount = category_totals[highest_category]
    percentage = highest_amount / total * 100 if total else 0

    return f"""
### 📊 Your Spending Analysis

- **Total recorded spending:** ₹{total:,.2f}
- **Highest spending category:** {highest_category}
- **Amount spent in that category:** ₹{highest_amount:,.2f}
- **Share of total spending:** {percentage:.1f}%

### 💡 Personalized Recommendations

- Review your spending on **{highest_category}** and identify
  purchases you could reduce.
- Set a weekly spending limit and track your progress.
- Review your expenses regularly to identify saving opportunities.

*These insights are calculated locally from your expense records.
No paid API is required.*
"""

