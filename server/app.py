from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from server.config import Config
from server.extensions import db, migrate
from server.routes import register_routes

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
api = Api(app)

# Initialize DB and Migrate
db.init_app(app)
migrate.init_app(app, db)

# Register all routes
register_routes(api)

@app.route('/')
def index():
    return '<h1>FitFlow Fitness Tracker API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
