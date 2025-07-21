from flask import Blueprint, jsonify, current_app
import boto3
import base64

images_bp = Blueprint('images', __name__)

@images_bp.route('/api/images/proxy/<path:image_path>')
def proxy_image(image_path):
    """Proxy S3 images through the backend when direct access is blocked"""
    if not current_app.config['USE_S3']:
        return jsonify({'error': 'S3 not enabled'}), 400
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
    )
    
    try:
        # Get object from S3
        response = s3_client.get_object(
            Bucket=current_app.config['S3_BUCKET_NAME'],
            Key=f'diary-images/{image_path}'
        )
        
        # Read the image data
        image_data = response['Body'].read()
        content_type = response.get('ContentType', 'image/jpeg')
        
        # Return the image
        from flask import Response
        return Response(image_data, mimetype=content_type)
        
    except Exception as e:
        current_app.logger.error(f"Failed to proxy image: {e}")
        return jsonify({'error': 'Failed to load image'}), 404