
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from ai_assistant import get_spending_advice
from database import (
    initialize_database,
    add_expense,
    get_expenses,
    delete_expense
)

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="PayPal AI SpendWise",
    page_icon="💳",
    layout="wide"
)

initialize_database()


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
    /* Main application background */
    .stApp {
        background-color: #F4F7FB;
        color: #172B4D;
    }

    /* Main content text */
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp li,
    .stApp div[data-testid="stMarkdownContainer"] {
        color: #172B4D;
    }

    /* Main title */
    .main-title {
        color: #003087 !important;
        font-size: 38px;
        font-weight: 800;
    }

    /* Subtitle */
    .subtitle {
        color: #536579 !important;
        font-size: 16px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E8F0FC;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #D6E0EF;
    }

    div[data-testid="stMetric"] label {
        color: #536579 !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #003087 !important;
    }

    /* Input fields */
    .stTextInput input,
    .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #172B4D !important;
        border: 1px solid #B8C7DC !important;
    }

    /* Dropdowns and date inputs */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        color: #172B4D;
    }

    /* Buttons */
    .stButton button,
    .stFormSubmitButton button {
        background-color: #003087;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
    }

    .stButton button p,
    .stFormSubmitButton button p {
        color: #FFFFFF !important;
    }

    /* Data tables */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #003087 !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">💳 PayPal AI SpendWise</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Track expenses. Understand spending. Make smarter financial decisions.</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("💰 SpendWise")
st.sidebar.caption("Your personal expense manager")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Add Expense", "AI Insights", "PayPal Checkout"]
)

st.sidebar.divider()
st.sidebar.info(
    "Track your spending and discover where your money goes."
)

# ---------------- LOAD EXPENSES ----------------

expenses = get_expenses()

columns = [
    "ID", "Title", "Amount", "Category", "Date"
]

df = pd.DataFrame(expenses, columns=columns)

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.subheader("📊 Financial Dashboard")

    today = date.today()

    if df.empty:
        st.info(
            "No expenses recorded yet. Open 'Add Expense' "
            "from the sidebar to record your first expense."
        )

        st.metric("Total Expenses", "₹0")
        st.metric("This Month", "₹0")

    else:
        monthly_df = df[
            (df["Date"].dt.month == today.month) &
            (df["Date"].dt.year == today.year)
        ]

        total_spending = df["Amount"].sum()
        monthly_spending = monthly_df["Amount"].sum()
        transaction_count = len(df)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💸 Total Spending",
            f"₹{total_spending:,.2f}"
        )

        col2.metric(
            "📅 This Month",
            f"₹{monthly_spending:,.2f}"
        )

        col3.metric(
            "🧾 Transactions",
            transaction_count
        )

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("Spending by Category")

            category_data = (
                df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                category_data,
                names="Category",
                values="Amount",
                hole=0.45,
                title="Expense Distribution"
            )

            st.plotly_chart(fig, width="stretch")

        with right:
            st.subheader("Spending Over Time")

            daily_data = (
                df.groupby("Date")["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                daily_data,
                x="Date",
                y="Amount",
                title="Daily Expenses",
                labels={
                    "Date": "Date",
                    "Amount": "Amount (₹)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📝 Recent Expenses")

        display_df = df.copy()
        display_df["Date"] = display_df["Date"].dt.strftime(
            "%Y-%m-%d"
        )

        st.dataframe(
            display_df.sort_values("ID", ascending=False),
            use_container_width=True,
            hide_index=True
        )

# ---------------- ADD EXPENSE ----------------

elif page == "Add Expense":

    st.subheader("➕ Add a New Expense")
    st.write("Record your spending to keep your budget organized.")

    with st.form("expense_form", clear_on_submit=True):

        title = st.text_input(
            "Expense Name",
            placeholder="e.g. Lunch, Bus Ticket, Books"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=100.0,
            step=10.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Education",
                "Bills",
                "Entertainment",
                "Health",
                "Travel",
                "Other"
            ]
        )

        expense_date = st.date_input(
            "Expense Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Save Expense",
            use_container_width=True
        )

        if submitted:
            if not title.strip():
                st.error("Please enter an expense name.")

            elif amount <= 0:
                st.error("Amount must be greater than zero.")

            else:
                add_expense(
                    title.strip(),
                    amount,
                    category,
                    expense_date.isoformat()
                )

                st.success("Expense saved successfully!")
                st.rerun()

# ---------------- AI INSIGHTS PLACEHOLDER ----------------


elif page == "AI Insights":

    st.subheader("🤖 AI Spending Insights")
    st.write(
        "Get personalized spending analysis and "
        "budgeting suggestions powered by AI."
    )

    if df.empty:
        st.info("Add some expenses first to generate AI insights.")

    else:
        if st.button("✨ Analyze My Spending", width="stretch"):
            with st.spinner("AI is analyzing your expenses..."):
                advice = get_spending_advice(expenses)

            st.markdown("### Your Personalized Recommendations")
            st.markdown(advice)

# ---------------- PAYPAL CHECKOUT PLACEHOLDER ----------------

elif page == "PayPal Checkout":

    st.subheader("🅿️ PayPal Sandbox Checkout")

    st.write(
        "This section will be connected to PayPal Developer "
        "Sandbox for testing payment flows."
    )

    st.warning(
        "Checkout is not connected yet. No payment can be "
        "processed from this page at this stage."
    )

    st.markdown(
        "Next, we will configure PayPal Sandbox credentials "
        "and implement the checkout approval and capture flow."
    )

st.divider()

st.caption(
    "PayPal AI SpendWise | Personal Finance Dashboard | "
    "Hackathon Project"
)
