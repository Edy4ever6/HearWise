from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from dotenv import load_dotenv
from func.helpers import hash_password, check_password
from func.database import register_user, get_user_password, get_user_name
from func.jwt_utils import create_jwt_token, decode_jwt_token

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/account_access', methods=['GET', 'POST'])
def account_access():
    if request.method == 'POST':
        # Get form data (assuming it's form data and not JSON)
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        # If 'name' is provided, it's a registration request
        if data.get('name'):
            name = data.get('name')
            if not email or not password or not name:
                return jsonify({"error": "Email, name, and password are required"}), 400
            
            hashed_password = hash_password(password)
            register_user(name, email, hashed_password)
            
            # Redirect to login page or to account page (better flow)
            return redirect(url_for('account_access'))  # Or use redirect(url_for('login')) if you want to direct users to login

        # Otherwise, it's a login request
        stored_password = get_user_password(email)
        if stored_password and check_password(password, stored_password):
            name = get_user_name(email)
            session['user'] = email
            
            # Generate JWT token
            token = create_jwt_token(email, name)
            
            # Redirect to index page with token in query parameter
            return redirect(url_for('index', token=token))
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    # Render account access page if method is GET
    return render_template('account_access.html')


@app.route('/account', methods=['GET'])
def account():
    token = request.args.get('token')  # Get the token from query parameters

    if token:
        try:
            decoded_token = decode_jwt_token(token)  # Decode the JWT token
            name = decoded_token.get('name')  # Retrieve the name from the decoded token

            if not name:
                return jsonify({"error": "Token invalid or expired"}), 401

            # Redirect to the index page with the token
            return redirect(url_for('index', token=token))
        except Exception as e:
            return jsonify({"error": "Invalid or expired token"}), 401
    else:
        return redirect(url_for('account_access'))  # Redirect if no token is present


@app.route('/index')
def index():
    # Get the token from the query string
    token = request.args.get('token')

    if token:
        try:
            decoded_token = decode_jwt_token(token)  # Decode the JWT token
            name = decoded_token.get('name')  # Retrieve the name from the decoded token

            if not name:
                return jsonify({"error": "Token invalid or expired"}), 401

            # Pass name to the template
            return render_template('index.html', name=name)
        except Exception as e:
            return jsonify({"error": "Invalid or expired token"}), 401
    else:
        return redirect(url_for('account_access'))  # Redirect to login page if no token
  # Redirect if no token is present


if __name__ == '__main__':
    app.run(debug=True)
