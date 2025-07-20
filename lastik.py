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
import copy

# ==============================================================================
# 1. "LASTİK GENOM VERİTABANI": SİZİN TARAFINIZDAN DEŞİFRE EDİLEN NİHAİ HARİTA
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
    'triple_2': {'a': 3.33, 'b': 1, 'fase_pi': 1.0, 't_range_pi': (0.2, 1.8)}, # Mysterious shape 1
    'triple_3': {'a': 3.33, 'b': 1, 'fase_pi': 0, 't_range_pi': (0.2, 1.8)}, # Mysterious shape 2 (symmetry of Mysterious shape 1 )
    'triple_4': {'a': 2, 'b': 1, 'fase_pi': 1.0}, # Nuancer bow tie

    # --- LASTİK ---
    'lastik_complete': {'a': 3, 'b': 1, 'fase_pi': 0.5},
}


# ==============================================================================
# 2. Algebraic world: atoms and collision physics
# ==============================================================================
class Atom:
    """A algebraic entity: a shape identity, a value and a burden."""
    def __init__(self, shape_id, value, potantial='+'):
        self.shape_id = shape_id
        self.value = value
        self.potantial = potantial

def collision(molecule1, molecule2):
    """It multiplies two molecules and produces a 'residues soup'."""
    # Collision Physics Rules: This is the translation of my white board.
    COLLISION_RULES = {
        ('single_1', 'single_1'): 'double_3', # a*e, a*h, d*e, d*h...
        ('single_1', 'single_2'): 'double_1', # a*b
        ('single_1', 'single_3'): 'double_1', # a*c (symmetrical)
        ('single_1', 'single_4'): 'double_1', # a*f
        ('single_1', 'single_5'): 'double_1', # a*g (symmetrical)
        ('single_2', 'single_1'): 'double_5', # b*h
        ('single_2', 'single_5'): 'double_6', # b*g
        ('single_3', 'single_1'): 'double_5', # c*e (symmetrical)
        ('single_3', 'single_4'): 'double_6', # c*f (symmetrical)
    }
    soup = []
    for atom1 in molecule1:
        for atom2 in molecule2:
            new_value = atom1.value + atom2.value
            new_potantial = '+' if atom1.potantial == atom2.potantial else '-'
            key = tuple(sorted((atom1.shape_id, atom2.shape_id)))
            new_shape_id = COLLISION_RULES.get(key, 'double_3') # Unknown Collision Produces Papyon by default
            soup.append(Atom(new_shape_id, new_value, new_potantial))
    return soup

def cancel(soup):
    remaining, canceled = [], []; temp_soup = copy.deepcopy(soup)
    while temp_soup:
        atom = temp_soup.pop(0); convention = -1
        for i, another in enumerate(temp_soup):
            if atom.value==another.value and atom.potantial!=another.potantial and atom.shape_id==another.shape_id:
                convention = i; break
        if convention != -1: canceled.extend([atom, temp_soup.pop(convention)])
        else: remaining.append(atom)
    return remaining, canceled

def flip_signs(molekul):
    return [Atom(a.shape_id, a.value, '-' if a.potantial == '+' else '+') for a in molekul]

# ==============================================================================
# 3. Visual World: Smart and Regular Drawing Engine
# ==============================================================================
class LissajousEngine:
    def __init__(self, ax): self.ax = ax
    def _get_recipe(self, shape_id): return SHAPE_DATABASE.get(shape_id)
    def _ciz_tek_atom(self, atom, center, scale=1.0, color='darkorange'):
        recipe = self._get_recipe(atom.shape_id)
        if not recipe: return
        a,b,faz_pi = recipe.get('a',1), recipe.get('b',1), recipe.get('faz_pi',0)
        t_range = recipe.get('t_range_pi', (0, 2))
        transform = recipe.get('transform', {})
        if transform.get('negate_a'): a *= -1
        if transform.get('negate_b'): b *= -1
        t = np.linspace(t_range[0]*np.pi, t_range[1]*np.pi, 400)
        x = scale * np.sin(a * t + faz_pi * np.pi); y = scale * 1.5 * np.sin(b * t)
        self.ax.plot(x + center[0], y + center[1], color=color, lw=4)
        self.ax.text(center[0] + scale*1.2, center[1], atom.value, fontsize=16, color=color, weight='bold')
        self.ax.text(center[0], center[1] + scale*1.5, atom.potantial, fontsize=24, color='red', weight='bold')

    def draw_molecule_group(self, molekul, title="", color='darkorange'):
        self.ax.set_title(title, fontsize=14, pad=20)
        if not molekul: self.ax.axis('off'); return
        
        # Spacing factor has been increased to leave more range.
        spacing = 3.0 
        
        num_atoms = len(molekul)
        cols = int(np.ceil(np.sqrt(num_atoms))) if num_atoms > 1 else 1
        rows = int(np.ceil(num_atoms / cols)) if cols > 0 else 0
        x_pos = np.linspace(-spacing*(cols-1)/2, spacing*(cols-1)/2, cols) if cols > 1 else [0]
        y_pos = np.linspace(spacing*(rows-1)/2, -spacing*(rows-1)/2, rows) if rows > 1 else [0]
        positions = [(x,y) for y in y_pos for x in x_pos]
        for i, atom in enumerate(molekul):
            self._ciz_tek_atom(atom, center=positions[i], scale=0.8, color=color)
            
        # Set the view area according to Spacing
        self.ax.set_xlim(-cols*spacing/1.5, cols*spacing/1.5); self.ax.set_ylim(-rows*spacing/1.5, rows*spacing/1.5)
        self.ax.set_aspect('equal'); self.ax.axis('off')

