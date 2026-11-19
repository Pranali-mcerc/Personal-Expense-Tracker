import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

DATA_FILE = "data/expenses.csv"
BUDGET_FILE = "data/budgets.json"


# ==========================================
# PROFESSIONAL CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e6e9ef;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    font-size: 16px;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #1565C0;
}

h1 {
    color: #123456;
}

h2, h3 {
    color: #234567;
}

section[data-testid="stSidebar"] {
    background-color: #eaf0f8;
}

.stButton > button {
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
}

div[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD EXPENSE DATA
# ==========================================

@st.cache_data
def load_data():

    if os.path.exists(DATA_FILE):

        df = pd.read_csv(DATA_FILE)

        if not df.empty:

            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

            df["amount"] = pd.to_numeric(
                df["amount"],
                errors="coerce"
            )

            df = df.dropna(
                subset=["date", "amount"]
            )

            return df

    return pd.DataFrame(
        columns=[
            "expense_id",
            "date",
            "category",
            "description",
            "amount",
            "payment_method"
        ]
    )


# ==========================================
# BUDGET FUNCTIONS
# ==========================================

def load_budgets():

    if os.path.exists(BUDGET_FILE):

        try:

            with open(BUDGET_FILE, "r") as file:
                return json.load(file)

        except Exception:
            return {}

    return {}


def save_budgets(budgets):

    os.makedirs("data", exist_ok=True)

    with open(BUDGET_FILE, "w") as file:

        json.dump(
            budgets,
            file,
            indent=4
        )


# ==========================================
# INITIALIZE DATA
# ==========================================

df = load_data()

budgets = load_budgets()


# ==========================================
# HEADER
# ==========================================

st.title("💰 Personal Expense Tracker")

st.markdown(
    "### Interactive Financial Analytics Dashboard"
)

st.caption(
    "Monitor expenses • Analyze spending • Manage budgets"
)

st.divider()


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🔎 Dashboard Filters")

if not df.empty:

    min_date = df["date"].min().date()

    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    categories = (
        ["All"]
        + sorted(
            df["category"].dropna().unique().tolist()
        )
    )

    selected_category = st.sidebar.selectbox(
        "Category",
        categories
    )

    payment_methods = (
        ["All"]
        + sorted(
            df["payment_method"].dropna().unique().tolist()
        )
    )

    selected_payment = st.sidebar.selectbox(
        "Payment Method",
        payment_methods
    )

    filtered_df = df.copy()

    # Date filter

    if len(date_range) == 2:

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date)
            &
            (filtered_df["date"].dt.date <= end_date)
        ]

    # Category filter

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    # Payment filter

    if selected_payment != "All":

        filtered_df = filtered_df[
            filtered_df["payment_method"] == selected_payment
        ]

else:

    filtered_df = df.copy()


# ==========================================
# KPI METRICS
# ==========================================

