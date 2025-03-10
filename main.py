from __future__ import annotations
from typing import Optional


class User:
    """
    Representation invariants:
    - name != ""
    - romantic_degree >= 0
    - social_degree >= 0
    """
    name: str
    romantic_current: Optional[User]
    romantic_ex: list[User]
    social_current: Optional[User]
    social_ex: list[User]
    romantic_degree: int
    social_degree: int

    def __init__(self, name: str, romantic_current: Optional[User] = None, romantic_ex: list[User] = [],
                 social_current: Optional[User] = None, social_ex: list[User] = [], romantic_degree: int = 0,
                 social_degree: int = 0):
        self.name = name
        self.romantic_current = romantic_current
        self.romantic_ex = romantic_ex
        self.social_current = social_current
        self.social_ex = social_ex
        self.romantic_degree = romantic_degree
        self.social_degree = social_degree

# TEST VS CODE