import pandas as pd

def get_spending_insights(df, budgets_df):
    """
    Generates a list of insights based on transaction data and budgets.
    """
    insights = []
    
    if df.empty:
        return ["👋 Welcome! Add your first transaction to get personalized insights."]

    # 1. Total Spending Alert
    total_spent = df['amount'].sum()
    if not budgets_df.empty:
        total_budget = budgets_df['budget_limit'].sum()
        if total_budget > 0:
            percent_used = (total_spent / total_budget) * 100
            if percent_used > 90:
                insights.append(f"⚠️ **Critical Alert**: You have used **{percent_used:.1f}%** of your total budget!")
            elif percent_used > 75:
                insights.append(f"⚠️ **Warning**: You have used **{percent_used:.1f}%** of your total budget.")
            elif percent_used < 50:
                insights.append(f"✅ **Good Job**: You are well within your budget ({percent_used:.1f}% used).")

    # 2. Category Analysis
    category_group = df.groupby('category')['amount'].sum()
    if not category_group.empty:
        top_category = category_group.idxmax()
        top_amount = category_group.max()
        insights.append(f"📊 **Top Spending**: You spent the most on **{top_category}** (₹{top_amount:,.2f}).")

        # Check specific budget overruns
        if not budgets_df.empty:
            for _, row in budgets_df.iterrows():
                cat = row['category']
                limit = row['budget_limit']
                spent = category_group.get(cat, 0)
                
                if spent > limit:
                    insights.append(f"🚨 **Over Budget**: You exceeded your **{cat}** budget by ₹{spent - limit:,.2f}!")
                elif spent > 0.8 * limit:
                    insights.append(f"⚠️ **Near Limit**: You are nearing your limit for **{cat}**.")

    # 3. Weekend Spender?
    df['day_of_week'] = pd.to_datetime(df['txn_date']).dt.dayofweek
    weekend_spend = df[df['day_of_week'] >= 5]['amount'].sum()
    weekday_spend = df[df['day_of_week'] < 5]['amount'].sum()
    
    if weekend_spend > weekday_spend:
        insights.append("📅 **Weekend Spender**: You tend to spend more on weekends. Keep an eye on it!")

    return insights
