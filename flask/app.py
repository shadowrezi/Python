from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = '5a03317be98fd912ee32b0a60b4e4304'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


users = {'admin': {'password': 'admin123'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user = User()
        user.id = user_id
        return user
    return None


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.date_posted = datetime.utcnow()


@app.route('/posts')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        with app.app_context():
            db.session.add(new_post)
            db.session.commit()
        return redirect('/posts')
    return render_template('create_post.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login.html', error='Неверное имя пользователя или пароль')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin.html')


@app.errorhandler(404)
def page_not_found(*_):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # with app.app_context(): db.create_all()
    app.run(debug=True)
