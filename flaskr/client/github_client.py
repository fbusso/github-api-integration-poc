import urllib.parse
from typing import List, Dict, Tuple

import requests

from flaskr.dto import GitHubRepository, GitHubPullRequest
from flaskr.models.user import User
from flaskr.utils import CryptographyUtils


class GitHubClient:
    _access_token: str
    _cryptography_utils: CryptographyUtils
    _client_id: str
    _client_secret: str

    def __init__(self, cryptography_utils: CryptographyUtils, client_id: str, client_secret: str):
        self._cryptography_utils = cryptography_utils
        self._client_id = client_id
        self._client_secret = client_secret

    def get_authorization_url(self, authorization_request_id: str, scope: List[str]) -> str:
        state = self._cryptography_utils.encrypt(authorization_request_id)

        url = (f'https://github.com/login/oauth/authorize?'
               f'client_id={self._client_id}&'
               f'scope={",".join(scope)}&'
               f'state={state}'
               )

        return url

    def get_access_token(self, code: str) -> Tuple[str, str]:
        url = 'https://github.com/login/oauth/access_token'
        request_body = {
            'code': code,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }

        result = requests.post(url, data=request_body)
        content = result.content.decode("utf-8")
        dict_with_lists: Dict[str, List[str]] = urllib.parse.parse_qs(content)
        result_dict: Dict[str, str] = {key: value[0] for key, value in dict_with_lists.items()}
        access_token = result_dict.get('access_token', None)
        error = result_dict.get('error', None)
        return access_token, error

    def get_repositories(self, user: User) -> List[GitHubRepository]:
        headers = self._get_request_headers(user)

        result = requests.get(f"https://api.github.com/user/repos", headers=headers)
        return [GitHubRepository(**repository) for repository in result.json()]

    def get_pull_requests(self, user: User, url: str) -> List[GitHubPullRequest]:
        headers = self._get_request_headers(user)

        result = requests.get(url, headers=headers)
        return [GitHubPullRequest(**repository) for repository in result.json()]

    def get_patch(self, user: User, url: str) -> str:
        decrypted_access_token = self._cryptography_utils.decrypt(user.access_token)
        headers = {
            'Accept': 'application/vnd.github.v3.diff',
            'Authorization': f'token {decrypted_access_token}'
        }

        formatted_url = url.replace("github.com", "api.github.com/repos").replace("/pull/", "/pulls/")
        response = requests.get(formatted_url, headers=headers)
        return response.text

    def _get_request_headers(self, user: User):
        decrypted_access_token = self._cryptography_utils.decrypt(user.access_token)
        headers = {
            'Authorization': f'Bearer {decrypted_access_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        return headers
