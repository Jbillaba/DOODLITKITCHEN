from rest_framework.views import exception_handler


def invalid_token(exc, ctx):
    response = exception_handler(exc, ctx)

    if response.status_code == 401:
        response.data['status_code'] = response.status_code
        response.delete_cookie("uid")
        response.delete_cookie("token")
    return response



        