st.header("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

total_expense = (
    filtered_df["amount"].sum()
    if not filtered_df.empty
    else 0
)

average_expense = (
    filtered_df["amount"].mean()
    if not filtered_df.empty
    else 0
)

highest_expense = (
    filtered_df["amount"].max()
    if not filtered_df.empty
    else 0
)

total_transactions = len(filtered_df)


col1.metric(
    "💰 Total Expenses",
    f"₹{total_expense:,.2f}"
)

col2.metric(
    "📊 Average Expense",
    f"₹{average_expense:,.2f}"
)

col3.metric(
    "🔝 Highest Expense",
    f"₹{highest_expense:,.2f}"
)

col4.metric(
    "🧾 Transactions",
    total_transactions
)


st.divider()


# ==========================================
# MONTHLY COMPARISON
# ==========================================

st.header("📅 Monthly Expense Comparison")

if not df.empty:

    comparison_df = df.copy()

    comparison_df["month"] = (
        comparison_df["date"].dt.to_period("M")
    )

    current_month = pd.Timestamp.today().to_period("M")

    previous_month = current_month - 1

    current_month_expense = comparison_df[
        comparison_df["month"] == current_month
    ]["amount"].sum()

    previous_month_expense = comparison_df[
        comparison_df["month"] == previous_month
    ]["amount"].sum()

    difference = (
        current_month_expense
        - previous_month_expense
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Month",
        f"₹{current_month_expense:,.2f}"
    )

    col2.metric(
        "Previous Month",
        f"₹{previous_month_expense:,.2f}"
    )

    if previous_month_expense > 0:

        percentage_change = (
            difference / previous_month_expense
        ) * 100

        col3.metric(
            "Monthly Change",
            f"{percentage_change:.2f}%",
            delta=f"₹{difference:,.2f}"
        )

    else:

        col3.metric(
            "Monthly Change",
            "N/A"
        )


    comparison_data = pd.DataFrame({
        "Month": [
            "Previous Month",
            "Current Month"
        ],
        "Expenses": [
            previous_month_expense,
            current_month_expense
        ]
    })

    fig_comparison = px.bar(
        comparison_data,
        x="Month",
        y="Expenses",
        color="Month",
        title="Current Month vs Previous Month"
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )

else:

    st.info("No expense data available.")


st.divider()


# ==========================================
# VISUAL ANALYTICS
# ==========================================

if not filtered_df.empty:

    category_data = filtered_df.groupby(
        "category"
    )["amount"].sum().reset_index()


    # CATEGORY PIE CHART

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🥧 Category Distribution")

        fig_pie = px.pie(
            category_data,
            names="category",
            values="amount",
            hole=0.5
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


    # CATEGORY BAR CHART

    with col2:

        st.subheader("📊 Category Comparison")

        fig_bar = px.bar(
            category_data,
            x="category",
            y="amount",
            color="category"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )


    # MONTHLY TREND

    st.subheader("📈 Monthly Spending Trend")

    monthly_data = filtered_df.copy()

    monthly_data["month"] = (
        monthly_data["date"].dt.strftime("%Y-%m")
    )

    monthly_data = monthly_data.groupby(
        "month"
    )["amount"].sum().reset_index()

    fig_line = px.line(
        monthly_data,
        x="month",
        y="amount",
        markers=True,
        title="Monthly Expense Trend"
    )

    st.plotly_chart(
        fig_line,
        use_container_width=True
    )


    # DAILY + PAYMENT ANALYSIS

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📅 Daily Spending")

        daily_data = filtered_df.groupby(
            filtered_df["date"].dt.date
        )["amount"].sum().reset_index()

        daily_data.columns = [
            "date",
            "amount"
        ]

        fig_daily = px.area(
            daily_data,
            x="date",
            y="amount",
            title="Daily Spending Pattern"
        )

        st.plotly_chart(
            fig_daily,
            use_container_width=True
        )


    with col2:

        st.subheader("💳 Payment Analysis")

        payment_data = filtered_df.groupby(
            "payment_method"
        )["amount"].sum().reset_index()

        fig_payment = px.bar(
            payment_data,
            x="payment_method",
            y="amount",
            color="payment_method",
            title="Payment Method Analysis"
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )


else:

    st.warning(
        "No expenses found for the selected filters."
    )


st.divider()


# ==========================================
# BUDGET MANAGEMENT
# ==========================================

st.header("🎯 Monthly Budget Management")

budget_categories = [
    "Food",
    "Transportation",
    "Shopping",
    "Bills",
    "Education",
    "Healthcare",
    "Entertainment",
    "Travel",
    "Other"
]


# SET BUDGET

with st.expander("➕ Set or Update Budget"):

    selected_budget_category = st.selectbox(
        "Select Category",
        budget_categories,
        key="budget_category"
    )

    budget_amount = st.number_input(
        "Monthly Budget Amount (₹)",
        min_value=0.0,
        step=500.0
    )

    if st.button("Save Budget"):

        if budget_amount > 0:

            budgets[selected_budget_category] = budget_amount

            save_budgets(budgets)

            st.success(
                f"Budget saved for {selected_budget_category}!"
            )

            st.rerun()

        else:

            st.error(
                "Budget must be greater than zero."
            )


# BUDGET OVERVIEW

if budgets:

    st.subheader("📋 Budget Overview")

    current_month = pd.Timestamp.today().strftime("%Y-%m")

    current_month_df = (
        df[
            df["date"].dt.strftime("%Y-%m") == current_month
        ]
        if not df.empty
        else pd.DataFrame()
    )

    budget_records = []

    for category, budget in budgets.items():

        spent = (
            current_month_df[
                current_month_df["category"] == category
            ]["amount"].sum()
            if not current_month_df.empty
            else 0
        )

        remaining = budget - spent

        percentage = (
            (spent / budget) * 100
            if budget > 0
            else 0
        )

        budget_records.append({
            "Category": category,
            "Budget": budget,
            "Spent": spent,
            "Remaining": remaining,
            "Used (%)": round(percentage, 2)
        })


    budget_df = pd.DataFrame(budget_records)

    st.dataframe(
        budget_df,
        use_container_width=True,
        hide_index=True
    )


    # PROGRESS + ALERTS

    for category, budget in budgets.items():

        spent = (
            current_month_df[
                current_month_df["category"] == category
            ]["amount"].sum()
            if not current_month_df.empty
            else 0
        )

        percentage = (
            spent / budget
            if budget > 0
            else 0
        )

        st.markdown(f"### {category}")

        st.progress(
            min(float(percentage), 1.0)
        )

        st.write(
            f"Budget: ₹{budget:,.2f} | "
            f"Spent: ₹{spent:,.2f} | "
            f"Remaining: ₹{budget-spent:,.2f}"
        )

        if spent > budget:

            st.error(
                f"🚨 Budget exceeded for {category}!"
            )

        elif percentage >= 0.8:

            st.warning(
                f"⚠️ You have used {percentage*100:.1f}% of your budget!"
            )

        else:

            st.success(
                f"✅ Budget under control ({percentage*100:.1f}% used)."
            )


else:

    st.info(
        "No budgets set yet. Create your category budgets above."
    )


st.divider()


# ==========================================
# TRANSACTION HISTORY
# ==========================================

st.header("📋 Transaction History")

if not filtered_df.empty:

    display_df = filtered_df.sort_values(
        "date",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # CSV DOWNLOAD

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Expense Data",
        data=csv_data,
        file_name="expense_report.csv",
        mime="text/csv"
    )

else:

    st.info(
        "No transaction records available."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Personal Expense Tracker | Python | Pandas | Plotly | Streamlit"
)