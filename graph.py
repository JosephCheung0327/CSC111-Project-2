from user_network import generate_users_with_class, add_fixed_users, User, user_looking_for_friends, user_looking_for_love

import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, callback_context
import networkx as nx

def plot_user_connections(users: list, search_name: str = None, positions = None) -> tuple:
    """Create a graph visualization showing social connections between users"""
    G = nx.Graph()

    # First add all users as nodes without edges
    for user in users:
        try:
            # Get size from social_degree or social_current
            size = 1  # Default size
            if hasattr(user, 'social_degree') and user.social_degree is not None:
                size = max(1, user.social_degree)
            elif hasattr(user, 'social_current') and user.social_current:
                size = max(1, len(user.social_current))
        except Exception as e:
            print(f"Error calculating size for {user.name}: {e}")
            size = 1  # Default size on error
            
        # Add node with explicit size attribute
        G.add_node(user.name, size=size, type="user")
    
    # Then add all edges after nodes are created
    for user in users:
        try:
            if hasattr(user, 'social_current') and user.social_current:
                for friend in user.social_current:
                    if friend and friend.name in G.nodes:  # Safety check
                        G.add_edge(user.name, friend.name)
        except Exception as e:
            print(f"Error adding edges for {user.name}: {e}")

    # Get positions for the nodes in the graph
    if positions is None:
        pos = nx.spring_layout(G, k=0.3, seed=1234)
    else:
        pos = positions
    
    # Create edge traces
    edge_x = []
    edge_y = []
    highlight_edge_x = []
    highlight_edge_y = []
    
    # Find the actual node name in case-insensitive way
    actual_search_name = None
    if search_name:
        search_name_lower = search_name.lower()
        for node in G.nodes():
            if node.lower() == search_name_lower:
                actual_search_name = node
                print(f"Found matching node: {actual_search_name}")
                break
    
    # Add edges to traces
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        if actual_search_name and (edge[0] == actual_search_name or edge[1] == actual_search_name):
            highlight_edge_x.extend([x0, x1, None])
            highlight_edge_y.extend([y0, y1, None])
        else:
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    # Create traces for the graph
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    highlight_edge_trace = go.Scatter(
        x=highlight_edge_x, y=highlight_edge_y,
        line=dict(width=2, color='#E74C3C'),
        hoverinfo='none',
        mode='lines')

    # Create node traces
    node_x = []
    node_y = []
    node_size = []
    node_text = []
    hover_text = []
    node_color = []
    
    # Add nodes to traces with safe access to size attribute
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Safely access the size attribute with a default value
        try:
            size_value = G.nodes[node].get('size', 1)  # Use .get() with default value
            node_size.append(size_value * 3 + 5)  # Scale size for visibility
        except Exception as e:
            print(f"Error accessing size for node {node}: {e}")
            node_size.append(8)  # Default size
            
        # Node text and color
        node_text.append(node)  # Always show node name
        hover_text.append(node)
        
        # Highlight the searched node
        if node == actual_search_name:
            node_color.append('#E74C3C')  # Red for searched node
        else:
            # Color gradient based on connections
            try:
                size_value = G.nodes[node].get('size', 1)
                node_color.append(size_value)
            except:
                node_color.append(1)  # Default color value
    
    # Create the node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hovertext=hover_text,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=node_color,
            size=node_size,
            colorbar=dict(
                thickness=15,
                title='Friend Count',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2, color='DarkSlateGrey')
        ),
        textposition="top center"
    )
    
    # Create figure
    fig = go.Figure(data = [edge_trace, highlight_edge_trace, node_trace],
                   layout = go.Layout(
                       showlegend = False,
                       hovermode = "closest",
                       margin = dict(b = 20, l = 5, r = 5, t = 40),
                       xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
                       yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)))
    
    # Zoom to the searched node's neighborhood if found
    if actual_search_name and actual_search_name in G.nodes:
        relevant_positions = [pos[actual_search_name]]
        for neighbor in G.neighbors(actual_search_name):
            relevant_positions.append(pos[neighbor])
        
        x_coords = [p[0] for p in relevant_positions]
        y_coords = [p[1] for p in relevant_positions]
        
        if x_coords and y_coords:
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            padding = 0.2  # More padding for better view
            x_range = [x_min - padding, x_max + padding]
            y_range = [y_min - padding, y_max + padding]
            
            fig.update_layout(
                xaxis = dict(range = x_range, showgrid = False, zeroline = False, showticklabels = False),
                yaxis = dict(range = y_range, showgrid = False, zeroline = False, showticklabels = False)
            )
            
            # Add title indicating the search
            fig.update_layout(
                title = f"Showing connections for: {actual_search_name}",
                titlefont = dict(size = 16)
            )
    
    return fig, pos

