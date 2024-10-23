from flask import Flask, render_template
from database import db_session, init_db
from config import get_config

app = Flask(__name__)
app.config.from_object(get_config())

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=app.config['DEBUG'])
