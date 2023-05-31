from flask import Flask
from views import views

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thesis'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.register_blueprint(views)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