def plot_romantic_connections(users: list, search_name: str = None, positions = None) -> tuple:
    """Create a graph visualization showing romantic connections between users"""
    G = nx.Graph()

    # First add all users as nodes with default size
    for user in users:
        G.add_node(user.name, gender=user.gender if hasattr(user, 'gender') else 'Unknown', size=10)
    
    # Then add edges for romantic connections
    for user in users:
        try:
            if hasattr(user, 'romantic_current') and user.romantic_current is not None:
                # Handle both single object and list cases
                if isinstance(user.romantic_current, list):
                    for partner in user.romantic_current:
                        if partner and partner.name in G.nodes:  # Safety check
                            G.add_edge(user.name, partner.name)
                else:
                    if user.romantic_current and user.romantic_current.name in G.nodes:  # Safety check
                        G.add_edge(user.name, user.romantic_current.name)
        except Exception as e:
            print(f"Error adding romantic edges for {user.name}: {e}")

    if positions is None:
        pos = nx.spring_layout(G, k = 0.3, seed = 1234)
    else:
        pos = positions
    
    # Create edge traces
    edge_x = []
    edge_y = []
    highlight_edge_x = []
    highlight_edge_y = []
    
    # Find the actual node name in case-insensitive way
    actual_search_name = None
    if search_name:
        search_name_lower = search_name.lower()
        # Print search info for debugging
        print(f"Searching for romantic connections: {search_name_lower}")
        
        # Case-insensitive search for the node
        for node in G.nodes():
            if node.lower() == search_name_lower:
                actual_search_name = node
                print(f"Found matching node: {actual_search_name}")
                break
    
    # Add edges to appropriate traces
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        if actual_search_name and (edge[0] == actual_search_name or edge[1] == actual_search_name):
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
    
    # Add nodes to traces
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        hover_text.append(f"{node}")
        node_size.append(15)
        
        # Use different color scheme for romantic graph (reds/pinks instead of blues)
        if actual_search_name:
            if node == actual_search_name:
                node_color.append("#E74C3C")  # Red for the searched node
            elif node in G.neighbors(actual_search_name):
                node_color.append("#FF85A2")  # Pink for connected nodes 
            else:
                node_color.append("rgba(200,200,200,0.5)")  # Other nodes faded out
        else:
            node_color.append("#F5A9BC")  # Light pink default
    
    # Create traces
    edge_trace = go.Scatter(
        x = edge_x, y = edge_y,
        line = dict(width = 0.7, color = "#FF85A2"),  # Pink edges for romantic
        hoverinfo = "none",
        mode = "lines")
    
    highlight_edge_trace = go.Scatter(
        x = highlight_edge_x, y = highlight_edge_y,
        line = dict(width = 2.0, color = "#E74C3C"),  # Red highlight for romantic
        hoverinfo = "none",
        mode = "lines")
    
    node_trace = go.Scatter(
        x = node_x, y = node_y,
        mode = "markers+text",
        text = node_text,
        textposition = "top center",
        textfont = dict(size = 12),
        hoverinfo = "text",
        hovertext = hover_text,
        marker = dict(
            color = node_color,
            size = node_size,
            line = dict(width = 1, color = "#440000")))  # Darker border for romantic nodes
    
    # Create figure with romantic theme colors
    fig = go.Figure(data = [edge_trace, highlight_edge_trace, node_trace],
                   layout = go.Layout(
                       showlegend = False,
                       hovermode = "closest",
                       margin = dict(b = 20, l = 5, r = 5, t = 40),
                       plot_bgcolor="#FFF9F9",  # Very light pink background
                       xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
                       yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)))
    
    # Zoom to the searched node's romantic neighborhood if found
    if actual_search_name and actual_search_name in G.nodes:
        relevant_positions = [pos[actual_search_name]]
        for neighbor in G.neighbors(actual_search_name):
            relevant_positions.append(pos[neighbor])
        
        x_coords = [p[0] for p in relevant_positions]
        y_coords = [p[1] for p in relevant_positions]
        
        if x_coords and y_coords:
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            padding = 0.2  # More padding for better view
            x_range = [x_min - padding, x_max + padding]
            y_range = [y_min - padding, y_max + padding]
            
            fig.update_layout(
                xaxis = dict(range = x_range, showgrid = False, zeroline = False, showticklabels = False),
                yaxis = dict(range = y_range, showgrid = False, zeroline = False, showticklabels = False)
            )
            
            # Add title indicating the romantic search
            fig.update_layout(
                title = f"Showing romantic connections for: {actual_search_name}",
                titlefont = dict(size = 16, color = "#E74C3C")
            )
    
    return fig, pos

