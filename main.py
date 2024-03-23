# This is the main file to execute
from Website import create_app
from dotenv import load_dotenv

load_dotenv('.env')

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, ssl_context=('cert.pem', 'key.pem'))