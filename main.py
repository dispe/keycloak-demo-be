from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from jose import jwt
import requests

app = Flask(__name__)
CORS(app, resources={r"/users/me": {"origins": "http://localhost:5173",
                                    "methods": ["GET", "OPTIONS"],
                                    "allow_headers": [
                                        "Authorization", 
                                        "Content-Type", 
                                        "Access-Control-Allow-Origin", 
                                        "Access-Control-Allow-Headers", 
                                        "Access-Control-Allow-Methods"
                                                    ]
                                    }})

# Your Keycloak server details
KEYCLOAK_URL = "http://localhost:8080/realms/myrealm"
KEYCLOAK_CLIENT_ID = "myclient-be"
KEYCLOAK_CLIENT_SECRET = "JM11hsFrjiGu3L8HlF3cwfEwJTieKCvv"
KEYCLOAK_PUBLIC_KEY = None

@app.route('/users/me', methods=['GET', 'OPTIONS'])
def user_me():
    if request.method == 'OPTIONS':
        # Preflight request handling
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    else:
        # Check if the Authorization header is present
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 401

        token = request.headers.get('Authorization').split()[1]

        try:
            # introspect token
            introspect_url = f"{KEYCLOAK_URL}/protocol/openid-connect/token/introspect"
            introspect_response = requests.post(introspect_url, data={'token': token, 'client_id': KEYCLOAK_CLIENT_ID, 'client_secret': KEYCLOAK_CLIENT_SECRET})
            decoded_token = introspect_response.json()
            if decoded_token['active'] == False:
                return jsonify({'error': 'Token is not active'}), 401
            
            return jsonify(decoded_token)
        except Exception as e:
            return jsonify({'error': str(e)}), 401


def get_keycloak_public_key():
    global KEYCLOAK_PUBLIC_KEY
    if not KEYCLOAK_PUBLIC_KEY:
        # Fetch the public key from Keycloak
        r = requests.get(f"{KEYCLOAK_URL}/protocol/openid-connect/certs")
        jwk = r.json()['keys'][0]
        KEYCLOAK_PUBLIC_KEY = jwt.jwk.construct(jwk).to_pem()
    return KEYCLOAK_PUBLIC_KEY

if __name__ == '__main__':
    app.run(debug=True)
