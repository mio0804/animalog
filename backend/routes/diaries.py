from flask import Blueprint, jsonify, request, current_app
from auth import login_required
from models import db, Diary, Pet
from utils.s3 import save_file_locally, generate_presigned_url, delete_file, allowed_file

diaries_bp = Blueprint('diaries', __name__)

@diaries_bp.route('/api/pets/<pet_id>/diaries', methods=['GET'])
@login_required
def get_diaries(pet_id):
    """Get all diaries for a specific pet"""
    # Verify pet ownership
    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=request.current_user.id
    ).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query diaries
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
    # Handle both JSON and multipart/form-data
    if request.is_json:
        data = request.get_json()
        image_file = None
    else:
        data = request.form.to_dict()
        image_file = request.files.get('image')
    
    # Validate required fields
    if not data.get('pet_id') or not data.get('content'):
        return jsonify({'error': 'Pet ID and content are required'}), 400
    
    # Verify pet ownership
    pet = Pet.query.filter_by(
        id=data['pet_id'],
        user_id=request.current_user.id
    ).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Handle image upload if provided
    image_url = None
    if image_file and image_file.filename != '':
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        if current_app.config['USE_S3']:
            # For S3, we would typically use presigned URL flow
            # but for direct upload, save temporarily and upload
            pass
        else:
            image_url = save_file_locally(image_file)
    elif data.get('image_url'):
        # Image was already uploaded via presigned URL
        image_url = data['image_url']
    
    # Create diary entry
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
    
    # Update fields if provided
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
    
    # Delete associated image if exists
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