"""
The program handling the GUI for the dating app.
Generative AI was used for generating sample templates of implementing visual elements across the GUI.
We modified the generated templates to complete this program.
"""
import tkinter as tk
import sys
import threading
import time
import socket
import webbrowser
import traceback
from typing import Union

from PIL import Image, ImageTk
from dash import Dash
import python_ta

from user_network import User, Characteristics, generate_users_with_class, add_fixed_users
import user_network
import tree
import common
import graph


class DestinyApp:
    """
    A dating app interface that allows users to create profiles and visualize social networks.

    Instance Attributes:
        - root: The tkinter root window for the application interface
        - window_width: The width of the application window in pixels
        - window_height: The height of the application window in pixels
        - image_path: The file path to the app's logo/splash screen image
        - username: The name of the current user being processed (str)
        - username_entry: The tkinter Entry widget for inputting username
        - attributes: A dictionary mapping attribute names to their tkinter variable objects
                    (StringVar, BooleanVar, etc.) for user profile creation
        - status_label: A tkinter Label widget for displaying status messages
        - result_label: A tkinter Label widget for showing input validation results
        - user_list: A list of User objects representing all users in the network
        - current_user: The User object representing the currently logged-in user
        - priority_attributes: A list of attribute names in order of user's priority ranking
        - recommendations_dict: A dictionary mapping attribute names to lists of recommended users
        - recommendations: A list of User objects representing recommended matches for the current user
        - match_frame: A tkinter Frame widget for displaying match results
        - matches_made: An integer counter for the number of matches made
        - counter_label: A tkinter Label widget for displaying the number of matches made
        - background_color: The background color of the application window
        - users_label: A tkinter Label widget for displaying the number of users in the network

    Representation Invariants:
        - self.window_width > 0
        - self.window_height > 0
        - len(self.image_path) > 0

        # Conditional checks are used below because these attributes are not initialized in __init__

        - if hasattr(self, 'username'): len(self.username) > 0
        - if hasattr(self, 'user_list'):
            - all(isinstance(user, User) for user in self.user_list)
        - if hasattr(self, 'current_user'):
            - self.current_user in self.user_list
    """
    root: tk.Tk
    window_width: int
    window_height: int
    image_path: str
    username: str
    username_entry: tk.Entry
    attributes: dict[str, Union[tk.StringVar, tk.BooleanVar, dict[str, tk.BooleanVar]]]
    status_label: tk.Label
    result_label: tk.Label
    user_list: list[User]
    user_list_friends: list[User]
    user_list_love: list[User]
    current_user: User
    priority_attributes: list[str]
    recommendations_dict: dict[str, list[User]]
    recommendations: list[User]
    match_frame: tk.Frame
    matches_made: int
    counter_label: tk.Label
    background_color: str = "#7A8B9C"
    users_label: tk.Label

    def __init__(self, image_path: str, window_width: int = 720, window_height: int = 720) -> None:
        self.root = tk.Tk()
        self.root.title("Destiny App")
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg=self.background_color)

        self.window_width = window_width
        self.window_height = window_height

        self.image_path = image_path
        self.create_welcome_page(image_path)

        self.priority_attributes = []
        self.recommendations_dict = {}
        self.recommendations = []

        # Generate users locally
        self.user_list = generate_users_with_class(2000, 1234)

        add_fixed_users(self.user_list)

        self.user_list_friends, self.user_list_love = user_network.simulate_connections(self.user_list)

        add_fixed_users(self.user_list_friends)
        add_fixed_users(self.user_list_love)

    def create_welcome_page(self, image_path: str) -> None:
        """
        Create the initial welcome page with image and username input.
        """
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.background_color)

        # Create two frames, one for the image (top half) and one for username input (bottom half)
        top_frame = tk.Frame(self.root, width=self.window_width, height=self.window_height // 2,
                             bg=self.background_color)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH)
        top_frame.pack_propagate(False)  # Prevent frame from shrinking

        bottom_frame = tk.Frame(self.root, width=self.window_width, height=self.window_height // 2,
                                bg=self.background_color)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Load and display the image in the top half
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size

            horizontal_padding = 40
            vertical_padding = 60
            display_width = self.window_width - horizontal_padding
            display_height = (self.window_height // 2) - vertical_padding

            width_ratio = display_width / img_width
            height_ratio = display_height / img_height
            scale_factor = min(width_ratio, height_ratio)

            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            img = img.resize((new_width, new_height))

            photo = ImageTk.PhotoImage(img)

            image_label = tk.Label(top_frame, image=photo, bg=self.background_color)
            image_label.image = photo

            image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        except Exception as e:
            error_label = tk.Label(top_frame, text=f"Error loading image: {e}", fg="white", bg=self.background_color,
                                   padx=20,
                                   pady=20, font=("Arial", 16))
            error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the bottom half for username input
        heading = tk.Label(bottom_frame, text="Welcome to Destiny",
                           font=("Arial", 36, "bold"), fg="white", bg=self.background_color)
        heading.pack(pady=(50, 20))

        description = tk.Label(bottom_frame, text="Please enter your name to continue", font=("Arial", 18), fg="white",
                               bg=self.background_color)
        description.pack(pady=(0, 40))

        input_frame = tk.Frame(bottom_frame, bg=self.background_color)
        input_frame.pack(pady=20, padx=(0, 62.5))

        username_label = tk.Label(input_frame, text="Name:", font=("Arial", 16), fg="white", bg=self.background_color)
        username_label.pack(side=tk.LEFT, padx=(0, 10))

        self.username_entry = tk.Entry(input_frame, font=("Arial", 16), width=20)
        self.username_entry.pack(side=tk.LEFT)
        self.username_entry.focus_set()

        submit_button = tk.Button(bottom_frame, text="Continue", font=("Arial", 16), bg="#4CAF50", fg="black", padx=20,
                                  pady=10, command=self.handle_username_submit)
        submit_button.pack(pady=20)

        self.result_label = tk.Label(bottom_frame, text="", font=("Arial", 14), fg="white", bg=self.background_color)
        self.result_label.pack(pady=10)

        self.root.bind('<Return>', lambda event: self.handle_username_submit())

    def handle_username_submit(self) -> None:
        """
        Handle the username submission and transition to appropriate page.
        """
        username = self.username_entry.get().strip()
        if not username:
            self.result_label.config(text="Please enter your name")
            return

        self.username = username

        if username.lower() == "admin":
            self.create_admin_page() 
        else:
            self.create_attributes_page()

    def create_admin_page(self) -> None:
        """
        Create the admin page with direct access to the network graph.
        """
        self.root.unbind_all("<MouseWheel>")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.background_color) 

        # Create main frame
        frame = tk.Frame(self.root, bg=self.background_color)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Description
        admin_label = tk.Label(frame, text="ADMIN MODE",
                               font=("Arial", 36, "bold"), fg="white", bg=self.background_color)
        admin_label.pack(pady=20)

        self.users_label = tk.Label(frame, text=f"The user network has {len(self.user_list)} users", font=("Arial", 24),
                                    fg="white", bg=self.background_color)
        self.users_label.pack(pady=20)

        description = tk.Label(frame, text="You have direct access to the network visualization",
                               font=("Arial", 18), fg="white", bg=self.background_color)
        description.pack(pady=(20, 40))

        # Buttons
        graph_button = tk.Button(frame, text="View Network Graph", font=("Arial", 16, "bold"),
                                 bg="#3498DB", fg="black", padx=30, pady=15,
                                 command=self.view_network_graph)
        graph_button.pack(pady=20)

        print_button = tk.Button(frame, text="Print User List to Console", font=("Arial", 16),
                                 bg="#2ECC71", fg="black", padx=20, pady=10,
                                 command=self.print_user_list_debug)
        print_button.pack(pady=20)

        logout_button = tk.Button(frame, text="Logout", font=("Arial", 16),
                                  bg="#E74C3C", fg="black", padx=20, pady=10,
                                  command=lambda: self.create_welcome_page(self.image_path))
        logout_button.pack(pady=20)

    def update_user_count_display(self) -> None:
        """
        Update the displayed user count on the admin page.
        """
        if hasattr(self, "users_label"):
            self.users_label.config(text=f"The user network has {len(self.user_list)} users")

    def configure_dropdown(self, dropdown: tk.OptionMenu, width: int = 29) -> None:
        """
        Apply simple consistent styling to a dropdown menu.
        """
        # Set the background of the dropdown button part
        dropdown.config(
            font=("Arial", 14),
            width=width,
            bg=self.background_color,
            fg="black",
            highlightbackground="black",
            activebackground="black",
            activeforeground="black"
        )

        # Configure the dropdown menu part
        dropdown["menu"].config(
            bg="black",
            fg="black",
            activebackground="black",
            activeforeground="white",
            font=("Arial", 14)
        )

    def create_attributes_page(self) -> None:
        """
        Create the page with input fields for all user attributes.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.background_color)

        main_frame = tk.Frame(self.root, bg=self.background_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg=self.background_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.background_color)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Define mousewheel event handlers
        def _bound_to_mousewheel(event: tk.Event) -> None:
            if sys.platform == 'darwin':  # macOS
                canvas.bind_all("<MouseWheel>", _on_scrollwheel)
            else:  # Windows and others
                canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event: tk.Event) -> None:
            # Unbind scrolling when mouse leaves the canvas
            if sys.platform == 'darwin':  # macOS
                canvas.unbind_all("<MouseWheel>")
            else:  # Windows and others
                canvas.unbind_all("<MouseWheel>")

        # Enable mousewheel/trackpad scrolling
        def _on_mousewheel(event: tk.Event) -> None:
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except (tk.TclError, RuntimeError):
                # Widget no longer exists, unbind the event
                if sys.platform == 'darwin':  # macOS
                    self.root.unbind_all("<MouseWheel>")
                else:  # Windows and others
                    self.root.unbind_all("<MouseWheel>")

        def _on_scrollwheel(event: tk.Event) -> None:
            # For macOS with trackpad
            try:
                canvas.yview_scroll(-1 * int(event.delta), "units")
            except (tk.TclError, RuntimeError):
                # Widget no longer exists, unbind the event
                self.root.unbind_all("<MouseWheel>")

        # Bind events to the canvas
        canvas.bind('<Enter>', _bound_to_mousewheel)
        canvas.bind('<Leave>', _unbound_to_mousewheel)

        # Add heading
        heading = tk.Label(scroll_frame, text=f"Create Profile for {self.username}",
                           font=("Arial", 24, "bold"), fg="white", bg=self.background_color)
        heading.pack(pady=(20, 30))

        self.attributes = {}

        # Age input
        age_frame = tk.Frame(scroll_frame, bg=self.background_color)
        age_frame.pack(fill="x", padx=20, pady=10)

        age_label = tk.Label(age_frame, text="Age:", width=20, anchor="e",
                             font=("Arial", 14), fg="white", bg=self.background_color)
        age_label.pack(side="left", padx=(0, 10))

        age_var = tk.StringVar()
        age_entry = tk.Entry(age_frame, textvariable=age_var, font=("Arial", 14), width=30)
        age_entry.pack(side="left")
        self.attributes["age"] = age_var

        # Gender dropdown
        gender_frame = tk.Frame(scroll_frame, bg=self.background_color)
        gender_frame.pack(fill="x", padx=20, pady=10)

        gender_label = tk.Label(gender_frame, text="Gender:", width=20, anchor="e",
                                font=("Arial", 14), fg="white", bg=self.background_color)
        gender_label.pack(side="left", padx=(0, 10))

        gender_var = tk.StringVar()
        gender_options = ["M", "F"]
        gender_dropdown = tk.OptionMenu(gender_frame, gender_var, *gender_options)
        self.configure_dropdown(gender_dropdown)
        gender_dropdown.pack(side="left")
        self.attributes["gender"] = gender_var

        # Pronouns input
        pronouns_frame = tk.Frame(scroll_frame, bg=self.background_color)
        pronouns_frame.pack(fill="x", padx=20, pady=10)

        pronouns_label = tk.Label(pronouns_frame, text="Pronouns:", width=20, anchor="e",
                                  font=("Arial", 14), fg="white", bg=self.background_color)
        pronouns_label.pack(side="left", padx=(0, 10))

        pronouns_var = tk.StringVar()
        pronouns_entry = tk.Entry(pronouns_frame, textvariable=pronouns_var, font=("Arial", 14), width=30)
        pronouns_entry.pack(side="left")
        self.attributes["pronouns"] = pronouns_var

        # Ethnicity dropdown
        ethnicity_frame = tk.Frame(scroll_frame, bg=self.background_color)
        ethnicity_frame.pack(fill="x", padx=20, pady=10)

        ethnicity_label = tk.Label(ethnicity_frame, text="Ethnicity:", width=20, anchor="e",
                                   font=("Arial", 14), fg="white", bg=self.background_color)
        ethnicity_label.pack(side="left", padx=(0, 10))

        ethnicity_var = tk.StringVar()
        ethnicity_options = ["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]
        ethnicity_dropdown = tk.OptionMenu(ethnicity_frame, ethnicity_var, *ethnicity_options)
        self.configure_dropdown(ethnicity_dropdown)
        ethnicity_dropdown.pack(side="left")
        self.attributes["ethnicity"] = ethnicity_var

        # Interests multi-select
        interests_frame = tk.Frame(scroll_frame, bg=self.background_color)
        interests_frame.pack(fill="x", padx=20, pady=10)

        interests_label = tk.Label(interests_frame, text="Interests:", width=20, anchor="e",
                                   font=("Arial", 14), fg="white", bg=self.background_color)
        interests_label.pack(side="left", anchor="n", padx=(0, 10))

        interests_options_frame = tk.Frame(interests_frame, bg=self.background_color)
        interests_options_frame.pack(side="left", fill="x")

        interests_options = ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding", "Doing math"]
        interests_vars = {user_interest: tk.BooleanVar() for user_interest in interests_options}

        for i, interest in enumerate(interests_options):
            cb = tk.Checkbutton(interests_options_frame, text=interest, variable=interests_vars[interest],
                                font=("Arial", 14), fg="white", bg=self.background_color, selectcolor="#7A8B9C",
                                activebackground="#7A8B9C", activeforeground="white")
            cb.pack(anchor="w")

        self.attributes["interests"] = interests_vars

        # MBTI input
        mbti_frame = tk.Frame(scroll_frame, bg=self.background_color)
        mbti_frame.pack(fill="x", padx=20, pady=10)

        mbti_label = tk.Label(mbti_frame, text="MBTI:", width=20, anchor="e",
                              font=("Arial", 14), fg="white", bg=self.background_color)
        mbti_label.pack(side="left", padx=(0, 10))

        mbti_var = tk.StringVar()
        mbti_entry = tk.Entry(mbti_frame, textvariable=mbti_var, font=("Arial", 14), width=30)
        mbti_entry.pack(side="left")
        self.attributes["mbti"] = mbti_var

        # Communication Type
        comm_frame = tk.Frame(scroll_frame, bg=self.background_color)
        comm_frame.pack(fill="x", padx=20, pady=10)

        comm_label = tk.Label(comm_frame, text="Communication Type:", width=20, anchor="e",
                              font=("Arial", 14), fg="white", bg=self.background_color)
        comm_label.pack(side="left", padx=(0, 10))

        comm_var = tk.StringVar()
        comm_options = ["Texting", "Phonecall"]
        comm_dropdown = tk.OptionMenu(comm_frame, comm_var, *comm_options)
        self.configure_dropdown(comm_dropdown)
        comm_dropdown.pack(side="left")
        self.attributes["communication_type"] = comm_var

        # Political Interests
        politics_frame = tk.Frame(scroll_frame, bg=self.background_color)
        politics_frame.pack(fill="x", padx=20, pady=10)

        politics_label = tk.Label(politics_frame, text="Political Interests:", width=20, anchor="e",
                                  font=("Arial", 14), fg="white", bg=self.background_color)
        politics_label.pack(side="left", padx=(0, 10))

        politics_var = tk.StringVar()
        politics_options = ["Liberal", "Conservative"]
        politics_dropdown = tk.OptionMenu(politics_frame, politics_var, *politics_options)
        self.configure_dropdown(politics_dropdown)
        politics_dropdown.pack(side="left")
        self.attributes["political_interests"] = politics_var

        # Religion
        religion_frame = tk.Frame(scroll_frame, bg=self.background_color)
        religion_frame.pack(fill="x", padx=20, pady=10)

        religion_label = tk.Label(religion_frame, text="Religion:", width=20, anchor="e",
                                  font=("Arial", 14), fg="white", bg=self.background_color)
        religion_label.pack(side="left", padx=(0, 10))

        religion_var = tk.StringVar()
        religion_options = ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism",
                            "Taoism", "Jewish", "Agnostic", "Other"]
        religion_dropdown = tk.OptionMenu(religion_frame, religion_var, *religion_options)
        self.configure_dropdown(religion_dropdown)
        religion_dropdown.pack(side="left")
        self.attributes["religion"] = religion_var

        # Major
        major_frame = tk.Frame(scroll_frame, bg=self.background_color)
        major_frame.pack(fill="x", padx=20, pady=10)

        major_label = tk.Label(major_frame, text="Major:", width=20, anchor="e",
                               font=("Arial", 14), fg="white", bg=self.background_color)
        major_label.pack(side="left", padx=(0, 10))

        major_var = tk.StringVar()
        major_options = ["Computer Science", "Accounting", "Actuarial Science", "Psychology",
                         "Biochemistry", "Mathematics", "Statistics", "Economics", "Literature",
                         "History", "Political Science", "Music", "Physics", "Chemistry",
                         "Cognitive Science", "Philosophy", "Others"]
        major_dropdown = tk.OptionMenu(major_frame, major_var, *major_options)
        self.configure_dropdown(major_dropdown)
        major_dropdown.pack(side="left")
        self.attributes["major"] = major_var

        # Year
        year_frame = tk.Frame(scroll_frame, bg=self.background_color)
        year_frame.pack(fill="x", padx=20, pady=10)

        year_label = tk.Label(year_frame, text="Year:", width=20, anchor="e",
                              font=("Arial", 14), fg="white", bg=self.background_color)
        year_label.pack(side="left", padx=(0, 10))

        year_var = tk.StringVar()
        year_options = ["1", "2", "3", "4", "5", "Master"]
        year_dropdown = tk.OptionMenu(year_frame, year_var, *year_options)
        self.configure_dropdown(year_dropdown)
        year_dropdown.pack(side="left")
        self.attributes["year"] = year_var

        # Language
        language_frame = tk.Frame(scroll_frame, bg=self.background_color)
        language_frame.pack(fill="x", padx=20, pady=10)

        language_label = tk.Label(language_frame, text="Language:", width=20, anchor="e",
                                  font=("Arial", 14), fg="white", bg=self.background_color)
        language_label.pack(side="left", padx=(0, 10))

        language_var = tk.StringVar()
        language_options = ["English", "Cantonese", "Mandarin", "French", "Spanish", "Japanese", "Korean", "Others"]
        language_dropdown = tk.OptionMenu(language_frame, language_var, *language_options)
        self.configure_dropdown(language_dropdown)
        language_dropdown.pack(side="left")
        self.attributes["language"] = language_var

        # Dating Goal
        goal_frame = tk.Frame(scroll_frame, bg=self.background_color)
        goal_frame.pack(fill="x", padx=20, pady=10)

        goal_label = tk.Label(goal_frame, text="Dating Goal:", width=20, anchor="e",
                              font=("Arial", 14), fg="white", bg=self.background_color)
        goal_label.pack(side="left", padx=(0, 10))

        goal_var = tk.StringVar()
        goal_options = ["Meeting new friends", "Short-term relationship", "Long-term relationship", "Situationship"]
        goal_dropdown = tk.OptionMenu(goal_frame, goal_var, *goal_options)
        self.configure_dropdown(goal_dropdown)
        goal_dropdown.pack(side="left")
        self.attributes["dating_goal"] = goal_var

        # Boolean attributes
        for bool_attr, text in [
            ("likes_pets", "Likes Pets"),
            ("likes_outdoor_activities", "Likes Outdoor Activities"),
            ("enjoys_watching_movies", "Enjoys Watching Movies")
        ]:
            bool_frame = tk.Frame(scroll_frame, bg=self.background_color)
            bool_frame.pack(fill="x", padx=20, pady=10)

            bool_label = tk.Label(bool_frame, text=f"{text}:", width=20, anchor="e",
                                  font=("Arial", 14), fg="white", bg=self.background_color)
            bool_label.pack(side="left", padx=(0, 10))

            bool_var = tk.BooleanVar()
            bool_true = tk.Radiobutton(bool_frame, text="True", variable=bool_var, value=True,
                                       font=("Arial", 14), fg="white", bg=self.background_color,
                                       selectcolor="#5A6B7C", activebackground="#7A8B9C",
                                       activeforeground="white")
            bool_true.pack(side="left", padx=(0, 20))

            bool_false = tk.Radiobutton(bool_frame, text="False", variable=bool_var, value=False,
                                        font=("Arial", 14), fg="white", bg=self.background_color,
                                        selectcolor="#5A6B7C", activebackground="#7A8B9C",
                                        activeforeground="white")
            bool_false.pack(side="left")

            self.attributes[bool_attr] = bool_var

        # Attribute priority ranking section
        priority_heading = tk.Label(scroll_frame, text="Rank Attribute Importance",
                                    font=("Arial", 18, "bold"), fg="white", bg=self.background_color)
        priority_heading.pack(pady=(30, 10))

        priority_description = tk.Label(scroll_frame,
                                        text="Select attributes and use the buttons to rank them by importance "
                                             "(top = most important)",
                                        font=("Arial", 14), fg="white", bg=self.background_color)
        priority_description.pack(pady=(0, 20))

        # Attribute priority frame
        priority_frame = tk.Frame(scroll_frame, bg=self.background_color)
        priority_frame.pack(fill="x", padx=20, pady=10)

        attribute_list = ["Ethnicity", "Interests", "MBTI", "Communication Type", "Political Interests",
                          "Religion", "Major", "Year", "Language", "Likes Pets",
                          "Likes Outdoor Activities", "Enjoys Watching Movies"]

        priority_listbox = tk.Listbox(priority_frame,
                                      font=("Arial", 14),
                                      bg="#5A6B7C",
                                      fg="white",
                                      selectbackground="#3A4B5C",
                                      selectforeground="white",
                                      height=len(attribute_list),
                                      width=40)

        for attr in attribute_list:
            priority_listbox.insert(tk.END, attr)

        priority_listbox.pack(side="left", padx=(50, 0))

        # Add up/down buttons
        button_frame = tk.Frame(priority_frame, bg=self.background_color)
        button_frame.pack(side="left", padx=10)

        def move_up() -> None:
            """
            Move the selected item up in the listbox.
            """
            selected_idx = priority_listbox.curselection()
            if not selected_idx or selected_idx[0] == 0:
                return

            idx = selected_idx[0]
            text = priority_listbox.get(idx)
            priority_listbox.delete(idx)
            priority_listbox.insert(idx - 1, text)
            priority_listbox.selection_set(idx - 1)
            priority_listbox.activate(idx - 1)

        def move_down() -> None:
            """
            Move the selected item down in the listbox.
            """
            selected_idx = priority_listbox.curselection()
            if not selected_idx or selected_idx[0] == priority_listbox.size() - 1:
                return

            idx = selected_idx[0]
            text = priority_listbox.get(idx)
            priority_listbox.delete(idx)
            priority_listbox.insert(idx + 1, text)
            priority_listbox.selection_set(idx + 1)
            priority_listbox.activate(idx + 1)

        up_button = tk.Button(button_frame, text="↑", font=("Arial", 18, "bold"),
                              bg="#E74C3C", fg="black", width=3, command=move_up,
                              activebackground="#C0392B", activeforeground="white")
        up_button.pack(pady=(0, 10))

        down_button = tk.Button(button_frame, text="↓", font=("Arial", 18, "bold"),
                                bg="#E74C3C", fg="black", width=3, command=move_down,
                                activebackground="#C0392B", activeforeground="white")
        down_button.pack()

        for i in range(priority_listbox.size()):
            self.priority_attributes.append(priority_listbox.get(i))

        # Map UI attribute names to internal attribute keys
        priority_mapping = {
            "MBTI": "mbti",
            "Ethnicity": "ethnicity",
            "Communication Type": "communication_type",
            "Interests": "interests",
            "Political Interests": "political_interests",
            "Religion": "religion",
            "Major": "major",
            "Year": "year",
            "Language": "language",
            "Likes Pets": "likes_pets",
            "Likes Outdoor Activities": "likes_outdoor_activities",
            "Enjoys Watching Movies": "enjoys_watching_movies"
        }

        self.priority_attributes = [priority_mapping.get(attribute, attribute.lower())
                                    for attribute in self.priority_attributes]

        spacer = tk.Label(scroll_frame, text="", bg=self.background_color)
        spacer.pack(pady=20)

        self.status_label = tk.Label(scroll_frame, text="", font=("Arial", 14, "bold"),
                                     fg="#E74C3C", bg=self.background_color)
        self.status_label.pack(pady=10)

        submit_button = tk.Button(scroll_frame, text="Create Profile", font=("Arial", 18, "bold"),
                                  bg="#2ECC71", fg="black", padx=30, pady=15,
                                  command=self.submit_user_profile)
        submit_button.pack(pady=(20, 40))

        bottom_spacer = tk.Label(scroll_frame, text="", bg=self.background_color)
        bottom_spacer.pack(pady=50)

    def submit_user_profile(self) -> None:
        """
        Collect all the input values and create a new user.
        """
        try:
            name = self.username 

            # Validate and process age
            try:
                age = int(self.attributes["age"].get())
                if not 18 <= age <= 30:
                    self.status_label.config(text="Age must be between 18 and 30")
                    return
            except ValueError:
                self.status_label.config(text="Please enter a valid age")
                return

            # Get other attributes
            gender = self.attributes["gender"].get()
            if not gender:
                self.status_label.config(text="Please select a gender")
                return

            pronouns = self.attributes["pronouns"].get()

            # Get ethnicity
            ethnicity = self.attributes["ethnicity"].get()
            if not ethnicity:
                self.status_label.config(text="Please select an ethnicity")
                return

            # Get selected interests
            interests = [interest for interest, var in self.attributes["interests"].items() if var.get()]
            if not interests:
                self.status_label.config(text="Please select at least one interest")
                return

            # Get MBTI
            mbti = self.attributes["mbti"].get().upper()
            if not (len(mbti) == 4 and all(char in "IESNTFPJ" for char in mbti)):
                self.status_label.config(text="Please enter a valid MBTI (e.g., INFP)")
                return

            # Get other dropdown values
            communication_type = self.attributes["communication_type"].get()
            political_interests = self.attributes["political_interests"].get()
            religion = self.attributes["religion"].get()
            major = self.attributes["major"].get()
            year = self.attributes["year"].get()
            language = self.attributes["language"].get()
            dating_goal = self.attributes["dating_goal"].get()

            # Get boolean values
            likes_pets = self.attributes["likes_pets"].get()
            likes_outdoor_activities = self.attributes["likes_outdoor_activities"].get()
            enjoys_watching_movies = self.attributes["enjoys_watching_movies"].get()

            # Create the user object
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
                interested_friend=[],
                social_current=[],
                interested_romantic=[],
                romantic_current=None
            )

            self.user_list.append(user)

            if user.dating_goal == "Meeting new friends":
                if user not in self.user_list_friends:
                    self.user_list_friends.append(user)
            else:
                if user not in self.user_list_love:
                    self.user_list_love.append(user)

            # Display success message
            self.status_label.config(text=f"Profile created successfully for {name}!", fg="white")

            self.current_user = user
            self.root.after(200, self.show_success_page)

        except Exception as e:
            traceback.print_exc()
            self.status_label.config(text=f"Error: {str(e)}")

    def show_success_page(self) -> None:
        """
        Show a success page after profile creation.
        """
        self.root.unbind_all("<MouseWheel>")

        for widget in self.root.winfo_children():
            widget.destroy()

        # Success message
        frame = tk.Frame(self.root, bg=self.background_color)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        success_label = tk.Label(frame, text="Profile Created Successfully!",
                                 font=("Arial", 24, "bold"), fg="white", bg=self.background_color)
        success_label.pack(pady=20)

        name_label = tk.Label(frame, text=f"Welcome, {self.username}!",
                              font=("Arial", 18), fg="white", bg=self.background_color)
        name_label.pack(pady=10)

        message = tk.Label(frame, text="Your profile has been created and added to the system.",
                           font=("Arial", 14), fg="white", bg=self.background_color)
        message.pack(pady=10)

        continue_button = tk.Button(frame, text="Find Matches", font=("Arial", 16),
                                    bg="#4CAF50", fg="black", padx=20, pady=10,
                                    command=self.show_matching_page)
        continue_button.pack(pady=30)

    def show_matching_page(self) -> None:
        """
        Show a page where users can swipe through recommended matches and connect with them.
        """
        self.root.unbind_all("<MouseWheel>")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.background_color)

        # Get the dating goal of the current user
        dating_goal = self.current_user.dating_goal
        connection_type = "friendship" if dating_goal == "Meeting new friends" else "romantic"

        main_frame = tk.Frame(self.root, bg=self.background_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(main_frame, text="Find Your Matches",
                          font=("Arial", 28, "bold"), fg="white", bg=self.background_color)
        header.pack(pady=(30, 10))

        # Description
        if connection_type == "friendship":
            desc = "Find new friends based on your preferences"
        else:
            desc = "Find a romantic partner based on your preferences"

        description = tk.Label(main_frame, text=desc,
                               font=("Arial", 16), fg="white", bg=self.background_color)
        description.pack(pady=(0, 20))

        common.data_wrangling(current_user=self.current_user, user_characteristics=self.priority_attributes,
                              users_list=self.user_list)
        preference_tree = common.build_preference_tree("data.csv")
        recommendation_names = preference_tree.run_preference_tree()

        user_keypair = {user_object.name: user_object for user_object in self.user_list}

        # Filter out users who already have romantic partners if looking for romance
        for name in recommendation_names:
            if name in user_keypair:
                user = user_keypair[name]
                self.recommendations.append(user)

        if not self.recommendations:
            # No recommendations
            no_matches = tk.Label(main_frame, text="No potential matches found!",
                                  font=("Arial", 20), fg="#E74C3C", bg=self.background_color)
            no_matches.pack(pady=40)

            back_button = tk.Button(main_frame, text="Return to Home", font=("Arial", 16),
                                    bg="#3498DB", fg="black", padx=20, pady=10,
                                    command=lambda: self.create_welcome_page(self.image_path))
            back_button.pack(pady=30)
            return

        # Create a frame for the current recommendation
        self.match_frame = tk.Frame(main_frame, bg="#5A6B7C", padx=40, pady=40,
                                    highlightbackground="#3A4B5C", highlightthickness=2)
        self.match_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=80)

        self.matches_made = 0

        self.display_current_recommendation()

        button_frame = tk.Frame(main_frame, bg=self.background_color)
        button_frame.pack(pady=30)

        pass_button = tk.Button(button_frame, text="Pass", font=("Arial", 16),
                                bg="#E74C3C", fg="black", padx=30, pady=15,
                                command=self.pass_current_recommendation)
        pass_button.pack(side=tk.LEFT, padx=15)

        match_button = tk.Button(button_frame, text="Match!", font=("Arial", 16, "bold"),
                                 bg="#2ECC71", fg="black", padx=30, pady=15,
                                 command=self.match_current_recommendation)
        match_button.pack(side=tk.LEFT, padx=15)

        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 16),
                                bg="#95A5A6", fg="black", padx=30, pady=15,
                                command=lambda: self.create_welcome_page(self.image_path))
        exit_button.pack(side=tk.LEFT, padx=15)

        counter_text = f"Showing match 1 of {len(self.recommendations)}"
        self.counter_label = tk.Label(main_frame, text=counter_text,
                                      font=("Arial", 14), fg="white", bg=self.background_color)
        self.counter_label.pack(pady=(20, 0))

    def display_current_recommendation(self) -> None:
        """
        Display the current recommendation in the match frame.
        """
        for widget in self.match_frame.winfo_children():
            widget.destroy()

        # Get the current recommendation
        if not self.recommendations:
            no_more = tk.Label(self.match_frame, text="No more matches!",
                               font=("Arial", 20), fg="white", bg="#5A6B7C")
            no_more.pack(pady=40)
            return

        user = self.recommendations[0]  # Always show the first user in the list

        # Create the profile display
        name = tk.Label(self.match_frame, text=user.name,
                        font=("Arial", 24, "bold"), fg="white", bg="#5A6B7C")
        name.pack(pady=(0, 20))

        basic_info = tk.Label(self.match_frame,
                              text=f"{user.age} • {user.gender} • {user.characteristics.mbti}",
                              font=("Arial", 16), fg="white", bg="#5A6B7C")
        basic_info.pack(pady=(0, 15))

        major_year = tk.Label(self.match_frame,
                              text=f"{user.characteristics.major}, Year {user.characteristics.year}",
                              font=("Arial", 16), fg="white", bg="#5A6B7C")
        major_year.pack(pady=(0, 15))

        interests_label = tk.Label(self.match_frame, text="Interests:",
                                   font=("Arial", 16, "bold"), fg="white", bg="#5A6B7C")
        interests_label.pack(pady=(15, 5), anchor="w", padx=40)

        interests_text = ", ".join(user.characteristics.interests)
        interests = tk.Label(self.match_frame, text=interests_text,
                             font=("Arial", 14), fg="white", bg="#5A6B7C",
                             wraplength=400, justify="left")
        interests.pack(pady=(0, 15), anchor="w", padx=40)

        # Update the counter label
        try:
            if hasattr(self, 'counter_label') and self.counter_label.winfo_exists():
                counter_text = f"Showing match {self.recommendations.index(user) + 1} of {len(self.recommendations)}"
                self.counter_label.config(text=counter_text)
        except (tk.TclError, AttributeError):
            pass

    def pass_current_recommendation(self) -> None:
        """
        Skip the current recommendation and show the next one.
        """
        if self.recommendations:
            current_user = self.recommendations[0]
            current_name = current_user.name

            # Update recommendation status in dictionary
            if current_name in self.recommendations_dict:
                self.recommendations_dict[current_name]["status"] = "rejected"

            self.recommendations.pop(0)

            if not self.recommendations:
                self.show_matching_summary()
                return

            self.display_current_recommendation()

    def show_blocking_error(self, message: str) -> None:
        """
        Show a very visible blocking error message that can't be missed.
        """
        # Create overlay
        overlay = tk.Frame(self.root, bg="#000000")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create an error box
        error_frame = tk.Frame(overlay, bg="#E74C3C", padx=30, pady=30)
        error_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title = tk.Label(error_frame, text="CANNOT MATCH",
                         font=("Arial", 24, "bold"), fg="white", bg="#E74C3C")
        title.pack(pady=(0, 20))

        msg = tk.Label(error_frame, text=message,
                       font=("Arial", 18), fg="white", bg="#E74C3C",
                       wraplength=400)
        msg.pack()

        # OK button
        ok_button = tk.Button(error_frame, text="OK", font=("Arial", 16),
                              bg="white", fg="#E74C3C", padx=30, pady=10,
                              command=overlay.destroy)
        ok_button.pack(pady=(30, 0))

        # Auto-remove after 3 seconds
        self.root.after(3000, overlay.destroy)

    def match_current_recommendation(self) -> None:
        """
        Match with the current recommendation and show the next one.
        """
        if not self.recommendations:
            return

        candidate = self.recommendations[0]
        dating_goal = self.current_user.dating_goal

        candidate_updated = None
        for user in self.user_list:
            if user.name == candidate.name:
                candidate_updated = user
                break

        candidate = candidate_updated if candidate_updated else candidate

        if dating_goal != "Meeting new friends":
            # Check if candidate has a romantic partner
            has_partner, partner_name = self.check_if_user_has_partner(
                candidate, self.user_list, self.user_list_friends, self.user_list_love)

            if has_partner:
                error_text = f"{candidate.name} is already in a relationship with {partner_name}!"
                self.show_blocking_error(error_text)
                self.recommendations.pop(0)
                self.root.after(200, self.show_next)
                return

            else:
                self.match_with_user(candidate)
                success_text = f"You've matched with {candidate.name}!"
                self.show_temporary_message(success_text, "#E74C3C")
                self.matches_made += 1
                self.recommendations.pop(0)
                self.show_matching_summary()
        else:
            # Friend matching
            self.current_user.socialize(candidate)
            success_text = f"You've connected with {candidate.name}!"
            self.show_temporary_message(success_text, "#2ECC71")
            self.matches_made += 1
            self.recommendations.pop(0)
            if not self.recommendations:
                self.root.after(1500, self.show_matching_summary)
            else:
                self.root.after(200, self.display_current_recommendation)

    def check_if_user_has_partner(self, candidate: User, user_list: list[User],
                                  user_looking_for_friends: list[User],
                                  user_looking_for_love: list[User]) -> tuple[bool, str]:
        """
        Check if a user already has a romantic partner in any of the user lists.
        """
        has_partner = False
        partner_name = None

        # Check in all three lists
        for check_list in [user_list, user_looking_for_friends, user_looking_for_love]:
            for user in check_list:
                # Check if this user is our candidate and has a partner
                if user.name == candidate.name and user.romantic_current is not None:
                    has_partner = True
                    partner_name = user.romantic_current.name
                    break

                # Check if candidate is someone's partner
                if user.romantic_current is not None and hasattr(user.romantic_current, 'name'):
                    if user.romantic_current.name == candidate.name:
                        has_partner = True
                        partner_name = user.name
                        break

            if has_partner:
                break

        return has_partner, partner_name

    def show_next(self) -> None:
        """
        Show the next recommendation in the list.
        """
        if not self.recommendations:
            self.show_matching_summary()
        else:
            self.display_current_recommendation()

    def match_with_user(self, other_user: User) -> None:
        """
        Match the current user with another user and update the network visualization.
        """
        self.current_user.match(other_user)

        # Make sure both users exist in the global user list and update their romantic connections
        for user in self.user_list:
            if user.name == self.current_user.name:
                user.romantic_current = self.current_user.romantic_current
                user.romantic_degree = self.current_user.romantic_degree
            elif user.name == other_user.name:
                user.romantic_current = other_user.romantic_current
                user.romantic_degree = other_user.romantic_degree

        found_current = False
        found_other = False

        for user in self.user_list_love:
            if user.name == self.current_user.name:
                user.romantic_current = self.current_user.romantic_current
                user.romantic_degree = self.current_user.romantic_degree
                found_current = True
            elif user.name == other_user.name:
                user.romantic_current = other_user.romantic_current
                user.romantic_degree = other_user.romantic_degree
                found_other = True

        # Add users to self.user_list_love if they're not there but should be
        if not found_current and self.current_user.dating_goal != "Meeting new friends":
            self.user_list_love.append(self.current_user)
        if not found_other and other_user.dating_goal != "Meeting new friends":
            self.user_list_love.append(other_user)

        self.show_next()

    def show_temporary_message(self, message: str, color: str = "#2ECC71") -> None:
        """
        Show a temporary message overlay on the match frame.
        """
        # Create overlay
        overlay = tk.Frame(self.match_frame, bg="#5A6B7C")
        overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

        msg = tk.Label(overlay, text=message,
                       font=("Arial", 24, "bold"), fg=color, bg="#5A6B7C")
        msg.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Remove overlay after 1.5 seconds
        self.root.after(1500, overlay.destroy)

    def show_matching_summary(self) -> None:
        """
        Show a summary of the user's matches.
        """
        self.root.unbind_all("<MouseWheel>")

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=self.background_color)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Header
        header = tk.Label(frame, text="Matching Complete!",
                          font=("Arial", 28, "bold"), fg="white", bg=self.background_color)
        header.pack(pady=20)

        # Results
        dating_goal = self.current_user.dating_goal

        if dating_goal == "Meeting new friends":
            social_count = len(self.current_user.social_current)
            results_text = f"You've made {self.matches_made} new friends!"

            results = tk.Label(frame, text=results_text,
                               font=("Arial", 20), fg="white", bg=self.background_color)
            results.pack(pady=20)

            if self.matches_made > 0:
                connections = tk.Label(frame, text=f"Total social connections: {social_count}",
                                       font=("Arial", 16), fg="white", bg=self.background_color)
                connections.pack(pady=10)

                # List new connections
                if self.matches_made > 0:
                    new_connections_label = tk.Label(frame, text="Your new connections:",
                                                     font=("Arial", 16, "bold"), fg="white", bg=self.background_color)
                    new_connections_label.pack(pady=(20, 10))

                    # Create a scrollable frame for connections
                    connections_canvas = tk.Canvas(frame, bg=self.background_color, highlightthickness=0,
                                                   width=300, height=min(200, self.matches_made * 30))
                    connections_canvas.pack()

                    scrollable_frame = tk.Frame(connections_canvas, bg=self.background_color)
                    connections_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                    # Add connections to the scrollable frame
                    for i, user in enumerate(self.current_user.social_current[-self.matches_made:]):
                        connection = tk.Label(scrollable_frame, text=f"{i + 1}. {user.name}",
                                              font=("Arial", 14), fg="white", bg=self.background_color,
                                              anchor="w", padx=10)
                        connection.pack(fill="x", pady=2)

                    scrollable_frame.bind("<Configure>", lambda e: connections_canvas.configure(
                        scrollregion=connections_canvas.bbox("all")))
        else:
            # Romantic match summary
            if self.matches_made > 0:
                matched_user = self.current_user.romantic_current
                results_text = f"Congratulations! You've matched with {matched_user.name}!"

                results = tk.Label(frame, text=results_text,
                                   font=("Arial", 20), fg="white", bg=self.background_color)
                results.pack(pady=20)

                match_details = tk.Label(frame,
                                         text=f"{matched_user.age} • {matched_user.gender} • "
                                              f"{matched_user.characteristics.mbti}",
                                         font=("Arial", 16), fg="white", bg=self.background_color)
                match_details.pack(pady=10)

            else:
                results_text = "You didn't make any romantic connections."

                results = tk.Label(frame, text=results_text,
                                   font=("Arial", 20), fg="white", bg=self.background_color)
                results.pack(pady=20)

        # Add button to continue to main app
        continue_button = tk.Button(frame, text="Continue to App", font=("Arial", 16),
                                    bg="#4CAF50", fg="black", padx=20, pady=10,
                                    command=self.launch_main_app)
        continue_button.pack(pady=30)

    def launch_main_app(self) -> None:
        """
        Launch the main app (graph visualization or other main functionality).
        """
        self.root.unbind_all("<MouseWheel>")

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=self.background_color)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Show info about the user list
        label = tk.Label(frame, text=f"User network has {len(self.user_list)} users",
                         font=("Arial", 24), fg="white", bg=self.background_color)
        label.pack(pady=20)

        # Show social connections
        social_count = len(self.current_user.social_current)
        romantic_count = 1 if self.current_user.romantic_current is not None else 0
        connections_text = f"You have {social_count} friends. You have {romantic_count} romantic partner."

        connections_label = tk.Label(frame, text=connections_text,
                                     font=("Arial", 18), fg="white", bg=self.background_color)
        connections_label.pack(pady=10)

        # Create button frame
        button_frame = tk.Frame(frame, bg=self.background_color)
        button_frame.pack(pady=20)

        home_button = tk.Button(button_frame, text="Return to Home", font=("Arial", 16),
                                bg="#3498DB", fg="black", padx=20, pady=10,
                                command=lambda: self.create_welcome_page(self.image_path))
        home_button.pack(side=tk.LEFT, padx=10)

        # Add a close button
        close_button = tk.Button(button_frame, text="Exit", font=("Arial", 16),
                                 bg="#E74C3C", fg="black", padx=20, pady=10,
                                 command=self.root.destroy)
        close_button.pack(side=tk.LEFT, padx=10)

    def view_network_graph(self) -> None:
        """
        Show the network graph visualization.
        """
        try:
            # Create a temporary message
            temp_label = tk.Label(self.root, text="Loading network graph...",
                                  font=("Arial", 24), fg="white", bg=self.background_color)
            temp_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.root.update()

            # Find an available port
            def find_available_port(start: int = 8050, max_attempts: int = 10) -> int:
                for port in range(start, start + max_attempts):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        if s.connect_ex(('localhost', port)) != 0:
                            return port
                return start + 100

            port = find_available_port()

            # Define a function to run the Dash app in a separate thread
            def run_dash_app() -> None:
                destiny_app = graph.create_app(
                    user_list=self.user_list,
                    user_looking_for_friends=self.user_list_friends,
                    user_looking_for_love=self.user_list_love
                )

                destiny_app.run(debug=False, port=port)

            # Define a function to open the browser after a short delay
            def open_browser() -> None:
                time.sleep(3)
                url = f'http://127.0.0.1:{port}/'
                print(f"Opening browser to {url}")
                webbrowser.open(url)

                self.root.after(0, lambda: self.update_status_message("Graph visualization opened in browser"))

            # Create and start the thread for running the Dash app
            dash_thread = threading.Thread(target=run_dash_app, daemon=True)
            dash_thread.start()

            # Open browser in another thread to avoid blocking
            browser_thread = threading.Thread(target=open_browser, daemon=True)
            browser_thread.start()

            self.root.after(1500, lambda: temp_label.destroy())
            self.update_status_message("Graph launching in browser. Close browser tab when done.")

        except Exception as e:
            traceback.print_exc()
            error_label = tk.Label(self.root, text=f"Error: {str(e)}",
                                   font=("Arial", 16), fg="white", bg=self.background_color)
            error_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def update_status_message(self, message: str) -> None:
        """
        Update status message at the bottom of the window.
        """
        # Clear any existing status message
        for widget in self.root.winfo_children():
            if hasattr(widget, 'status_tag') and widget.status_tag:
                widget.destroy()

        # Create a new status frame at the bottom
        status_frame = tk.Frame(self.root, bg="#5A6B7C")
        status_frame.status_tag = True
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        status_label = tk.Label(status_frame, text=message,
                                font=("Arial", 14), fg="white", bg="#5A6B7C",
                                padx=10, pady=5)
        status_label.pack(fill=tk.X)

    def print_user_list_debug(self) -> None:
        """
        Print debug information about all users in the network to the terminal.
        """
        print("\n===== USER LIST DEBUG INFORMATION =====")
        print(f"Total users in network: {len(self.user_list)}")

        # Print information about the newly added user
        if hasattr(self, 'current_user'):
            print("\nNEWLY ADDED USER:")
            u = self.current_user
            print(f"  Name: {u.name}")
            print(f"  Age: {u.age}")
            print(f"  Gender: {u.gender}")
            print(f"  MBTI: {u.characteristics.mbti}")
            print(f"  Interests: {', '.join(u.characteristics.interests)}")
            print(f"  Match count: {len(u.social_current)}")
            print(f"  Social degree: {u.social_degree}")

        # Print sample of users from the list
        print("\nSAMPLE USERS FROM NETWORK:")
        # First 3 users
        for i, user in enumerate(self.user_list[:3]):
            print(f"  {i + 1}. {user.name}, {user.age}, {user.gender}, MBTI: {user.characteristics.mbti}")

        # Middle 3 users
        mid_point = len(self.user_list) // 2
        print("  ...")
        for i, user in enumerate(self.user_list[mid_point:mid_point + 3]):
            print(f"  {mid_point + i + 1}. {user.name}, {user.age}, {user.gender}, MBTI: {user.characteristics.mbti}")

        # Last 3 users (should include the newly added user)
        print("  ...")
        for i, user in enumerate(self.user_list[-3:]):
            print(
                f"  {len(self.user_list) - 2 + i}. {user.name}, {user.age}, {user.gender}, "
                f"MBTI: {user.characteristics.mbti}")

        print("\n==========================================")

    def run(self) -> None:
        """
        Run the application.
        """
        self.root.mainloop()


if __name__ == "__main__":
    home_image_path = "destiny_home_page.png"  # The path to the PNG image for home page
    app = DestinyApp(home_image_path)
    app.run()

    python_ta.check_all(config={
        'extra-imports': ["tkinter", "PIL", "sys", "user_network", "traceback", "tree", "common", "graph", "threading",
                          "time", "socket", "webbrowser", "dash"],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        "forbidden-io-functions": [],
        'max-line-length': 120,
        'max-module-lines': 2000,
        'max-attributes': 20,
        'max-locals': 100,
        'disable': ["W0718", "W0613", "R0915", "W0621", "W0404", "W0611", "R1702", "W0108"]
    })
