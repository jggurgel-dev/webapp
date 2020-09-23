from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Filmes %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Filmes(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."
    else:
        titulos = Filmes.query.order_by(Filmes.created_at).all()
        return render_template('index.html', titulos=titulos)

@app.route('/delete/<int:id>')
def delete(id):
    titulo = Filmes.query.get_or_404(id)
    try:
        db.session.delete(titulo)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem adding new stuff."


if __name__ == '__main__':
    app.run(debug=True)