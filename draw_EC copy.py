import numpy as np
import matplotlib.pyplot as plt

# Define the elliptic curve parameters: y^2 = x^3 + ax + b
a = -2
b = 2

# Generate x values for plotting the elliptic curve
x = np.linspace(-3, 3, 600)  # Wider range for better visualization
y_squared = x**3 + a*x + b

# Filter out negative values since y^2 must be non-negative
valid_x = x[y_squared >= 0]
valid_y = np.sqrt(y_squared[y_squared >= 0])

# Function to find y values for given x on the elliptic curve
def get_y_values(x_val, a, b):
    y2 = x_val**3 + a*x_val + b
    if y2 >= 0:
        return np.sqrt(y2), -np.sqrt(y2)  # Two possible y values
    else:
        return None  # No real solutions

# Select two different points P and Q
P_x = -1.5
Q_x = 0.2

P_y_values = get_y_values(P_x, a, b)
Q_y_values = get_y_values(Q_x, a, b)

if P_y_values and Q_y_values:
    P = (P_x, P_y_values[0])  # Upper y-value for P
    Q = (Q_x, Q_y_values[0])  # Upper y-value for Q
else:
    raise ValueError("Chosen x values do not lie on the elliptic curve.")

# ---- Compute Corrected Point Addition ----
m_add = (Q[1] - P[1]) / (Q[0] - P[0])  # Secant slope
x3_add = m_add**2 - P[0] - Q[0]
y3_add = m_add * (P[0] - x3_add) - P[1]

R_add = (x3_add, y3_add)  # Correct R (without extra negation)
R_add_reflected = (x3_add, -y3_add)  # Final reflected point

# ---- Compute Corrected Point Doubling ----
m_double = (3 * P[0]**2 + a) / (2 * P[1])  # Slope for tangent at P
x3_double = m_double**2 - 2 * P[0]
y3_double = m_double * (P[0] - x3_double) - P[1]

R_double = (x3_double, y3_double)  # Correct R (without extra negation)
R_double_reflected = (x3_double, -y3_double)  # Final reflected point

# ---- Plot 1: Enlarged Elliptic Curve Visualization ----
fig1, ax1 = plt.subplots(figsize=(10, 8))
ax1.plot(valid_x, valid_y, color='blue', label=r"$y^2 = x^3 - 2x + 2$")
ax1.plot(valid_x, -valid_y, color='blue')
ax1.set_title("Elliptic Curve (Enlarged)")
ax1.legend()
ax1.axhline(0, color='black', linewidth=1.0)
ax1.axvline(0, color='black', linewidth=1.0)
plt.show()

# ---- Plot 2: Corrected Point Addition with Reflection Line ----
fig2, ax2 = plt.subplots(figsize=(10, 8))
ax2.plot(valid_x, valid_y, color='blue', label="Elliptic Curve")
ax2.plot(valid_x, -valid_y, color='blue')

# Plot points P, Q, R (computed), and -R (reflected)
ax2.scatter(*P, color='red', label="P", s=100)
ax2.scatter(*Q, color='green', label="Q", s=100)
ax2.scatter(*R_add_reflected, color='orange', label="- R", s=100)
ax2.scatter(*R_add, color='purple', label="Final R = P + Q", s=100)

# Draw the secant line
x_line = np.linspace(P[0], Q[0], 100)
y_line = m_add * (x_line - P[0]) + P[1]
ax2.plot(x_line, y_line, 'gray', linestyle="dashed", label="Secant Line")

# Draw vertical reflection line from -R to R
ax2.plot([R_add[0], R_add[0]], [R_add[1], R_add_reflected[1]], 'black', linestyle="dotted", label="Reflection Line")

ax2.set_title("Point Addition")
ax2.legend()
ax2.axhline(0, color='black', linewidth=1.0)
ax2.axvline(0, color='black', linewidth=1.0)
plt.show()

# ---- Plot 3: Corrected Point Doubling with Reflection Line ----
fig3, ax3 = plt.subplots(figsize=(10, 8))
ax3.plot(valid_x, valid_y, color='blue', label="Elliptic Curve")
ax3.plot(valid_x, -valid_y, color='blue')

# Plot points P, 2P (computed), and -2P (reflected)
ax3.scatter(*P, color='red', label="P", s=100)
ax3.scatter(*R_double_reflected, color='orange', label="- 2P", s=100)
ax3.scatter(*R_double, color='purple', label="Final 2P", s=100)


# Draw the tangent line at P
x_line = np.linspace(P[0] - 1.5, P[0] + 1.5, 100)
y_line = m_double * (x_line - P[0]) + P[1]
ax3.plot(x_line, y_line, 'gray', linestyle="dashed", label="Tangent Line")

# Draw vertical reflection line from -2P to 2P
ax3.plot([R_double[0], R_double[0]], [R_double[1], R_double_reflected[1]], 'black', linestyle="dotted", label="Reflection Line")

ax3.set_title("Point Doubling")
ax3.legend()
ax3.axhline(0, color='black', linewidth=1.0)
ax3.axvline(0, color='black', linewidth=1.0)
plt.show()
