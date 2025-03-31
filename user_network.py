"""
The program for handling user_network.
"""
from __future__ import annotations
from typing import Optional
import random
import python_ta
from faker import Faker


user_list = []
user_keypair = {}


def generate_users_with_class(list_size: int, seed: int = 1234) -> list[User]:
    """Return a list of list_size number of users with randomly generated attributes, and randomly simulate
    interested_friend_sim_size number of users in the interested_friend list
    (users that a user is interested in). If both users have each other in their interested_friend list mutually,
     they are added to their self.social_current list as user.

    Preconditions:
    - seed is not None
    - isinstance(seed, int) == True


    >>> user_list_generated = generate_users_with_class(2, 1234)
    >>> user_list_generated[0].social_current == user_list_generated[1].social_current
    True
    Since there are only two users generated, and each of them has a interested_friend (the other person),
    they are matched.
    """
    fake = Faker()
    Faker.seed(seed)
    user_list_1 = []

    interests = ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding", "Doing math"]
    mbti_types = ["I", "E"], ["S", "N"], ["T", "F"], ["P", "J"]
    communication_types = ["Texting", "Phonecall"]
    political_interests = ["Liberal", "Conservative"]
    religions = ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism", "Taoism", "Jewish",
                 "Agnosticism", "Other"]
    majors = ["Computer Science", "Accounting", "Actuarial Science", "Psychology", "Biochemistry", "Mathematics",
              "Statistics", "Economics",
              "Literature", "History", "Political Science", "Music", "Physics", "Chemistry", "Cognitive Science",
              "Philosophy", "Others"]
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
            dating_goal=random.choice(dating_goals), interested_friend=[],
            interested_romantic=[],
            social_current=[],
            romantic_current=None

        )
        user_list_1.append(user)

    return user_list_1


