from knox.auth import TokenAuthentication;

class AuthFromCookie(TokenAuthentication):
    def authenticate(self, request):
        knox_token=request.COOKIES.get('token')
        if not knox_token:
            return None
        request.META['HTTP_AUTHORIZATION']=f'Token {knox_token}'
        return super().authenticate(request)