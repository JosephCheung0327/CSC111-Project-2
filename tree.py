from __future__ import annotations

import user_network

from typing import List, Optional, Any
import pandas as pd
import csv
import json
from python_ta.contracts import check_contracts



users_list = user_network.users

char1 = users_list[-2].characteristics

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

class BinaryTree:
    _root:Optional[Any]
    _left:list[BinaryTree]
    _right:list[BinaryTree]

    def __init__(self, root:Optional[Any]=None)-> None:
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinaryTree(None)
            self._right = BinaryTree(None)

    def insert_sequence(self, items:list) -> None:
        """
        >>> t = BinaryTree("")
        >>> t.insert_sequence([1, 1, 1, 1])  # Leftmost branch
        >>> t.insert_sequence([0, 1, 1, 1])  # Right → Left → Left → Left
        >>> t.insert_sequence([1, 0, 1, 1])  # Left → Right → Left → Left
        >>> t.insert_sequence([1, 1, 1, 0])  # Left → Left → Left → Right
        >>> t.insert_sequence([0, 0, 0, 1])  # Rightmost branch with final left
    
        # Verify the complete tree structure
        >>> t == BinaryTree("",
        ...     BinaryTree(1,
        ...         BinaryTree(1,
        ...             BinaryTree(1,
        ...                 BinaryTree(1),
        ...                 BinaryTree(0)
        ...             ),
        ...             BinaryTree(0,
        ...                 BinaryTree(1,
        ...                     BinaryTree(1),
        ...                     None
        ...                 ),
        ...                 None
        ...             )
        ...         ),
        ...         None
        ...     ),
        ...     BinaryTree(0,
        ...         BinaryTree(1,
        ...             BinaryTree(1,
        ...                 BinaryTree(1),
        ...                 None
        ...             ),
        ...             None
        ...         ),
        ...         BinaryTree(0,
        ...             None,
        ...             BinaryTree(0,
        ...                 BinaryTree(1),
        ...                 None
        ...             )
        ...         )
        ...     )
        ... )
        True
    
        # Test individual nodes
        >>> t.left.left.left.left.value == 1  # [1,1,1,1]
        True
        >>> t.right.left.left.left.value == 1  # [0,1,1,1]
        True
        >>> t.left.right.left.left.value == 1  # [1,0,1,1]
        True
        >>> t.left.left.left.right.value == 0  # [1,1,1,0]
        True
        >>> t.right.right.right.left.value == 1  # [0,0,0,1]
        True
        """
        if not items:
            return

        current = items[0]
        rest = items[1:]

        if current == 1:
            if self._left is None:
                self._left = BinaryTree(current)
            self._left.insert_sequence(rest)
        else:  # current == 0
            if self._right is None:
                self._right = BinaryTree(current)
            self._right.insert_sequence(rest)
                



#     def run_decision_tree(self) -> list[str]:
#         """Run the decision tr"""

# ,visited:setn the desgined algorithm and return a recommendation list of top 10 people matched with the useer.. That is, recurse into the branch with all 1s (leftmost branch), followed by the second leftmost branch with all 1s except the last subdivision that goes to 0. Retur
list[str]

        #corner case:        

        # recommendation_list = []
        # stack = [self]

        # while stack and len(recommendation_list) < 10:
        #     node = stack.pop()

        #     if node._root is None or id(node) in visited:
        #         continue

        #     # If it's a leaf and hasn't been visited
        #     if not node._left and not node._right:
        #         recommendation_list.append(node._root)
        #         visited.add(id(node))
        #     else:
        #         # Push right first so left is processed first
        #         if node._right:
        #             stack.append(node._right[0])
        #         if node._left:
        #             stack.append(node._left[0])

        return recommendation_list


def refresh_tree()  -> None:
    """This function is called """
      if response == "Yes" :  
        run_decision_tree()         
       
# class Tree:
#     _root:Optional[Any]
#     _subtrees:list[Tree]


#     def __init__(self, root:Optional[Any],subtrees:list[Tree])-> None:
#         self._root = root
#         self._subtrees = subtrees

#     def insert_sequence(self, items: list) -> None:
#         """Insert the given items onto this tree."""
#         if not items:
#             return
#         else:
#             first = items[0]
#             rest = items[1:]
#             for subtree in self._subtrees:
#                 if subtree._root == first:
#                     subtree.insert_sequence(rest)
#                     return
#             self._subtrees.append(Tree(first, []))
#             self._subtrees[-1].insert_sequence(rest)

