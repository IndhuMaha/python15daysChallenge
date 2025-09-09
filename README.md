

# 💸 Expense Splitter App

A dynamic and interactive Streamlit application that helps groups of friends or colleagues split shared expenses fairly. Whether it's a trip, dinner, or group purchase, this app calculates individual contributions, highlights balances, and visualizes the data with charts.

---

## 🚀 Features

- **Dynamic Input Fields**: Automatically adjusts based on the number of people.
- **Instant Calculation**: Displays per-person share immediately after entering total expense and group size.
- **Balance Summary**: Shows how much each person owes or should be refunded.
- **Pie Chart Visualization**: Displays contribution breakdown with amount and percentage labels.
- **CSV Export**: Download the full summary for record-keeping or sharing.

---

## 🧮 How It Works

1. Enter the **total expense amount**.
2. Specify the **number of people** involved.
3. Input each person's **name** and **contribution**.
4. Click **"Calculate Split"** to view:
   - Per-person share
   - Individual balances
   - Settlement suggestions
   - Contribution chart
5. Optionally, click **"Download CSV"** to export the summary.

---

## 📊 Visualization

The app uses **Plotly** to generate a pie chart showing:
- Each person's contribution
- Percentage of total
- Actual amount paid

---

## 🛠 Installation

Make sure you have Python installed, then install the required packages:

```bash
pip install streamlit pandas plotly
▶️ Run the App
bash
streamlit run expense_splitter.py
📁 File Structure
Code
expense_splitter/
├── expense_splitter.py      # Main Streamlit app
├── README.md                # App documentation
📌 Notes
Maximum supported group size: 20 people

Contributions must be non-negative

App resets all fields with the "Clear All" button

📬 Feedback & Contributions
Feel free to fork, improve, or suggest new features like:

Settlement optimization

Expense categories

Multi-currency support

Pull requests are welcome!

🧑‍💻 Author
