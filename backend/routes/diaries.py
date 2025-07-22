from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from auth import login_required
from models import db, Diary, Pet
from utils.s3 import save_file_locally, generate_presigned_url, delete_file, allowed_file

diaries_bp = Blueprint('diaries', __name__)

@diaries_bp.route('/api/pets/<pet_id>/diaries', methods=['GET'])
@login_required
def get_diaries(pet_id):
    """特定のペットのすべての日記を取得"""
    # ペットの所有権を検証
    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=request.current_user.id
    ).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # ページネーションパラメータを取得
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 日記をクエリ
    diaries_query = Diary.query.filter_by(pet_id=pet_id).order_by(Diary.created_at.desc())
    pagination = diaries_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'diaries': [diary.to_dict() for diary in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@diaries_bp.route('/api/diaries', methods=['GET'])
@login_required
def get_all_diaries():
    """Get all diaries for current user's pets"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    diaries_query = Diary.query.filter_by(
        user_id=request.current_user.id
    ).order_by(Diary.created_at.desc())
    
    pagination = diaries_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'diaries': [diary.to_dict() for diary in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@diaries_bp.route('/api/diaries/<diary_id>', methods=['GET'])
@login_required
def get_diary(diary_id):
    """Get a specific diary entry"""
    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=request.current_user.id
    ).first()
    
    if not diary:
        return jsonify({'error': 'Diary not found'}), 404
    
    return jsonify({'diary': diary.to_dict()})

@diaries_bp.route('/api/diaries', methods=['POST'])
@login_required
def create_diary():
    """Create a new diary entry"""
    # JSONとmultipart/form-dataの両方を処理
    if request.is_json:
        data = request.get_json()
        image_file = None
    else:
        data = request.form.to_dict()
        image_file = request.files.get('image')
    
    # 必須フィールドを検証
    if not data.get('pet_id') or not data.get('content'):
        return jsonify({'error': 'Pet ID and content are required'}), 400
    
    # ペットの所有権を検証
    pet = Pet.query.filter_by(
        id=data['pet_id'],
        user_id=request.current_user.id
    ).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # 画像が提供された場合のアップロード処理
    image_url = None
    if image_file and image_file.filename != '':
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        if current_app.config['USE_S3']:
            # S3の場合、プリサインドURLを生成して直接アップロード
            try:
                import boto3
                from utils.s3 import generate_unique_filename
                
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                    aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                    region_name=current_app.config['AWS_REGION']
                )
                
                # 一意なファイル名を生成
                filename = generate_unique_filename(secure_filename(image_file.filename))
                key = f"diary-images/{filename}"
                
                # パブリック読み取りアクセスでS3にファイルをアップロード
                s3_client.upload_fileobj(
                    image_file,
                    current_app.config['S3_BUCKET_NAME'],
                    key,
                    ExtraArgs={
                        'ContentType': image_file.content_type
                    }
                )
                
                # パブリックURLを生成
                image_url = f"https://{current_app.config['S3_BUCKET_NAME']}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{key}"
                
            except Exception as e:
                current_app.logger.error(f"Failed to upload to S3: {e}")
                return jsonify({'error': 'Failed to upload image'}), 500
        else:
            image_url = save_file_locally(image_file)
    elif data.get('image_url'):
        # 画像はすでにプリサインドURL経由でアップロード済み
        image_url = data['image_url']
    
    # 日記エントリを作成
    diary = Diary(
        pet_id=pet.id,
        user_id=request.current_user.id,
        title=data.get('title'),
        content=data['content'],
        image_url=image_url
    )
    
    db.session.add(diary)
    db.session.commit()
    
    return jsonify({'diary': diary.to_dict()}), 201

@diaries_bp.route('/api/diaries/<diary_id>', methods=['PUT'])
@login_required
def update_diary(diary_id):
    """Update a diary entry"""
    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=request.current_user.id
    ).first()
    
    if not diary:
        return jsonify({'error': 'Diary not found'}), 404
    
    data = request.get_json()
    
    # 提供されたフィールドを更新
    if 'title' in data:
        diary.title = data['title']
    if 'content' in data:
        diary.content = data['content']
    
    db.session.commit()
    
    return jsonify({'diary': diary.to_dict()})

@diaries_bp.route('/api/diaries/<diary_id>', methods=['DELETE'])
@login_required
def delete_diary(diary_id):
    """Delete a diary entry"""
    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=request.current_user.id
    ).first()
    
    if not diary:
        return jsonify({'error': 'Diary not found'}), 404
    
    # 関連する画像がある場合は削除
    if diary.image_url:
        delete_file(diary.image_url)
    
    db.session.delete(diary)
    db.session.commit()
    
    return jsonify({'message': 'Diary deleted successfully'})

@diaries_bp.route('/api/upload/presigned-url', methods=['POST'])
@login_required
def get_presigned_url():
    """Get presigned URL for S3 upload"""
    if not current_app.config['USE_S3']:
        return jsonify({'error': 'S3 uploads not configured'}), 400
    
    data = request.get_json()
    filename = data.get('filename')
    file_type = data.get('file_type', 'image/jpeg')
    
    if not filename:
        return jsonify({'error': 'Filename required'}), 400
    
    if not allowed_file(filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    result = generate_presigned_url(filename, file_type)
    if not result:
        return jsonify({'error': 'Failed to generate upload URL'}), 500
    
    return jsonify(result)