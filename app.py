from flask import Flask
from routes.main import main

app = Flask(__name__)

# registrando o blueprint
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)