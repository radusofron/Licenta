from flask import Flask
from controllers.index import index_controller_blueprint
from controllers.login import login_controller_blueprint
from controllers.register import register_controller_blueprint
from controllers.home import home_controller_blueprint
from controllers.destinations import destinations_controller_blueprint
from controllers.profile import profile_controller_blueprint
from controllers.destination_details import destination_details_controller_blueprint
from controllers.destination_evaluate import destination_evaluate_controller_blueprint
from controllers.itineraries import itineraries_controller_blueprint
from controllers.statistics import statistics_controller_blueprint
from views.index import index_view_blueprint
from views.login import login_view_blueprint
from views.register import register_view_blueprint
from views.home import home_view_blueprint
from views.destinations import destinations_view_blueprint
from views.profile import profile_view_blueprint
from views.error_404 import error_404_view_blueprint
from views.destination_details import destination_details_view_blueprint
from views.destination_evaluate import destination_evaluate_view_blueprint
from views.itineraries import itineraries_view_blueprint
from views.statistics import statistics_view_blueprint
from datetime import timedelta


app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = "ae30665140bb47595f0814b9456eb1e4e29f6411a04c52ae"
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["UPLOAD_FOLDER"] = "webapp/static/assets/user_photos/"


app.register_blueprint(index_controller_blueprint)
app.register_blueprint(index_view_blueprint)
app.register_blueprint(login_controller_blueprint)
app.register_blueprint(login_view_blueprint)
app.register_blueprint(register_controller_blueprint)
app.register_blueprint(register_view_blueprint)
app.register_blueprint(home_controller_blueprint)
app.register_blueprint(home_view_blueprint)
app.register_blueprint(destinations_controller_blueprint)
app.register_blueprint(destinations_view_blueprint)
app.register_blueprint(profile_controller_blueprint)
app.register_blueprint(profile_view_blueprint)
app.register_blueprint(destination_details_controller_blueprint)
app.register_blueprint(destination_details_view_blueprint)
app.register_blueprint(destination_evaluate_controller_blueprint)
app.register_blueprint(destination_evaluate_view_blueprint)
app.register_blueprint(itineraries_controller_blueprint)
app.register_blueprint(itineraries_view_blueprint)
app.register_blueprint(statistics_controller_blueprint)
app.register_blueprint(statistics_view_blueprint)
app.register_blueprint(error_404_view_blueprint)


if __name__ == "__main__":
    app.run("127.0.0.1", port=80, debug=True)
