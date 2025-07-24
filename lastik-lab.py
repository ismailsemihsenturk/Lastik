# ==============================================================================
# STRASSEN:
    # M1 = (a+d) * (e+h)
    # M2 = (c+d) * e
    # M3 = a * (f-h)
    # M4 = d * (g-e)
    # M5 = (a+b) * h
    # M6 = (c-a) * (e+f)
    # M7 = (b-d) * (g+h)

    # P = M1 + M4 - M5 + M7
    # Q = M3 + M5
    # R = M2 + M4
    # S = M1 - M2 + M3 + M6

# ==============================================================================

import matplotlib.pyplot as plt
import numpy as np

# ==============================================================================
# 1. ""LASTIK Genome Database": The final map deciphered by me.
# ==============================================================================
SHAPE_DATABASE = {
    # --- Single combination ---
    'single_1': {'a': 1, 'b': 1, 'fase_pi': 0.5},   # Circle
    'single_2': {'a': 2, 'b': 1, 'fase_pi': 1.5},   # C
    'single_3': {'a': 2, 'b': 1, 'fase_pi': 0.5},   # C inverse
    'single_4': {'a': 1, 'b': 1, 'fase_pi': 0.5},   # Circle (same as the single_1)

    # --- Double combination ---
    'double_1': {'a': -1.49, 'b': 0.375, 'fase_pi': 0},
    'double_2': {'a': 1.49, 'b': 0.375, 'fase_pi': 0},
    'double_3': {'a': 2, 'b': 1, 'fase_pi': 1.0},
    'double_4': {'a': 1, 'b': 1, 'fase_pi': 0.5},
    'double_5': {'a': -1.49, 'b': -0.375, 'fase_pi': 0},
    'double_6': {'a': 1.49, 'b': -0.375, 'fase_pi': 0},
    
    # --- Triple combination ---
    'triple_1': {'a': 2, 'b': 1, 'fase_pi': 1.0}, # Nuancer bow tie
    'triple_2': {'a': 3, 'b': 1, 'fase_pi': 1.5, 't_range_pi': (0.17, 1.83)}, # Mysterious shape 2 (symmetry of Mysterious shape 1 )
    'triple_3': {'a': 3, 'b': 1, 'fase_pi': 0.5, 't_range_pi': (0.17, 1.83)}, # Mysterious shape 2 (symmetry of Mysterious shape 1 )
    'triple_4': {'a': 2, 'b': 1, 'fase_pi': 1.0}, # Nuancer bow tie

    # --- LASTİK ---
    'lastik_complete': {'a': 3, 'b': 1, 'fase_pi': 0.5},
}

# ==============================================================================
# 2. Visual World: Motor Reading and Drawing from the Database
# ==============================================================================
class LissajousMotoru:
    def __init__(self, ax):
        self.ax = ax

    def draw(self, shape_id, center=(0,0), scale=1.0, color='darkorange', label=""):
        """
        It takes a shape identity, reads and draws the full recipe from the database.
        """
        recipe = SHAPE_DATABASE.get(shape_id)
        if not recipe:
            self.ax.text(0.5, 0.5, f"Error:\n'{shape_id}'\n not defined.", 
                         ha='center', va='center', color='red', fontsize=10)
            self.ax.axis('off'); self.ax.set_title(f"Unknown ID: '{shape_id}'")
            return

        # Read all parameters from the database
        a = recipe.get('a', 1.0)
        b = recipe.get('b', 1.0)
        fase_pi = recipe.get('fase_pi', 0.0)
        # Vital Feature: t_range now comes from the database!
        t_range_pi = recipe.get('t_range_pi', (0, 2))
        
        t = np.linspace(t_range_pi[0] * np.pi, t_range_pi[1] * np.pi, 400)

        # Basic Lissajous Formulas
        x = scale * np.sin(a * t + fase_pi * np.pi)
        y = scale * 1.5 * np.sin(b * t)
        
        self.ax.plot(x + center[0], y + center[1], color=color, lw=4)
        self.ax.text(center[0] + scale * 1.5, center[1], label, 
                     ha='center', va='center', fontsize=16, color=color, weight='bold')
        
        self.ax.set_aspect('equal'); self.ax.margins(0.5); self.ax.axis('off')
        self.ax.set_title(f"'{shape_id}'", pad=15, fontsize=12)


# ==============================================================================
# Main Program: Visualization of my genome map
# ==============================================================================
if __name__ == "__main__":
    
    # List of shapes to be shown
    shapes_to_show = [
        'single_1', 'single_2', 'single_3',
        'double_1', 'double_3', 'double_5',
        'triple_2', 'triple_3', 'lastik_complete'
    ]
    
    # Dynamically adjust the grid size to provide sufficient space
    num_shapes = len(shapes_to_show)
    cols = 3
    rows = (num_shapes + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5))
    fig.canvas.manager.set_window_title('Deciphered genome library')
    
    # Draw each shape in your own field
    for i, shape_id in enumerate(shapes_to_show):
        ax = axes.flatten()[i]
        motor = LissajousMotoru(ax)
        motor.draw(shape_id)

    # Hide the remaining empty subplots
    for i in range(num_shapes, len(axes.flatten())):
        axes.flatten()[i].axis('off')

    plt.tight_layout()
    plt.show()