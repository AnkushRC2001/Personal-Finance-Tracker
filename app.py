import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from db import add_transaction, get_transactions, set_budget, check_budgets
from categorizer import categorize_transaction
from insights import get_spending_insights

# --- Page Config ---
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰", layout="wide")

# --- Custom CSS ---
# --- Custom CSS ---
st.markdown("""
    <style>
    /* Remove hardcoded backgrounds to support Dark Mode */
    .stMetric {
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .insight-box {
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #38b2ac;
        background-color: rgba(56, 178, 172, 0.1); /* Semi-transparent teal */
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper Functions ---
def load_data():
    df = get_transactions()
    if not df.empty:
        df['txn_date'] = pd.to_datetime(df['txn_date'])
        df['month_year'] = df['txn_date'].dt.strftime('%Y-%m')
    return df

# --- Sidebar ---
with st.sidebar:
    st.title("💰 Finance Tracker")
    page = st.radio("Navigation", ["Dashboard", "Add Transaction", "Manage Budgets"])
    st.markdown("---")
    
    # Global Date Filter
    df = load_data()
    selected_month = None
    
    if not df.empty:
        st.subheader("📅 Filter Data")
        unique_months = sorted(df['month_year'].unique(), reverse=True)
        selected_month = st.selectbox("Select Month", unique_months)
        monthly_df = df[df['month_year'] == selected_month]
    else:
        monthly_df = pd.DataFrame()
        st.info("No data available yet.")

# --- Dashboard Page ---
if page == "Dashboard":
    st.title("📊 Financial Dashboard")
    st.markdown(f"**Overview for {selected_month}**")
    
    if monthly_df.empty:
        st.info("No transactions found for the selected month. Add some data to get started!")
    else:
        # 1. Smart Insights Section
        st.subheader("💡 Smart Insights")
        budgets = check_budgets()
        insights = get_spending_insights(monthly_df, budgets)
        
        for insight in insights:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)
        
        st.markdown("---")

        # 2. Key Metrics
        total_spent = monthly_df['amount'].sum()
        total_budget = budgets['budget_limit'].sum() if not budgets.empty else 0
        remaining = total_budget - total_spent
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spent", f"₹{total_spent:,.2f}", delta=f"{len(monthly_df)} transactions")
        col2.metric("Total Budget", f"₹{total_budget:,.2f}")
        col3.metric("Remaining", f"₹{remaining:,.2f}", delta_color="normal" if remaining >= 0 else "inverse")
        
        # 3. Visualizations
        st.subheader("📈 Spending Analysis")
        
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown("### Category Breakdown")
            category_group = monthly_df.groupby('category')['amount'].sum().reset_index()
            fig_pie = px.pie(category_group, values='amount', names='category', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.markdown("### Daily Trend")
            daily_trend = monthly_df.groupby(monthly_df['txn_date'].dt.day)['amount'].sum().reset_index()
            fig_line = px.line(daily_trend, x='txn_date', y='amount', markers=True, line_shape='spline')
            fig_line.update_traces(line_color='#38b2ac')
            fig_line.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Day of Month", yaxis_title="Amount")
            st.plotly_chart(fig_line, use_container_width=True)

# --- Add Transaction Page ---
elif page == "Add Transaction":
    st.title("➕ Add New Transaction")
    
    with st.container():
        st.markdown("### Manual Entry")
        with st.form("transaction_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", datetime.today())
                amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
            with col2:
                desc = st.text_input("Description")
                category_option = st.selectbox("Category", ["Auto", "Food", "Travel", "Shopping", "Utilities", "Entertainment", "Health", "Rent", "Other"])
            
            submitted = st.form_submit_button("Add Transaction", use_container_width=True)
            if submitted:
                if desc and amount > 0:
                    cat = categorize_transaction(desc) if category_option == "Auto" else category_option
                    add_transaction(date.strftime('%Y-%m-%d'), desc, amount, cat)
                    st.success(f"✅ Added: **{desc}** (₹{amount}) in *{cat}*")
                else:
                    st.error("Please enter valid description and amount.")

    st.markdown("---")
    st.markdown("### 📂 Bulk Upload")
    uploaded_file = st.file_uploader("Upload CSV (Date, Description, Amount)", type=["csv"])
    if uploaded_file:
        try:
            csv_df = pd.read_csv(uploaded_file)
            st.dataframe(csv_df.head(), use_container_width=True)
            
            # Column Validation
            required_cols = ['Date', 'Description', 'Amount']
            missing_cols = [col for col in required_cols if col not in csv_df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing columns: {', '.join(missing_cols)}. Please check your CSV.")
            else:
                if st.button("Import Data", type="primary"):
                    count = 0
                    errors = 0
                    for _, row in csv_df.iterrows():
                        try:
                            # Robust Date Parsing
                            raw_date = str(row['Date'])
                            try:
                                d = pd.to_datetime(raw_date, dayfirst=True).strftime('%Y-%m-%d')
                            except:
                                d = datetime.today().strftime('%Y-%m-%d') # Fallback
                            
                            desc = str(row['Description'])
                            
                            # Clean Amount (remove currency symbols, commas)
                            raw_amount = str(row['Amount'])
                            clean_amount = raw_amount.replace('₹', '').replace('$', '').replace(',', '').strip()
                            amt = float(clean_amount)
                            
                            cat = categorize_transaction(desc)
                            add_transaction(d, desc, amt, cat)
                            count += 1
                        except Exception as e:
                            errors += 1
                            continue
                    
                    if count > 0:
                        st.success(f"✅ Successfully imported {count} transactions!")
                    if errors > 0:
                        st.warning(f"⚠️ Skipped {errors} rows due to errors.")
                        
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# --- Manage Budgets Page ---
elif page == "Manage Budgets":
    st.title("💸 Manage Budgets")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Set Limit")
        with st.form("budget_form"):
            b_cat = st.selectbox("Category", ["Food", "Travel", "Shopping", "Utilities", "Entertainment", "Health", "Rent", "Other"])
            b_limit = st.number_input("Monthly Limit (₹)", min_value=0.0)
            
            if st.form_submit_button("Set Budget", use_container_width=True):
                set_budget(b_cat, b_limit)
                st.success(f"Budget set for {b_cat}")
                st.rerun()
    
    with col2:
        st.markdown("### Budget Status")
        budgets_df = check_budgets()
        if not budgets_df.empty:
            budgets_df['percent'] = (budgets_df['spent'] / budgets_df['budget_limit']) * 100
            budgets_df['percent'] = budgets_df['percent'].clip(upper=100)
            
            st.dataframe(
                budgets_df.style.format({"budget_limit": "₹{:.2f}", "spent": "₹{:.2f}"})
                .bar(subset=['percent'], color='#ef4444', vmin=0, vmax=100),
                use_container_width=True,
                height=400
            )
        else:
            st.info("No budgets set yet. Set one to get started!")
