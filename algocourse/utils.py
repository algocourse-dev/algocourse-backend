from knox.models import AuthToken


class KnoxTokenString:
    def __init__(self, token):
        self.token = token


def create_knox_token(token_model, user, serializer):
    instance, token = AuthToken.objects.create(user=user)
    return KnoxTokenString(token)
