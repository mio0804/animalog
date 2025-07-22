"""
S3 URL utilities for generating presigned URLs for image access
"""
import boto3
from flask import current_app
from datetime import datetime, timedelta

def get_presigned_url(image_url):
    """Generate a presigned URL for S3 object access"""
    if not image_url or not current_app.config['USE_S3']:
        return image_url
    
    bucket_name = current_app.config['S3_BUCKET_NAME']
    s3_prefix = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/"
    
    # ローカルパスの場合はS3キーに変換
    if image_url.startswith('/uploads/'):
        filename = image_url.replace('/uploads/', '')
        key = f"diary-images/{filename}"
    elif image_url.startswith(s3_prefix):
        # S3 URLの場合はキーを抽出
        key = image_url.replace(s3_prefix, '')
    else:
        # その他の形式はそのまま返す
        return image_url
    
    # プリサインドURLを生成
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
    )
    
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key
            },
            ExpiresIn=3600  # 1 hour
        )
        return presigned_url
    except Exception as e:
        current_app.logger.error(f"Failed to generate presigned URL: {e}")
        return image_url