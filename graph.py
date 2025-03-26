from user_network import generate_users_with_class, add_fixed_users, User

import plotly.graph_objects as go
import networkx as nx
from dash import Dash, dcc, html, Input, Output, State, callback_context

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

app = Dash(__name__)

# Generate the initial graph and node positions
initial_user_list = generate_users_with_class(200, 25, 1234)
add_fixed_users(initial_user_list)
initial_fig, node_positions = plot_user_connections(initial_user_list)

app.layout = html.Div([
    dcc.Input(id = "search-input", type = "text", placeholder = "Enter user name"),
    html.Button("Search", id = "search-button"),
    html.Button("Reset", id = "reset-button"),
    html.Div(id = "clicked-node-output"),  # Add an output area to display clicked node
    dcc.Graph(id = "user-graph", figure = initial_fig)
])

@app.callback(
    [Output("user-graph", "figure"), Output("clicked-node-output", "children")],
    [Input("search-button", "n_clicks"), 
     Input("reset-button", "n_clicks"),
     Input("user-graph", "clickData")],  # Add clickData as an input
    [State("search-input", "value")]
)
def update_graph(search_clicks, reset_clicks, click_data, search_name):
    ctx = callback_context
    
    if not ctx.triggered:
        return initial_fig, ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    prop_type = ctx.triggered[0]['prop_id'].split('.')[1] if '.' in ctx.triggered[0]['prop_id'] else None
    
    clicked_node = ""
    
    # Handle reset button click
    if button_id == "reset-button":
        reset_fig, _ = plot_user_connections(initial_user_list, positions=node_positions)
        return reset_fig, ""
    
    # Handle search button click
    elif button_id == "search-button" and search_name:
        search_fig, _ = plot_user_connections(initial_user_list, search_name, node_positions)
        return search_fig, f"Searched for: {search_name}"
    
    # Handle node click
    elif button_id == "user-graph" and prop_type == "clickData" and click_data:
        # Extract the node name from the click data
        try:
            clicked_node = click_data['points'][0]['hovertext']
            click_fig, _ = plot_user_connections(initial_user_list, clicked_node, node_positions)
            return click_fig, f"Clicked on: {clicked_node}"
        except (KeyError, IndexError):
            # If the click wasn't on a node with hover text
            return initial_fig, "Click missed or was on a non-node element"
    
    # Default return
    return initial_fig, clicked_node

def generate_user_graph():
    app.run_server(debug=True)