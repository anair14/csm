from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snippet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for code snippets
class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Routes
@app.route('/')
def index():
    snippets = Snippet.query.all()
    return render_template('index.html', snippets=snippets)

@app.route('/add', methods=['GET', 'POST'])
def add_snippet():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_snippet = Snippet(title=title, content=content)
        db.session.add(new_snippet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_snippet.html')

@app.route('/delete/<int:id>')
def delete_snippet(id):
    snippet = Snippet.query.get(id)
    if snippet:
        db.session.delete(snippet)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

