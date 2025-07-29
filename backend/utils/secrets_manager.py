"""
AWS Secrets Manager クライアント
RDSパスワードなどのシークレット情報を取得する
"""
import json
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name='ap-northeast-1'):
    """
    AWS Secrets Managerからシークレットを取得
    
    Args:
        secret_name: シークレット名
        region_name: AWSリージョン
        
    Returns:
        dict: シークレットの内容
        
    Raises:
        Exception: シークレット取得エラー
    """
    # Secrets Managerクライアントを作成
    # 本番環境ではIAMロールを使用（クレデンシャル省略）
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # シークレットが見つからない、アクセス権限がないなどのエラー
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            raise Exception(f"The requested secret {secret_name} was not found")
        elif error_code == 'InvalidRequestException':
            raise Exception(f"The request was invalid due to: {e}")
        elif error_code == 'InvalidParameterException':
            raise Exception(f"The request had invalid params: {e}")
        elif error_code == 'DecryptionFailure':
            raise Exception(f"The requested secret can't be decrypted: {e}")
        elif error_code == 'InternalServiceError':
            raise Exception(f"An internal service error occurred: {e}")
        else:
            raise Exception(f"Unknown error occurred: {e}")

    # シークレットの値を取得
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        # バイナリシークレットの場合（今回は使用しない）
        raise Exception("Binary secrets are not supported")


def get_rds_password(secret_name, region_name='ap-northeast-1'):
    """
    RDSパスワードを取得する簡易メソッド
    
    Args:
        secret_name: シークレット名
        region_name: AWSリージョン
        
    Returns:
        str: パスワード
    """
    try:
        secret = get_secret(secret_name, region_name)
        # RDS自動生成シークレットの場合
        if 'password' in secret:
            return secret['password']
        # カスタムシークレットの場合
        elif 'rds_password' in secret:
            return secret['rds_password']
        else:
            raise Exception("Password field not found in secret")
    except Exception as e:
        raise Exception(f"Failed to retrieve RDS password: {str(e)}")