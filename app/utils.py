import plotly.graph_objs as go

def render_3d_surface(terrain_data):
    latitudes = [data['latitude'] for data in terrain_data]
    longitudes = [data['longitude'] for data in terrain_data]
    altitudes = [data['altitude'] for data in terrain_data]

    trace = go.Scatter3d(
        x=latitudes,
        y=longitudes,
        z=altitudes,
        mode='markers',
        marker=dict(size=5, color=altitudes, colorscale='Viridis')
    )

    layout = go.Layout(
        title='3D Terrain Surface',
        scene=dict(
            xaxis_title='Latitude',
            yaxis_title='Longitude',
            zaxis_title='Altitude'
        )
    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.show()
