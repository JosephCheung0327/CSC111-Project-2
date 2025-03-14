from __future__ import annotations
from typing import Optional
from faker import Faker
import random
import json
import os


user_list = []

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


class DatingApp:
    """
    Representation invariants:
    - users != []
    """
    users: list[User]

    def __init__(self, users: list[User]):
        self.users = users

    def match(self, user1: User, user2: User) -> None:
        user1.romantic_current = user2
        user2.romantic_current = user1
        user1.romantic_degree += 1
        user2.romantic_degree += 1
        user1.romantic_ex.append(user2)
        user2.romantic_ex.append(user1)

    def unmatch(self, user1: User, user2: User) -> None:
        user1.romantic_current = None
        user2.romantic_current = None
        user1.romantic_degree -= 1
        user2.romantic_degree -= 1
        user1.romantic_ex.remove(user2)
        user2.romantic_ex.remove(user1)

    def socialize(self, user1: User, user2: User) -> None:
        user1.social_current = user2
        user2.social_current = user1
        user1.social_degree += 1
        user2.social_degree += 1
        user1.social_ex.append(user2)
        user2.social_ex.append(user1)

    def unsocialize(self, user1: User, user2: User) -> None:
        user1.social_current = None
        user2.social_current = None
        user1.social_degree -= 1
        user2.social_degree -= 1
        user1.social_ex.remove(user2)
        user2.social_ex.remove(user1)

    def get_romantic_degree(self, user: User) -> int:
        return user.romantic_degree

    def get_social_degree(self, user: User) -> int:
        return user.social_degree

    def get_romantic_current(self, user: User) -> Optional[User]:
        return user.romantic_current

    def get_social_current(self, user: User) -> Optional[User]:
        return user.social_current

class Tree:
    def __init__(self):
        pass



class Graph:
    def __init__(self):
        self.graph = {}
    
    

class DecisionTree:
    pass
    

def generate_users(seed: int = 1234) -> None:
    fake = Faker()
    Faker.seed(seed)

    # Predefined attribute choices
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

    # Generate 200 users
    for _ in range(200):
        gender = random.choice(["M", "F"])
        user = {
            "Name": fake.name(),
            "Age": random.randint(18, 30),
            "Gender": gender,
            "Pronouns": "He/Him" if gender == "M" else "She/Her",
            "Ethnicity": random.choice(["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]),
            "Interests": random.sample(interests, k=random.randint(1, 3)),
            "MBTI": "".join(random.choice(pair) for pair in mbti_types),
            "Communication Type": random.choice(communication_types),
            "Political Interests": random.choice(political_interests),
            "Religion": random.choice(religions),
            "Major": random.choice(majors),
            "Year": random.choice(years),
            "Language": random.choice(languages),
            "Dating Goal": random.choice(dating_goals),
            "Likes Pets": random.choice([True, False]),
            "Likes Outdoor Activities": random.choice([True, False]),
            "Enjoys Watching Movies": random.choice([True, False]),
        }
        user_list.append(user)

    # Add 4 fixed users     
    fixed_users = [
        {
            "Name": "Charlotte Wong",
            "Age": 18,
            "Gender": "F",
            "Pronouns": "She/Her",
            "Ethnicity": "Asian",
            "Interests": [
                "Dancing",
                "Singing"
            ],
            "MBTI": "ISTP",
            "Communication Type": "Phonecall",
            "Political Interests": "Liberal",
            "Religion": "Agnosticism",
            "Major": "Computer Science",
            "Year": "1",
            "Language": "Cantonese",
            "Dating Goal": "Long-term relationship",
            "Likes Pets": False,
            "Likes Outdoor Activities": True,
            "Enjoys Watching Movies": True
        },
        {
            "Name": "Joseph Cheung",
            "Age": 18,
            "Gender": "M",
            "Pronouns": "He/Him",
            "Ethnicity": "Asian",
            "Interests": [
                "Coding"
            ],
            "MBTI": "ISTP",
            "Communication Type": "Texting",
            "Political Interests": "Conservative",
            "Religion": "Protestant",
            "Major": "Computer Science",
            "Year": "1",
            "Language": "Cantonese",
            "Dating Goal": "Long-term relationship",
            "Likes Pets": True,
            "Likes Outdoor Activities": False,
            "Enjoys Watching Movies": True
        },
        {
            "Name": "Janice Lam",
            "Age": 18,
            "Gender": "F",
            "Pronouns": "She/Her",
            "Ethnicity": "Mixed",
            "Interests": [
                "Playing instruments"
            ],
            "MBTI": "ENTP",
            "Communication Type": "Phonecall",
            "Political Interests": "Conservative",
            "Religion": "Other",
            "Major": "Computer Science",
            "Year": "1",
            "Language": "Cantonese",
            "Dating Goal": "Meeting new friends",
            "Likes Pets": False,
            "Likes Outdoor Activities": True,
            "Enjoys Watching Movies": False
        },
        {
            "Name": "Winston Liang",
            "Age": 18,
            "Gender": "M",
            "Pronouns": "He/Him",
            "Ethnicity": "Asian",
            "Interests": [
                "Doing math"
            ],
            "MBTI": "ISFP",
            "Communication Type": "Texting",
            "Political Interests": "Conservative",
            "Religion": "Protestant",
            "Major": "Computer Science",
            "Year": "1",
            "Language": "Cantonese",
            "Dating Goal": "Meeting new friends",
            "Likes Pets": True,
            "Likes Outdoor Activities": False,
            "Enjoys Watching Movies": False
        }
    ]
    user_list.extend(fixed_users)
        

def add_user():
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
    
    likes_pets = input("Likes Pets (True/False): ").lower() == 'true'
    likes_outdoor_activities = input("Likes Outdoor Activities (True/False): ").lower() == 'true'
    enjoys_watching_movies = input("Enjoys Watching Movies (True/False): ").lower() == 'true'


    user = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Pronouns": pronouns,
        "Ethnicity": ethnicity,
        "Interests": interests,
        "MBTI": mbti,
        "Communication Type": communication_type,
        "Political Interests": political_interests,
        "Religion": religion,
        "Major": major,
        "Year": year,
        "Language": language,
        "Dating Goal": dating_goal,
        "Likes Pets": likes_pets,
        "Likes Outdoor Activities": likes_outdoor_activities,
        "Enjoys Watching Movies": enjoys_watching_movies,
    }

    users.append(user)
    print("User added successfully!")


def generate_json(users: list[dict]) -> None:
    # Set output directory of the generated JSON file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "new_data.json"
    output_path = os.path.join(output_dir, filename)

    # Save list of users to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

    print(f"Dataset saved as {output_path}")


if __name__ == "__main__":
    generate_users(1234)
    generate_json(user_list)
