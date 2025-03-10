from __future__ import annotations
from typing import Optional
from faker import Faker
import random
import json
import os


allUsers = []

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
    


# Initialize Faker
fake = Faker()
Faker.seed(1234)

# Predefined attribute choices
interests = ["reading", "dancing", "singing", "playing instruments", "running", "coding", "doing math"]
mbti_types = ["I", "E"], ["S", "N"], ["T", "F"], ["P", "J"]
communication_types = ["texting", "phonecall"]
political_interests = ["Liberal", "Conservative"]
religions = ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism", "Taoism", "Jewish", "Agnosticism", "Other"]
majors = ["Computer Science", "Accounting", "Actuarial Science", "Psychology", "Biochemistry", "Mathematics", "Statistics", "Economics", "Literature", "History"]
years = ["1", "2", "3", "4", "5", "Master"]
languages = ["English", "Cantonese", "Mandarin", "French", "Spanish", "Japanese", "Korean", "Others"]
dating_goals = ["meeting new friends", "short-term relationship", "long-term relationship", "situationship"]

# Generate 200 users
users = []
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
    users.append(user)

# Add fixed users     
fixed_users = [
    {
        "Name": "Charlotte Wong",
        "Age": 18,
        "Gender": "F",
        "Pronouns": "She/Her",
        "Ethnicity": "Asian",
        "Interests": [
            "dancing",
            "singing"
        ],
        "MBTI": "ISTP",
        "Communication Type": "phonecall",
        "Political Interests": "Liberal",
        "Religion": "Agnosticism",
        "Major": "Computer Science",
        "Year": "1",
        "Language": "Cantonese",
        "Dating Goal": "long-term relationship",
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
            "coding"
        ],
        "MBTI": "ISTP",
        "Communication Type": "texting",
        "Political Interests": "Conservative",
        "Religion": "Protestant",
        "Major": "Computer Science",
        "Year": "1",
        "Language": "Cantonese",
        "Dating Goal": "long-term relationship",
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
            "playing instruments"
        ],
        "MBTI": "ENTP",
        "Communication Type": "phonecall",
        "Political Interests": "Conservative",
        "Religion": "Other",
        "Major": "Computer Science",
        "Year": "1",
        "Language": "Cantonese",
        "Dating Goal": "meeting new friends",
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
            "doing math"
        ],
        "MBTI": "ISFP",
        "Communication Type": "texting",
        "Political Interests": "Conservative",
        "Religion": "Protestant",
        "Major": "Computer Science",
        "Year": "1",
        "Language": "Cantonese",
        "Dating Goal": "meeting new friends",
        "Likes Pets": True,
        "Likes Outdoor Activities": False,
        "Enjoys Watching Movies": False
    }
]
users.extend(fixed_users)

output_dir = "/Users/joseph/Desktop/Joseph Folder/[01] UofT/[01] Year 1/[05] CSC111/csc111/assignments/project2/" 

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the full output path
output_path = os.path.join(output_dir, "new_data.json")

# Save to JSON file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(users, f, indent=4)

print(f"Dataset saved as {output_path}")




