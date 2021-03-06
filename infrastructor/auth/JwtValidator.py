import calendar
from infrastructor.utils.Utils import Utils
import json
from datetime import datetime

from jwkest.jwk import KEYS
from jwkest.jws import JWS
from requests import request
import base64

from infrastructor.logging.ConsoleLogger import ConsoleLogger


class JwtValidatorException(Exception):
    pass


class JwtValidator:
    def __init__(self, jwks_url, issuer, audience, verify_ssl_server=True):
        self.supported_algorithms = ['RS256', "RS512"]
        self.jwks_url = jwks_url
        self.aud = audience
        self.iss = issuer
        self.verify_ssl_server = verify_ssl_server
        self.jwks = self.load_keys()
        self.logger = ConsoleLogger()

    def base64_urldecode(self, string):
        string.replace('-', '+')
        string.replace('_', '/')
        string += '=' * (4 - (len(string) % 4))
        return base64.b64decode(string)

    def validate(self, jwt):
        parts = jwt.split('.')
        if len(parts) != 3:
            self.logger.debug('Invalid JWT. Only JWS supported.')
            return {"active": False}
        # noinspection PyBroadException
        try:
            header = json.loads(self.base64_urldecode(parts[0]))
            payload = json.loads(self.base64_urldecode(parts[1]))
        except Exception:
            self.logger.debug("Invalid JWT, format not json")
            return {"active": False}

        if self.iss != payload['iss']:
            self.logger.debug("Invalid issuer %s, expected %s" % (payload['iss'], self.iss))
            return {"active": False}

        if 'aud' not in payload:
            self.logger.debug("Invalid audience, no audience in payload")
            return {"active": False}

        aud = payload['aud']

        if self.aud not in aud:
            self.logger.debug("Invalid audience %s, expected %s" % (aud, self.aud))
            return {"active": False}

        if 'alg' not in header:
            self.logger.debug("Missing algorithm in header")
            return {"active": False}

        if header['alg'] not in self.supported_algorithms:
            self.logger.debug("Unsupported algorithm in header %s" % (header['alg']))
            return {"active": False}

        jws = JWS(alg=header['alg'])

        # noinspection PyBroadException
        try:
            jws.verify_compact(jwt, self.jwks)
        except Exception as ex:
            self.logger.debug(f"Exception validating signature. Err:{ex}")
            return {'active': False}

        self.logger.debug("Successfully validated signature.")

        if 'exp' not in payload:
            self.logger.debug("No expiration in body, invalid token")
            return {"active": False}

        if 'sub' not in payload:
            self.logger.debug("No subject in body, invalid token")
            return {"active": False}

        # Could be an empty scope, which may be allowed, so replace with empty string if not found
        if 'scope' not in payload:
            scope = ""
        else:
            scope = payload['scope']

        exp = payload['exp']

        d = datetime.utcnow()
        now = calendar.timegm(d.utctimetuple())

        if now >= exp:
            return {"active": False}
        else:
            payload["active"] = True
            return payload

    def load_keys(self):
        # load the jwk set.
        jwks = KEYS()
        jwks_data=Utils.get_request(self.jwks_url);
        jwks.load_jwks(jwks_data)
        return jwks