def simulate_connections(user_list_2: list[User]) -> tuple:
    """
    Create social and romantic connections between users based on compatibility.
    """
    from common import data_wrangling, build_preference_tree, generate_10_people_list

    user_keypair_local = {user.name: user for user in user_list_2}

    users_looking_for_friends = [user for user in user_list_2 if user.dating_goal == "Meeting new friends"]
    users_looking_for_love = [user for user in user_list_2 if user.dating_goal != "Meeting new friends"]

    characteristics_default_rank = ["ethnicity", "interests", "mbti", "communication_type", "political_interests",
                                    "religion", "major", "year", "language", "likes_pets",
                                    "likes_outdoor_activities", "enjoys_watching_movies"]

    print(f"Processing {len(users_looking_for_friends)} friend seekers")

    for user in users_looking_for_friends:
        try:
            data_wrangling(user, characteristics_default_rank, users_looking_for_friends, "friends.csv")
            t = build_preference_tree('friends.csv')
            result = t.run_preference_tree()
            name_list = generate_10_people_list(result)

            # Convert name strings to User objects with error checking
            user.interested_friend = []
            for namestring in name_list:
                if namestring in user_keypair_local:
                    user.interested_friend.append(user_keypair_local[namestring])
                else:
                    print(f"Warning: User '{namestring}' not found for {user.name}")
        except Exception as e:
            print(f"Error generating friends for {user.name}: {e}")

    print(f"Processing {len(users_looking_for_love)} romantic seekers")

    for user in users_looking_for_love:
        try:
            data_wrangling(user, characteristics_default_rank, users_looking_for_love, "love.csv")
            t = build_preference_tree('love.csv')
            result = t.run_preference_tree()
            name_list = generate_10_people_list(result)

            # Convert name strings to User objects with error checking
            user.interested_romantic = []
            for namestring in name_list:
                if namestring in user_keypair_local:
                    user.interested_romantic.append(user_keypair_local[namestring])
                else:
                    print(f"Warning: User '{namestring}' not found for {user.name}")
        except Exception as e:
            print(f"Error generating romantic interests for {user.name}: {e}")

    for user in users_looking_for_friends:
        user.social_current = [social_current for social_current in user.interested_friend
                               if user in social_current.interested_friend]
        user.update_social_degree()

    for user in users_looking_for_love:
        # Skip users with no romantic interests
        if not user.interested_romantic:
            continue

        # Get the user's top romantic interest
        top_match = user.interested_romantic[0]

        # Check if it's a mutual top match (they also have the user as their top interest)
        if (hasattr(top_match, 'interested_romantic') and
                top_match.interested_romantic and top_match.interested_romantic[0] == user):
            # Create mutual romantic connection
            user.romantic_current = top_match
            top_match.romantic_current = user

        user.update_romantic_degree()

    return users_looking_for_friends, users_looking_for_love


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
    ethnicity: str
    interests: list[str]
    mbti: str
    communication_type: str
    political_interests: str
    religion: str
    major: str
    year: str
    language: str
    likes_pets: bool
    likes_outdoor_activities: bool
    enjoys_watching_movies: bool

    def __init__(self, ethnicity: str, interests: list[str], mbti: str, communication_type: str,
                 political_interests: str, religion: str, major: str, year: str, language: str,
                 likes_pets: bool, likes_outdoor_activities: bool, enjoys_watching_movies: bool) -> None:
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
    - interested_friend: a list of users that the user is interested in.
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
    age: int
    gender: str
    pronouns: str
    dating_goal: str
    interested_friend: list
    interested_romantic: list
    romantic_current: Optional[User]
    characteristics: Characteristics
    romantic_ex: list[User]
    social_current: list[User]
    social_ex: list[User]
    romantic_degree: int
    social_degree: int

    def __init__(self, name: str, age: int, gender: str, pronouns: str, dating_goal: str,
                 characteristics: Characteristics,
                 interested_friend: list, interested_romantic: list, romantic_current: Optional[User] = None,
                 romantic_ex: list[User] = [], social_current: Optional[list[User]] = None, social_ex: list[User] =[],
                 romantic_degree: int = 0,
                 social_degree: int = 0) -> None:
        self.name = name
        self.age = age
        self.gender = gender
        self.pronouns = pronouns
        self.characteristics = characteristics
        self.dating_goal = dating_goal

        self.interested_friend = interested_friend
        self.interested_romantic = interested_romantic

        self.romantic_current = romantic_current
        self.romantic_ex = romantic_ex
        self.social_current = social_current
        self.social_ex = social_ex
        self.romantic_degree = romantic_degree
        self.social_degree = social_degree

    def __repr__(self) -> str:
        return f"User({self.name}, {self.age}, {self.gender}, {self.characteristics.mbti})"

    def update_social_degree(self) -> None:
        """Update_social_degree"""
        self.social_degree = len(self.social_current)

    def update_romantic_degree(self) -> None:
        """Update_ramantic_degree"""
        if self.romantic_current is not None:
            self.romantic_degree = 1

    def match(self, user1: User) -> None:
        """Match self with user1 as romantic relationship.
        Preconditions:
        - (self not in user1.romantic_current and user1 not in self.romantic_current)
            or (self in user1.romantic_current and user1 in self.romantic_current)
        """
        if self is not user1.romantic_current and user1 is not self.romantic_current:
            self.romantic_current = user1
            user1.romantic_current = self
            self.romantic_degree += 1
            user1.romantic_degree += 1
        else:
            print(f"Matching failed. {self} and {user1} are already couples.")

    def socialize(self, user1: User) -> None:
        """Create self and user1 friendship.
        Preconditions:
        - (self not in user1.social_current and user1 not in self.social_current)
            or (self in user1.social_current and user1 in self.social_current)
        """
        if self not in user1.social_current and user1 not in self.social_current:
            self.social_current.append(user1)
            user1.social_current.append(self)
            self.social_degree += 1
            user1.social_degree += 1
        else:
            print(f"Friend add failed. {self} and {user1} are already friends.")

    def get_romantic_degree(self, user: User) -> int:
        """Get romantic degree."""
        return user.romantic_degree

    def get_social_degree(self, user: User) -> int:
        """Get social degree."""
        return user.social_degree

    def get_romantic_current(self, user: User) -> Optional[User]:
        """Get romantic current """
        return user.romantic_current

    def get_social_current(self, user: User) -> list[User]:
        """Get social current"""
        return user.social_current


