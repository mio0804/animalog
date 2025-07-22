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
    
    # S3 URLかどうかをチェック
    bucket_name = current_app.config['S3_BUCKET_NAME']
    s3_prefix = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/"
    
    if not image_url.startswith(s3_prefix):
        return image_url
    
    # URLからキーを抽出
    key = image_url.replace(s3_prefix, '')
    
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