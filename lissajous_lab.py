import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox,Slider
import numpy as np

# ==============================================================================
# 1. LISSAJOUS GENERATOR:
# ==============================================================================

def generate_coords(a, b, phase_shift, scale=1.0, points=400, t_range=(0, 2 * np.pi)):
    """
    It produces the coordinates of a shape according to the lisajous parameters given. 
This is our basic experiment tool.
    """
    t = np.linspace(t_range[0], t_range[1], points)
    
    # Basic Lissajous Formulas
    x = scale * np.sin(a * t + phase_shift)
    y = scale * 1.5 * np.sin(b * t) 
    
    return x, y

# ==============================================================================
# 2. Interactive Console (with Time Control)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8, 9))
plt.subplots_adjust(left=0.15, bottom=0.45) 
fig.canvas.manager.set_window_title('Final Discovery Console V25.0')

initial_a = 2.0; initial_b = 1.0; initial_phase_pi = 1.0
initial_t_start_pi = 0.0; initial_t_end_pi = 2.0 # Initially full tour

line, = ax.plot([], [], lw=3, color='darkorange')
ax.set_aspect('equal'); ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.7, 1.7)

# --- Controls ---
# Frequency a
ax_slider_a = plt.axes([0.25, 0.30, 0.65, 0.03])
slider_a = Slider(ax_slider_a, 'Frequency a (Horizontal)', -5.0, 5.0, valinit=initial_a)

# Frequency b
ax_slider_b = plt.axes([0.25, 0.25, 0.65, 0.03])
slider_b = Slider(ax_slider_b, 'Frequency b (Vertical)', -5.0, 5.0, valinit=initial_b)

# Phase difference
ax_slider_phase = plt.axes([0.25, 0.20, 0.65, 0.03])
slider_phase = Slider(ax_slider_phase, 'Phase difference (π times)', 0.0, 2.0, valinit=initial_phase_pi)

# Time Range (T) Controls
ax_slider_t_start = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_t_start = Slider(ax_slider_t_start, 't starting (π times)', 0.0, 2.0, valinit=initial_t_start_pi)
ax_slider_t_end = plt.axes([0.25, 0.10, 0.65, 0.03])
slider_t_end = Slider(ax_slider_t_end, 't ending (π times)', 0.0, 2.0, valinit=initial_t_end_pi)

# ==============================================================================
# 3. UPDATE SYSTEM
# ==============================================================================
def update(val):
    a = slider_a.val; b = slider_b.val; phase_pi = slider_phase.val
    t_start_pi = slider_t_start.val; t_end_pi = slider_t_end.val
    
    # If the start is greater than the end, don't draw anything
    if t_start_pi >= t_end_pi:
        line.set_data([], [])
    else:
        phase_rad = phase_pi * np.pi
        t_range = (t_start_pi * np.pi, t_end_pi * np.pi)
        new_x, new_y = generate_coords(a, b, phase_rad, t_range=t_range)
        line.set_data(new_x, new_y)
    
    ax.set_title(f"a/b = {a:.2f}:{b:.2f}, φ = {phase_pi:.2f}π, t=[{t_start_pi:.2f}π, {t_end_pi:.2f}π]", fontsize=12)
    fig.canvas.draw_idle()

# --- Connect the controls ---
slider_a.on_changed(update); slider_b.on_changed(update)
slider_phase.on_changed(update); slider_t_start.on_changed(update)
slider_t_end.on_changed(update)

update(None)
plt.show()