def count_romantic_connections(user):
    """
    Helper function to correctly count romantic connections.
    """
    if not hasattr(user, 'romantic_current') or user.romantic_current is None:
        return 0
        
    # Check if it's a list (should be a single object but just in case)
    if isinstance(user.romantic_current, list):
        return len(user.romantic_current)
    else:
        # It's a single object (or should be)
        return 1 if user.romantic_current else 0

def create_app(user_list=None):
    """Create and return a Dash app instance with multiple tabs for different network views
    
    Args:
        user_list: Optional list of User objects to use instead of generating new ones
    """
    # Import the necessary modules at the function level
    # This prevents circular imports
    from dash import Dash, html, dcc, Input, Output, State, callback_context, dash_table
    import plotly.graph_objects as go
    
    # Store the provided user list in a globally scoped variable
    global initial_user_list, node_positions, initial_fig
    
    # Use provided user list or generate a new one
    if user_list is not None:
        initial_user_list = user_list
        print(f"Using provided user list with {len(initial_user_list)} users")
    else:
        # Import the user network functions here to avoid circular imports
        from user_network import generate_users_with_class, add_fixed_users
        initial_user_list = generate_users_with_class(200, 25, 1234)
        add_fixed_users(initial_user_list)
        print(f"Generated new user list with {len(initial_user_list)} users")
    
    # Generate the initial graph and node positions for social connections 
    initial_social_fig, social_node_positions = plot_user_connections(user_looking_for_friends)
    initial_romantic_fig, romantic_node_positions = plot_romantic_connections(user_looking_for_love)
    
    # Create the Dash app
    app = Dash(__name__, suppress_callback_exceptions=True)
    
    # Define the layout with tabs
    app.layout = html.Div([
        # App title
        html.H1("Destiny Network Visualization", 
               style={
                   'textAlign': 'center',
                   'color': '#2C3E50',
                   'marginTop': '20px',
                   'marginBottom': '20px',
                   'fontFamily': 'Arial, sans-serif'
               }),
        
        # Top controls div with search input and buttons
        html.Div([
            dcc.Input(id="search-input", type="text", placeholder="Enter user name",
                     style={'margin': '10px', 'padding': '8px', 'borderRadius': '4px', 'width': '250px'}),
            html.Button("Search", id="search-button",
                       style={'margin': '10px', 'padding': '8px', 'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none', 'borderRadius': '4px'}),
            html.Button("Reset", id="reset-button",
                       style={'margin': '10px', 'padding': '8px', 'backgroundColor': '#f44336', 'color': 'white', 'border': 'none', 'borderRadius': '4px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '10px'}),
        
        # Clicked node output
        html.Div(
            id="clicked-node-output",  
            style={
                'textAlign': 'center',
                'fontSize': '18px',
                'fontWeight': 'bold',
                'padding': '10px',
                'margin': '10px 0',
                'color': '#2C3E50'
            }
        ),
        
        # Tabs component
        dcc.Tabs(id='graph-tabs', value='social-tab', children=[
            dcc.Tab(label='Social Connections', value='social-tab', children=[
                html.Div([
                    html.H3("User Social Network", 
                           style={'textAlign': 'center', 'color': '#3498DB', 'marginTop': '20px'}),
                    html.P("This graph shows social connections between users in the network.",
                          style={'textAlign': 'center', 'fontStyle': 'italic', 'marginBottom': '20px'}),
                    dcc.Graph(id="social-graph", figure=initial_social_fig, style={'height': '120vh'})
                ])
            ]),
            dcc.Tab(label='Romantic Connections', value='romantic-tab', children=[
                html.Div([
                    html.H3("User Romantic/Dating Network", 
                           style={'textAlign': 'center', 'color': '#E74C3C', 'marginTop': '20px'}),
                    html.P("This graph shows potential romantic connections between users in the network.",
                          style={'textAlign': 'center', 'fontStyle': 'italic', 'marginBottom': '20px'}),
                    dcc.Graph(id="romantic-graph", figure=initial_romantic_fig, style={'height': '120vh'})
                ])
            ])
        ], style={'fontFamily': 'Arial, sans-serif'}),
        
        # Footer with stats
        html.Div([
            html.Hr(),
            html.P(f"Network size: {len(initial_user_list)} users", 
                  style={'textAlign': 'center', 'color': '#7F8C8D'})
        ], style={'marginTop': '20px'})
        
    ], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1800px', 'margin': '0 auto', 'padding': '20px'})

    # Define the callbacks for the active tab
    @app.callback(
    [Output("social-graph", "figure"), 
     Output("romantic-graph", "figure"), 
     Output("clicked-node-output", "children")],
    [Input("search-button", "n_clicks"), 
     Input("reset-button", "n_clicks"),
     Input("social-graph", "clickData"),
     Input("romantic-graph", "clickData"),
     Input("graph-tabs", "value")],
    [State("search-input", "value")]
)
    def update_graphs(search_clicks, reset_clicks, social_click_data, romantic_click_data, active_tab, search_name):
        ctx = callback_context
        
        if not ctx.triggered:
            return initial_social_fig, initial_romantic_fig, ""

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_type = ctx.triggered[0]['prop_id'].split('.')[1] if '.' in ctx.triggered[0]['prop_id'] else None
        
        social_fig = initial_social_fig
        romantic_fig = initial_romantic_fig
        output_text = ""
        
        # Handle reset button click
        if button_id == "reset-button":
            social_fig, _ = plot_user_connections(user_looking_for_friends, positions=social_node_positions)
            romantic_fig, _ = plot_romantic_connections(user_looking_for_love, positions=romantic_node_positions)  # Fixed: use plot_romantic_connections
            output_text = ""
        
        # Handle search button click
        elif button_id == "search-button" and search_name:
            print(f"Search button clicked for: {search_name}")
            
            # Normalize search name by stripping whitespace
            search_name = search_name.strip()
            
            # Generate figures with the search term
            social_fig, _ = plot_user_connections(user_looking_for_friends, search_name, social_node_positions)
            romantic_fig, _ = plot_romantic_connections(user_looking_for_love, search_name, romantic_node_positions)
            
            # Find user with case-insensitive search
            selected_user = next(
                (u for u in user_looking_for_friends if u.name.lower() == search_name.lower()), 
                next(
                    (u for u in user_looking_for_love if u.name.lower() == search_name.lower()),
                    None
                )
            )
            
            if selected_user:
                # Calculate friend count based directly on social_current
                friend_count = len(selected_user.social_current) if hasattr(selected_user, 'social_current') and selected_user.social_current else 0
                
                # Use the helper function for romantic count
                romantic_count = count_romantic_connections(selected_user)
                
                output_text = html.Div([
                    html.Div([
                        "Found user: ",
                        html.Span(selected_user.name, style={'color': '#4CAF50', 'fontWeight': 'bold'})
                    ]),
                    html.Div([
                        html.Span(f"Social connections: {friend_count}", style={'marginRight': '20px'}),
                        html.Span(f"Romantic partners: {romantic_count}")
                    ], style={'marginTop': '5px', 'fontSize': '16px'})
                ])
        
        # Handle node click in social graph
        # Replace the incomplete social graph click handler (around line 487-491) with this:

        # Handle node click in social graph
        elif button_id == "social-graph" and prop_type == "clickData" and social_click_data:
            try:
                # Debug to see what's in the click data
                print("Social click data:", social_click_data)
                
                # Access the point data more safely
                if 'points' in social_click_data and len(social_click_data['points']) > 0:
                    point = social_click_data['points'][0]
                    # Try to get the node name from various possible properties
                    clicked_node = None
                    if 'hovertext' in point:
                        clicked_node = point['hovertext']
                    elif 'text' in point:
                        clicked_node = point['text']
                    elif 'customdata' in point:
                        clicked_node = point['customdata']
                    
                    if clicked_node:
                        social_fig, _ = plot_user_connections(user_looking_for_friends, clicked_node, social_node_positions)
                        romantic_fig, _ = plot_romantic_connections(user_looking_for_love, clicked_node, romantic_node_positions)
                        
                        # Find user with case-insensitive search
                        selected_user = next(
                            (u for u in user_looking_for_friends if u.name == clicked_node), 
                            next(
                                (u for u in user_looking_for_love if u.name == clicked_node),
                                None
                            )
                        )
                        
                        if selected_user:
                            # Calculate friend count based directly on social_current
                            friend_count = len(selected_user.social_current) if hasattr(selected_user, 'social_current') and selected_user.social_current else 0
                            
                            # Use the helper function for romantic count
                            romantic_count = count_romantic_connections(selected_user)
                            
                            output_text = html.Div([
                                html.Div([
                                    "Found user: ",
                                    html.Span(selected_user.name, style={'color': '#4CAF50', 'fontWeight': 'bold'})
                                ]),
                                html.Div([
                                    html.Span(f"Social connections: {friend_count}", style={'marginRight': '20px'}),
                                    html.Span(f"Romantic partners: {romantic_count}")
                                ], style={'marginTop': '5px', 'fontSize': '16px'})
                            ])
                        else:
                            output_text = "User data not found"
                    else:
                        output_text = "Click missed or was on a non-node element"
                else:
                    output_text = "No point data in click"
                    
            except Exception as e:
                print(f"Error handling social graph click: {e}")
                output_text = f"Error processing click: {str(e)}"

        # Handle node click in romantic graph
        elif button_id == "romantic-graph" and prop_type == "clickData" and romantic_click_data:
            try:
                # Debug output to see the exact structure
                print("Romantic click data:", romantic_click_data)
                
                # Access the point data safely
                if 'points' in romantic_click_data and len(romantic_click_data['points']) > 0:
                    point = romantic_click_data['points'][0]
                    clicked_node = None
                    
                    # Extract the node name from multiple possible sources
                    if 'hovertext' in point:
                        # More robust parsing of the hovertext
                        hover = point['hovertext']
                        if '\n' in hover:
                            clicked_node = hover.split('\n')[0]
                        else:
                            clicked_node = hover
                    elif 'text' in point and point['text']:
                        clicked_node = point['text']
                    elif 'customdata' in point:
                        clicked_node = point['customdata']
                    elif 'pointNumber' in point and 'curveNumber' in point:
                        # If we can get the index, use it to find the node in the graph
                        curve_num = point['curveNumber']
                        point_num = point['pointNumber']
                        print(f"Looking for node at curve {curve_num}, point {point_num}")
                    
                    print(f"Extracted clicked node: {clicked_node}")
                    
                    if clicked_node:
                        # Update both graphs
                        social_fig, _ = plot_user_connections(user_looking_for_friends, clicked_node, social_node_positions)
                        romantic_fig, _ = plot_romantic_connections(user_looking_for_love, clicked_node, romantic_node_positions)
                        
                        # Find user with case-insensitive search
                        selected_user = next(
                            (u for u in user_looking_for_friends if u.name == clicked_node), 
                            next(
                                (u for u in user_looking_for_love if u.name == clicked_node),
                                None
                            )
                        )
                        
                        if selected_user:
                            # Calculate friend count based directly on social_current
                            friend_count = len(selected_user.social_current) if hasattr(selected_user, 'social_current') and selected_user.social_current else 0
                            
                            # Use the helper function for romantic count
                            romantic_count = count_romantic_connections(selected_user)
                            
                            output_text = html.Div([
                                html.Div([
                                    "Found user: ",
                                    html.Span(selected_user.name, style={'color': '#4CAF50', 'fontWeight': 'bold'})
                                ]),
                                html.Div([
                                    html.Span(f"Social connections: {friend_count}", style={'marginRight': '20px'}),
                                    html.Span(f"Romantic partners: {romantic_count}")
                                ], style={'marginTop': '5px', 'fontSize': '16px'})
                            ])
                        else:
                            output_text = f"User data not found for {clicked_node}"
                    else:
                        output_text = "Couldn't determine which node was clicked"
                else:
                    output_text = "No point data in click"
            except Exception as e:
                print(f"Error handling romantic graph click: {e}")
                output_text = f"Error processing click: {str(e)}"

        # Return appropriate output based on active tab
        return social_fig, romantic_fig, output_text
    
    # Return the app instance
    return app

app = create_app()

def find_available_port(start=8050, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start, start + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None  # No available ports found

if __name__ == "__main__":
    # When run directly, find an available port
    port = find_available_port(8050)
    if port:
        print(f"Starting server on port {port}")
        app.run(debug=True, port=port)
    else:
        print("No available ports found. Try closing other applications.")