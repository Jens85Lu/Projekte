import json
import numpy as np
import matplotlib.pyplot as plt

with open("orbitals/orbital_n6_l4_m2_complex.json") as f:
    data = json.load(f)

points = data["points"]

x = np.array([p["x"] for p in points])
y = np.array([p["y"] for p in points])
z = np.array([p["z"] for p in points])

psi_re = np.array([p["psi_re"] for p in points])
psi_im = np.array([p["psi_im"] for p in points])

# Compute phase
phase = np.arctan2(psi_im, psi_re)

prob = psi_re**2 + psi_im**2
mask = prob > np.percentile(prob, 20)  # Filter out low-probability points
x,y,z,phase = x[mask], y[mask], z[mask], phase[mask]
sign = np.sign(psi_re[mask])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

#sc = ax.scatter(x, y, z, c=sign, s=5, cmap='bwr')
sc = ax.scatter(x, y, z, c=phase, s=5)
ax.view_init(elev=0, azim=45)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Orbital n=2, l=1, m=0 (color = phase)")  # Updated title to reflect phase coloring

plt.colorbar(sc, label="Phase")

plt.show()