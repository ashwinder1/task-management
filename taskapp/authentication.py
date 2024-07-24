from rest_framework import authentication
from rest_framework import exceptions
from .models import User
import jwt

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Split the header, but handle the case where it's not properly formatted
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')

            token = parts[1]
            payload = jwt.decode(token ,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid Token')
        
        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        return(user, None)