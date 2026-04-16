import json
import matplotlib.pyplot as plt

# Load JSON
with open("orbitals/orbital_n7_l6_m5_complex.json") as f:
    data = json.load(f)

points = data["points"]

x = [p["x"] for p in points]
y = [p["y"] for p in points]
z = [p["z"] for p in points]

# Optional: probability density |psi|^2
intensity = [
    p["psi_re"]**2 + p["psi_im"]**2
    for p in points
]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

sc = ax.scatter(x, y, z, c=intensity, s=5)
# Look from the top down
ax.view_init(elev=45, azim=45)
# set labeling of axes
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.colorbar(sc, label="|ψ|²")

plt.show()
