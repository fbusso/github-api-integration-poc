from urllib import request
from urllib.parse import unquote

from flask import Blueprint, render_template, request
from flask.views import MethodView

from flaskr.models import User
from flaskr.routes.base_github_route import BaseGitHubRoute

github_bp = Blueprint('github', __name__, url_prefix='/github')


class Repositories(MethodView, BaseGitHubRoute):
    def get(self):
        user_name = request.args.get('user', default=None, type=str)

        if not user_name:
            return render_template(
                'error.html',
                title='Error',
                error='Parameter `user_name` is required'
            )

        user = User.find_by_name(user_name)
        if not user:
            return render_template(
                'error.html',
                title='Error',
                error=f"User '{user_name}' not found"
            )

        repositories = self._github_client.get_repositories(user)
        return render_template('repositories.html', user_id=user.id, repositories=repositories)


github_bp.add_url_rule('/repositories', view_func=Repositories.as_view('repositories'))


class PullRequests(MethodView, BaseGitHubRoute):
    def get(self):
        encoded_url = request.args.get('url')
        repository_name = request.args.get('repository_name')
        repos_url = unquote(encoded_url).replace("{/number}", "") + "?state=all"
        user_id = request.args.get('user_id')

        user = User.find_by_id(user_id)
        if not user:
            return render_template('error.html', title='Error', error='User not found')

        pull_requests = self._github_client.get_pull_requests(user, repos_url)

        return render_template(
            'pull_requests.html',
            repository_name=repository_name,
            pull_requests=pull_requests,
            user_id=user_id
        )


github_bp.add_url_rule('/pull-requests', view_func=PullRequests.as_view('pull_requests'))


class ViewPullRequest(MethodView, BaseGitHubRoute):
    def get(self):
        args = request.args
        title = args.get('title')
        description = args.get('description')
        encoded_patch_url = args.get('patch_url')
        patch_url = unquote(encoded_patch_url)
        user_id = args.get('user_id')

        user = User.find_by_id(user_id)
        if not user:
            return render_template('error.html', title='Error', error='User not found')

        patch = self._github_client.get_patch(user, patch_url)

        return render_template(
            'view_pull_request.html',
            title=title,
            description=description,
            patch=patch
        )


github_bp.add_url_rule('/view-pull-request', view_func=ViewPullRequest.as_view('view_pull_request'))
