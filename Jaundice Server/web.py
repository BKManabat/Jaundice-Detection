
from flask import Flask, session, redirect, url_for, render_template

from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret!'
        
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # start_thread()
    app.run( host="0.0.0.0", port=5000, debug=True)

