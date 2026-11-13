import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def authenticate_or_create_google_user(code):
    token_res = requests.post("https://oauth2.googleapis.com/token", data={
        'code': code, 
        'client_id': getattr(settings, 'GOOGLE_CLIENT_ID', ''),
        'client_secret': getattr(settings, 'GOOGLE_CLIENT_SECRET', ''), 
        'redirect_uri': 'postmessage', 
        'grant_type': 'authorization_code'
    }).json()
    
    if 'access_token' not in token_res:
        raise ValueError(f"Ошибка получения токена Google: {token_res}")

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo", 
        headers={'Authorization': f"Bearer {token_res.get('access_token')}"}
    ).json()
    
    email = user_info.get('email')
    if not email:
        raise ValueError("Google аккаунт не содержит email.")
    
    user, created = User.objects.get_or_create(email=email, defaults={'role': 'student'})
    refresh = RefreshToken.for_user(user)
    
    return {
        "access": str(refresh.access_token), 
        "refresh": str(refresh),
        "is_new_user": created, 
        "user": {
            "id": user.id, 
            "email": user.email, 
            "role": user.role
        }
    }