from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.srno} - {self.title}"

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        todo = Todo(title=request.form['title'], desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(srno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['POST', 'GET'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        todo = Todo.query.filter_by(srno=sno).first()

        todo.title = title
        todo.desc = description 
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(srno=sno).first()

    return render_template('update.html', allTodo=todo)

if __name__ == "__main__":
    app.run(debug=True)