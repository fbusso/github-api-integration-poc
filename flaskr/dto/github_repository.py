from dataclasses import dataclass

from flaskr.dto.base_dataclass import BaseDataclass


@dataclass
class GitHubRepository(BaseDataclass):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    url: str
    pulls_url: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
