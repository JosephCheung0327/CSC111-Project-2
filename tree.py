import main
from main import User, Characteristics
import json

users_list = main.users

char1 = Characteristics(
    ethnicity="Asian",
    interests=["coding", "data science", "movies"],
    mbti="INTJ",
    communication_type="Direct",
    political_interests="Moderate",
    religion="None",
    major="Computer Science",
    year="3rd",
    language="English, Cantonese",
    likes_pets=True,
    likes_outdoor_activities=True,
    enjoys_watching_movies=True
)





def filter_user_by_dating_goal (users:List[User],user:User)-> list[User]:
    """Filters users who have the same dating goal as the given user, excluding themselves"""

    return [u for u in users if u.dating_goal == user.dating_goal and u!= user]
        


def add_priority(Characteristics):
    priority_dict = {}
    rank = 1
    for attribute in vars(Characteristics):
        priority_dict[attribute] = rank
        rank += 1
    print("Please rank the following criteria in order of importance (from most to least important):")
    
    for key, value in prior.items():
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
    heading = add_priority()
    data = {"name":[]}
    for person in potential_users:
        data["name"] += person
    for attribute in heading:
        answer = []
        for person in potential_users:
        if main.users[-1].


class Tree:
    _root:Optional[Any]
    _subtrees:list[Tree]


    def __init__(self, root:Optional[Any],subtrees:list[Tree])-> None:
        self._root = root
        self._subtrees = subtrees

  
  
def build_preference_tree(listofusers:list[User]) -> Tree:
    tree = Tree('', [])

  