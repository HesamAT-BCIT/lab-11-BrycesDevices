from flask import Flask

from blueprints.api import api_bp
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.profile import profile_bp
from config import Config
import firebase  # noqa: F401
from utils.logging import JSONFormatter  # noqa: F401

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
