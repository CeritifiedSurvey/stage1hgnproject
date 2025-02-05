from flask import Flask, request, jsonify # type: ignore
import requests # type: ignore
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 1:
        return False
    # 1 is a proper divisor for any n > 1
    divisors_sum = 1 if n > 1 else 0
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors_sum += i
            if i != n // i:
                divisors_sum += n // i
    return divisors_sum == n

def is_armstrong(n):
    # Check Armstrong property on the absolute value to ignore a potential negative sign
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d**power for d in digits) == abs(n)

def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number')
    
    # Validate input; if not convertible to int, return error JSON with 400 status
    try:
        number = int(number_param)
    except (ValueError, TypeError):
        return jsonify({
            "number": number_param,
            "error": True
        }), 400
    
    # Calculate mathematical properties
    prime_flag = is_prime(number)
    perfect_flag = is_perfect(number)
    armstrong_flag = is_armstrong(number)
    
    # Determine properties field based on Armstrong check and parity
    if armstrong_flag:
        properties = ["armstrong", "even"] if number % 2 == 0 else ["armstrong", "odd"]
    else:
        properties = ["even"] if number % 2 == 0 else ["odd"]
    
    # Calculate the sum of the digits
    d_sum = digit_sum(number)
    
    # Retrieve a fun fact using the Numbers API (math type)
    fun_fact = ""
    try:
        fact_response = requests.get(f"http://numbersapi.com/{number}/math?json", timeout=3)
        if fact_response.status_code == 200:
            fact_data = fact_response.json()
            fun_fact = fact_data.get("text", "")
    except Exception as e:
        # In case of error, leave fun_fact as an empty string
        fun_fact = ""
    
    # Build the response object
    response_data = {
        "number": number,
        "is_prime": prime_flag,
        "is_perfect": perfect_flag,
        "properties": properties,
        "digit_sum": d_sum,
        "fun_fact": fun_fact
    }
    
    return jsonify(response_data), 200

if __name__ == '__main__':
    # Run the app; for production, deploy using a WSGI server
    app.run(debug=True)
