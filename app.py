# 导入Flask 模板
from flask import Flask, render_template, request, redirect, jsonify, url_for
import db_option
from db_option import db,Video,app

import hashlib
import pathlib
from flask import Flask, request
from werkzeug.utils import secure_filename
import os


app.config["UPLOAD_FOLDER"] = "static"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # 登录的路由
# @app.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         id = request.form.get('name')
#         pwd = request.form.get('password')
#         a = User.query.filter_by(id=int(id)).first()
#         if a.password == pwd and int(id) == a.id:
#             return redirect('index')
#     return render_template('login.html')


# 登录成功后返回index
@app.route('/')
def admin():
    return render_template('index.html')


# 处理提交视频文件，返回提交是否成功


# 查询函数，根据日期范围和地点/备注查询视频信息
def query_videos(start_date, end_date, region_remark):
    # 在这里执行查询操作，根据传入的参数查询相关视频信息
    # 这里假设 get_videos_by_date_range是你自定义的查询函数
    if not region_remark:
        videos = db_option.get_videos_by_date_range(start_date, end_date)
    else:
        videos = db_option.get_videos_by_date_range_and_others(start_date, end_date, region_remark)
    return videos

# 定义路由，处理查询请求和渲染查询结果页面
@app.route('/query_results', methods=['GET'])
def query_results():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    region_remark = request.args.get('region_remark')
    print(start_date)
    print(end_date)

    if start_date and end_date:
        # 执行查询操作，并获取查询结果
        videos = query_videos(start_date, end_date, region_remark)
        # 返回查询结果给前端页面
        return render_template('result.html', videos=videos)
    else:
        return jsonify({'success': False, 'message': 'Missing query parameters'})


#
# @app.post('/submit_video')
# def submit_video():
#     files = request.files.getlist("files")
#     if files:
#         for file in files:
#             """接收并保存视频文件"""
#             filename = file.filename
#             # 读取视频内容
#             content = file.read()
#             # 获取视频的 md5 值
#             hex_name = hashlib.md5(content).hexdigest()
#             # 获取文件后缀
#             suffix = pathlib.Path(filename).suffix
#             # 拼接新的名字 hex + 原有后缀
#             new_filename = hex_name + suffix
#             print('new_filename', new_filename)
#             upload_dir = pathlib.Path(app.config["UPLOAD_FOLDER"])
#             # 获取写入地址
#             new_path = upload_dir.joinpath(new_filename)
#             # 写入文件
#             open(new_path, mode="wb").write(content)
#
#             vd = Video()
#             vd.v_path = str(new_path)  # 将路径转换为字符串
#             vd.v_class = request.form.get('class')
#             # 记录时间
#             vd.v_time = request.form.get('date')
#
#             vd.v_region = request.form.get('region')
#             vd.description = request.form.get('remark')
#
#             try:
#                 db.session.add(vd)
#                 db.session.commit()
#             except Exception as e:
#                 print("数据库操作错误:", e)
#                 db.session.rollback()
#                 return {"code": 1, "msg": "上传视频失败，请稍后再试"}
#     return {"code": 0, "msg": "成功"}
@app.post('/submit_video')
def submit_video():
    date = request.form.get('date')
    region = request.form.get('region')
    remark = request.form.get('remark')
    print(date)
    files = request.form.getlist("files")
    print(files)
    if files:
        print(files)
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file_content = file.read()
                file_hash = hashlib.md5(file_content).hexdigest()

                # 保存文件到服务器
                new_filename = file_hash + '_' + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                file.save(file_path)

                # 将文件信息保存到数据库
                vd = Video()
                vd.v_path = file_path  # 文件路径
                vd.v_class = request.form.get('class')
                vd.v_time = date
                vd.v_region = region
                vd.description = remark
                print(vd)
                try:
                    db.session.add(vd)
                    db.session.commit()
                    print("存入数据库")
                except Exception as e:
                    print("数据库操作错误:", e)
                    db.session.rollback()
                    return {"code": 1, "msg": "上传视频失败，请稍后再试"}

        return {"code": 0, "msg": "成功"}
    else:
        return {"code": 1, "msg": "未收到文件"}

if __name__ == '__main__':
    app.run(debug=True)

    # # 添加视频
    # db_option.add_video('D:\Demo\\DetectSystem\\static\\test1.mp4', 'class1', '2024-03-29', '坐标(1,1)', 'A区', 'description111')
    # db_option.add_video('D:\Demo\\DetectSystem\\static\\test2.mp4', 'class2', '2023-09-12', '坐标(10,300)', 'B区', 'description222')
    # # # 删除视频
    # # delete_video(1)
    # # video1 = db_option.get_video_by_id(2)
    # video_all = db_option.get_all_videos()
    # # print(video1)
    # print(video_all)
    #
    # video2 = db_option.get_videos_by_time_range('2021-01-01', '2024-01-01')
    # print(video2)

    # # 修改视频信息
    # db_option.update_video(2, 'new_class', 'new_description', '23:45:01', '/path/to/new_video.mp4')
    # print(video_all)
    #
    # # 添加用户
    # db_option.add_user('user1', 'password1')
    # db_option.add_user('user2', 'password2')
    #
    # # 查询用户
    # user = db_option.get_user_by_id(1)
    # print(user)
    #
    # # 删除用户
    # db_option.delete_user(1)
    #
    # # 修改用户密码
    # db_option.update_user_password(2, 'new_password')
    # user2 = db_option.get_user_by_id(2)
    # print(user2)
