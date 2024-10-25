from flask import Flask, request

app = Flask(__name__)

@app.route('/test')
def index():
    
    headers = {key: value for key, value in request.headers.items()}
    print(f"Incoming Headers: {headers}")  # Log all incoming headers


    # Retrieve CLIENTIP header
    client_ip_header = request.headers.get('Client_IP')
    
    # Determine which IP to use
    client_ip = client_ip_header if client_ip_header else request.remote_addr

    # Prepare response with labeled values
    response = {
        "client_ip": {
            "value": client_ip,
            "source": "X-Forwarded-For" if client_ip_header else "remote_addr"
        },
        "x_real_ip": {
            "value": request.headers.get('X-Real-IP'),
            "source": "X-Real-IP header"
        },
        "x_forwarded_for": {
            "value": request.headers.get('X-Forwarded-For'),
            "source": "X-Forwarded-For header"
        },
        "x_original_forwarded_for": {
            "value": request.headers.get('X-Original-Forwarded-For'),
            "source": "X-Original-Forwarded-For header"
        },
        "headers": headers  # Include all request headers
    }

    # Log values for debugging
    print(f"CLIENTIP Header: {client_ip_header}")
    print(f"Remote Address: {request.remote_addr}")

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
