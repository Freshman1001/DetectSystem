# 导入Flask 模板
from flask import Flask, render_template, request, redirect
# 导入要用到的数据库 第三方库
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# 连接数据库的配置
# MySQL所在主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，自己设置
USERNAME = "cora"
# 连接MySQL的密码，自己设置
PASSWORD = "cora1234"
# MySQL上创建的数据库名称
DATABASE = "detector"
# 通过修改以下代码来操作不同的SQL比写原生SQL简单很多 --》通过ORM可以实现从底层更改使用的SQL
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
db = SQLAlchemy(app)


# 定义模型类user
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<User user_id={self.user_id}, user_name={self.user_name}>"
    # 表中的属性已经建好：user_id(key) user_name password
    # id = db.Column(db.Integer, primary_key=True, comment="用户id")
    # password = db.Column(db.String(20), nullable=False, comment="用户密码")


# 定义模型类video
class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    v_class = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(20), nullable=True)
    v_time = db.Column(db.Time, nullable=True)
    video_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Video id={self.id}, v_class={self.v_class}>"


# 查询用户
def get_user_by_id(user_id):
    with app.app_context():
        return User.query.filter_by(user_id=user_id).first()


# 添加用户
def add_user(username, password):
    with app.app_context():
        new_user = User(user_name=username, password=password)
        db.session.add(new_user)
        db.session.commit()


# 删除用户
def delete_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()


# 修改用户密码
def update_user_password(user_id, new_password):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.password = new_password
            db.session.commit()


# 添加视频
def add_video(v_class, description, v_time, video_path):
    with app.app_context():
        new_video = Video(v_class=v_class, description=description, v_time=v_time, video_path=video_path)
        db.session.add(new_video)
        db.session.commit()


# 删除视频
def delete_video(video_id):
    with app.app_context():
        video = Video.query.get(video_id)
        if video:
            db.session.delete(video)
            db.session.commit()


# 修改视频信息
def update_video(video_id, new_v_class, new_description, new_v_time, new_video_path):
    with app.app_context():
        video = Video.query.get(video_id)
        if video:
            video.v_class = new_v_class
            video.description = new_description
            video.v_time = new_v_time
            video.video_path = new_video_path
            db.session.commit()


# 根据视频ID查询视频信息
def get_video_by_id(video_id):
    with app.app_context():
        return Video.query.get(video_id)


# 根据视频分类查询视频信息
def get_videos_by_class(v_class):
    with app.app_context():
        return Video.query.filter_by(v_class=v_class).all()


# 查询所有视频信息
def get_all_videos():
    with app.app_context():
        return Video.query.all()


# 执行所有的创建表格的语句
# 表已经建好了
# with app.app_context():
#     db.create_all()

# 登录的路由
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        id = request.form.get('name')
        pwd = request.form.get('password')
        a = User.query.filter_by(id=int(id)).first()
        if a.password == pwd and int(id) == a.id:
            return redirect('index')
    return render_template('login.html')


# 登录成功后返回index
@app.route('/index')
def admin():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

    # # 添加视频
    # add_video('class1', 'description1', '12:34:56', '/path/to/video1.mp4')
    # add_video('class2', 'description2', '18:34:56', '/path/to/video2.mp4')
    # # # 删除视频
    # # delete_video(1)
    # video1 = get_video_by_id(2)
    # video_all = get_all_videos()
    # print(video1)
    # print(video_all)
    #
    # # 修改视频信息
    # update_video(2, 'new_class', 'new_description', '23:45:01', '/path/to/new_video.mp4')
    # print(video_all)

    # # 添加用户
    # add_user('user1', 'password1')
    # add_user('user2', 'password2')
    #
    # # 查询用户
    # user = get_user_by_id(1)
    # print(user)
    #
    # # 删除用户
    # delete_user(1)
    #
    # # 修改用户密码
    # update_user_password(2, 'new_password')
    # user2 = get_user_by_id(2)
    # print(user2)
