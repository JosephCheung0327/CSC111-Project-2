"""
This program handles the generation of graphs for all users in the network.
Generative AI was used for generating sample templates of implementing visual elements in the web interface.
We modified the generated templates to complete this program.
"""
import socket

import networkx as nx
import plotly.graph_objects as go
import python_ta
from dash import Dash, html, dcc, Input, Output, State, callback_context

from user_network import User, generate_users_with_class, add_fixed_users


def get_romantic_count(user: User, user_looking_for_love: list[User]) -> int:
    """
    Get the number of romantic connections for a user in the network.
    """
    if hasattr(user, 'romantic_current') and user.romantic_current is not None:
        return 1

    # Check if anyone points to this user (handles one-way connections)
    for other_user in user_looking_for_love:
        if other_user != user and hasattr(other_user, 'romantic_current') and other_user.romantic_current is not None:
            if hasattr(other_user.romantic_current, 'name') and other_user.romantic_current.name == user.name:
                return 1

    return 0


def plot_social_connections(users_social: list, search_name: str = None,
                            positions: dict[str, tuple[float, float]] = None) -> tuple:
    """
    Create a graph visualization showing social connections between users.
    """
    graph = nx.Graph()

    user_dict = {user_object.name: user_object for user_object in users_social}

    # Add all users from user_looking_for_friends as nodes
    for user in users_social:
        # Get size based on social connections
        if hasattr(user, 'social_current') and user.social_current:
            valid_friends = [f for f in user.social_current
                             if hasattr(f, 'name') and f.name in user_dict]
            size = max(1, len(valid_friends))
        else:
            size = 1

        graph.add_node(user.name, size=size, type="user")

        for friend in user.social_current:
            graph.add_edge(user.name, friend.name)

    # Get positions for the nodes in the graph
    if positions is None:
        pos = nx.spring_layout(graph, k=0.3, seed=1234)
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
        for node in graph.nodes():
            if node.lower() == search_name_lower:
                actual_search_name = node
                break

    # Add edges to traces
    for edge in graph.edges():
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

    # Add nodes to traces
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        try:
            size_value = graph.nodes[node].get('size', 1)
            node_size.append(size_value * 3 + 5)  # Scale size
        except:
            node_size.append(8)  # Default size

        # Node text and color
        node_text.append(node)
        hover_text.append(node)

        # Highlight the searched node
        if node == actual_search_name:
            node_color.append('#E74C3C')
        else:
            # Color gradient based on connections
            try:
                size_value = graph.nodes[node].get('size', 1)
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
                titlefont=dict(size=20),
                tickfont=dict(size=18),
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2, color='DarkSlateGrey')
        ),
        textposition="top center"
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, highlight_edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode="closest",
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # Zoom to the searched node's neighborhood if found
    if actual_search_name and actual_search_name in graph.nodes:
        relevant_positions = [pos[actual_search_name]]
        for neighbor in graph.neighbors(actual_search_name):
            relevant_positions.append(pos[neighbor])

        x_coords = [p[0] for p in relevant_positions]
        y_coords = [p[1] for p in relevant_positions]

        if x_coords and y_coords:
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            padding = 0.2
            x_range = [x_min - padding, x_max + padding]
            y_range = [y_min - padding, y_max + padding]

            fig.update_layout(
                xaxis=dict(range=x_range, showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=y_range, showgrid=False, zeroline=False, showticklabels=False)
            )

            # Add title indicating the search
            fig.update_layout(
                title=f"Showing connections for: {actual_search_name}",
                titlefont=dict(size=16)
            )

    return fig, pos


