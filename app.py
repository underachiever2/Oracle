from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}
user_charts = {}
user_favorites = {}

def save_chart_analysis(username, stock_name, ticker, analysis):
    if username not in user_charts:
        user_charts[username] = []
    user_charts[username].append(analysis)

def generate_stock_illustration(df, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Close/Last'], label=ticker)
    plt.title(f"{ticker} Stock Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"static/{ticker}_illustration.png")
    plt.close()

def clean_price(price):
    """Function to clean the price string and convert it to a float."""
    return float(price.replace('$', '').replace(',', ''))

def calculate_prediction_accuracy(df):
    df['Close/Last'] = df['Close/Last'].apply(clean_price)
    df['Days'] = np.arange(len(df))
    
    X = df[['Days']].values
    y = df['Close/Last'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    accuracy = 100 - (np.mean(np.abs((y - predictions) / y)) * 100)
    return round(accuracy, 2)

@app.route('/')
def home():
    return render_template('UI.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users[username] = {'email': email, 'password': password}
        user_favorites[username] = []
        return redirect(url_for('sign_in'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            if username not in user_charts:
                user_charts[username] = []
            return redirect(url_for('member_interface'))
        return "Invalid credentials, please try again."
    return render_template('signin.html')

@app.route('/member')
def member_interface():
    if 'username' not in session:
        return redirect(url_for('sign_in'))
    
    username = session['username']
    
    if username not in user_favorites:
        user_favorites[username] = []

    return render_template('member_interface.html', username=username, charts=user_charts[username])

@app.route('/upload_chart', methods=['GET', 'POST'])
def upload_chart():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        stock_name = request.form['stock_name']
        ticker = request.form['ticker']

        # Load CSV data
        df = pd.read_csv(file)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        last_row = df.iloc[-1]
        last_price = last_row['Close/Last']

        # Clean the last price and convert it to a float
        last_price = clean_price(last_price)

        # Generate predictions based on the last price
        prediction_30_days = last_price * 1.05
        prediction_60_days = last_price * 1.10
        prediction_90_days = last_price * 1.15
        prediction_today = last_price * 1.02

        # Calculate prediction accuracy
        prediction_accuracy = calculate_prediction_accuracy(df)

        # Generate stock-specific analysis summary
        summary = (f"The stock {stock_name} ({ticker}) is currently priced at ${last_price:.2f}. "
                   f"In 30 days, the price is predicted to reach ${prediction_30_days:.2f}. "
                   f"In 60 days, the price is predicted to reach ${prediction_60_days:.2f}. "
                   f"In 90 days, the price is predicted to reach ${prediction_90_days:.2f}. "
                   f"The prediction accuracy is estimated to be {prediction_accuracy}%. "
                   f"Based on the current trends, the stock is showing a bullish pattern.")

        analysis = {
            'stock_name': stock_name,
            'ticker': ticker,
            'last_price': round(last_price, 2),
            'prediction_30_days': round(prediction_30_days, 2),
            'prediction_60_days': round(prediction_60_days, 2),
            'prediction_90_days': round(prediction_90_days, 2),
            'prediction_today': round(prediction_today, 2),
            'summary': summary,
            'prediction_accuracy': prediction_accuracy
        }

        generate_stock_illustration(df, ticker)

        # Save the analysis to user charts
        if not any(analysis['ticker'] == chart['ticker'] for chart in user_charts[session['username']]):
            save_chart_analysis(session['username'], stock_name, ticker, analysis)

        return render_template('member_interface.html', username=session['username'], charts=user_charts[session['username']], analysis=analysis)

    return render_template('upload_chart.html')

@app.route('/save_chart', methods=['POST'])
def save_chart():
    if 'username' not in session:
        return redirect(url_for('sign_in'))

    username = session['username']
    stock_name = request.form['stock_name']
    ticker = request.form['ticker']
    last_price = request.form['last_price']
    prediction_30_days = request.form['prediction_30_days']
    prediction_60_days = request.form['prediction_60_days']
    prediction_90_days = request.form['prediction_90_days']
    summary = request.form['summary']

    analysis = {
        'stock_name': stock_name,
        'ticker': ticker,
        'last_price': last_price,
        'prediction_30_days': prediction_30_days,
        'prediction_60_days': prediction_60_days,
        'prediction_90_days': prediction_90_days,
        'summary': summary
    }

    save_chart_analysis(username, stock_name, ticker, analysis)

    return redirect(url_for('member_interface'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)

