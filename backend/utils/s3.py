import os
import boto3
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp and UUID"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.{ext}"

def save_file_locally(file):
    """Save file to local filesystem"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    filename = generate_unique_filename(secure_filename(file.filename))
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # アップロードディレクトリが存在することを確認
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    file.save(filepath)
    # ローカルファイルの相対的URLを返す
    return f"/uploads/{filename}"

def generate_presigned_url(filename, file_type):
    """Generate presigned URL for S3 upload"""
    if not current_app.config['USE_S3']:
        return None
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
    )
    
    key = f"diary-images/{generate_unique_filename(filename)}"
    
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': current_app.config['S3_BUCKET_NAME'],
            'Key': key,
            'ContentType': file_type,
            'ACL': 'public-read'
        },
        ExpiresIn=3600  # 1 hour
    )
    
    # プリサインドURLと最終ファイルURLの両方を返す
    file_url = f"https://{current_app.config['S3_BUCKET_NAME']}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{key}"
    
    return {
        'upload_url': presigned_url,
        'file_url': file_url
    }

def delete_file(file_url):
    """Delete file from storage"""
    if not file_url:
        return
    
    if current_app.config['USE_S3']:
        # S3 URLからキーを抽出
        bucket_name = current_app.config['S3_BUCKET_NAME']
        if bucket_name in file_url:
            key = file_url.split(f"{bucket_name}/")[-1]
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                region_name=current_app.config['AWS_REGION']
            )
            
            try:
                s3_client.delete_object(Bucket=bucket_name, Key=key)
            except Exception as e:
                current_app.logger.error(f"Failed to delete S3 object: {e}")
    else:
        # ローカルファイルを削除
        if file_url.startswith('/uploads/'):
            filename = file_url.replace('/uploads/', '')
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    current_app.logger.error(f"Failed to delete local file: {e}")