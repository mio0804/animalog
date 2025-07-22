#!/usr/bin/env python
"""
Update ACL for existing S3 objects to make them publicly readable
"""
import boto3
from config import Config

def update_s3_acl():
    config = Config()
    
    if not config.USE_S3:
        print("USE_S3 is not enabled. Please set USE_S3=true in .env file")
        return
    
    # S3クライアントを初期化
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )
    
    # diary-imagesプレフィックス内のすべてのオブジェクトをリスト
    try:
        response = s3_client.list_objects_v2(
            Bucket=config.S3_BUCKET_NAME,
            Prefix='diary-images/'
        )
        
        if 'Contents' not in response:
            print("No images found in S3")
            return
        
        objects = response['Contents']
        print(f"Found {len(objects)} objects to update")
        
        # 各オブジェクトのACLを更新
        for obj in objects:
            key = obj['Key']
            try:
                s3_client.put_object_acl(
                    Bucket=config.S3_BUCKET_NAME,
                    Key=key,
                    ACL='public-read'
                )
                print(f"✓ Updated ACL for {key}")
            except Exception as e:
                print(f"✗ Failed to update ACL for {key}: {e}")
        
        print("\nACL update complete!")
        
    except Exception as e:
        print(f"Error listing objects: {e}")

if __name__ == '__main__':
    update_s3_acl()