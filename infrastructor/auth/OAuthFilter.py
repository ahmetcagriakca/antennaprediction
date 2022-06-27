from infrastructor.utils.Utils import Utils
import json
from functools import wraps
from models.configs.ApiConfig import ApiConfig

from flask import request, abort, make_response
from infrastructor.auth.JwtValidator import JwtValidator


class OAuthFilter:
    def __init__(self, api_config: ApiConfig=None):
        self.protected_endpoints = {}
        self.configured = False
        self.verify_ssl = False
        self.validator = None
        self.scopes = api_config.scopes
        self.authority = api_config.authority
        self.audience = api_config.audience
        self.configure()

    def configure(self):
        """

        :param jwks_url:
        :param issuer:
        :param audience:
        :param scopes:
        :return:
        """
        if self.authority is not None and  self.authority!='':
            auth_json=Utils.get_request(self.authority+'/.well-known/openid-configuration');
            self.auth_info = json.loads(auth_json)
            self.validator = JwtValidator(jwks_url= self.auth_info['jwks_uri'],issuer= self.auth_info['issuer'], audience= self.audience, verify_ssl_server= self.verify_ssl)

    def _add_protected_endpoint(self, func, scopes):
        self.protected_endpoints[func] = scopes

    @staticmethod
    def _extract_access_token(incoming_request=None):
        """
        Extract the token from the Authorization header
        OAuth Access Tokens are placed in the header in the form "Bearer XYZ", so Bearer
        needs to be removed and the whitespaces trimmed.

        The method will abort if no token is present, and return a 401
        :param incoming_request: The incoming flask request
        :return: the stripped token
        """

        authorization_header = incoming_request.headers.get("authorization", type=str)
        query_param_access_token = incoming_request.args.get("access_token", type=str)

        if authorization_header is None and query_param_access_token is None:
            abort(401)

        if authorization_header is not None:
            authorization_header_parts = authorization_header.split()
            authorization_type = authorization_header_parts[0].lower()

            # Extract the token from the Bearer string
            if authorization_type != "bearer":
                abort(401)

            return authorization_header_parts[1] if len(authorization_header_parts) >= 2 else None

        return query_param_access_token

    def _authorize(self, token_claims, endpoint_scopes, endpoint_claims):
        if endpoint_claims is not None:
            for claim in endpoint_claims:
                if claim not in token_claims or \
                        (endpoint_claims[claim] is not None and token_claims[claim] != endpoint_claims[claim]):
                    return False

        scope = token_claims['scope']
        if isinstance(token_claims['scope'], (list, tuple)):
            incoming_scopes = scope
        else:
            incoming_scopes = scope.split()

        if endpoint_scopes is None:
            required_scopes = self.scopes
        else:
            required_scopes = endpoint_scopes

        return all(s in incoming_scopes for s in required_scopes)

    def protect(self, scopes=None, claims=None):
        """
        This is a decorator function that can be used on a flask route:
        @_oauth.protect(["read","write]) or @_oauth.protect()
        :param claims: The claims that are required for the protected endpoint (dict)
        :param scopes: The scopes that are required for the protected endpoint (list or space separated string)
        """

        if scopes is None:
            scopes = []

        if not isinstance(scopes, list):
            scopes = scopes.split()

        if claims is None:
            claims = {}

        if not isinstance(claims, dict):
            claims = {}

        def decorator(f):
            @wraps(f)
            def inner_decorator(*args, **kwargs):
                if self.authority is  None or  self.authority=='':
                    return f(*args, **kwargs)
                if self.filter(scopes=scopes, claims=claims) is None:
                    return f(*args, **kwargs)
                else:
                    abort(500)

            return inner_decorator

        return decorator

    def filter_with_token(self, token, scopes=None, claims=None):

        # noinspection PyBroadException
        try:
            validated_token = self.validator.validate(token)
        except Exception:
            abort(make_response("Server Error", 500))
            return

        if not validated_token['active']:
            abort(make_response("Access Denied", 401))

        # Authorize scope
        authorized = self._authorize(validated_token, endpoint_scopes=scopes, endpoint_claims=claims)
        if not authorized:
            abort(make_response("Forbidden", 403))

        # Set the user info in a context global variable
        request.claims = validated_token

        return None

    def filter(self, scopes=None, claims=None):
        token = self._extract_access_token(request)
        # noinspection PyBroadException
        try:
            validated_token = self.validator.validate(token)
        except Exception:
            abort(make_response("Server Error", 500))
            return

        if not validated_token['active']:
            abort(make_response("Access Denied", 401))

        # Authorize scope
        authorized = self._authorize(validated_token, endpoint_scopes=scopes, endpoint_claims=claims)
        if not authorized:
            abort(make_response("Forbidden", 403))

        # Set the user info in a context global variable
        request.claims = validated_token

        return None

