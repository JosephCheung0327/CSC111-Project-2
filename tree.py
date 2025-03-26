from __future__ import annotations

import user_network

from typing import List, Optional, Any
import pandas as pd
import csv
import json
from python_ta.contracts import check_contracts



users_list = user_network.users

char1 = users_list[-1].characteristics

# char1 = user_network.Characteristics(
#     ethnicity="Asian",
#     interests=["coding", "data science", "movies"],
#     mbti="INTJ",
#     communication_type="Direct",
#     political_interests="Moderate",
#     religion="None",
#     major="Computer Science",
#     year="3rd",
#     language="English, Cantonese",
#     likes_pets=True,
#     likes_outdoor_activities=True,
#     enjoys_watching_movies=True
# )





def filter_user_by_dating_goal (users:List[user_network.User],user:user_network.User)-> list[user_network.User]:
    """Filters users who have the same dating goal as the given user, excluding themselves"""

    return [u for u in users if u.dating_goal == user.dating_goal and u!= user]
        


def add_priority(Characteristics: user_network.Characteristics) -> List[str]:
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


class Tree:
    _root:Optional[Any]
    _subtrees:list[Tree]


    def __init__(self, root:Optional[Any],subtrees:list[Tree])-> None:
        self._root = root
        self._subtrees = subtrees

    def insert_sequence(self, items: list) -> None:
        """Insert the given items onto this tree."""
        if not items:
            return
        else:
            first = items[0]
            rest = items[1:]
            for subtree in self._subtrees:
                if subtree._root == first:
                    subtree.insert_sequence(rest)
                    return
            self._subtrees.append(Tree(first, []))
            self._subtrees[-1].insert_sequence(rest)

    def __str__(self, level=0) -> str:
        """Return a string representation of the tree."""
        result = "  " * level + str(self._root) + "\n"
        for subtree in self._subtrees:
            result += subtree.__str__(level + 1)
        return result


    # def show_result(self) -> Any:
        



    # def run_preference_tree(self) -> list[User]:
    #     """Run the preference tree and return a list of 10 users that will display to the target user."""
        
    #     # base  case ()(return the leave of the tree):
    #     if self.is_empty():
    #       return []

    #     else: 
    #       for subtree in

        
        
        
  

@check_contracts
def build_preference_tree(file:str) -> Tree:
    tree = Tree('', [])

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader) #skip the header row

        for row in reader: 
                characteristics = str(row[0])
                match = [int(item) for item in row[1:]]
                match.append(characteristics)
                tree.insert_sequence(match)
    print(tree)
    return tree

@check_contracts
def run_preference_tree(self, user: user_network.User) -> list[user_network.User]:
        """Run the decision tree and return a list of 10 users that will display to the target user."""
        recommendation_list = []
        t = build_preference_tree('data.csv')
        result = t.show_result()
        
        if self._root != "" and isinstance(self._root, str):
            recommendation_list.append(self._root)
        elif self._root == "":
            for subtree in self._subtrees:
                if subtree._root == 1:
                    




if __name__ == "__main__":
    data_wrangling()
    # build_preference_tree('data.csv')
    # print('Tree


  