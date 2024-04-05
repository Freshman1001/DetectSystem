# 四川大学 田亚君
# 开发时间：2024-03-29 19:31
# 导入Flask 模板
from flask import Flask, render_template, request, redirect, jsonify, url_for
# 导入要用到的数据库 第三方库
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)

# 连接数据库的配置
# MySQL所在主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，自己设置
USERNAME = ""
# 连接MySQL的密码，自己设置
PASSWORD = ""
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
    v_path = db.Column(db.String(255), nullable=False)
    v_class = db.Column(db.String(255), nullable=True)
    v_time = db.Column(db.Date, nullable=True)
    v_location = db.Column(db.String(255), nullable=True)
    v_region = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Video id={self.id}, v_path={self.v_path}, v_class={self.v_class}, \
        v_time={self.v_time}, v_location={self.v_location}, v_region={self.v_region}, description={self.description}>"


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
def add_video(v_path, v_class, v_time, v_location, v_region, description):
    with app.app_context():
        new_video = Video(v_path=v_path, v_class=v_class, v_time=v_time,
                          v_location=v_location, v_region=v_region, description=description)
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
def update_video(video_id, new_v_path, new_v_class, new_v_time, new_v_location, new_v_region, new_description):
    with app.app_context():
        video = Video.query.get(video_id)
        if video:
            video.v_path = new_v_path
            video.v_class = new_v_class
            video.v_time = new_v_time
            video.v_location = new_v_location
            video.v_region = new_v_region
            video.description = new_description
            db.session.commit()

# 根据视频存储时间查询视频信息
def get_videos_by_date_range(start_date, end_date):
    with app.app_context():
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return Video.query.filter(Video.v_time.between(start_date, end_date)).all()

def get_videos_by_date_range_and_others(start_date, end_date,region_remark):
    with app.app_context():
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        return Video.query.filter(Video.v_time.between(start_datetime, end_datetime),
                                  or_(Video.v_region == region_remark, Video.description == region_remark)).all()

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

















