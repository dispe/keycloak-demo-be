# Prerequisites

- Install Python
- Activate an environment
- pip install Flask flask-cors python-jose requests
- pip freeze > requirements.txt
- chnage the secret key with the one from your Keycloak instance
- run main.py

- Keycloak is installed - see the FE project
  - create a new client: myclient-be - https://www.keycloak.org/docs/latest/authorization_services/index.html
  

:information_source: For simplicity demonstration, no .env is used. Being a local and temporary docker instance, client secret is not a threat and it's lifespan is limited for this demo purposes only.