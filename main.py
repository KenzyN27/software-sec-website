from website import create_app
from dotenv import load_dotenv

load_dotenv('.env')

app = create_app()

# only run the app if main.py executes
if __name__ == '__main__':
    # debug is on during development
    # default port is 5000 but that doesn't work with ssl
    app.run(host='127.0.0.1', port=5001, ssl_context=('cert.pem', 'key.pem'))