# ==============================================================================
# 4. P,Q,R,S Scenes: A separate and regular scene for each result
# ==============================================================================
def visualize_P():
    # P = M1 + M4 - M5 + M7
    # Define inputs
    M1_A = [Atom('single_1','a','+'), Atom('single_1','d','+')]; M1_B = [Atom('single_1','e','+'), Atom('single_1','h','+')]
    M4_A = [Atom('single_1','d','+')]; M4_B = [Atom('single_3','g','+'), Atom('single_1','e','-')]
    M5_A = [Atom('single_1','a','+'), Atom('single_2','b','+')]; M5_B = [Atom('single_1','h','+')]
    M7_A = [Atom('single_2','b','+'), Atom('single_1','d','-')]; M7_B = [Atom('single_3','g','+'), Atom('single_1','h','+')]
    # Compute
    m1=collision(M1_A,M1_B); m4=collision(M4_A,M4_B); m5=collision(M5_A,M5_B); m7=collision(M7_A,M7_B)
    soup = m1 + m4 + flip_signs(m5) + m7
    sonuc, iptal = cancel(soup)
    # Visualize
    fig=plt.figure(figsize=(18,12)); fig.suptitle("Analysis scene: P = M1+M4-M5+M7", fontsize=20)
    LissajousEngine(fig.add_subplot(2,2,1)).draw_molecule_group(soup, "Total remaning soup")
    LissajousEngine(fig.add_subplot(2,2,2)).draw_molecule_group(iptal, "CANCELED", color='lightgray')
    LissajousEngine(fig.add_subplot(2,2,3)).draw_molecule_group(sonuc, "Final result: P", color='green')
    plt.show()

def visualize_Q():
    M3_A=[Atom('single_1','a','+')]; M3_B=[Atom('single_2','f','+'), Atom('single_1','h','-')]
    M5_A=[Atom('single_1','a','+'), Atom('single_2','b','+')]; M5_B=[Atom('single_1','h','+')]
    m3=collision(M3_A,M3_B); m5=collision(M5_A,M5_B); soup=m3+m5
    sonuc, iptal = cancel(soup)
    fig=plt.figure(figsize=(12,12)); fig.suptitle("Analysis scene: Q = M3+M5", fontsize=20)
    LissajousEngine(fig.add_subplot(2,2,1)).draw_molecule_group(m3, "Remainings From M3")
    LissajousEngine(fig.add_subplot(2,2,2)).draw_molecule_group(m5, "Remainings From M5")
    LissajousEngine(fig.add_subplot(2,2,3)).draw_molecule_group(iptal, "CANCELED", color='lightgray')
    LissajousEngine(fig.add_subplot(2,2,4)).draw_molecule_group(sonuc, "Final result: Q", color='green')
    plt.show()

def visualize_R():
    # R = M2 + M4
    M2_A = [Atom('single_3','c','+'), Atom('single_1','d','+')]; M2_B = [Atom('single_1','e','+')]
    M4_A = [Atom('single_1','d','+')]; M4_B = [Atom('single_3','g','+'), Atom('single_1','e','-')]
    m2=collision(M2_A,M2_B); m4=collision(M4_A,M4_B); soup=m2+m4
    sonuc, iptal = cancel(soup)
    fig=plt.figure(figsize=(12,12)); fig.suptitle("Analysis scene: R = M2+M4", fontsize=20)
    LissajousEngine(fig.add_subplot(2,2,1)).draw_molecule_group(soup, "Total remaning soup")
    LissajousEngine(fig.add_subplot(2,2,2)).draw_molecule_group(iptal, "CANCELED", color='lightgray')
    LissajousEngine(fig.add_subplot(2,2,3)).draw_molecule_group(sonuc, "Final result: R", color='green')
    plt.show()

def visualize_S():
    # S = M1 - M2 + M3 + M6
    M1_A = [Atom('single_1','a','+'), Atom('single_1','d','+')]; M1_B = [Atom('single_1','e','+'), Atom('single_1','h','+')]
    M2_A = [Atom('single_3','c','+'), Atom('single_1','d','+')]; M2_B = [Atom('single_1','e','+')]
    M3_A = [Atom('single_1','a','+')]; M3_B = [Atom('single_2','f','+'), Atom('single_1','h','-')]
    M6_A = [Atom('single_3','c','+'), Atom('single_1','a','-')]; M6_B = [Atom('single_1','e','+'), Atom('single_2','f','+')]
    m1=collision(M1_A,M1_B); m2=collision(M2_A,M2_B); m3=collision(M3_A,M3_B); m6=collision(M6_A,M6_B)
    soup = m1 + flip_signs(m2) + m3 + m6
    sonuc, iptal = cancel(soup)
    fig=plt.figure(figsize=(20,15)); fig.suptitle("Analysis scene: S = M1-M2+M3+M6", fontsize=20)
    LissajousEngine(fig.add_subplot(2,2,1)).draw_molecule_group(soup, "Total remaning soup")
    LissajousEngine(fig.add_subplot(2,2,2)).draw_molecule_group(iptal, "CANCELED", color='lightgray')
    LissajousEngine(fig.add_subplot(2,2,3)).draw_molecule_group(sonuc, "Final result: S", color='green')
    plt.show()

if __name__ == "__main__":
    print("The calculation process of Q is visualized ...")
    visualize_Q()
    
    print("\nThe calculation process of P is visualized ...")
    visualize_P()

    print("\nThe calculation process of R is visualized ...")
    visualize_R()
    
    print("\nThe calculation process of S is visualized ...")
    visualize_S()