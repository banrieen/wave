import plotly.graph_objects as go
import pandas as pd

# 示例数据
data = {
    'lat': [34.0522, 40.7128, 51.5074],
    'lon': [-118.2437, -74.0060, -0.1278],
    'alt': [100, 200, 150],
    'city': ['Los Angeles', 'New York', 'London']
}

df = pd.DataFrame(data)

# 创建 3D 散点图对象
fig = go.Figure(data=[go.Scatter3d(
    x=df['lon'],
    y=df['lat'],
    z=df['alt'],
    mode='markers',
    marker=dict(
        size=10,
        color=df.index,  # 设置颜色根据索引
        colorscale='Viridis',
        opacity=0.8
    ),
    text=df['city']
)])

# 设置布局
fig.update_layout(title='3D Map of Cities',
                  scene=dict(
                      xaxis_title='Longitude',
                      yaxis_title='Latitude',
                      zaxis_title='Altitude'
                  ))

# 显示图形
fig.show()