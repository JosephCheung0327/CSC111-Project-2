from __future__ import annotations

import user_network

from typing import List, Optional, Any
import pandas as pd
import csv
import json
from python_ta.contracts import check_contracts



users_list = user_network.users

char1 = users_list[-1].characteristics


def filter_user_by_dating_goal (users:List[user_network.User],user:user_network.User)-> list[user_network.User]:
    """Filters users who have the same dating goal as the given user, excluding themselves"""

    return [u for u in users if u.dating_goal == user.dating_goal and u!= user]
        

def add_priority(Characteristics: user_network.Characteristics) -> List[str]:
    """
    Ask the user to rank the attributes of the Characteristics class in order of importance. 
    Returns a list of attributes sorted by the user's ranking.

    """
    priority_dict = {}
    rank = 1
    for attribute in vars(Characteristics):
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
            key for rank in ranking
            for key, value in priority_dict.items()
            if value == rank
        ]

        return ordered_attributes

    except ValueError as e:
        print(f"Error: {e}")
        return add_priority(Characteristics)
        
def data_wrangling():
    """
    Creates a CSV file containing user data, including their characteristics and potential matches.

    The CSV file structure:
    - The first row contains characteristics ordered according to users' ranking.
    - The first column contains user names.
    - Each row represents a potential match, with a ranking value of 0 or 1.
      - A value of 1 indicates a match in characteristics with the current user.
      - A value of 0 indicates no match.
    """
    heading = add_priority(char1)

    potential_users = filter_user_by_dating_goal(users_list, users_list[-1])

    data = {"name":[]}

    for person in potential_users:
        data["name"].append(person.name)
        
    for attribute in heading:
        answer = []
        for person in potential_users:
            current_user_value = getattr(users_list[-1].characteristics, attribute, None)
            potential_user_value = getattr(person.characteristics, attribute, None)

            if current_user_value == potential_user_value:
                answer.append(1)
            else:
                answer.append(0)
        data[attribute] = answer

    # print(data)
    df = pd.DataFrame(data)
    csv_file_path = 'data.csv'

    df.to_csv(csv_file_path, index = False)

    print(f'CSV file "{csv_file_path}" has been created successfully.')

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
        "A"
        >>> t._left is None
        True
        >>> t._right is None
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
        return json.dumps(self.to_nested_list(), indent=2)

    def insert_sequence(self, items: list) -> None:
        """
        >>> t = BinaryTree("")
        >>> t.insert_sequence([1, 1, "Charlie"])
        >>> t.insert_sequence([0, 1, "Bob"])
        >>> t.insert_sequence([1, 0, "Alice"])
        >>> t.insert_sequence([1, 1, "Mary"])
        >>> t.to_nested_list()
        ['', [1, [1, [['Charlie', 'Mary'], None, None], None], [0, [['Alice'], None, None], None]], [0, [1, [['Bob'], None, None], None], None]]
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
        if self._root is None:
            return None
        return [self._root,
                self._left.to_nested_list() if self._left else None,
                self._right.to_nested_list() if self._right else None]
                


    def run_preference_tree(self) -> list:
        """
        >>> t = BinaryTree("")
        >>> t.insert_sequence([1, 1, "Charlie"])
        >>> t.insert_sequence([0, 1, "Bob"])
        >>> t.insert_sequence([1, 0, "Alice"])
        >>> t.insert_sequence([1, 1, "Mary"])
        >>> t.insert_sequence([0, 0, "Hi"])
        >>> t.run_preference_tree()
        ['Charlie', 'Mary', 'Alice', 'Bob', 'Hi']
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

       

def generate_10_people_list(tree:BinaryTree, full_list:list)->list:
    full_recommendation_list = tree.run_preference_tree
    
    new_list = []
    while len (new_list)<10:
        new_list.append(full_list.pop(0))
    
    return new_list



# @check_contracts
def build_preference_tree(file:str) -> Tree:
    tree = BinaryTree("")

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader) #skip the header row

        for row in reader: 
            name = str(row[0])
            match = [int(item) for item in row[1:]]
            match.append(name)
            tree.insert_sequence(match)
    print(tree)
    return tree



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    data_wrangling()
    
    print("\nBuilding preference tree...")
    t = build_preference_tree('data.csv')
    
    print("\nFinding recommendations...")
    result = t.run_preference_tree()
    print(generate_10_people_list(t,result))

    
    


  

  