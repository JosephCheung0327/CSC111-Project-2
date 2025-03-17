from __future__ import annotations
from typing import Optional
from faker import Faker
import plotly.graph_objects as go
import networkx as nx
from dash import Dash, dcc, html, Input, Output, State, callback_context
import numpy as np
import random
import json
import os



def generate_users_with_class(seed: int = 1234):
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

    for _ in range(200):
        gender = random.choice(["M", "F"])
        user = User(
            name=fake.name(),
            age=random.randint(18, 30),
            gender=gender,
            pronouns="He/Him" if gender == "M" else "She/Her",
            ethnicity=random.choice(["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]),
            interests=random.sample(interests, k=random.randint(1, 3)),
            mbti="".join(random.choice(pair) for pair in mbti_types),
            communication_type=random.choice(communication_types),
            political_interests=random.choice(political_interests),
            religion=random.choice(religions),
            major=random.choice(majors),
            year=random.choice(years),
            language=random.choice(languages),
            dating_goal=random.choice(dating_goals),
            likes_pets=random.choice([True, False]),
            likes_outdoor_activities=random.choice([True, False]),
            enjoys_watching_movies=random.choice([True, False]),
            topmatch = [],
            match = [],
            social_current = []
        )
        user_list.append(user)

    
    # Assign top matches for each user (Simulation)
    for user in user_list:
        user.topmatch = random.sample([u for u in user_list if u != user], 25)
    for user in user_list:
        user.match = [match for match in user.topmatch if user in match.topmatch]
    for user in user_list:
        user.social_current = [match for match in user.topmatch if user in match.topmatch]

    for user in user_list:
        user.update_social_degree()

    return user_list






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
    social_current: list[User]
    social_ex: list[User]
    romantic_degree: int
    social_degree: int

    def __init__(self, name: str,  age, gender, pronouns, ethnicity, interests, mbti, communication_type, 
                 political_interests, religion, major, year, language, dating_goal, 
                 likes_pets, likes_outdoor_activities, enjoys_watching_movies, topmatch, match,
                 romantic_current: Optional[User] = None, romantic_ex: list[User] = [],
                 social_current: Optional[list[User]] = None, social_ex: list[User] = [], romantic_degree: int = 0,
                 social_degree: int = 0):
        self.name = name
        self.age = age
        self.gender = gender
        self.pronouns = pronouns
        
        self.ethnicity = ethnicity
        self.interests = interests
        self.mbti = mbti
        self.communication_type = communication_type
        self.political_interests = political_interests
        self.religion = religion
        self.major = major
        self.year = year
        self.language = language
        self.dating_goal = dating_goal
        self.likes_pets = likes_pets
        self.likes_outdoor_activities = likes_outdoor_activities
        self.enjoys_watching_movies = enjoys_watching_movies
        
        # self.characteristic = charactersituc (dataclass)

        # @dataclass: characteristic
        #     self.ethnicity: 
        
        #one sec we comment ur code to run the file
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



class Graph:
    def __init__(self):
        self.graph = {}
        
        



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
    



class Treeforfriends:
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        self._root = root
        self._subtrees = subtrees
        

class Treeforpartners:
    pass
    
class DecisionTree:
    pass
    

# def generate_users(seed: int = 1234) -> None:
#     fake = Faker()
#     Faker.seed(seed)

#     # Predefined attribute choices
#     interests = ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding", "Doing math"]
#     mbti_types = ["I", "E"], ["S", "N"], ["T", "F"], ["P", "J"]
#     communication_types = ["Texting", "Phonecall"]
#     political_interests = ["Liberal", "Conservative"]
#     religions = ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism", "Taoism", "Jewish", "Agnosticism", "Other"]
#     majors = ["Computer Science", "Accounting", "Actuarial Science", "Psychology", "Biochemistry", "Mathematics", "Statistics", "Economics", 
#     "Literature", "History", "Political Science", "Music", "Physics", "Chemistry", "Cognitive Science", "Philosophy", "Others"]
#     years = ["1", "2", "3", "4", "5", "Master"]
#     languages = ["English", "Cantonese", "Mandarin", "French", "Spanish", "Japanese", "Korean", "Others"]
#     dating_goals = ["Meeting new friends", "Short-term relationship", "Long-term relationship", "Situationship"]

#     # Generate 200 users
#     for _ in range(200):
#         gender = random.choice(["M", "F"])
#         user = {
#             "Name": fake.name(),
#             "Age": random.randint(18, 30),
#             "Gender": gender,
#             "Pronouns": "He/Him" if gender == "M" else "She/Her",
#             "Ethnicity": random.choice(["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]),
#             "Interests": random.sample(interests, k=random.randint(1, 3)),
#             "MBTI": "".join(random.choice(pair) for pair in mbti_types),
#             "Communication Type": random.choice(communication_types),
#             "Political Interests": random.choice(political_interests),
#             "Religion": random.choice(religions),
#             "Major": random.choice(majors),
#             "Year": random.choice(years),
#             "Language": random.choice(languages),
#             "Dating Goal": random.choice(dating_goals),
#             "Likes Pets": random.choice([True, False]),
#             "Likes Outdoor Activities": random.choice([True, False]),
#             "Enjoys Watching Movies": random.choice([True, False]),
#         }
#         user_list.append(user)


def add_fixed_users(users: list[dict]) -> None:
    fixed_users = [
        User(
            name="Charlotte Wong",
            age=18,
            gender="F",
            pronouns="She/Her",
            ethnicity="Asian",
            interests=["Dancing", "Singing"],
            mbti="ISTP",
            communication_type="Phonecall",
            political_interests="Liberal",
            religion="Agnosticism",
            major="Computer Science",
            year="1",
            language="Cantonese",
            dating_goal="Long-term relationship",
            likes_pets=False,
            likes_outdoor_activities=True,
            enjoys_watching_movies=True,
            topmatch = [],
            match = [],
            social_current = []
        ),
        User(
            name="Joseph Cheung",
            age=18,
            gender="M",
            pronouns="He/Him",
            ethnicity="Asian",
            interests=["Coding"],
            mbti="ISTP",
            communication_type="Texting",
            political_interests="Conservative",
            religion="Protestant",
            major="Computer Science",
            year="1",
            language="Cantonese",
            dating_goal="Long-term relationship",
            likes_pets=True,
            likes_outdoor_activities=False,
            enjoys_watching_movies=True,
            topmatch = [],
            match = [],
            social_current = []
        ),
        User(
            name="Janice Lam",
            age=18,
            gender="F",
            pronouns="She/her",
            ethnicity="Mixed",
            interests=["Playing instruments"],
            mbti="ENTP",
            communication_type="Phonecall",
            political_interests="Conservative",
            religion="Other",
            major="Computer Science",
            year="1",
            language="Cantonese",
            dating_goal="Meeting new friends",
            likes_pets=False,
            likes_outdoor_activities=True,
            enjoys_watching_movies=False,
            topmatch = [],
            match = [],
            social_current = []
        ),
         User(
            name="Winston Liang",
            age=18,
            gender="M",
            pronouns="He/him",
            ethnicity="Asian",
            interests=["Doing math"],
            mbti="ISFP",
            communication_type="Texting",
            political_interests="Conservative",
            religion="Protestant",
            major="Computer Science",
            year="1",
            language="Cantonese",
            dating_goal="Meeting new friends",
            likes_pets=True,
            likes_outdoor_activities=False,
            enjoys_watching_movies=False,
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
    
    user_list.append(user)
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
    


    


# def generate_json(users: list[dict]) -> None:
#     # Set output directory of the generated JSON file
#     output_dir = os.path.dirname(os.path.abspath(__file__))
#     filename = "new_data.json"
#     output_path = os.path.join(output_dir, filename)

#     # Save list of users to JSON file
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(users, f, indent=4)

#     print(f"Dataset saved as {output_path}")


def plot_user_connections(users: list[User], search_name: str = None, positions = None) -> go.Figure:
    G = nx.Graph()

    # Add all users as nodes
    for user in users:
        G.add_node(user.name, size = max(1, user.social_degree))  # Minimum size of 1 even if the user has no connections
    
    # Add all edges based on social_current connections
    for user in users:
        for friend in user.social_current:
            G.add_edge(user.name, friend.name)

    # Get positions for the nodes in the graph or use provided positions
    if positions is None:
        pos = nx.spring_layout(G, k = 0.3, seed = 1234)  # Fixed seed for consistent layout
    else:
        pos = positions
    
    # Create edge traces
    edge_x = []
    edge_y = []
    
    # Create lists for highlighted edges if searching
    highlight_edge_x = []
    highlight_edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        # If we're searching and this edge connects to the search node
        if search_name and (edge[0] == search_name or edge[1] == search_name):
            highlight_edge_x.extend([x0, x1, None])
            highlight_edge_y.extend([y0, y1, None])
        else:
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    # Create node traces
    node_x = []
    node_y = []
    node_size = []
    node_text = []
    hover_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_size.append(G.nodes[node]["size"] * 3 + 5)
        node_text.append(node if G.nodes[node]["size"] > 5 else "")
        hover_text.append(node)
        
        # Set node color based on search
        if search_name:
            if node == search_name:
                node_color.append("red")
            elif search_name in G and node in G.neighbors(search_name):
                node_color.append("blue")
            else:
                node_color.append("gray")
        else:
            node_color.append("gray")

    # Create the basic edge trace
    edge_trace = go.Scatter(
        x = edge_x, y = edge_y,
        line = dict(width = 0.5, color = "#888"),
        hoverinfo = "none",
        mode = "lines")
    
    # Create node trace
    node_trace = go.Scatter(
        x = node_x, y = node_y,
        mode = "markers+text",
        text = node_text,
        textposition = "top center",
        textfont = dict(size = 15),
        hoverinfo = "text",
        hovertext = hover_text,
        marker = dict(
            showscale = False,
            color = node_color,
            size = node_size,
            line_width = 2))
    
    # Create the figure with the basic edge trace and node trace
    fig = go.Figure(data = [edge_trace, node_trace],
                   layout = go.Layout(
                       title = "User Connections",
                       titlefont_size = 16,
                       showlegend = False,
                       hovermode = "closest",
                       margin = dict(b = 20, l = 5, r = 5, t = 40),
                       height = 1300,
                       xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
                       yaxis = dict(showgrid = False, zeroline = False, showticklabels = False))
                   )
    
    # Add highlighted edges if searching
    if search_name and highlight_edge_x:
        highlight_edge_trace = go.Scatter(
            x = highlight_edge_x, y = highlight_edge_y,
            line = dict(width = 2, color = "red"),
            hoverinfo = "none",
            mode = "lines")
        fig.add_trace(highlight_edge_trace)
        
        # Zoom to show searched user and connections
        if search_name in G.nodes:
            relevant_positions = [pos[search_name]]
            for neighbor in G.neighbors(search_name):
                relevant_positions.append(pos[neighbor])
            
            x_coords = [p[0] for p in relevant_positions]
            y_coords = [p[1] for p in relevant_positions]
            
            if x_coords and y_coords:
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                
                padding = 0.1
                x_range = [x_min - padding, x_max + padding]
                y_range = [y_min - padding, y_max + padding]
                
                fig.update_layout(
                    xaxis = dict(range = x_range, showgrid = False, zeroline = False, showticklabels = False),
                    yaxis = dict(range = y_range, showgrid = False, zeroline = False, showticklabels = False)
                )
    
    return fig, pos

app = Dash(__name__)

# Generate the initial graph and node positions
initial_user_list = generate_users_with_class(1234)
add_fixed_users(initial_user_list)
initial_fig, node_positions = plot_user_connections(initial_user_list)

app.layout = html.Div([
    dcc.Input(id = "search-input", type = "text", placeholder = "Enter user name"),
    html.Button("Search", id = "search-button"),
    html.Button("Reset", id = "reset-button"),
    dcc.Graph(id = "user-graph", figure = initial_fig)
])

@app.callback(
    Output("user-graph", "figure"),
    [Input("search-button", "n_clicks"), Input("reset-button", "n_clicks")],
    State("search-input", "value")
)
def update_graph(search_clicks, reset_clicks, search_name):
    ctx = callback_context

    if not ctx.triggered:
        return initial_fig

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "reset-button":
        # Reset by creating a new figure with the initial node positions
        reset_fig, _ = plot_user_connections(initial_user_list, positions = node_positions)
        return reset_fig

    if button_id == "search-button" and search_name:
        # Create a new figure with the search highlighting
        search_fig, _ = plot_user_connections(initial_user_list, search_name, node_positions)
        return search_fig

    return initial_fig

if __name__ == "__main__":
    app.run_server(debug=True)