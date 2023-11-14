from typing import Dict

from flask import Blueprint, request, render_template
from flask.views import MethodView

from flaskr.models import AuthorizationRequest
from flaskr.routes.base_github_route import BaseGitHubRoute

oauth_bp = Blueprint('oauth', __name__, url_prefix='/oauth')


class Callback(MethodView, BaseGitHubRoute):
    def get(self):
        args: Dict = request.args

        error = args.get('error', None)
        if error:
            return render_template('error.html', title='Account Link error', error=error)

        code = args.get('code', None)
        state = args.get('state', None)

        if not code or not state:
            return render_template('error.html', title='Unknown Error', error='Unknown error')

        access_token, error = self._github_client.get_access_token(code)

        if error:
            return render_template('error.html', title='Account Link Error', error=error)

        decrypted_authorization_request_id = self._cryptography_utils.decrypt(state)
        authorization_request = AuthorizationRequest.find_by_id(decrypted_authorization_request_id)

        if not authorization_request:
            return render_template('error.html', title='Error', error='Authorization request not found')

        encrypted_access_token = self._cryptography_utils.encrypt(access_token)

        user = authorization_request.user
        user.update_access_token(encrypted_access_token=encrypted_access_token)
        authorization_request.complete()

        return render_template('github_link_success.html', user=user.user_name)


oauth_bp.add_url_rule('/callback', view_func=Callback.as_view('callback'))
