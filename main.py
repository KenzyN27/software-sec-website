from website import create_app
from dotenv import load_dotenv

load_dotenv('.env')

app = create_app()

# only run the app if main.py executes
if __name__ == '__main__':
    # debug is on during development
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))