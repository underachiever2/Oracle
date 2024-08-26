import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import time

def initialize_database():
    print("Initializing database...")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password_hash TEXT)''')
    print("Users table created.")
    
    # Create charts table
    c.execute('''CREATE TABLE IF NOT EXISTS charts
                 (chart_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, stock_name TEXT, ticker TEXT, 
                 last_price REAL, last_date TEXT, chart_data BLOB, uploaded_at TEXT)''')
    print("Charts table created.")
    
    # Create admin management table
    c.execute('''CREATE TABLE IF NOT EXISTS admin_management
                 (admin_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, operation TEXT, timestamp TEXT)''')
    print("Admin management table created.")
    
    conn.commit()
    conn.close()
    print("Database initialization complete.\n")

def sign_up(username, email, password):
    print(f"Signing up user: {username}")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    c.execute('''INSERT INTO users (username, email, password_hash)
                 VALUES (?, ?, ?)''', (username, email, password_hash))
    conn.commit()
    conn.close()
    print("User signed up successfully.\n")

def sign_in(username, password):
    print(f"Signing in user: {username}")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    c.execute('''SELECT password_hash FROM users WHERE username = ?''', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[0], password):
        print("Sign-in successful!\n")
        return True
    print("Sign-in failed.\n")
    return False

def upload_chart(user_id, stock_name, ticker, chart_data):
    print(f"Uploading chart for {stock_name} ({ticker})...")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    
    # Ensure last_price is a single numeric value
    last_price = float(chart_data['Close'].iloc[-1])  # Convert to float to ensure it's a numeric type
    last_date = str(chart_data['Date'].iloc[-1])  # Ensure date is a string
    
    # Insert the data into the database
    c.execute('''INSERT INTO charts (user_id, stock_name, ticker, last_price, last_date, chart_data, uploaded_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (user_id, stock_name, ticker, last_price, last_date, chart_data.to_json(), 
               pd.Timestamp.today().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    print("Chart uploaded successfully.\n")

def retrieve_chart_data(stock_name, ticker):
    print(f"Retrieving chart data for {stock_name} ({ticker})...")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    c.execute('''SELECT chart_data FROM charts WHERE stock_name = ? AND ticker = ? ORDER BY last_date DESC LIMIT 1''', 
              (stock_name, ticker))
    data = c.fetchone()
    conn.close()
    if data:
        chart_data = pd.read_json(data[0])
        print("Chart data retrieved successfully.\n")
        return chart_data
    else:
        print(f"No data found for {stock_name} ({ticker}).\n")
        return None

def generate_analysis(stock_name, ticker, chart_data):
    print(f"Generating analysis for {stock_name} ({ticker})...")
    # Perform analysis (mocked for this script)
    analysis_results = {
        "Last Price": chart_data['Close'].iloc[-1],
        "30-Day Prediction": chart_data['Close'].iloc[-1] * 1.02,
        "60-Day Prediction": chart_data['Close'].iloc[-1] * 1.04,
        "90-Day Prediction": chart_data['Close'].iloc[-1] * 1.06,
        "Recommended Strategy": "Buy and Hold"
    }
    print("Analysis generated.\n")
    return analysis_results

def create_downloadable_report(stock_name, analysis_results, format="PDF"):
    print(f"Creating {format} report for {stock_name}...")
    # Generate a downloadable report in the specified format (PDF/CSV)
    if format == "PDF":
        # Mocked PDF generation
        pdf_content = f"Analysis Report for {stock_name}\n\n"
        for key, value in analysis_results.items():
            pdf_content += f"{key}: {value}\n"
        print("PDF report created.\n")
        return pdf_content
    elif format == "CSV":
        df = pd.DataFrame([analysis_results])
        csv_content = df.to_csv(index=False)
        print("CSV report created.\n")
        return csv_content

def add_disclaimer(report_content):
    disclaimer = "\n\nDisclaimer: This analysis is not financial advice. Please consult a financial professional before making investment decisions."
    print("Disclaimer added to the report.\n")
    return report_content + disclaimer

# Initialize the database
initialize_database()

# Example usage

# Sign-up a new user
sign_up("real_user", "real_user@example.com", "securepassword")

# Sign-in an existing user
if sign_in("real_user", "securepassword"):
    # Prompt the user to enter stock name and ticker symbol
    stock_name = input("Enter the stock name: ")
    ticker = input("Enter the ticker symbol: ")
    
    # Retrieve chart data for analysis
    chart_data = retrieve_chart_data(stock_name, ticker)
    
    if chart_data is not None:
        # Generate an analysis and create a downloadable report
        analysis = generate_analysis(stock_name, ticker, chart_data)
        report = create_downloadable_report(stock_name, analysis, "PDF")
        final_report = add_disclaimer(report)
        print(final_report)
    else:
        print("No data available for analysis. Please upload data and try again.")
import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import time

def initialize_database():
    print("Initializing database...")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password_hash TEXT)''')
    print("Users table created.")
    
    # Create charts table
    c.execute('''CREATE TABLE IF NOT EXISTS charts
                 (chart_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, stock_name TEXT, ticker TEXT, 
                 last_price REAL, last_date TEXT, chart_data BLOB, uploaded_at TEXT)''')
    print("Charts table created.")
    
    # Create admin management table
    c.execute('''CREATE TABLE IF NOT EXISTS admin_management
                 (admin_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, operation TEXT, timestamp TEXT)''')
    print("Admin management table created.")
    
    conn.commit()
    conn.close()
    print("Database initialization complete.\n")

def sign_up(username, email, password):
    print(f"Signing up user: {username}")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    c.execute('''INSERT INTO users (username, email, password_hash)
                 VALUES (?, ?, ?)''', (username, email, password_hash))
    conn.commit()
    conn.close()
    print("User signed up successfully.\n")

def sign_in(username, password):
    print(f"Signing in user: {username}")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    c.execute('''SELECT password_hash FROM users WHERE username = ?''', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[0], password):
        print("Sign-in successful!\n")
        return True
    print("Sign-in failed.\n")
    return False

def upload_chart(user_id, stock_name, ticker, chart_data):
    print(f"Uploading chart for {stock_name} ({ticker})...")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    
    # Ensure last_price is a single numeric value
    last_price = float(chart_data['Close'].iloc[-1])  # Convert to float to ensure it's a numeric type
    last_date = str(chart_data['Date'].iloc[-1])  # Ensure date is a string
    
    # Insert the data into the database
    c.execute('''INSERT INTO charts (user_id, stock_name, ticker, last_price, last_date, chart_data, uploaded_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (user_id, stock_name, ticker, last_price, last_date, chart_data.to_json(), 
               pd.Timestamp.today().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    print("Chart uploaded successfully.\n")

def retrieve_chart_data(stock_name, ticker):
    print(f"Retrieving chart data for {stock_name} ({ticker})...")
    conn = sqlite3.connect('/home/ec2-user/stock_analysis.db')
    c = conn.cursor()
    c.execute('''SELECT chart_data FROM charts WHERE stock_name = ? AND ticker = ? ORDER BY last_date DESC LIMIT 1''', 
              (stock_name, ticker))
    data = c.fetchone()
    conn.close()
    if data:
        chart_data = pd.read_json(data[0])
        print("Chart data retrieved successfully.\n")
        return chart_data
    else:
        print(f"No data found for {stock_name} ({ticker}).\n")
        return None

def generate_analysis(stock_name, ticker, chart_data):
    print(f"Generating analysis for {stock_name} ({ticker})...")
    # Perform analysis (mocked for this script)
    analysis_results = {
        "Last Price": chart_data['Close'].iloc[-1],
        "30-Day Prediction": chart_data['Close'].iloc[-1] * 1.02,
        "60-Day Prediction": chart_data['Close'].iloc[-1] * 1.04,
        "90-Day Prediction": chart_data['Close'].iloc[-1] * 1.06,
        "Recommended Strategy": "Buy and Hold"
    }
    print("Analysis generated.\n")
    return analysis_results

def create_downloadable_report(stock_name, analysis_results, format="PDF"):
    print(f"Creating {format} report for {stock_name}...")
    # Generate a downloadable report in the specified format (PDF/CSV)
    if format == "PDF":
        # Mocked PDF generation
        pdf_content = f"Analysis Report for {stock_name}\n\n"
        for key, value in analysis_results.items():
            pdf_content += f"{key}: {value}\n"
        print("PDF report created.\n")
        return pdf_content
    elif format == "CSV":
        df = pd.DataFrame([analysis_results])
        csv_content = df.to_csv(index=False)
        print("CSV report created.\n")
        return csv_content

def add_disclaimer(report_content):
    disclaimer = "\n\nDisclaimer: This analysis is not financial advice. Please consult a financial professional before making investment decisions."
    print("Disclaimer added to the report.\n")
    return report_content + disclaimer

# Initialize the database
initialize_database()

# Example usage

# Sign-up a new user
sign_up("real_user", "real_user@example.com", "securepassword")

# Sign-in an existing user
if sign_in("real_user", "securepassword"):
    # Prompt the user to enter stock name and ticker symbol
    stock_name = input("Enter the stock name: ")
    ticker = input("Enter the ticker symbol: ")
    
    # Retrieve chart data for analysis
    chart_data = retrieve_chart_data(stock_name, ticker)
    
    if chart_data is not None:
        # Generate an analysis and create a downloadable report
        analysis = generate_analysis(stock_name, ticker, chart_data)
        report = create_downloadable_report(stock_name, analysis, "PDF")
        final_report = add_disclaimer(report)
        print(final_report)
    else:
        print("No data available for analysis. Please upload data and try again.")

