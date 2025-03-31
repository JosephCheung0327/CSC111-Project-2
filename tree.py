"""
The program build a Binary Tree to match users to generate a list of matches based on the users' preference.
"""
from __future__ import annotations

import json
from typing import List, Optional, Any
import python_ta


def filter_user_by_dating_goal(users, user) -> list:
    """Filters users who have the same dating goal as the given user, excluding themselves"""

    return [u for u in users if u.dating_goal == user.dating_goal and u != user]


def add_priority(characteristics) -> List[str]:
    """
    Ask the user to rank the attributes of the Characteristics class in order of importance.
    Returns a list of attributes sorted by the user's ranking.

    """
    priority_dict = {}
    rank = 1
    for attribute in vars(characteristics):
        priority_dict[attribute] = rank
        rank += 1
    print("Please rank the following criteria in order of importance (from most to least important):")

    for key, value in priority_dict.items():
        print(f"({value}) {key.replace('_', ' ').title()}")

    try:
        ranking = input("Enter the numbers in order (e.g., 3 1 4 2 5 6 7 8 10 11 9 12): ").split()
        ranking = [int(x) for x in ranking]

        if set(ranking) != set(priority_dict.values()):
            raise ValueError("Invalid ranking: Ensure all numbers are present and unique.")

        ordered_attributes = [
            k for r in ranking
            for k, v in priority_dict.items()
            if v == r
        ]
        return ordered_attributes

    except ValueError as e:
        print(f"Error: {e}")
        return add_priority(characteristics)


class BinaryTree:
    """
    A binary tree data structure that can be used to represent a preference tree.

    Representation Invariants:
    - (self._root is None) == (self._left is None)
    - (self._root is None) == (self._right is None)

    Private Instance Attributes:
    - _root: The value stored at the root of the tree, or None if the tree is empty.
    - _left: The left subtree, or None if there is no left child.
    - _right: The right subtree, or None if there is no right child.

    """
    _root: Optional[Any]
    _left: Optional[BinaryTree]
    _right: Optional[BinaryTree]

    def __init__(self, root: Optional[Any] = None) -> None:
        """
        Initialize a new binary tree containing only the given root value.
        If root is None, initialize an empty tree.

        >>> t = BinaryTree("A")
        >>> t._root
        'A'
        >>> t._left._root is None
        True
        >>> t._right._root is None
        True
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinaryTree(None)
            self._right = BinaryTree(None)

    def __str__(self) -> str:
        """
        Return a string representation of the binary tree in JSON format.
        >>> tree = BinaryTree([1, [2, None, None], [3, [4, None, None], None]])
        >>> print(tree)
        [
        1,
        [
            2,
            null,
            null
        ],
        [
            3,
            [
            4,
            null,
            null
            ],
            null
        ]
        ]
        """
        return json.dumps(self.to_nested_list(), indent=2)

    def insert_sequence(self, items: list) -> None:
        """
        A helper function for build_preference_tree.

        Insert a sequence of items into the binary tree.
        The first attribute is ranked at depth 1, the second at depth 2, and so on.

        A value of `1` (a match) goes to the left child.
        A value of `0` (a non-match) goes to the right child.

        >>> t = BinaryTree("")
        >>> t.insert_sequence([1, 1, "Charlie"])
        >>> t.insert_sequence([0, 1, "Bob"])
        >>> t.insert_sequence([1, 0, "Alice"])
        >>> t.insert_sequence([1, 1, "Mary"])
        >>> t.to_nested_list()
        ['', [1, [1, [['Charlie', 'Mary'], None, None], None], [0, [['Alice'], None, None], None]], [0, [1, [['Bob'], \
        None, None], None], None]]
        """
        if not items:
            return

        first, rest = items[0], items[1:]
        if isinstance(first, str):
            if self._left._root is None:
                self._left._root = [first]
                self._left._left = BinaryTree()
                self._left._right = BinaryTree()
            else:
                self._left._root.append(first)
        if first == 1:
            if self._left is None:
                self._left = BinaryTree()
            if self._left._root is None:
                self._left._root = 1
                self._left._left = BinaryTree()
                self._left._right = BinaryTree()
            self._left.insert_sequence(rest)
        elif first == 0:  # first == 0
            if self._right is None:
                self._right = BinaryTree()
            if self._right._root is None:
                self._right._root = 0
                self._right._left = BinaryTree()
                self._right._right = BinaryTree()
            self._right.insert_sequence(rest)

    def to_nested_list(self) -> Optional[list]:
        """
        Returns a nested list representation of the binary tree, \
        and has a format of [root, left_subtree, right_subtree].

        None is returned if the node is empty

        >>> t = BinaryTree("")
        >>> t.insert_sequence([1, 1, "Charlie"])
        ['', [1, [1, ['Charlie'], None], None], None]
        """

        if self._root is None:
            return None
        return [self._root,
                self._left.to_nested_list() if self._left else None,
                self._right.to_nested_list() if self._right else None]

    def run_preference_tree(self) -> list[str]:
        """
        Return a list of ranked recommended users by traversing the binary tree in the preferencce-based manner.

        >>> t = BinaryTree("")
        >>> t.insert_sequence([1, 1, "Charlie"])
        >>> t.insert_sequence([0, 1, "Bob"])
        >>> t.insert_sequence([1, 0, "Alice"])
        >>> t.insert_sequence([1, 1, "Mary"])
        >>> t.insert_sequence([0, 0, "Justin"])
        >>> t.run_preference_tree()
        ['Charlie', 'Mary', 'Alice', 'Bob', 'Justin']
        """
        recommendation_list = []

        # If it's a leaf node, append the root value.
        if isinstance(self._root, list):
            recommendation_list.extend(self._root)

        # Otherwise, include the current node and combine with children.
        else:
            if self._left:
                recommendation_list.extend(self._left.run_preference_tree())
            if self._right:
                recommendation_list.extend(self._right.run_preference_tree())

        return recommendation_list


if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True)
    # doctest.testmod()
    #
    # data_wrangling()
    #
    # print("\nBuilding preference tree...")
    # t = build_preference_tree('data.csv')
    #
    # print("\nFinding recommendations...")
    # result = t.run_preference_tree()
    # print(generate_10_people_list(t,result))

    python_ta.check_all(config={
        'extra-imports': ["json"],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        "forbidden-io-functions": [],
        'disable': ['E9970']
    })
