from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category'].lower()
        video = request.files['video']
        if video:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
            video.save(video_path)
            new_video = Video(title=title, description=description, category=category, filename=video.filename)
            db.session.add(new_video)
            db.session.commit()
            return redirect(url_for('category', category_name=category))
    return render_template('upload.html')

@app.route('/category/<category_name>')
def category(category_name):
    category_name = category_name.lower()
    videos_in_category = Video.query.filter_by(category=category_name).all()
    return render_template('category.html', category=category_name, videos=videos_in_category)

if __name__ == '__main__':
    app.run(debug=True)
