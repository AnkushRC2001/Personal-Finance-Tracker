# 💰 Personal Finance Tracker

A modern, interactive personal finance dashboard built with **Python** and **Streamlit**. Track your expenses, set monthly budgets, and visualize your spending habits with ease.

## ✨ Features

- **📊 Interactive Dashboard**: Get a high-level overview of your finances with key metrics (Total Spent, Budget, Remaining) and dynamic charts.
- **💡 Smart Insights**: Receive automated insights about your spending patterns (e.g., "You've spent 80% of your Food budget").
- **📈 Visualizations**:
    - **Category Breakdown**: Interactive pie chart showing where your money goes.
    - **Daily Trend**: Line chart tracking daily spending fluctuations.
- **➕ Add Transactions**:
    - **Manual Entry**: Easy-to-use form for single transactions.
    - **Bulk Upload**: Upload CSV files to import multiple transactions at once.
- **💸 Budget Management**: Set monthly limits for different categories and track your progress with visual progress bars.
- **🎨 Theme-Adaptive UI**: A beautiful interface that automatically adapts to Light and Dark modes.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **Visualization**: [Plotly](https://plotly.com/python/)
- **Database**: SQLite (Local storage)

## 🚀 Installation & Setup

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone <repository-url>
    cd Personal-Finance-Tracker
    ```

2.  **Install dependencies**:
    Make sure you have Python installed. Then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

4.  **Open in Browser**:
    The app will automatically open in your default web browser (usually at `http://localhost:8501`).

## 📂 Project Structure

```
Personal-Finance-Tracker/
├── app.py              # Main Streamlit application entry point
├── db.py               # Database operations (SQLite)
├── categorizer.py      # Logic for auto-categorizing transactions
├── insights.py         # Logic for generating spending insights
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 📝 Usage Guide

1.  **Dashboard**: Start here to see your financial health at a glance. Use the sidebar to filter data by month.
2.  **Add Transaction**:
    - Go to the "Add Transaction" page.
    - Use the **Manual Entry** tab to add single expenses.
    - Use the **Bulk Upload** tab to upload a CSV with columns: `Date`, `Description`, `Amount`.
3.  **Manage Budgets**:
    - Go to the "Manage Budgets" page.
    - Select a category and set a monthly limit.
    - View the progress bars to see how close you are to your limits.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is open-source and available under the MIT License.
