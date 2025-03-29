import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import os
import sys
import random

# Import the add_user() function from user_network.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from user_network import add_user, User, Characteristics, generate_users_with_class, add_fixed_users, user_looking_for_friends, user_looking_for_love
except ImportError:
    print("Error importing from user_network.py")

class DestinyApp:
    """
    A dating app interface that allows users to create profiles and visualize social networks.

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

    Representation Invariants:
        - self.window_width > 0
        - self.window_height > 0
        - isinstance(self.root, tk.Tk)
        - isinstance(self.image_path, str) and len(self.image_path) > 0

        # Conditional checks are used below because these attributes are not initialized in __init__

        - if hasattr(self, 'username'): isinstance(self.username, str) and len(self.username) > 0
        - if hasattr(self, 'attributes'): isinstance(self.attributes, dict)
        - if hasattr(self, 'user_list'): 
            - isinstance(self.user_list, list)
            - all(isinstance(user, User) for user in self.user_list)
        - if hasattr(self, 'current_user'): 
            - isinstance(self.current_user, User)
            - self.current_user in self.user_list
        - if hasattr(self, 'username_entry'): isinstance(self.username_entry, tk.Entry)
        - if hasattr(self, 'status_label'): isinstance(self.status_label, tk.Label)
        - if hasattr(self, 'result_label'): isinstance(self.result_label, tk.Label)
    """

    def __init__(self, image_path, window_width=720, window_height=720):
        self.root = tk.Tk()
        self.root.title("Destiny App")
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg="#7A8B9C")
    
        self.window_width = window_width
        self.window_height = window_height
    
        self.image_path = image_path
        
        self.create_welcome_page(image_path)

        self.user_list = generate_users_with_class(200, 25, 1234)
        add_fixed_users(self.user_list)
        print(f"Generated initial user list with {len(self.user_list)} users")
    
    def create_welcome_page(self, image_path):
        """
        Create the initial welcome page with image and username input.
        """
        # Unbind any mousewheel events first
        

        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg="#7A8B9C") # Set background color
        
        # Create two frames, one for the image (top half) and one for username input (bottom half)
        top_frame = tk.Frame(self.root, width=self.window_width, height=self.window_height // 2, bg="#7A8B9C")
        top_frame.pack(side=tk.TOP, fill=tk.BOTH)
        top_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        bottom_frame = tk.Frame(self.root, width=self.window_width, height=self.window_height // 2, bg="#7A8B9C")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # Load and display the image in the top half
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            
            # Get the display area dimensions for the top half, and account for some padding
            horizontal_padding = 40
            vertical_padding = 60
            display_width = self.window_width - horizontal_padding
            display_height = (self.window_height // 2) - vertical_padding
            
            # Calculate scale factors
            width_ratio = display_width / img_width
            height_ratio = display_height / img_height
            scale_factor = min(width_ratio, height_ratio)  # Use the smaller ratio to ensure the image fits
            
            # Always resize to fit the top half
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)  # Use LANCZOS filter for high-quality downsampling
            
            photo = ImageTk.PhotoImage(img)  # Convert the image to PhotoImage format
            
            # Create a label to display the image in the top frame
            image_label = tk.Label(top_frame, image=photo, bg="#7A8B9C")
            image_label.image = photo  # Keep a reference to prevent garbage collection
            
            image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Center the image in the top frame
            
        except Exception as e:
            # Show error message instead
            error_label = tk.Label(top_frame, text=f"Error loading image: {e}", 
                                  fg="white", bg="#7A8B9C", padx=20, pady=20, font=("Arial", 16))
            error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Add heading and create the username input field in the bottom frame
        heading = tk.Label(bottom_frame, text="Welcome to Destiny",
                          font=("Arial", 36, "bold"), fg="white", bg="#7A8B9C")
        heading.pack(pady=(50, 20))
        
        # Add description
        description = tk.Label(bottom_frame, text="Please enter your name to continue",
                             font=("Arial", 18), fg="white", bg="#7A8B9C")
        description.pack(pady=(0, 40))
        
        # Create a frame for the input field to control its width
        input_frame = tk.Frame(bottom_frame, bg="#7A8B9C")
        input_frame.pack(pady=20, padx=(0, 62.5))  # Add right padding to shift everything to the left
        
        # Create username label, input field, and submit button
        username_label = tk.Label(input_frame, text="Name:", font=("Arial", 16), fg="white", bg="#7A8B9C")
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.username_entry = tk.Entry(input_frame, font=("Arial", 16), width=20)
        self.username_entry.pack(side=tk.LEFT)
        self.username_entry.focus_set()  # Set cursor focus to this field
        
        submit_button = tk.Button(bottom_frame, text="Continue", font=("Arial", 16),
                                 bg="#4CAF50", fg="black", padx=20, pady=10,
                                 command=self.handle_username_submit)
        submit_button.pack(pady=20)
        
        # Result label to show feedback
        self.result_label = tk.Label(bottom_frame, text="", font=("Arial", 14),
                              fg="white", bg="#7A8B9C")
        self.result_label.pack(pady=10)
        
        self.root.bind('<Return>', lambda event: self.handle_username_submit())  # Handle Enter key press to advance
    
    def handle_username_submit(self):
        """
        Handle the username submission and transition to appropriate page.
        """
        username = self.username_entry.get().strip()
        if not username:
            self.result_label.config(text="Please enter your name")
            return
        
        self.username = username
        
        # Check if this is the admin user
        if username.lower() == "admin":
            self.create_admin_page()  # Admin user, proceed to admin page
        else:
            self.create_attributes_page()  # Regular user, proceed to attributes page

    def create_admin_page(self):
        """
        Create the admin page with direct access to the network graph.
        """
        # Unbind any mousewheel events first
        self.root.unbind_all("<MouseWheel>")

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.configure(bg="#7A8B9C")  # Set background color
        
        # Create main frame
        frame = tk.Frame(self.root, bg="#7A8B9C")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Description
        admin_label = tk.Label(frame, text="ADMIN MODE",
                            font=("Arial", 36, "bold"), fg="white", bg="#7A8B9C")
        admin_label.pack(pady=20)
        
        users_label = tk.Label(frame, text=f"The user network has {len(self.user_list)} users",
                            font=("Arial", 24), fg="white", bg="#7A8B9C")
        users_label.pack(pady=20)
        
        description = tk.Label(frame, text="You have direct access to the network visualization",
                            font=("Arial", 18), fg="white", bg="#7A8B9C")
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
                                command=lambda: self.create_welcome_page(image_path))
        logout_button.pack(pady=20)
    
    def configure_dropdown(self, dropdown, width=29):
        """
        Apply simple consistent styling to a dropdown menu.
        """
        # Set the background of the dropdown button part
        dropdown.config(
            font=("Arial", 14),
            width=width,
            bg="#7A8B9C",
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
    
    def create_attributes_page(self):
        """
        Create the page with input fields for all user attributes.
        """
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.configure(bg="#7A8B9C")  # Set background color
        
        # Create a main frame with scrolling capability
        main_frame = tk.Frame(self.root, bg="#7A8B9C")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a canvas with scrollbar
        canvas = tk.Canvas(main_frame, bg="#7A8B9C", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#7A8B9C")
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Define mousewheel event handlers first before using them
        def _bound_to_mousewheel(event):
            # Bind scrolling when mouse enters the canvas
            if sys.platform == 'darwin':  # macOS
                canvas.bind_all("<MouseWheel>", _on_scrollwheel)
            else:  # Windows and others
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbound_to_mousewheel(event):
            # Unbind scrolling when mouse leaves the canvas
            if sys.platform == 'darwin':  # macOS
                canvas.unbind_all("<MouseWheel>")
            else:  # Windows and others
                canvas.unbind_all("<MouseWheel>")

        # Enable mousewheel/trackpad scrolling
        def _on_mousewheel(event):
            # For Windows and macOS
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except (tk.TclError, RuntimeError):
                # Widget no longer exists, unbind the event
                if sys.platform == 'darwin':  # macOS
                    self.root.unbind_all("<MouseWheel>")
                else:  # Windows and others
                    self.root.unbind_all("<MouseWheel>")
        
        def _on_scrollwheel(event):
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
                         font=("Arial", 24, "bold"), fg="white", bg="#7A8B9C")
        heading.pack(pady=(20, 30))
        
        self.attributes = {}
        
        # Age input (numeric)
        age_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        age_frame.pack(fill="x", padx=20, pady=10)
        
        age_label = tk.Label(age_frame, text="Age:", width=20, anchor="e", 
                          font=("Arial", 14), fg="white", bg="#7A8B9C")
        age_label.pack(side="left", padx=(0, 10))
        
        age_var = tk.StringVar()
        age_entry = tk.Entry(age_frame, textvariable=age_var, font=("Arial", 14), width=30)
        age_entry.pack(side="left")
        self.attributes["age"] = age_var
        
        # Gender dropdown
        gender_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        gender_frame.pack(fill="x", padx=20, pady=10)
        
        gender_label = tk.Label(gender_frame, text="Gender:", width=20, anchor="e", 
                             font=("Arial", 14), fg="white", bg="#7A8B9C")
        gender_label.pack(side="left", padx=(0, 10))

        gender_var = tk.StringVar()
        gender_options = ["M", "F"]
        gender_dropdown = tk.OptionMenu(gender_frame, gender_var, *gender_options)
        self.configure_dropdown(gender_dropdown)
        gender_dropdown.pack(side="left")
        self.attributes["gender"] = gender_var
        
        # Pronouns input
        pronouns_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        pronouns_frame.pack(fill="x", padx=20, pady=10)
        
        pronouns_label = tk.Label(pronouns_frame, text="Pronouns:", width=20, anchor="e", 
                               font=("Arial", 14), fg="white", bg="#7A8B9C")
        pronouns_label.pack(side="left", padx=(0, 10))
        
        pronouns_var = tk.StringVar()
        pronouns_entry = tk.Entry(pronouns_frame, textvariable=pronouns_var, font=("Arial", 14), width=30)
        pronouns_entry.pack(side="left")
        self.attributes["pronouns"] = pronouns_var
        
        # Ethnicity dropdown
        ethnicity_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        ethnicity_frame.pack(fill="x", padx=20, pady=10)
        
        ethnicity_label = tk.Label(ethnicity_frame, text="Ethnicity:", width=20, anchor="e", 
                                font=("Arial", 14), fg="white", bg="#7A8B9C")
        ethnicity_label.pack(side="left", padx=(0, 10))

        ethnicity_var = tk.StringVar()
        ethnicity_options = ["Asian", "Black", "Hispanic", "White", "Mixed", "Other"]
        ethnicity_dropdown = tk.OptionMenu(ethnicity_frame, ethnicity_var, *ethnicity_options)
        self.configure_dropdown(ethnicity_dropdown)
        ethnicity_dropdown.pack(side="left")
        self.attributes["ethnicity"] = ethnicity_var
        
        # Interests multi-select
        interests_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        interests_frame.pack(fill="x", padx=20, pady=10)
        
        interests_label = tk.Label(interests_frame, text="Interests:", width=20, anchor="e", 
                                font=("Arial", 14), fg="white", bg="#7A8B9C")
        interests_label.pack(side="left", anchor="n", padx=(0, 10))
        
        interests_options_frame = tk.Frame(interests_frame, bg="#7A8B9C")
        interests_options_frame.pack(side="left", fill="x")
        
        interests_options = ["Reading", "Dancing", "Singing", "Playing instruments", "Running", "Coding", "Doing math"]
        interests_vars = {interest: tk.BooleanVar() for interest in interests_options}
        
        for i, interest in enumerate(interests_options):
            cb = tk.Checkbutton(interests_options_frame, text=interest, variable=interests_vars[interest], 
                             font=("Arial", 14), fg="white", bg="#7A8B9C", selectcolor="#7A8B9C",
                             activebackground="#7A8B9C", activeforeground="white")
            cb.pack(anchor="w")
        
        self.attributes["interests"] = interests_vars
        
        # MBTI input
        mbti_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        mbti_frame.pack(fill="x", padx=20, pady=10)
        
        mbti_label = tk.Label(mbti_frame, text="MBTI:", width=20, anchor="e", 
                          font=("Arial", 14), fg="white", bg="#7A8B9C")
        mbti_label.pack(side="left", padx=(0, 10))
        
        mbti_var = tk.StringVar()
        mbti_entry = tk.Entry(mbti_frame, textvariable=mbti_var, font=("Arial", 14), width=30)
        mbti_entry.pack(side="left")
        self.attributes["mbti"] = mbti_var
        
        # Communication Type
        comm_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        comm_frame.pack(fill="x", padx=20, pady=10)
        
        comm_label = tk.Label(comm_frame, text="Communication Type:", width=20, anchor="e", 
                          font=("Arial", 14), fg="white", bg="#7A8B9C")
        comm_label.pack(side="left", padx=(0, 10))
        
        comm_var = tk.StringVar()
        comm_options = ["Texting", "Phonecall"]
        comm_dropdown = tk.OptionMenu(comm_frame, comm_var, *comm_options)
        self.configure_dropdown(comm_dropdown)
        comm_dropdown.pack(side="left")
        self.attributes["communication_type"] = comm_var

        # Political Interests
        politics_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        politics_frame.pack(fill="x", padx=20, pady=10)
        
        politics_label = tk.Label(politics_frame, text="Political Interests:", width=20, anchor="e", 
                              font=("Arial", 14), fg="white", bg="#7A8B9C")
        politics_label.pack(side="left", padx=(0, 10))
        
        politics_var = tk.StringVar()
        politics_options = ["Liberal", "Conservative"]
        politics_dropdown = tk.OptionMenu(politics_frame, politics_var, *politics_options)
        self.configure_dropdown(politics_dropdown)
        politics_dropdown.pack(side="left")
        self.attributes["political_interests"] = politics_var
        
        # Religion
        religion_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        religion_frame.pack(fill="x", padx=20, pady=10)
        
        religion_label = tk.Label(religion_frame, text="Religion:", width=20, anchor="e", 
                               font=("Arial", 14), fg="white", bg="#7A8B9C")
        religion_label.pack(side="left", padx=(0, 10))
        
        religion_var = tk.StringVar()
        religion_options = ["Protestant", "Orthodox", "Catholic", "Buddhism", "Hinduism", 
                         "Taoism", "Jewish", "Agnostic", "Other"]
        religion_dropdown = tk.OptionMenu(religion_frame, religion_var, *religion_options)
        self.configure_dropdown(religion_dropdown)
        religion_dropdown.pack(side="left")
        self.attributes["religion"] = religion_var
        
        # Major
        major_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        major_frame.pack(fill="x", padx=20, pady=10)
        
        major_label = tk.Label(major_frame, text="Major:", width=20, anchor="e", 
                            font=("Arial", 14), fg="white", bg="#7A8B9C")
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
        year_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        year_frame.pack(fill="x", padx=20, pady=10)
        
        year_label = tk.Label(year_frame, text="Year:", width=20, anchor="e", 
                           font=("Arial", 14), fg="white", bg="#7A8B9C")
        year_label.pack(side="left", padx=(0, 10))
        
        year_var = tk.StringVar()
        year_options = ["1", "2", "3", "4", "5", "Master"]
        year_dropdown = tk.OptionMenu(year_frame, year_var, *year_options)
        self.configure_dropdown(year_dropdown)
        year_dropdown.pack(side="left")
        self.attributes["year"] = year_var
        
        # Language
        language_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        language_frame.pack(fill="x", padx=20, pady=10)
        
        language_label = tk.Label(language_frame, text="Language:", width=20, anchor="e", 
                               font=("Arial", 14), fg="white", bg="#7A8B9C")
        language_label.pack(side="left", padx=(0, 10))
        
        language_var = tk.StringVar()
        language_options = ["English", "Cantonese", "Mandarin", "French", "Spanish", "Japanese", "Korean", "Others"]
        language_dropdown = tk.OptionMenu(language_frame, language_var, *language_options)
        self.configure_dropdown(language_dropdown)
        language_dropdown.pack(side="left")
        self.attributes["language"] = language_var
        
        # Dating Goal
        goal_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        goal_frame.pack(fill="x", padx=20, pady=10)
        
        goal_label = tk.Label(goal_frame, text="Dating Goal:", width=20, anchor="e", 
                           font=("Arial", 14), fg="white", bg="#7A8B9C")
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
            bool_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
            bool_frame.pack(fill="x", padx=20, pady=10)
            
            bool_label = tk.Label(bool_frame, text=f"{text}:", width=20, anchor="e", 
                               font=("Arial", 14), fg="white", bg="#7A8B9C")
            bool_label.pack(side="left", padx=(0, 10))
            
            bool_var = tk.BooleanVar()
            bool_true = tk.Radiobutton(bool_frame, text="True", variable=bool_var, value=True, 
                                    font=("Arial", 14), fg="white", bg="#7A8B9C", 
                                    selectcolor="#5A6B7C", activebackground="#7A8B9C",
                                    activeforeground="white")
            bool_true.pack(side="left", padx=(0, 20))
            
            bool_false = tk.Radiobutton(bool_frame, text="False", variable=bool_var, value=False,
                                     font=("Arial", 14), fg="white", bg="#7A8B9C",
                                     selectcolor="#5A6B7C", activebackground="#7A8B9C",
                                     activeforeground="white")
            bool_false.pack(side="left")
            
            self.attributes[bool_attr] = bool_var

        # Attribute priority ranking section
        priority_heading = tk.Label(scroll_frame, text="Rank Attribute Importance",
                                font=("Arial", 18, "bold"), fg="white", bg="#7A8B9C")
        priority_heading.pack(pady=(30, 10))

        priority_description = tk.Label(scroll_frame, text="Select attributes and use the buttons to rank them by importance (top = most important)",
                                font=("Arial", 14), fg="white", bg="#7A8B9C")
        priority_description.pack(pady=(0, 20))
        
        # Create a listbox with attribute names that can be reordered
        priority_frame = tk.Frame(scroll_frame, bg="#7A8B9C")
        priority_frame.pack(fill="x", padx=20, pady=10)

        # Define the attributes to rank
        attribute_list = ["Ethnicity", "Interests", "MBTI", "Communication Type", "Political Interests",
                          "Religion", "Major", "Year", "Language", "Likes Pets",
                          "Likes Outdoor Activities", "Enjoys Watching Movies"]

        # Create a listbox for drag and drop
        priority_listbox = tk.Listbox(priority_frame, 
                                font=("Arial", 14),
                                bg="#5A6B7C",
                                fg="white",
                                selectbackground="#3A4B5C",
                                selectforeground="white",
                                height=len(attribute_list),
                                width=40)
        
        # Add attributes to the listbox
        for attr in attribute_list:
            priority_listbox.insert(tk.END, attr)

        priority_listbox.pack(side="left", padx=(50, 0))

       # Add up/down buttons for reordering
        button_frame = tk.Frame(priority_frame, bg="#7A8B9C")
        button_frame.pack(side="left", padx=10)

        def move_up():
            selected_idx = priority_listbox.curselection()
            if not selected_idx or selected_idx[0] == 0:
                return
            
            idx = selected_idx[0]
            text = priority_listbox.get(idx)
            priority_listbox.delete(idx)
            priority_listbox.insert(idx-1, text)
            priority_listbox.selection_set(idx-1)
            priority_listbox.activate(idx-1)

        def move_down():
            selected_idx = priority_listbox.curselection()
            if not selected_idx or selected_idx[0] == priority_listbox.size()-1:
                return
            
            idx = selected_idx[0]
            text = priority_listbox.get(idx)
            priority_listbox.delete(idx)
            priority_listbox.insert(idx+1, text)
            priority_listbox.selection_set(idx+1)
            priority_listbox.activate(idx+1)

        up_button = tk.Button(button_frame, text="↑", font=("Arial", 18, "bold"), 
                    bg="#E74C3C", fg="black", width=3, command=move_up,
                    activebackground="#C0392B", activeforeground="white")
        up_button.pack(pady=(0, 10))

        down_button = tk.Button(button_frame, text="↓", font=("Arial", 18, "bold"), 
                            bg="#E74C3C", fg="black", width=3, command=move_down,
                            activebackground="#C0392B", activeforeground="white")
        down_button.pack()

        self.priority_attributes = []
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

        # Convert user-friendly names to internal attribute keys
        self.priority_attributes = [priority_mapping.get(attr, attr.lower()) for attr in self.priority_attributes]

        # Add some space
        spacer = tk.Label(scroll_frame, text="", bg="#7A8B9C")
        spacer.pack(pady=20)

        # Add status label for validation messages
        self.status_label = tk.Label(scroll_frame, text="", font=("Arial", 14, "bold"), 
                                fg="#E74C3C", bg="#7A8B9C")
        self.status_label.pack(pady=10)

        # Add submit button
        submit_button = tk.Button(scroll_frame, text="Create Profile", font=("Arial", 18, "bold"),
                            bg="#2ECC71", fg="black", padx=30, pady=15,
                            command=self.submit_user_profile)
        submit_button.pack(pady=(20, 40))

        # Add another spacer at the bottom for better scrolling
        bottom_spacer = tk.Label(scroll_frame, text="", bg="#7A8B9C")
        bottom_spacer.pack(pady=50)
    
    def add_user_to_network(self, new_user, user_list):
        """
        Add the newly created user to the existing user network.
        """
        # Add the user to the list
        user_list.append(new_user)

        print(f"Added user {new_user.name}.")
        
        return user_list

    def submit_user_profile(self):
        """
        Collect all the input values and create a new user.
        """
        try:
            # Get values from the inputs
            name = self.username
            
            # Validate and process age
            try:
                age = int(self.attributes["age"].get())
                if not (18 <= age <= 30):
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
            interested_romantic=[]
        )
        
            # Generate the initial user list if it hasn't been created yet
            if not hasattr(self, 'user_list'):
                self.user_list = generate_users_with_class(200, 25, 1234)
                add_fixed_users(self.user_list)
                print(f"Generated initial user list with {len(self.user_list)} users")
            
            # Add the user to the network
            self.user_list = self.add_user_to_network(user, self.user_list)
            add_fixed_users(user_looking_for_friends)
            self.user_list_friend = self.add_user_to_network(user, user_looking_for_friends)
            self.user_list_love = self.add_user_to_network(user, user_looking_for_love)

            # Print debug information to terminal
            self.print_user_list_debug()
            
            # Display success message
            self.status_label.config(text=f"Profile created successfully for {name}!", fg="white")
            
            # Store the user object for later use
            self.current_user = user
            
            # Show success page after a short delay
            self.root.after(1500, self.show_success_page)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.status_label.config(text=f"Error: {str(e)}")
    
    def show_success_page(self):
        """
        Show a success page after profile creation.
        """
        import tree
        # Unbind any mousewheel events first
        self.root.unbind_all("<MouseWheel>")
        
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
                
        # Success message
        frame = tk.Frame(self.root, bg="#7A8B9C")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
        success_label = tk.Label(frame, text="Profile Created Successfully!",
                            font=("Arial", 24, "bold"), fg="white", bg="#7A8B9C")
        success_label.pack(pady=20)
            
        name_label = tk.Label(frame, text=f"Welcome, {self.username}!",
                        font=("Arial", 18), fg="white", bg="#7A8B9C")
        name_label.pack(pady=10)
            
        message = tk.Label(frame, text="Your profile has been created and added to the system.",
                        font=("Arial", 14), fg="white", bg="#7A8B9C")
        message.pack(pady=10)
            
        # Add a button to launch the matching page
        continue_button = tk.Button(frame, text="Find Matches", font=("Arial", 16),
                                bg="#4CAF50", fg="black", padx=20, pady=10,
                                command=self.show_matching_page)
        continue_button.pack(pady=30)

    def show_matching_page(self):
        """
        Show a page where users can swipe through recommended matches and connect with them.
        """
        import tree
        # Unbind any mousewheel events first
        self.root.unbind_all("<MouseWheel>")

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.configure(bg="#7A8B9C")
        
        # Get the dating goal of the current user
        dating_goal = self.current_user.dating_goal
        connection_type = "friendship" if dating_goal == "Meeting new friends" else "romantic"
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#7A8B9C")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(main_frame, text="Find Your Matches", 
                        font=("Arial", 28, "bold"), fg="white", bg="#7A8B9C")
        header.pack(pady=(30, 10))
        
        # Description
        if connection_type == "friendship":
            desc = "Find new friends based on your preferences"
        else:
            desc = "Find a romantic partner based on your preferences"
        
        description = tk.Label(main_frame, text=desc,
                            font=("Arial", 16), fg="white", bg="#7A8B9C")
        description.pack(pady=(0, 20))

        tree.data_wrangling(currentUser=self.current_user, user_characteristics=self.priority_attributes, users_list=self.user_list)
        preference_tree = tree.build_preference_tree("data.csv")
        recommendation_names = preference_tree.run_preference_tree()
        
        # Convert names to user objects
        self.recommendations = []
        for name in recommendation_names:
            user = next((u for u in self.user_list if u.name == name), None)
            if user:
                self.recommendations.append(user)
        
        if not self.recommendations:
            # No recommendations
            no_matches = tk.Label(main_frame, text="No potential matches found!",
                                font=("Arial", 20), fg="#E74C3C", bg="#7A8B9C")
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
        
        # Initialize the match counter
        self.matches_made = 0
        
        # Display the first recommendation
        self.display_current_recommendation()
        
        # Create the buttons frame
        button_frame = tk.Frame(main_frame, bg="#7A8B9C")
        button_frame.pack(pady=30)
        
        # Pass button
        pass_button = tk.Button(button_frame, text="Pass", font=("Arial", 16),
                            bg="#E74C3C", fg="black", padx=30, pady=15,
                            command=self.pass_current_recommendation)
        pass_button.pack(side=tk.LEFT, padx=15)
        
        # Match button
        match_button = tk.Button(button_frame, text="Match!", font=("Arial", 16, "bold"),
                            bg="#2ECC71", fg="black", padx=30, pady=15,
                            command=self.match_current_recommendation)
        match_button.pack(side=tk.LEFT, padx=15)
        
        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 16),
                    bg="#95A5A6", fg="black", padx=30, pady=15,
                    command=lambda: self.create_welcome_page(self.image_path))
        exit_button.pack(side=tk.LEFT, padx=15)
        
        # Display counter
        counter_text = f"Showing match 1 of {len(self.recommendations)}"
        self.counter_label = tk.Label(main_frame, text=counter_text,
                                    font=("Arial", 14), fg="white", bg="#7A8B9C")
        self.counter_label.pack(pady=(20, 0))

    def display_current_recommendation(self):
        """
        Display the current recommendation in the match frame.
        """
        # Clear the match frame
        for widget in self.match_frame.winfo_children():
            widget.destroy()
        
        # Get the current recommendation
        if not self.recommendations:
            # No more recommendations
            no_more = tk.Label(self.match_frame, text="No more matches!",
                            font=("Arial", 20), fg="white", bg="#5A6B7C")
            no_more.pack(pady=40)
            return
        
        user = self.recommendations[0]  # Always show the first user in the list
        
        # Create the profile display
        name = tk.Label(self.match_frame, text=user.name,
                    font=("Arial", 24, "bold"), fg="white", bg="#5A6B7C")
        name.pack(pady=(0, 20))
        
        # Basic info
        basic_info = tk.Label(self.match_frame, 
                        text=f"{user.age} • {user.gender} • {user.characteristics.mbti}",
                        font=("Arial", 16), fg="white", bg="#5A6B7C")
        basic_info.pack(pady=(0, 15))
        
        # Major & Year
        major_year = tk.Label(self.match_frame, 
                        text=f"{user.characteristics.major}, Year {user.characteristics.year}",
                        font=("Arial", 16), fg="white", bg="#5A6B7C")
        major_year.pack(pady=(0, 15))
        
        # Interests
        interests_label = tk.Label(self.match_frame, text="Interests:",
                            font=("Arial", 16, "bold"), fg="white", bg="#5A6B7C")
        interests_label.pack(pady=(15, 5), anchor="w", padx=40)
        
        interests_text = ", ".join(user.characteristics.interests)
        interests = tk.Label(self.match_frame, text=interests_text,
                        font=("Arial", 14), fg="white", bg="#5A6B7C",
                        wraplength=400, justify="left")
        interests.pack(pady=(0, 15), anchor="w", padx=40)
        
        # Update the counter label - add safety check
        try:
            if hasattr(self, 'counter_label') and self.counter_label.winfo_exists():
                counter_text = f"Showing match {self.recommendations.index(user) + 1} of {len(self.recommendations)}"
                self.counter_label.config(text=counter_text)
        except (tk.TclError, AttributeError):
            # If counter_label doesn't exist or has been destroyed, create a new one
            pass

    def pass_current_recommendation(self):
        """
        Skip the current recommendation and show the next one.
        """
        if self.recommendations:
            self.recommendations.pop(0)  # Remove the current recommendation
            
            if not self.recommendations:
                # No more recommendations, go to the summary page
                self.show_matching_summary()
                return
            
            self.display_current_recommendation()

    def match_current_recommendation(self):
        """
        Match with the current recommendation and show the next one.
        """
        # Get the current recommendation
        if not self.recommendations:
            return
        
        matched_user = self.recommendations.pop(0)  # Remove and get the current recommendation
        dating_goal = self.current_user.dating_goal
        
        # Add connection based on dating goal
        if dating_goal == "Meeting new friends":
            # Add social connection
            if matched_user not in self.current_user.social_current:
                self.current_user.social_current.append(matched_user)
            if self.current_user not in matched_user.social_current:
                matched_user.social_current.append(self.current_user)
            
            # Update social degree
            self.current_user.update_social_degree()
            matched_user.update_social_degree()
            
            # Show success message
            success_text = f"You've connected with {matched_user.name}!"
            self.show_temporary_message(success_text, "#2ECC71")
            
            # Increment match counter
            self.matches_made += 1
            
            if not self.recommendations:
                # No more recommendations
                self.root.after(200, self.show_matching_summary)
                return
            
            # Display next recommendation after a short delay
            self.root.after(200, self.display_current_recommendation)
            
        else:
            # Add romantic connection
            if not hasattr(self.current_user, 'romantic_current') or self.current_user.romantic_current is None:
                self.current_user.romantic_current = []
                
            if not hasattr(matched_user, 'romantic_current') or matched_user.romantic_current is None:
                matched_user.romantic_current = []
                
            self.current_user.romantic_current.append(matched_user)
            matched_user.romantic_current.append(self.current_user)
            
            # Show success message
            success_text = f"You've matched with {matched_user.name}!"
            self.show_temporary_message(success_text, "#E74C3C")
            
            # Increment match counter
            self.matches_made += 1
            
            # For romantic connections, immediately go to summary after one match
            self.root.after(200, self.show_matching_summary)

    def show_temporary_message(self, message, color="#2ECC71"):
        """
        Show a temporary message overlay on the match frame.
        """
        # Create a semi-transparent overlay
        overlay = tk.Frame(self.match_frame, bg="#5A6B7C")
        overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        # Message
        msg = tk.Label(overlay, text=message,
                    font=("Arial", 24, "bold"), fg=color, bg="#5A6B7C")
        msg.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Remove overlay after 1.5 seconds
        self.root.after(1500, overlay.destroy)

    def show_matching_summary(self):
        """
        Show a summary of the user's matches.
        """
        # Unbind any mousewheel events first
        self.root.unbind_all("<MouseWheel>")

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = tk.Frame(self.root, bg="#7A8B9C")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Header
        header = tk.Label(frame, text="Matching Complete!",
                        font=("Arial", 28, "bold"), fg="white", bg="#7A8B9C")
        header.pack(pady=20)
        
        # Results
        dating_goal = self.current_user.dating_goal
        
        if dating_goal == "Meeting new friends":
            social_count = len(self.current_user.social_current)
            results_text = f"You've made {self.matches_made} new friends!"
            
            results = tk.Label(frame, text=results_text,
                            font=("Arial", 20), fg="white", bg="#7A8B9C")
            results.pack(pady=20)
            
            if self.matches_made > 0:
                connections = tk.Label(frame, text=f"Total social connections: {social_count}",
                                    font=("Arial", 16), fg="white", bg="#7A8B9C")
                connections.pack(pady=10)
                
                # List new connections
                if self.matches_made > 0:
                    new_connections_label = tk.Label(frame, text="Your new connections:",
                                                font=("Arial", 16, "bold"), fg="white", bg="#7A8B9C")
                    new_connections_label.pack(pady=(20, 10))
                    
                    # Create a scrollable frame for connections
                    connections_canvas = tk.Canvas(frame, bg="#7A8B9C", highlightthickness=0,
                                            width=300, height=min(200, self.matches_made * 30))
                    connections_canvas.pack()
                    
                    scrollable_frame = tk.Frame(connections_canvas, bg="#7A8B9C")
                    scrollable_frame_id = connections_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    
                    # Add connections to the scrollable frame
                    for i, user in enumerate(self.current_user.social_current[-self.matches_made:]):
                        connection = tk.Label(scrollable_frame, text=f"{i+1}. {user.name}",
                                        font=("Arial", 14), fg="white", bg="#7A8B9C",
                                        anchor="w", padx=10)
                        connection.pack(fill="x", pady=2)
                    
                    # Configure the scrollregion
                    scrollable_frame.bind("<Configure>", lambda e: connections_canvas.configure(
                        scrollregion=connections_canvas.bbox("all")))
        else:
            # Romantic match summary
            if self.matches_made > 0:
                matched_user = self.current_user.romantic_current[0]
                results_text = f"Congratulations! You've matched with {matched_user.name}!"
                
                results = tk.Label(frame, text=results_text,
                                font=("Arial", 20), fg="white", bg="#7A8B9C")
                results.pack(pady=20)
                
                match_details = tk.Label(frame, 
                                    text=f"{matched_user.age} • {matched_user.gender} • {matched_user.characteristics.mbti}",
                                    font=("Arial", 16), fg="white", bg="#7A8B9C")
                match_details.pack(pady=10)
            else:
                results_text = "You didn't make any romantic connections."
                
                results = tk.Label(frame, text=results_text,
                                font=("Arial", 20), fg="white", bg="#7A8B9C")
                results.pack(pady=20)
        
        # Add button to continue to main app
        continue_button = tk.Button(frame, text="Continue to App", font=("Arial", 16),
                                bg="#4CAF50", fg="black", padx=20, pady=10,
                                command=self.launch_main_app)
        continue_button.pack(pady=30)
    
    def launch_main_app(self):
        """
        Launch the main app (graph visualization or other main functionality).
        """
        # Unbind any mousewheel events first
        self.root.unbind_all("<MouseWheel>")

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = tk.Frame(self.root, bg="#7A8B9C")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Show info about the user list
        label = tk.Label(frame, text=f"User network has {len(self.user_list)} users",
                    font=("Arial", 24), fg="white", bg="#7A8B9C")
        label.pack(pady=20)
        
        # TODO: 

        # # Show the current user's matches
        # match_count = len(self.current_user.match)
        # match_text = f"You have {match_count} matches!" if match_count > 0 else "No matches yet"
        
        # matches_label = tk.Label(frame, text=match_text,
        #                     font=("Arial", 18), fg="white", bg="#7A8B9C")
        # matches_label.pack(pady=10)
        
        # Show social connections
        social_count = len(self.current_user.social_current)
        romantic_count = len(self.current_user.romantic_current)
        connections_text = f"You have {social_count} friends. You have {romantic_count} romantic partner."
        
        connections_label = tk.Label(frame, text=connections_text,
                            font=("Arial", 18), fg="white", bg="#7A8B9C")
        connections_label.pack(pady=10)
        
        # Create button frame for better layout
        button_frame = tk.Frame(frame, bg="#7A8B9C")
        button_frame.pack(pady=20)
        
        # Add a button to return to home page
        home_button = tk.Button(button_frame, text="Return to Home", font=("Arial", 16),
                            bg="#3498DB", fg="black", padx=20, pady=10,
                            command=lambda: self.create_welcome_page(image_path))
        home_button.pack(side=tk.LEFT, padx=10)
        
        # Add a close button
        close_button = tk.Button(button_frame, text="Exit", font=("Arial", 16),
                            bg="#E74C3C", fg="black", padx=20, pady=10,
                            command=self.root.destroy)
        close_button.pack(side=tk.LEFT, padx=10)

    def view_network_graph(self):
        """
        Show the network graph visualization.
        """
        # Import graph module here to avoid circular imports
        try:
            import graph
            import webbrowser
            import threading
            import time
            import socket
            
            # Create a temporary message
            temp_label = tk.Label(self.root, text="Loading network graph...",
                                font=("Arial", 24), fg="white", bg="#7A8B9C")
            temp_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.root.update()
            
            # Find an available port
            def find_available_port(start=8050, max_attempts=10):
                """Find an available port starting from start_port"""
                for port in range(start, start + max_attempts):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        if s.connect_ex(('localhost', port)) != 0:
                            return port
                return start + 100  # If no port found, try a higher number
            
            # Choose a port
            port = find_available_port()
            
            # Define a function to run the Dash app in a separate thread
            def run_dash_app():
                # Create the Dash app instance with our user list
                print(f"Creating graph visualization with {len(self.user_list)} users on port {port}")
                app = graph.create_app(self.user_list)
                
                # Configure the server to run without automatically opening the browser
                app.run(debug=False, port=port)
            
            # Define a function to open the browser after a short delay
            def open_browser():
                time.sleep(3)  # Wait for the server to start
                url = f'http://127.0.0.1:{port}/'
                print(f"Opening browser to {url}")
                webbrowser.open(url)
                
                # Update the original window to indicate graph is open
                self.root.after(0, lambda: self.update_status_message("Graph visualization opened in browser"))
            
            # Create and start the thread for running the Dash app
            dash_thread = threading.Thread(target=run_dash_app, daemon=True)
            dash_thread.start()
            
            # Open browser in another thread to avoid blocking
            browser_thread = threading.Thread(target=open_browser, daemon=True)
            browser_thread.start()
            
            # Remove the temporary message after a delay
            self.root.after(200, lambda: temp_label.destroy())
            
            # Keep the main window responsive
            self.update_status_message("Graph launching in browser. Close browser tab when done.")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_label = tk.Label(self.root, text=f"Error: {str(e)}",
                                font=("Arial", 16), fg="white", bg="#7A8B9C")
            error_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def update_status_message(self, message):
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
        
        # Add the status message
        status_label = tk.Label(status_frame, text=message, 
                            font=("Arial", 14), fg="white", bg="#5A6B7C",
                            padx=10, pady=5)
        status_label.pack(fill=tk.X)

    def print_user_list_debug(self):
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
            print(f"  {i+1}. {user.name}, {user.age}, {user.gender}, MBTI: {user.characteristics.mbti}")
        
        # Middle 3 users
        mid_point = len(self.user_list) // 2
        print("  ...")
        for i, user in enumerate(self.user_list[mid_point:mid_point+3]):
            print(f"  {mid_point+i+1}. {user.name}, {user.age}, {user.gender}, MBTI: {user.characteristics.mbti}")
        
        # Last 3 users (should include the newly added user)
        print("  ...")
        for i, user in enumerate(self.user_list[-3:]):
            print(f"  {len(self.user_list)-2+i}. {user.name}, {user.age}, {user.gender}, MBTI: {user.characteristics.mbti}")
        
        print("\n==========================================")
    
    def run(self):
        """
        Run the application.
        """
        self.root.mainloop()

image_path = "destiny_home_page.png"  # The path to the PNG image for home page

if __name__ == "__main__":
    app = DestinyApp(image_path)
    app.run()

#     python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],     # the names (strs) of functions that call print/open/input
#     'max-line-length': 120
# })