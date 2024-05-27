from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.String, default=datetime.now().strftime("%d %b, %Y %I:%M%p"))
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form['task']
        Todo = todo(task=task)
        db.session.add(Todo)
        db.session.commit()
    alltodo = todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    deltodo = todo.query.filter_by(sno=sno).first()
    db.session.delete(deltodo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()
