#!/usr/bin/env python
"""
Migrate existing local images to S3
This script uploads all existing images from the local uploads folder to S3
"""
import os
import boto3
from config import Config
from glob import glob

def migrate_images_to_s3():
    config = Config()
    
    if not config.USE_S3:
        print("USE_S3 is not enabled. Please set USE_S3=true in .env file")
        return
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )
    
    # Get all image files from uploads folder
    upload_folder = config.UPLOAD_FOLDER
    image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
    image_files = []
    
    for pattern in image_patterns:
        image_files.extend(glob(os.path.join(upload_folder, pattern)))
    
    if not image_files:
        print(f"No images found in {upload_folder}")
        return
    
    print(f"Found {len(image_files)} images to migrate")
    
    # Upload each image to S3
    for image_path in image_files:
        filename = os.path.basename(image_path)
        key = f"diary-images/{filename}"
        
        try:
            # Check if file already exists in S3
            try:
                s3_client.head_object(Bucket=config.S3_BUCKET_NAME, Key=key)
                print(f"✓ {filename} already exists in S3")
                continue
            except:
                pass
            
            # Upload file to S3 with public read access
            with open(image_path, 'rb') as f:
                s3_client.upload_fileobj(
                    f,
                    config.S3_BUCKET_NAME,
                    key,
                    ExtraArgs={
                        'ContentType': f'image/{os.path.splitext(filename)[1][1:]}',
                        'ACL': 'public-read'
                    }
                )
            print(f"✓ Uploaded {filename} to S3")
            
        except Exception as e:
            print(f"✗ Failed to upload {filename}: {e}")
    
    print("\nMigration complete!")
    print("Note: The local files are still in place. You can delete them manually if needed.")

if __name__ == '__main__':
    migrate_images_to_s3()