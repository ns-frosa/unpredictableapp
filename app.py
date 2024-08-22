from flask import Flask, render_template
import time
import random

app = Flask(__name__)

@app.route('/')
def unpredictable():
    start_time = time.time() * 1000  # Convert to milliseconds
    random_value = random.random()
    
    weight1 = 0.70  # 70% for variable delay
    weight2 = 0.20  # 20% for internal server error
    weight3 = 0.10  # 10% for 15 seconds delay

    if random_value < weight3:  # First 10%
        # Simulate a timeout with a 15 seconds delay
        time.sleep(15)
        return "Request Timeout", 408

    elif random_value < weight3 + weight2:  # Next 20% after the first 10%
        # Simulate an internal server error
        return "Internal Server Error", 500

    else:  # Remaining 70%
        # Simulate variable delay
        delay = random.uniform(0, 1)
        time.sleep(delay)

    end_time = time.time() * 1000  # Convert to milliseconds
    duration = end_time - start_time
    message = f"This response happened in {duration:.6f} milliseconds"
    return render_template('test.html', message=message)

@app.route('/test')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

