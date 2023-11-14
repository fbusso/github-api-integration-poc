from abc import ABC

from flask import current_app

from flaskr.client import GitHubClient
from flaskr.utils import CryptographyUtils


class BaseGitHubRoute(ABC):
    _github_client: GitHubClient
    _cryptography_utils: CryptographyUtils

    def __init__(self):
        config = current_app.config
        encryption_key = config.get('ENCRYPTION_KEY')
        client_id = config.get('GITHUB_CLIENT_ID')
        client_secret = config.get('GITHUB_CLIENT_SECRET')

        self._cryptography_utils = CryptographyUtils(encryption_key=encryption_key)
        self._github_client = GitHubClient(
            cryptography_utils=self._cryptography_utils,
            client_id=client_id,
            client_secret=client_secret
        )
