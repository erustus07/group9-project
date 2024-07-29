from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from routes import auth, products, users
app.register_blueprint(auth.bp)
app.register_blueprint(products.bp)
app.register_blueprint(users.bp)

@app.route('/')
def index():
    return "Welcome to the Online Shopping Community API!"

if __name__ == "__main__":
    app.run(debug=True)
