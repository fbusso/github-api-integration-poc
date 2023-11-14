from dataclasses import dataclass

from flaskr.dto.base_dataclass import BaseDataclass


@dataclass
class GitHubPullRequest(BaseDataclass):
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    number: int
    state: str
    locked: bool
    title: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
