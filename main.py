from website import create_app

app = create_app()

# only run the app if main.py executes
if __name__ == '__main__':
    # debug is on during development
    app.run(debug = True)