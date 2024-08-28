from flask import Flask, render_template, request
import time
import random
import socket
import struct

app = Flask(__name__)

@app.route('/')
def unpredictable():
    start_time = time.time() * 1000  # Convert to milliseconds
    random_value = random.random()

    weight1 = 0.60  # 60% for variable delay
    weight2 = 0.10  # 10% for internal server error
    weight3 = 0.15  # 15% for 15 seconds delay
    weight4 = 0.15  # 15% for TCP connection reset

    if random_value < weight4:  # First 15%
        # Reset the TCP connection by shutting down and closing the socket forcefully
        socket_fd = request.environ.get('wsgi.input').raw._sock
        socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        socket_fd.close()
        return  # No response will be sent; the connection is reset

    elif random_value < weight4 + weight3:  # Next 15% after the first 15%
        # Simulate a timeout with a 15 seconds delay
        time.sleep(15)
        return "Request Timeout", 408

    elif random_value < weight4 + weight3 + weight2:  # Next 10% after the first 30%
        # Simulate an internal server error
        return "Internal Server Error", 500

    else:  # Remaining 60%
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
