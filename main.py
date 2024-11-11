#Import Libraries
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

#Create Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
