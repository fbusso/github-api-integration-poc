from flask import Blueprint, render_template, request, redirect
from flask.views import MethodView

from flaskr.models import User, AuthorizationRequest
from flaskr.routes.base_github_route import BaseGitHubRoute

link_with_github_bp = Blueprint('link_with_github', __name__, url_prefix='/link-with-github')


class LinkWithGithub(MethodView):
    @staticmethod
    def get():
        return render_template('link_with_github.html')


link_with_github_bp.add_url_rule('/', view_func=LinkWithGithub.as_view('link_with_github'))


class Start(MethodView, BaseGitHubRoute):
    def post(self):
        username = request.form.get('username', None)
        if not username:
            return render_template('link_with_github.html')

        user = User.find_by_name(username)
        if not user:
            user = User(user_name=username)
            user.save()

        authorization_request = AuthorizationRequest(user)
        authorization_request.save()

        scope = ['repo', 'read:org']

        authorization_url = self._github_client.get_authorization_url(str(authorization_request.id), scope)

        return redirect(authorization_url)


link_with_github_bp.add_url_rule('/start', view_func=Start.as_view('start'))
