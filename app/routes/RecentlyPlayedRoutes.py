from flask import Blueprint, request, jsonify
from app.models import db, RecentlyPlayed

recently_played_bp = Blueprint('recently_played', __name__, url_prefix='/recently_played')

# 定义一个处理GET请求的路由，用于获取最近播放的歌曲列表
@recently_played_bp.route('/getSong', methods=['GET'])
def get_recently_played():
    """
    获取最近播放的歌曲信息.

    该函数查询数据库中最近播放的歌曲，按更新时间降序排列并限制最多20条记录。
    然后将查询结果转换为JSON格式返回，符合RESTful API的标准。

    :return: 包含最近播放的歌曲列表的JSON响应，格式如下：
             {
                 "songs": [
                     {
                         "id": <song_id>,
                         "title": "<song_title>",
                         "artist": "<song_artist>",
                         "update_time": "<update_time>"
                     },
                     ...
                 ]
             }
    """
    # 查询数据库中最近播放的歌曲，按更新时间降序排列并限制最多20条记录
    recently_played_songs = RecentlyPlayed.query.order_by(RecentlyPlayed.update_time.desc()).limit(20).all()
    
    # 将查询结果转换为JSON格式并返回
    return jsonify({"data": [song.to_dict() for song in recently_played_songs], "code": 200, "msg": "success" })

# 定义一个处理歌曲播放记录的路由，支持POST方法
@recently_played_bp.route('/addSong', methods=['POST'])
def add_or_update_recently_played():
    """
    添加或更新最近播放列表中的歌曲。
    
    该函数首先尝试从请求中解析JSON格式的歌曲信息。
    如果解析失败或歌曲信息中不包含必要的'id'字段，则返回错误信息和400状态码。
    
    接着，函数会检查数据库中是否存在具有相同ID的歌曲记录。
    如果存在，则更新该记录的时间戳为当前时间。
    如果不存在，则创建一条新的最近播放记录，并添加到数据库中。
    
    最后，提交数据库会话，并返回成功消息和200状态码。
    """
    # 尝试从请求中获取JSON格式的歌曲信息
    song_item = request.get_json()
    # 验证歌曲信息是否存在且包含必要的'id'字段
    if not song_item or 'id' not in song_item:
        return jsonify({'message': 'Invalid SongItem data'}), 400

    # 查询数据库中是否存在具有相同歌曲ID的记录
    existing_song = RecentlyPlayed.query.filter_by(song_id=song_item['id']).first()

    # 根据查询结果决定是更新现有记录还是添加新记录
    if existing_song:
        # 如果记录已存在，则更新时间戳为当前时间
        existing_song.update_time = db.func.now()
    else:
        # 如果记录不存在，则创建新的最近播放实例并添加到数据库会话
        new_song = RecentlyPlayed(song_item)
        db.session.add(new_song)

    # 提交数据库会话以保存更改
    db.session.commit()
    # 返回成功消息和200状态码
    return jsonify({"data": None, 'msg': 'Recently played updated successfully', "code": 200 })