def plot_romantic_connections(users_love: list, search_name: str = None,
                              positions: dict[str, tuple[float, float]] = None) -> tuple:
    """
    Create a graph visualization showing romantic connections between users.
    """
    graph_romantic = nx.Graph()

    # Add all users as nodes with default size
    for user in users_love:
        graph_romantic.add_node(user.name, gender=user.gender if hasattr(user, 'gender') else 'Unknown', size=10)

        try:
            if hasattr(user, 'romantic_current') and user.romantic_current is not None:
                if user.romantic_current.name in graph_romantic.nodes:
                    graph_romantic.add_edge(user.name, user.romantic_current.name)
        except:
            pass

    if positions is None:
        pos = nx.spring_layout(graph_romantic, k=0.3, seed=1234)
    else:
        pos = positions

    # Create edge traces
    edge_x = []
    edge_y = []
    highlight_edge_x = []
    highlight_edge_y = []

    actual_search_name = None
    if search_name:
        search_name_lower = search_name.lower()

        # Case-insensitive search for the node
        for node in graph_romantic.nodes():
            if node.lower() == search_name_lower:
                actual_search_name = node
                break

    # Add edges to appropriate traces
    for edge in graph_romantic.edges():
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
    for node in graph_romantic.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        hover_text.append(f"{node}")
        node_size.append(15)

        if actual_search_name:
            if node == actual_search_name:
                node_color.append("#E74C3C")
            elif node in graph_romantic.neighbors(actual_search_name):
                node_color.append("#FF85A2")
            else:
                node_color.append("rgba(200,200,200,0.5)")
        else:
            node_color.append("#F5A9BC")

    # Create traces
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.7, color="#FF85A2"),
        hoverinfo="none",
        mode="lines")

    highlight_edge_trace = go.Scatter(
        x=highlight_edge_x, y=highlight_edge_y,
        line=dict(width=2.0, color="#E74C3C"),
        hoverinfo="none",
        mode="lines")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        textfont=dict(size=12),
        hoverinfo="text",
        hovertext=hover_text,
        marker=dict(
            color=node_color,
            size=node_size,
            line=dict(width=1, color="#440000")))

    # Create figure with romantic theme colors
    fig = go.Figure(data=[edge_trace, highlight_edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode="closest",
                        margin=dict(b=20, l=5, r=5, t=40),
                        plot_bgcolor="#FFF9F9",
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # Zoom to the searched node's romantic neighborhood if found
    if actual_search_name and actual_search_name in graph_romantic.nodes:
        relevant_positions = [pos[actual_search_name]]
        for neighbor in graph_romantic.neighbors(actual_search_name):
            relevant_positions.append(pos[neighbor])

        x_coords = [p[0] for p in relevant_positions]
        y_coords = [p[1] for p in relevant_positions]

        if x_coords and y_coords:
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            padding = 0.2
            x_range = [x_min - padding, x_max + padding]
            y_range = [y_min - padding, y_max + padding]

            fig.update_layout(
                xaxis=dict(range=x_range, showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=y_range, showgrid=False, zeroline=False, showticklabels=False)
            )

            fig.update_layout(
                title=f"Showing romantic connections for: {actual_search_name}",
                titlefont=dict(size=16, color="#E74C3C")
            )

    return fig, pos


def create_app(user_list: list[User] = None, user_looking_for_friends: list[User] = None,
               user_looking_for_love: list[User] = None) -> go.Figure:
    """
    Create and return a Dash app instance with multiple tabs for different network views.
    """

    global initial_user_list, node_positions, initial_fig

    # Use provided user list or generate a new one
    if user_list is not None:
        initial_user_list = user_list
    else:
        initial_user_list = generate_users_with_class(200, 1234)
        add_fixed_users(initial_user_list)

    # Generate the initial graph and node positions for social connections
    initial_social_fig, social_node_positions = plot_social_connections(user_looking_for_friends)
    initial_romantic_fig, romantic_node_positions = plot_romantic_connections(user_looking_for_love)

    app = Dash(__name__)

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
                        style={'margin': '10px', 'padding': '8px', 'backgroundColor': '#4CAF50', 'color': 'white',
                               'border': 'none', 'borderRadius': '4px'}),
            html.Button("Reset", id="reset-button",
                        style={'margin': '10px', 'padding': '8px', 'backgroundColor': '#f44336', 'color': 'white',
                               'border': 'none', 'borderRadius': '4px'}),
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
                    html.H3("User Dating Network",
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
    def update_graphs(_search_clicks, _reset_clicks, social_click_data, romantic_click_data, _active_tab,
                      search_name) -> tuple:
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
            social_fig, _ = plot_social_connections(user_looking_for_friends, positions=social_node_positions)
            romantic_fig, _ = plot_romantic_connections(user_looking_for_love, positions=romantic_node_positions)
            output_text = ""

        # Handle search button click
        elif button_id == "search-button" and search_name:
            search_name = search_name.strip()

            # Generate figures with the search term
            social_fig, _ = plot_social_connections(user_looking_for_friends, search_name, social_node_positions)
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
                if hasattr(selected_user, "social_current") and selected_user.social_current:
                    friend_count = len(selected_user.social_current)
                else:
                    friend_count = 0
                romantic_count = get_romantic_count(selected_user, user_looking_for_love)

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
        elif button_id == "social-graph" and prop_type == "clickData" and social_click_data:
            try:
                if 'points' in social_click_data and len(social_click_data['points']) > 0:
                    point = social_click_data['points'][0]
                    clicked_node = None
                    if 'hovertext' in point:
                        clicked_node = point['hovertext']
                    elif 'text' in point:
                        clicked_node = point['text']
                    elif 'customdata' in point:
                        clicked_node = point['customdata']

                    if clicked_node:
                        social_fig, _ = plot_social_connections(user_looking_for_friends, clicked_node,
                                                                social_node_positions)
                        romantic_fig, _ = plot_romantic_connections(user_looking_for_love, clicked_node,
                                                                    romantic_node_positions)

                        # Find user with case-insensitive search
                        selected_user = next(
                            (u for u in user_looking_for_friends if u.name == clicked_node),
                            next(
                                (u for u in user_looking_for_love if u.name == clicked_node),
                                None
                            )
                        )

                        if selected_user:
                            if hasattr(selected_user, "social_current") and selected_user.social_current:
                                friend_count = len(selected_user.social_current)
                            else:
                                friend_count = 0
                            romantic_count = get_romantic_count(selected_user, user_looking_for_love)

                            output_text = html.Div([
                                html.Div([
                                    "Clicked on: ",
                                    html.Span(clicked_node, style={'color': '#3498DB', 'fontWeight': 'bold'})
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
                output_text = f"Error processing click: {str(e)}"

        # Handle node click in romantic graph
        elif button_id == "romantic-graph" and prop_type == "clickData" and romantic_click_data:
            try:
                if 'points' in romantic_click_data and len(romantic_click_data['points']) > 0:
                    point = romantic_click_data['points'][0]
                    clicked_node = None

                    if 'hovertext' in point:
                        hover = point['hovertext']
                        if '\n' in hover:
                            clicked_node = hover.split('\n')[0]
                        else:
                            clicked_node = hover
                    elif 'text' in point and point['text']:
                        clicked_node = point['text']
                    elif 'customdata' in point:
                        clicked_node = point['customdata']

                    if clicked_node:
                        # Update both graphs
                        social_fig, _ = plot_social_connections(user_looking_for_friends, clicked_node,
                                                                social_node_positions)
                        romantic_fig, _ = plot_romantic_connections(user_looking_for_love, clicked_node,
                                                                    romantic_node_positions)

                        # Find user with case-insensitive search
                        selected_user = next(
                            (u for u in user_looking_for_friends if u.name == clicked_node),
                            next(
                                (u for u in user_looking_for_love if u.name == clicked_node),
                                None
                            )
                        )

                        if selected_user:
                            if hasattr(selected_user, "social_current") and selected_user.social_current:
                                friend_count = len(selected_user.social_current)
                            else:
                                friend_count = 0
                            romantic_count = get_romantic_count(selected_user, user_looking_for_love)

                            output_text = html.Div([
                                html.Div([
                                    "Clicked on: ",
                                    html.Span(clicked_node, style={'color': '#E74C3C', 'fontWeight': 'bold'})
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
                output_text = f"Error processing click: {str(e)}"

        # Return appropriate output based on active tab
        return social_fig, romantic_fig, output_text

    # Return the app instance
    return app


def find_available_port(start: int = 8050, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port"""
    for port in range(start, start + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None  # No available ports found


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ["user_network", "plotly.graph_objects", "dash", "networkx", "socket"],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'disable': ["R0914", "R1714", "R1735", "W0702", "R0912", "R0915", "R1702", "C0415", "E9997", "E9970",
                    "E9959", "W0718"]
    })
