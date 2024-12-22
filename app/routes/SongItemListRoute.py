from flask import Blueprint, request, jsonify
from app.models.db import db
from app.models.RecentlyPlayed import RecentlyPlayed
from app.models.SongItem import SongItem
from datetime import datetime

song_list_bp = Blueprint('son_list', __name__, url_prefix='/song_list')

@song_list_bp.route('/getSong', methods=['GET'])
def get_favourite_song():
    """
    获取指定list_id歌单中的歌曲信息.

    该函数查询song_item表中list_id=list_id歌曲，按更新时间降序排列并限制最多20条记录。
    只返回未被删除的歌曲（is_deleted=False）。
    然后将查询结果转换为JSON格式返回，符合RESTful API的标准。
    """
    song_id = request.args.get('id')
    if song_id is not None:
        song_id = int(song_id)
        song = SongItem.query.filter_by(song_id=song_id).first()
        return jsonify({"data": song.to_dict(), "code": 200, "msg": "success"})
    
    # 从请求参数中获取list_id
    list_id = request.args.get('list_id')

    if not list_id:
        return jsonify({"code": 400, 'message': 'Invalid list_id'}), 400
    
    if list_id == 'all':
        songs = SongItem.query.filter_by(is_deleted=False).order_by(SongItem.update_time.desc()).limit(20).all()
        return jsonify({"data": [song.to_dict() for song in songs], "code": 200, "msg": "success"})
    
    # 查询数据库中list_id=list_id的歌曲，按更新时间降序排列并限制最多20条记录，只返回未被删除的歌曲
    songs = SongItem.query.filter_by(list_id=list_id, is_deleted=False).order_by(SongItem.update_time.desc()).limit(20).all()
    
    # 将查询结果转换为JSON格式并返回
    return jsonify({"data": [song.to_dict() for song in songs], "code": 200, "msg": "success"})

@song_list_bp.route('/addSong', methods=['POST'])
def add_or_update_recently_played():
    """
    添加或更新SongItem。
    
    该函数首先尝试从请求中解析JSON格式的歌曲信息。
    如果解析失败或歌曲信息中不包含必要的'id'字段，则返回错误信息和400状态码。
    
    首先检查是否有song_id=song_id且list_id=list_id的歌曲记录，如果存在则更新时间戳为当前时间。
    如果不存在，或者只有song_id=song_id而list_id != list_id，则创建一个新的SongItem对象，并添加到数据库中。

    同时，添加is_deleted的判断机制，当添加SongItem时，如果存在is_deleted=True，则更新is_deleted为False，并更新时间戳为当前时间。
    
    最后，提交数据库会话，并返回成功消息和200状态码。
    """
    # 尝试从请求中获取JSON格式的歌曲信息
    song_item_data = request.get_json()
    # 验证歌曲信息是否存在且包含必要的'id'字段
    if not song_item_data or 'id' not in song_item_data or 'list_id' not in song_item_data:
        return jsonify({'message': 'Invalid SongItem data'}), 400

    song_id = song_item_data['id']
    list_id = song_item_data['list_id']

    # 查询数据库中是否存在具有相同song_id且list_id=list_id的记录
    existing_song = SongItem.query.filter_by(song_id=song_id, list_id=list_id, is_deleted=False).first()
    
    if existing_song:
        # 如果记录已存在且未被删除，则更新时间戳为当前时间
        existing_song.update_time = datetime.utcnow()
    else:
        # 查询数据库中是否存在具有相同song_id但is_deleted=True的记录
        deleted_song = SongItem.query.filter_by(song_id=song_id, list_id=list_id, is_deleted=True).first()
        if deleted_song:
            # 如果记录已存在但被删除，则更新is_deleted为False并更新时间戳
            deleted_song.is_deleted = False
            deleted_song.update_time = datetime.utcnow()
        else:
            # 如果记录不存在，则创建新的SongItem实例并添加到数据库会话
            new_song = SongItem(song_item_data)
            db.session.add(new_song)

    # 提交数据库会话以保存更改
    db.session.commit()
    # 返回成功消息和200状态码
    return jsonify({"data": None, 'msg': 'SongItem updated successfully', "code": 200})

# 定义一个处理歌曲删除记录的路由，支持GET方法
@song_list_bp.route('/deleteSong', methods=['GET'])
def delete_recently_played():
    """
    删除最近播放列表中的歌曲。
    
    该函数首先尝试从路径参数中获取歌曲的ID。
    如果ID不存在，则返回错误信息和400状态码。
    
    接着，函数会检查数据库中是否存在具有相同ID的歌曲记录。
    如果存在，则将该记录的is_deleted属性设置为True。
    如果不存在，则返回错误信息和404状态码。
    
    最后，提交数据库会话，并返回成功消息和200状态码。
    """
    data = request.args
    song_id = data.get('id')
    list_id = data.get('list_id')
    if not song_id or not list_id:
        return jsonify({"code": 400, 'message': 'Invalid SongId or ListId'})
    song_id = int(song_id)
    list_id = int(list_id)
    # 查询数据库中是否存在具有相同歌曲ID的记录
    existing_song = SongItem.query.filter_by(song_id=song_id, list_id=list_id, is_deleted=False).first()
    # 根据查询结果决定是否更新记录
    if existing_song:
        # 如果记录已存在，则将is_deleted属性设置为True
        existing_song.is_deleted = True
        # 提交数据库会话以保存更改
        db.session.commit()
        # 返回成功消息和200状态码
        return jsonify({"data": None, 'msg': 'Song deleted successfully', "code": 200})
    else:
        # 如果记录不存在，则返回错误信息和404状态码
        return jsonify({"code": 404, 'message': 'Song not found'})
