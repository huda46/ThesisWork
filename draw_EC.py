import numpy as np
import matplotlib.pyplot as plt

# Define elliptic curve parameters: y^2 = x^3 + ax + b
a = -2
b = 2

# Function to find y values for given x on the elliptic curve
def get_y_values(x_val, a, b):
    y2 = x_val**3 + a*x_val + b
    if y2 >= 0:
        return np.sqrt(y2), -np.sqrt(y2)
    else:
        return None

# Select points P and Q
P_x = -1.5
Q_x = 0.2

P_y_values = get_y_values(P_x, a, b)
Q_y_values = get_y_values(Q_x, a, b)

if P_y_values and Q_y_values:
    P = (P_x, P_y_values[0])  # Use positive y
    Q = (Q_x, Q_y_values[0])
else:
    raise ValueError("Chosen x values do not lie on the elliptic curve.")

# ---- Point Addition ----
m_add = (Q[1] - P[1]) / (Q[0] - P[0])
x3_add = m_add**2 - P[0] - Q[0]
y3_add = m_add * (P[0] - x3_add) - P[1]

R_add = (x3_add, y3_add)
R_add_reflected = (x3_add, -y3_add)

# ---- Point Doubling ----
m_double = (3 * P[0]**2 + a) / (2 * P[1])
x3_double = m_double**2 - 2 * P[0]
y3_double = m_double * (P[0] - x3_double) - P[1]

R_double = (x3_double, y3_double)
R_double_reflected = (x3_double, -y3_double)

# ---- Define Dynamic Plot Ranges ----
all_x_vals = [P[0], Q[0], R_add[0], R_add_reflected[0], R_double[0], R_double_reflected[0]]
all_y_vals = [P[1], Q[1], R_add[1], R_add_reflected[1], R_double[1], R_double_reflected[1]]

x_min = min(all_x_vals) - 1
x_max = max(all_x_vals) + 1
y_min = min(all_y_vals) - 5
y_max = max(all_y_vals) + 5

# Generate curve points
x = np.linspace(x_min, x_max, 1000)
y_squared = x**3 + a*x + b
valid_x = x[y_squared >= 0]
valid_y = np.sqrt(y_squared[y_squared >= 0])

# ---- Plot 1: Elliptic Curve ----
fig1, ax1 = plt.subplots(figsize=(10, 8))
ax1.plot(valid_x, valid_y, color='blue', label=r"$y^2 = x^3 - 2x + 2$")
ax1.plot(valid_x, -valid_y, color='blue')
ax1.set_title("Elliptic Curve")
ax1.axhline(0, color='black')
ax1.axvline(0, color='black')
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
ax1.legend()
plt.show()

# ---- Plot 2: Point Addition ----
fig2, ax2 = plt.subplots(figsize=(10, 8))
ax2.plot(valid_x, valid_y, color='blue', label="Elliptic Curve")
ax2.plot(valid_x, -valid_y, color='blue')

# Plot points
ax2.scatter(*P, color='red', label="P", s=100)
ax2.scatter(*Q, color='green', label="Q", s=100)
ax2.scatter(*R_add_reflected, color='orange', label="- R", s=100)
ax2.scatter(*R_add, color='purple', label="Final R = P + Q", s=100)

# Draw secant line
x_line = np.linspace(P[0], Q[0], 100)
y_line = m_add * (x_line - P[0]) + P[1]
ax2.plot(x_line, y_line, 'gray', linestyle="dashed", label="Secant Line")

# Reflection line
ax2.plot([R_add[0], R_add[0]], [R_add[1], R_add_reflected[1]], 'black', linestyle="dotted", label="Reflection Line")

ax2.set_title("Point Addition")
ax2.axhline(0, color='black')
ax2.axvline(0, color='black')
ax2.set_xlim(x_min, x_max)
ax2.set_ylim(y_min, y_max)
ax2.legend()
plt.show()

# ---- Plot 3: Point Doubling ----
fig3, ax3 = plt.subplots(figsize=(10, 8))
ax3.plot(valid_x, valid_y, color='blue', label="Elliptic Curve")
ax3.plot(valid_x, -valid_y, color='blue')

# Plot points
ax3.scatter(*P, color='red', label="P", s=100)
ax3.scatter(*R_double_reflected, color='orange', label="- 2P", s=100)
ax3.scatter(*R_double, color='purple', label="Final 2P", s=100)

# Tangent line
x_line = np.linspace(P[0] - 1.5, P[0] + 1.5, 100)
y_line = m_double * (x_line - P[0]) + P[1]
ax3.plot(x_line, y_line, 'gray', linestyle="dashed", label="Tangent Line")

# Reflection line
ax3.plot([R_double[0], R_double[0]], [R_double[1], R_double_reflected[1]], 'black', linestyle="dotted", label="Reflection Line")

ax3.set_title("Point Doubling")
ax3.axhline(0, color='black')
ax3.axvline(0, color='black')
ax3.set_xlim(x_min, x_max)
ax3.set_ylim(y_min, y_max)
ax3.legend()
plt.show()
