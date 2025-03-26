from __future__ import annotations
from typing import Optional
from faker import Faker
import random
import json
import os



def generate_users_with_class(list_size: int, topmatch_simulation_size: int, seed: int = 1234) -> list[User]:
    """Return a list of list_size number of users with randomly generated attributes, and randomly simulate 
    top_match_simulation_size number of users in the topmatch list (users that a user is interested in). 
    If both users have each other in their  topmatch list mutually, they are added to their self.match list as user.
    
    Preconditions:
    - seed is not None
    - isinstance(seed, int) == True
    
    
    >>> user_list_generated = generate_users_with_class(2, 1, 1234)
    >>> user_list_generated[0].match == user_list_generated[1].match 
    True
    # Since there are only two users generated, and each of them has a topmatch (the other person), they are matched.
    """
    fake = Faker()
    Faker.seed(seed)
    user_list = []
    
    interests = ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding", "Doing math"]
    mbti_types = ["I", "E"], ["S", "N"], ["T", "F"], ["P", "J"]
    communication_types = ["Texting", "Phonecall"]
    political_interests = ["Liberal", "Conservative"]
    religions = ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism", "Taoism", "Jewish", "Agnosticism", "Other"]
    majors = ["Computer Science", "Accounting", "Actuarial Science", "Psychology", "Biochemistry", "Mathematics", "Statistics", "Economics", 
    "Literature", "History", "Political Science", "Music", "Physics", "Chemistry", "Cognitive Science", "Philosophy", "Others"]
    years = ["1", "2", "3", "4", "5", "Master"]
    languages = ["English", "Cantonese", "Mandarin", "French", "Spanish", "Japanese", "Korean", "Others"]
    dating_goals = ["Meeting new friends", "Short-term relationship", "Long-term relationship", "Situationship"]

    for _ in range(list_size):
        gender = random.choice(["M", "F"])
        user = User(
            name=fake.name(),
            age=random.randint(18, 30),
            gender=gender,
            pronouns="He/Him" if gender == "M" else "She/Her",
            characteristics=Characteristics(
            ethnicity=random.choice(["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]),
            interests=random.sample(interests, k=random.randint(1, 3)),
            mbti="".join(random.choice(pair) for pair in mbti_types),
            communication_type=random.choice(communication_types),
            political_interests=random.choice(political_interests),
            religion=random.choice(religions),
            major=random.choice(majors),
            year=random.choice(years),
            language=random.choice(languages),
            likes_pets=random.choice([True, False]),
            likes_outdoor_activities=random.choice([True, False]),
            enjoys_watching_movies=random.choice([True, False])),
            dating_goal=random.choice(dating_goals),
            topmatch = [],
            match = [],
            social_current = []
        )
        user_list.append(user)
    
    # Assign top matches for each user (Simulation)
    for user in user_list:
        user.topmatch = random.sample([u for u in user_list if u != user], topmatch_simulation_size)
    for user in user_list:
        user.match = [match for match in user.topmatch if user in match.topmatch]
    for user in user_list:
        user.social_current = [match for match in user.topmatch if user in match.topmatch]

    for user in user_list:
        user.update_social_degree()

    return user_list

class Characteristics:
    """Class representing user characteristics that influence a user's preference.
        Instance Attributes:
        - ethnicity: The user's ethnicity.
        - interests: A list of the user's hobbies or interests.
        - mbti: The user's Myers-Briggs personality type (e.g., INFP, ESTJ).
        - communication_type: The user's preferred communication style (e.g., text, call, in-person).
        - political_interests: The user's political views or level of political engagement.
        - religion: The user's religious belief.
        - major: The user's academic major (e.g., Computer Science, Psychology).
        - year: The user's academic year (e.g., First Year, Second Year, Junior, Senior).
        - language: The primary language the user speaks.
        - likes_pets: Whether the user likes pets or not.
        - likes_outdoor_activities: Whether the user enjoys outdoor activities (e.g., hiking, sports).
        - enjoys_watching_movies: Whether the user enjoys watching movies or shows.
    """
    

    def __init__(self, ethnicity: str, interests: list[str], mbti: str, communication_type: str,
                 political_interests: str, religion: str, major: str, year: str, language: str,
                 likes_pets: bool, likes_outdoor_activities: bool, enjoys_watching_movies: bool):
        self.ethnicity = ethnicity
        self.interests = interests
        self.mbti = mbti
        self.communication_type = communication_type
        self.political_interests = political_interests
        self.religion = religion
        self.major = major
        self.year = year
        self.language = language
        self.likes_pets = likes_pets
        self.likes_outdoor_activities = likes_outdoor_activities
        self.enjoys_watching_movies = enjoys_watching_movies 
    


class User:
    """Represents a user in the dating app. 

    Instance Attributes:
    - name: the name of the user.
    - age: the age of the user.
    - gender: the gender of the user.
    - pronouns: the pronouns of the user.
    - dating_goal: Whether the user is planning to just "Meeting new friends", having
        "Short-term relationship", "Long-term relationship", or "Situationship".
    - characteristics: the features of the user, as provided by the user.
    - topmatch: a list of users that the user is interested in.
    - match: a list of users that the user are interested in and they also are interested in the user.
    - romantic_current: the user's current romantic partner.
    - romantic_ex: a list of user's ex-partners.
    - social_current: a list of the user's friends.
    - social_ex: a list of the unfriended users of user.
    - romantic_degree: the number of romantic relationship the user is currently experiencing (0 or 1, we assume).
    - social_degree: the number of friends the user has. 

    Representation invariants:
    - name != ""
    - romantic_degree >= 0
    - social_degree >= 0
    """
    name: str
    romantic_current: Optional[User]
    romantic_ex: list[User]
    social_current: list[User]
    social_ex: list[User]
    romantic_degree: int
    social_degree: int

    def __init__(self, name: str,  age, gender, pronouns, dating_goal, characteristics: Characteristics, topmatch, match,
                 romantic_current: Optional[User] = None, romantic_ex: list[User] = [],
                 social_current: Optional[list[User]] = None, social_ex: list[User] = [], romantic_degree: int = 0,
                 social_degree: int = 0):
        self.name = name
        self.age = age
        self.gender = gender
        self.pronouns = pronouns
        self.characteristics = characteristics
        self.dating_goal = dating_goal
      
        
        self.topmatch = topmatch
        self.match = []
        self.romantic_current = romantic_current
        self.romantic_ex = romantic_ex
        self.social_current = social_current
        self.social_ex = social_ex
        self.romantic_degree = romantic_degree
        self.social_degree = social_degree

    def __repr__(self):
        return f"User({self.name}, {self.age}, {self.gender}, {self.mbti})"
    
    def update_social_degree(self):
        self.social_degree = len(self.social_current)



class DatingApp:
    """


    Representation invariants:
    - users != []
    """
    users: list[User]

    def __init__(self, users: list[User]):
        self.users = users

    def match(self, user1: User, user2: User) -> None:
        if user1 not in user2.romantic_current and user2 not in user1.romantic_current:
            user1.romantic_current.append(user2)
            user2.romantic_current.append(user1)
            user1.romantic_degree += 1
            user2.romantic_degree += 1
        else:
            print(f"Matching failed. {user1} and {user2} are already couples.")


    def unmatch(self, user1: User, user2: User) -> None:
        if user1 in user2.romantic_current and user2 in user1.romantic_current:
            user1.romantic_current.remove(user2)
            user2.romantic_current.remove(user2)
            user1.romantic_ex.append(user2)
            user2.romantic_ex.append(user1)
        else:
            print(f"Unmatch failed. {user1} and {user2} are not couples.")


    def socialize(self, user1: User, user2: User) -> None:
        if user1 not in user2.romantic_current and user2 not in user1.romantic_current:
            user1.social_current.append(user2)
            user2.social_current.append(user1)
            user1.social_degree += 1
            user2.social_degree += 1
        else:
            print(f"Friend add failed. {user1} and {user2} are already friends.")

    def unsocialize(self, user1: User, user2: User) -> None:
        if user1 in user2.romantic_current and user2 in user1.romantic_current:
            user1.social_current.remove(user2)
            user2.social_current.remove(user2)
            user1.social_degree -= 1
            user2.social_degree -= 1
            user1.social_ex.append(user2)
            user2.social_ex.append(user1)
        else:
            print(f"Unfriend failed. {user1} and {user2} are not friends.")

    def get_romantic_degree(self, user: User) -> int:
        return user.romantic_degree

    def get_social_degree(self, user: User) -> int:
        return user.social_degree

    def get_romantic_current(self, user: User) -> Optional[User]:
        return user.romantic_current

    def get_social_current(self, user: User) -> Optional[User]:
        return user.social_current
    
    

    
class DecisionTree:
    pass
    


def add_fixed_users(users: list[dict]) -> None:
    fixed_users = [
        User(
            name="Charlotte Wong",
            age=18,
            gender="F",
            pronouns="She/Her",
            characteristics=Characteristics(
            ethnicity="Asian",
            interests=["Dancing", "Singing"],
            mbti="ISTP",
            communication_type="Phonecall",
            political_interests="Liberal",
            religion="Agnosticism",
            major="Computer Science",
            year="1",
            language="Cantonese",
            likes_pets=False,
            likes_outdoor_activities=True,
            enjoys_watching_movies=True),
            dating_goal="Long-term relationship",
            topmatch = [],
            match = [],
            social_current = []
        ),
        User(
            name="Joseph Cheung",
            age=18,
            gender="M",
            pronouns="He/Him",
            characteristics=Characteristics(
            ethnicity="Asian",
            interests=["Coding"],
            mbti="ISTP",
            communication_type="Texting",
            political_interests="Conservative",
            religion="Protestant",
            major="Computer Science",
            year="1",
            language="Cantonese",
            likes_pets=True,
            likes_outdoor_activities=False,
            enjoys_watching_movies=True),
            dating_goal="Long-term relationship",
            topmatch = [],
            match = [],
            social_current = []
        ),
        User(
            name="Janice Lam",
            age=18,
            gender="F",
            pronouns="She/her",
            characteristics=Characteristics(
            ethnicity="Mixed",
            interests=["Playing instruments"],
            mbti="ENTP",
            communication_type="Phonecall",
            political_interests="Conservative",
            religion="Other",
            major="Computer Science",
            year="1",
            language="Cantonese",
            likes_pets=False,
            likes_outdoor_activities=True,
            enjoys_watching_movies=False),
            dating_goal="Meeting new friends",
            topmatch = [],
            match = [],
            social_current = []
        ),
         User(
            name="Winston Liang",
            age=18,
            gender="M",
            pronouns="He/him",
            characteristics=Characteristics(
            ethnicity="Asian",
            interests=["Doing math"],
            mbti="ISFP",
            communication_type="Texting",
            political_interests="Conservative",
            religion="Protestant",
            major="Computer Science",
            year="1",
            language="Cantonese",
            likes_pets=True,
            likes_outdoor_activities=False,
            enjoys_watching_movies=False),
            dating_goal="Meeting new friends",
            topmatch = [],
            match = [],
            social_current = []
        )
    ]

    for i in range(len(fixed_users)):
        for j in range(len(fixed_users)):
            if i != j:  # Don't connect user to themselves
                fixed_users[i].social_current.append(fixed_users[j])
    
    # Connect fixed users with some random existing users
    for fixed_user in fixed_users:
        # Select 3-5 random users from the existing list
        random_connections = random.sample(users[:20], random.randint(3, 5))
        for connection in random_connections:
            if connection not in fixed_user.social_current and connection != fixed_user:
                fixed_user.social_current.append(connection)
                connection.social_current.append(fixed_user)
    
    # Update social degrees
    for user in fixed_users:
        user.update_social_degree()
    
    # Add fixed users to the list
    users.extend(fixed_users)
        

def add_user(users: list[dict]) -> None:
    name = input("Enter Name: ").capitalize()
    
    while True:
        try:
            age = int(input("Enter Age: "))
            if 18 <= age <= 30:
                break
            else:
                print("This application is only designed for users aged between 18 and 30.")
        except ValueError:
            print("Invalid input. Please enter a valid age.")
    
    gender = input("Enter Gender (M/F): ").capitalize()
    while gender.upper() not in ["M", "F"]:
        gender = input("Invalid input. Enter Gender (M/F): ").capitalize()
    
    pronouns = "/".join([p.capitalize() for p in input("Enter Pronouns (e.g., he/him): ").split('/')])
    
    ethnicity = input("Enter Ethnicity (Asian, Black, Hispanic, White, Mixed, Other): ").capitalize()
    while ethnicity.capitalize() not in ["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]:
        ethnicity = input("Invalid input. Enter Ethnicity (Asian, Black, Hispanic, White, Mixed, Other): ").capitalize()
    
    interests = [interest.strip().capitalize() for interest in input("Enter Interests (comma-separated from Reading, Dancing, Singing, Playing instruments, Running, Coding, Doing math): ").split(',')]
    while not all(interest.capitalize() in ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding", "Doing math"] for interest in interests):
        interests = [interest.strip().capitalize() for interest in input("Invalid input. Enter Interests (comma-separated from Reading, Dancing, Singing, Playing instruments, Running, Coding, Doing math): ").split(',')]
    
    while True:
        mbti = input("Enter MBTI: ").upper()
        if len(mbti) == 4 and all(char in "IESTFPJ" for char in mbti) and mbti[0] in "IE" and mbti[1] in "SN" and mbti[2] in "TF" and mbti[3] in "PJ":
            break
        else:
            print("Invalid input. Enter MBTI (e.g., INFP, ESTJ): ")
    
    communication_type = input("Enter Communication Type (Texting, Phonecall): ").capitalize()
    while communication_type.capitalize() not in ["Texting", "Phonecall"]:
        communication_type = input("Invalid input. Enter Communication Type (Texting, Phonecall): ").capitalize()
    
    political_interests = input("Enter Political Interests (Liberal, Conservative): ").capitalize()
    while political_interests.capitalize() not in ["Liberal", "Conservative"]:
        political_interests = input("Invalid input. Enter Political Interests (Liberal, Conservative): ").capitalize()
    
    religion = input("Enter Religion (Protestant, Orthodox, Catholic, Buddhism, Hinduism, Taoism, Jewish, Agnostic, Other): ").capitalize()
    while religion.capitalize() not in ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism", "Taoism", "Jewish", "Agnostic", "Other"]:
        religion = input("Invalid input. Enter Religion (Protestant, Orthodox, Catholic, Buddhism, Hinduism, Taoism, Jewish, Agnostic, Other): ").capitalize()
    
    major = input("Enter Major (Computer Science, Accounting, Actuarial Science, Psychology, Biochemistry, Mathematics, Statistics, Economics, Literature, History, Political Science, Music, Physics, Chemistry, Cognitive Science, Philosophy, Others): ").title()
    while major.title() not in ["Computer Science", "Accounting", "Actuarial Science", "Psychology", "Biochemistry", "Mathematics", "Statistics", "Economics", "Literature", "History", "Political Science", "Music", "Physics", "Chemistry", "Cognitive Science", "Philosophy", "Others"]:
        major = input("Invalid input. Enter Major (Computer Science, Accounting, Actuarial Science, Psychology, Biochemistry, Mathematics, Statistics, Economics, Literature, History, Political Science, Music, Physics, Chemistry, Cognitive Science, Philosophy, Others): ").title()
    
    year = input("Enter Year (1, 2, 3, 4, 5, Master): ").capitalize()
    while year.capitalize() not in ["1", "2", "3", "4", "5", "Master"]:
        year = input("Invalid input. Enter Year (1, 2, 3, 4, 5, Master): ").capitalize()
    
    language = input("Enter Language (English, Cantonese, Mandarin, French, Spanish, Japanese, Korean, Others): ").capitalize()
    while language.capitalize() not in ["English", "Cantonese", "Mandarin", "French", "Spanish", "Japanese", "Korean", "Others"]:
        language = input("Invalid input. Enter Language (English, Cantonese, Mandarin, French, Spanish, Japanese, Korean, Others): ").capitalize()
    
    dating_goal = input("Enter Dating Goal (Meeting new friends, Short-term relationship, Long-term relationship, Situationship): ").capitalize()
    while dating_goal.capitalize() not in ["Meeting new friends", "Short-term relationship", "Long-term relationship", "Situationship"]:
        dating_goal = input("Invalid input. Enter Dating Goal (Meeting new friends, Short-term relationship, Long-term relationship, Situationship): ").capitalize()
    
    while True:
            likes_pets = input("Likes Pets (True/False): ").lower()
            if likes_pets in ['true', 'false']:
                likes_pets = likes_pets == 'true'
                break
            else:
                print("Invalid input. Please enter 'True' or 'False'.")
        
    while True:
        likes_outdoor_activities = input("Likes Outdoor Activities (True/False): ").lower()
        if likes_outdoor_activities in ['true', 'false']:
            likes_outdoor_activities = likes_outdoor_activities == 'true'
            break
        else:
            print("Invalid input. Please enter 'True' or 'False'.")
    
    while True:
        enjoys_watching_movies = input("Enjoys Watching Movies (True/False): ").lower()
        if enjoys_watching_movies in ['true', 'false']:
            enjoys_watching_movies = enjoys_watching_movies == 'true'
            break
        else:
            print("Invalid input. Please enter 'True' or 'False'.")


    user = User(
            name=name,
            age=age,
            gender=gender, 
            pronouns=pronouns,
            characteristics=Characteristics(
            ethnicity=ethnicity,
            interests=interests,
            mbti=mbti,
            communication_type=communication_type,
            political_interests=political_interests,
            religion=religion,
            major=major,
            year=year,
            language=language,
            likes_pets=likes_pets,
            likes_outdoor_activities=likes_outdoor_activities,
            enjoys_watching_movies=enjoys_watching_movies),
            dating_goal=dating_goal,
            topmatch = [],
            match = [],
            social_current = [])
    
    users.append(user)
    print("User added successfully!")

def add_priority():
    attributes = {"Ethnicity": 1, "Interests": 2, "MBTI": 3, "Communication Type": 4, "Political Interests": 5, \
    "Religion": 6, "Major": 7, "Year": 8, "Language": 9, "Likes Pets": 10, "Likes Outdoor Activities": 11,\
    "Enjoys Watching Movies": 12}

    print("Please rank the following criteria in order of importance (from most to least important):")
    for key, value in attributes.items():
        print(f"({value}) {key.replace('_', ' ').title()}")

    ranking = input("Enter the numbers in order (e.g., 3 1 4 2 5 6 7 8 10 11 9 12): ").split()

    #based on ranking, create decision tree (helper function)
    



users = generate_users_with_class(200, 25, 1234)

if __name__ == "__main__":
    import graph
    graph.app.run_server(debug=True)