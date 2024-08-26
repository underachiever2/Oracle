import pandas as pd
import matplotlib.pyplot as plt
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock database for users and stocks
users = {}
stocks = []

@app.route('/')
def home():
    return render_template('UI.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Store user information (You should hash the password in a real app)
        users[username] = {'email': email, 'password': password}
        return redirect(url_for('sign_in'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user exists and password is correct
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials, please try again."
    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('sign_in'))
    username = session['username']
    return render_template('dashboard.html', username=username, available_stocks=stocks)

@app.route('/upload_chart', methods=['GET', 'POST'])
def upload_chart():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        stock_name = request.form['stock_name']
        ticker = request.form['ticker']

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)

        # Ensure the Date column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'])

        # Sort the DataFrame by date to ensure the latest date is at the end
        df = df.sort_values(by='Date')

        # Get the last row of the DataFrame, which should be the most recent date
        last_row = df.iloc[-1]
        last_price = last_row['Close/Last']  # Assuming the column name is 'Close/Last'
        last_price = float(last_price.replace('$', '').replace(',', ''))  # Clean and convert to float

        # Simulated predictions (replace with actual logic)
        prediction_30_days = last_price * 1.05  # Example: 5% increase
        prediction_60_days = last_price * 1.10
        prediction_90_days = last_price * 1.15
        prediction_today = last_price * 1.02  # Example: 2% increase for today's prediction

        # Placeholder for prediction accuracy (replace with actual logic)
        prediction_accuracy = 85.0  # Example: 85% accuracy

        # Example bullish and bearish indicators (replace with actual logic)
        bullish_indicators = 3
        bearish_indicators = 1

        # Adjust the grammar based on the number of indicators
        bullish_text = f"{bullish_indicators} {'is' if bullish_indicators == 1 else 'are'} bullish"
        bearish_text = f"{bearish_indicators} {'is' if bearish_indicators == 1 else 'are'} bearish"

        summary = (f"The stock {stock_name} ({ticker}) is showing a bullish trend with an expected price increase "
                   f"over the next 90 days. Out of 4 indicators, {bullish_text} and {bearish_text}. "
                   f"The prediction accuracy is estimated to be {prediction_accuracy}%.")

        analysis = {
            'stock_name': stock_name,
            'ticker': ticker,
            'last_price': last_price,
            'prediction_30_days': round(prediction_30_days, 2),
            'prediction_60_days': round(prediction_60_days, 2),
            'prediction_90_days': round(prediction_90_days, 2),
            'prediction_today': round(prediction_today, 2),
            'summary': summary,
            'prediction_accuracy': prediction_accuracy
        }

        # Generate a chart
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Close/Last'].apply(lambda x: float(x.replace('$', '').replace(',', ''))), label='Historical Prices')
        plt.axhline(y=last_price, color='r', linestyle='--', label='Last Price')
        plt.axhline(y=prediction_today, color='g', linestyle='--', label="Today's Prediction")
        plt.title(f"{stock_name} ({ticker}) - Historical Data and Predictions")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()

        # Save the chart to a file
        chart_path = f'static/{ticker}_chart.png'
        plt.savefig(chart_path)
        plt.close()

        # Render the analysis template with the analysis results and the chart
        return render_template('analysis.html', analysis=analysis, chart_path=chart_path)

    return render_template('upload_chart.html')

@app.route('/analyze/<ticker>')
def analyze_stock(ticker):
    # Analysis logic goes here
    return f"Analysis for {ticker} is not implemented yet."

@app.route('/price_predictions')
def price_predictions():
    # Price prediction logic goes here
    return "Price prediction feature is not implemented yet."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

