
import json
import boto3
import os

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

BUCKET_NAME = os.getenv("STATE_BUCKET_NAME", "tg-bot-user-state")

def get_user_state(chat_id: str) -> dict:
    key = f"users/{chat_id}.json"
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        return json.loads(response["Body"].read().decode("utf-8"))
    except s3.exceptions.NoSuchKey:
        return {"quest": "1", "theory_index": 0}
    except Exception as e:
        print(f"Error loading state: {e}")
        return {}

def save_user_state(chat_id: str, state: dict):
    key = f"users/{chat_id}.json"
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(state, ensure_ascii=False).encode("utf-8"),
        )
    except Exception as e:
        print(f"Error saving state: {e}")
