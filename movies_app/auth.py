import jwt
from datetime import datetime, timedelta


def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