def add_fixed_users(users: list[User]) -> None:
    """
    Adding the creators into the user list. Creators also want to play!
    """
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
            interested_friend=[],
            social_current=[],
            interested_romantic=[]
        ),
        User(
            name="Joseph Cheung",
            age=19,
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
            interested_friend=[],
            social_current=[],
            interested_romantic=[]
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
            interested_friend=[],
            social_current=[],
            interested_romantic=[]
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
            interested_friend=[],
            social_current=[],
            interested_romantic=[]
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
    """
    Asks the user to input their information and parse the data into User object to be added to the user list.
    Used when the app is run without the ui.py.
    """
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

    interests = [interest.strip().capitalize() for interest in
                 input("Enter Interests (comma-separated from Reading, Dancing,"
                       " Singing, Playing instruments, Running, Coding, Doing math): ").split(',')]
    while not all(interest.capitalize() in ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding",
                                            "Doing math"] for interest in interests):
        interests = [interest.strip().capitalize() for interest in input("Invalid input."
                                                                         " Enter Interests (comma-separated from"
                                                                         " Reading, Dancing, Singing, "
                                                                         "Playing instruments, Running, Coding,"
                                                                         " Doing math): ").split(',')]

    while True:
        mbti = input("Enter MBTI: ").upper()
        if (len(mbti) == 4 and all(char in "IESNTFPJ" for char in mbti) and mbti[0] in "IE" and mbti[1] in "SN" and mbti[2] in "TF" and mbti[3] in "PJ"):
            break
        else:
            print("Invalid input. Enter MBTI (e.g., INFP, ESTJ): ")

    communication_type = input("Enter Communication Type (Texting, Phonecall): ").capitalize()
    while communication_type.capitalize() not in ["Texting", "Phonecall"]:
        communication_type = input("Invalid input. Enter Communication Type (Texting, Phonecall): ").capitalize()

    political_interests = input("Enter Political Interests (Liberal, Conservative): ").capitalize()
    while political_interests.capitalize() not in ["Liberal", "Conservative"]:
        political_interests = input("Invalid input. Enter Political Interests (Liberal, Conservative): ").capitalize()

    religion = input("Enter Religion (Protestant, Orthodox, Catholic, Buddhism,"
                     " Hinduism, Taoism, Jewish, Agnostic, Other): ").capitalize()
    while religion.capitalize() not in ["Protestant", "Orthodox", "Catholic", "Buddhism",
                                        "Hinduism", "Taoism", "Jewish", "Agnostic", "Other"]:
        religion = input("Invalid input. Enter Religion (Protestant, Orthodox, Catholic,"
                         " Buddhism, Hinduism, Taoism, Jewish, Agnostic, Other): ").capitalize()

    major = input("Enter Major (Computer Science, Accounting, Actuarial Science, Psychology, Biochemistry, "
                  "Mathematics, Statistics, Economics, Literature, History, Political Science, Music, Physics, "
                  "Chemistry, Cognitive Science, Philosophy, Others): ").title()
    while major.title() not in ["Computer Science", "Accounting", "Actuarial Science", "Psychology", "Biochemistry",
                                "Mathematics", "Statistics", "Economics", "Literature", "History", "Political Science",
                                "Music", "Physics", "Chemistry", "Cognitive Science", "Philosophy", "Others"]:
        major = input("Invalid input. Enter Major (Computer Science, Accounting, Actuarial Science, Psychology, "
                      "Biochemistry, Mathematics, Statistics, Economics, Literature, History, Political Science, Music,"
                      " Physics, Chemistry, Cognitive Science, Philosophy, Others): ").title()

    year = input("Enter Year (1, 2, 3, 4, 5, Master): ").capitalize()
    while year.capitalize() not in ["1", "2", "3", "4", "5", "Master"]:
        year = input("Invalid input. Enter Year (1, 2, 3, 4, 5, Master): ").capitalize()

    language = input("Enter Language (English, Cantonese, Mandarin, French, Spanish, Japanese, "
                     "Korean, Others): ").capitalize()
    while language.capitalize() not in ["English", "Cantonese", "Mandarin", "French", "Spanish",
                                        "Japanese", "Korean", "Others"]:
        language = input("Invalid input. Enter Language (English, Cantonese, Mandarin, French, Spanish, Japanese,"
                         " Korean, Others): ").capitalize()

    dating_goal = input("Enter Dating Goal (Meeting new friends, Short-term relationship, Long-term relationship, "
                        "Situationship): ").capitalize()
    while dating_goal.capitalize() not in ["Meeting new friends", "Short-term relationship",
                                           "Long-term relationship", "Situationship"]:
        dating_goal = input("Invalid input. Enter Dating Goal (Meeting new friends, Short-term relationship,"
                            " Long-term relationship, Situationship): ").capitalize()

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
                ethnicity=ethnicity, interests=interests,
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
            interested_friend=[],
            interested_romantic=[],
            social_current=[],
            romantic_current=None)

    users.append(user)
    print("User added successfully!")


users = generate_users_with_class(200,  1234)
add_fixed_users(users)
user_looking_for_friends, user_looking_for_love = simulate_connections(users)

if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['faker', 'random', 'json', 'os', 'common'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120, 'disable': ['C0415', 'E9969', 'E9992', 'E9997', 'R1702', 'R0913', 'W0102', 'R0914',
                                            'R0902', 'R0912', 'R0915', 'R0916', 'W0621', 'C9103', 'E9988', 'C0301',
                                            'E9989', 'W0718'],
        'forbidden-io-functions': []
    })