#     def __str__(self, level=0) -> str:
#         """Return a string representation of the tree."""
#         result = "  " * level + str(self._root) + "\n"
#         for subtree in self._subtrees:
#             result += subtree.__str__(level + 1)
#         return result


    # def show_result(self) -> Any:

    # def run_preference_tree(self) -> list[User]:
    #     """Run the preference tree and return a list of 10 users that will display to the target user."""
    
    #     # base  case ()(return the leave of the tree):
    #     if self.is_empty():
    #       return []

    #     else: 
    #       for subtree in

    # def run_preference_tree(self) -> list[str]:
    #     """Run the decision tree and return a list of 10 users that will display to the target user."""
    #     recommendation_list = []
    #     t = build_preference_tree('data.csv')
    #     # result = t.show_result()
    #     for subtree in self._subtrees:

    # def run_preference_tree(self) -> list[str]:
    #     """Run the decision tree and return a list of closest match users ordered by priority.
    #     >>> t = Tree("", Tree())
    #     """
    #     recommendation_list = []

    #     def traverse_tree(tree: Tree, path: list[int]):
    #         """Helper function to traverse the tree and collect recommendations."""
    #         if not tree._subtrees:  # Leaf node (user match)
    #             if tree._root != "":
    #                 recommendation_list.append((path, tree._root))  # (match pattern, user)
    #             return

    #         for i, subtree in enumerate(tree._subtrees):
    #             traverse_tree(subtree, path + [i])

    #     traverse_tree(self, [])

    #     # Custom sorting:
    #     def match_priority(path):
    #         # 1. First, find the position of the first 0 (or len(path) if all are 1)
    #         first_zero = next((i for i, bit in enumerate(path) if bit == 0), len(path))
    #         # 2. Higher priority for leftmost match, then total 1's
    #         return (first_zero, -sum(path))

    #     # Sort by the best match (leftmost 1s first, then total 1s)
    #     recommendation_list.sort(key=lambda x: match_priority(x[0]))

    #     return [item[1] for item in recommendation_list[:10]]  # Return top 10 users

        


    



        # if self._root != "" and isinstance(self._root, str):
        #     recommendation_list.append(self._root)
        #     return recommendation_list
        # elif self._root == "" or self._root == 1:
        #     for subtree in self._subtrees:
        #         # recommendation_list.append(subtree._root)
        #         recommendation_list.append(subtree.run_preference_tree())
    
        # # if recommendation_list < 10:

        # # else:
        # #     for subtree in self._subtrees:
        # #         # recommendation_list.append(subtree._root)
        # #         subtree.run_preference_tree


        # # print(recommendation_list)

        # # if len(recommendation_list) < 10:




# @check_contracts
# def get_input() -> list[int]:
#     answer_so_far = []
#     for i in range(len(vars(Characteristics))):
#         answer_so_far.append(1)

# @check_contracts
# def change_input(answer:list[int]) -> list[int]:
#     for i in range(len(answer)-1, -1, -1):
#         if answer[i] == 1:
#             answer_so_far[i] = 0
#             return answer_so_far

    
    


# @check_contracts
# def build_preference_tree(file:str) -> Tree:
#     tree = BinaryTree("")

#     with open(file) as csv_file:
#         reader = csv.reader(csv_file)
#         next(reader) #skip the header row

#         for row in reader: 
#             characteristics = str(row[0])
#             match = [int(item) for item in row[1:]]
#             match.append(characteristics)
#             tree.insert_sequence(match)
#     print(tree)
#     return tree




if __name__ == "__main__":
    t = BinaryTree("")
    match1 = [1, 1, 1, 1]
    match2 = [0, 1, 1, 1]
    match3 = [1, 0, 1, 1]
    match4 = [1, 1, 1, 0]
    match5 = [0, 0, 0, 1]
    t.insert_sequence(match1)
    t.insert_sequence(match2)
    t.insert_sequence(match3)
    t.insert_sequence(match4)
    t.insert_sequence(match5)
    expected = BinaryTree("", BinaryTree(1, BinaryTree(1, BinaryTree(1, BinaryTree(1), BinaryTree(0)), None), BinaryTree(0, \
    BinaryTree(1, BinaryTree(1), None), None)), BinaryTree(0, BinaryTree(1, BinaryTree(1, BinaryTree(1), None), None), \
    BinaryTree(0, None, BinaryTree(0, BinaryTree(1), None))))
    print(t == expected)

    
    # data_wrangling()
    
    # t = build_preference_tree('data.csv')
    # recommendation_list = t.run_preference_tree()
    # print(recommendation_list)
    # print('Tree


  