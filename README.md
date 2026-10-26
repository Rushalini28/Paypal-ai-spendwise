# PayPal AI SpendWise 💙

PayPal AI SpendWise is a personal expense tracking and spending analysis application built using Python and Streamlit.

## 🚀 Features

- **Expense Tracking:** Add and manage daily expenses.
- **Interactive Dashboard:** View total spending, monthly expenses, and transaction counts.
- **Spending Visualizations:** Explore spending patterns using charts.
- **AI-Style Spending Insights:** Analyze expenses locally and receive personalized saving recommendations without requiring a paid API.
- **SQLite Database:** Store expense records locally.
- **PayPal Integration:** PayPal Sandbox checkout integration is currently in progress.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Requests
- python-dotenv

## 📁 Project Structure

```text
paypal-ai-spendwise/
├── app.py
├── database.py
├── ai_assistant.py
├── paypal_service.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd paypal-ai-spendwise
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

- Never upload API keys or passwords.
- Keep `.env` private.
- The local SQLite database is excluded from GitHub.

## 📌 Project Status

The expense tracking dashboard, database, visualizations, and local spending analysis are implemented. PayPal Sandbox checkout integration is in progress.

## 👨‍💻 Author

Developed as a Python and AI-powered personal finance project.