from flask import Flask
from controllers.index import index_controller_blueprint
from controllers.login import login_controller_blueprint
from controllers.register import register_controller_blueprint
from controllers.home import home_controller_blueprint
from views.index import index_view_blueprint
from views.login import login_view_blueprint
from views.register import register_view_blueprint
from views.home import home_view_blueprint
from datetime import timedelta


app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = "a_secrey_key"
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

app.register_blueprint(index_controller_blueprint)
app.register_blueprint(index_view_blueprint)
app.register_blueprint(login_controller_blueprint)
app.register_blueprint(login_view_blueprint)
app.register_blueprint(register_controller_blueprint)
app.register_blueprint(register_view_blueprint)
app.register_blueprint(home_controller_blueprint)
app.register_blueprint(home_view_blueprint)


if __name__ == "__main__":
    app.run("127.0.0.1", port=80, debug=True)
