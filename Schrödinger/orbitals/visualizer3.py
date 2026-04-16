import json
import numpy as np
import plotly.graph_objects as go

with open("orbitals/orbital_n6_l4_m2_complex.json") as f:
    data = json.load(f)

points = data["points"]

x = np.array([p["x"] for p in points])
y = np.array([p["y"] for p in points])
z = np.array([p["z"] for p in points])

psi_re = np.array([p["psi_re"] for p in points])
psi_im = np.array([p["psi_im"] for p in points])

prob = psi_re**2 + psi_im**2
phase = np.arctan2(psi_im, psi_re)


mask = prob > np.percentile(prob, 20)  # Filter out low-probability points
x,y,z,phase = x[mask], y[mask], z[mask], phase[mask]
sign = np.sign(psi_re[mask])

print(len(x))
fig = go.Figure(data=[
    go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=4,
            color=sign,
            colorscale='RdBu',
            cmin=-1,
            cmax=1,
            opacity=1.0
        )
    )
])

fig.show()