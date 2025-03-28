from user_network import generate_users_with_class, add_fixed_users, User

import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, callback_context
import networkx as nx

def plot_user_connections(users: list, search_name: str = None, positions = None) -> go.Figure:
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
    
    if search_name:
        search_name_lower = search_name.lower()
    else:
        search_name_lower = None

    actual_search_name = None
    
    if search_name_lower:
        for node in G.nodes():
            if node.lower() == search_name_lower:
                actual_search_name = node
                break
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        # If we're searching and this edge connects to the search node
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
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_size.append(G.nodes[node]["size"] * 3 + 5)
        node_text.append(node if G.nodes[node]["size"] > 5 else "")
        hover_text.append(node)
        
        # Set node color based on search
        if actual_search_name:
            if node == actual_search_name:
                node_color.append("red")
            elif node in G.neighbors(actual_search_name):
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
                       titlefont_size = 16,
                       showlegend = False,
                       hovermode = "closest",
                       margin = dict(b = 20, l = 5, r = 5, t = 40),
                       height = 1800,
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
        if actual_search_name and actual_search_name in G.nodes:
            relevant_positions = [pos[actual_search_name]]
            for neighbor in G.neighbors(actual_search_name):
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
    initial_social_fig, social_node_positions = plot_user_connections(initial_user_list)
    
    # For now, use the same graph for romantic connections (this will be replaced later)
    # When you implement the romantic connections graph, replace this with your new function
    initial_romantic_fig, romantic_node_positions = initial_social_fig, social_node_positions
    
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
            social_fig, _ = plot_user_connections(initial_user_list, positions=social_node_positions)
            romantic_fig, _ = plot_user_connections(initial_user_list, positions=romantic_node_positions)
            output_text = ""
        
        # Handle search button click
        elif button_id == "search-button" and search_name:
            social_fig, _ = plot_user_connections(initial_user_list, search_name, social_node_positions)
            romantic_fig, _ = plot_user_connections(initial_user_list, search_name, romantic_node_positions)
            
            # Get the network stats if found
            selected_user = next((u for u in initial_user_list if u.name.lower() == search_name.lower()), None)
            if selected_user:
                friend_count = selected_user.social_degree
                match_count = len(selected_user.match) if hasattr(selected_user, 'match') else 0
                
                output_text = html.Div([
                    "Searched for: ",
                    html.Span(search_name, style={'color': '#4CAF50'}),
                    html.Div([
                        html.Span(f"Social connections: {friend_count}", style={'marginRight': '20px'}),
                        html.Span(f"Romantic partners: {match_count}")
                    ], style={'marginTop': '5px', 'fontSize': '16px'})
                ])
            else:
                output_text = html.Div([
                    "Searched for: ",
                    html.Span(search_name, style={'color': '#4CAF50'}),
                    html.Div("User not found", style={'marginTop': '5px', 'fontSize': '16px', 'color': '#999'})
                ])
        
        # Handle node click in social graph
        elif button_id == "social-graph" and prop_type == "clickData" and social_click_data:
            try:
                clicked_node = social_click_data['points'][0]['hovertext']
                social_fig, _ = plot_user_connections(initial_user_list, clicked_node, social_node_positions)
                romantic_fig, _ = plot_user_connections(initial_user_list, clicked_node, romantic_node_positions)
                
                # Find the clicked user in our list to get their stats
                selected_user = next((u for u in initial_user_list if u.name == clicked_node), None)
                friend_count = selected_user.social_degree if selected_user else "Unknown"
                match_count = len(selected_user.match) if selected_user and hasattr(selected_user, 'match') else 0
                
                output_text = html.Div([
                    html.Div([
                        "Clicked on: ",
                        html.Span(clicked_node, style={'color': '#3498DB'})
                    ]),
                    html.Div([
                        html.Span(f"Social connections: {friend_count}", style={'marginRight': '20px'}),
                        html.Span(f"Romantic partners: {match_count}")
                    ], style={'marginTop': '5px', 'fontSize': '16px'})
                ])
            except (KeyError, IndexError):
                # If the click wasn't on a node with hover text
                output_text = "Click missed or was on a non-node element"
        
        # Handle node click in romantic graph
        elif button_id == "romantic-graph" and prop_type == "clickData" and romantic_click_data:
            try:
                clicked_node = romantic_click_data['points'][0]['hovertext']
                social_fig, _ = plot_user_connections(initial_user_list, clicked_node, social_node_positions)
                romantic_fig, _ = plot_user_connections(initial_user_list, clicked_node, romantic_node_positions)
                
                # Find the clicked user in our list to get their stats
                selected_user = next((u for u in initial_user_list if u.name == clicked_node), None)
                friend_count = selected_user.social_degree if selected_user else "Unknown"
                match_count = len(selected_user.match) if selected_user and hasattr(selected_user, 'match') else 0
                
                output_text = html.Div([
                    html.Div([
                        "Clicked on: ",
                        html.Span(clicked_node, style={'color': '#E74C3C'})
                    ]),
                    html.Div([
                        html.Span(f"Social connections: {friend_count}", style={'marginRight': '20px'}),
                        html.Span(f"Romantic partners: {match_count}")
                    ], style={'marginTop': '5px', 'fontSize': '16px'})
                ])
            except (KeyError, IndexError):
                # If the click wasn't on a node with hover text
                output_text = "Click missed or was on a non-node element"
        
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