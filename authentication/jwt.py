from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthentication(BaseJWTAuthentication):

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        try:
            # Get the raw token from the request
            raw_token = self.get_raw_token(request)

            # Validate the token and retrieve its payload
            validated_token = self.get_validated_token(raw_token)

            # Get the user associated with the token
            user = self.get_user(validated_token)

        except AuthenticationFailed as exc:
            if self.raise_on_error:
                raise
            return None

        return user, validated_token
