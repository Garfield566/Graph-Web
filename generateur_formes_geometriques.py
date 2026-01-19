"""
Générateur de Formes Géométriques TikZ
Crée des cercles trigonométriques, triangles, formes 2D/3D, et diagrammes vectoriels
Compatible avec TikZJax pour Obsidian
"""

import math
import numpy as np

class GenerateurFormesGeometriques:
    """Génère des formes géométriques en TikZ."""

    def __init__(self, scale=3):
        self.scale = scale

    # ==================== CERCLE TRIGONOMÉTRIQUE ====================

    def cercle_trigonometrique(self, angle_deg=40, afficher_projections=True,
                               afficher_sin=True, afficher_cos=True,
                               couleur_cercle="black", couleur_angle="red",
                               couleur_sin="orange", couleur_cos="green!60!black"):
        """
        Génère un cercle trigonométrique avec angle et projections.

        Args:
            angle_deg: Angle en degrés (default: 40)
            afficher_projections: Afficher les projections sin/cos
            afficher_sin: Afficher la projection sin
            afficher_cos: Afficher la projection cos
            couleur_*: Couleurs personnalisées
        """
        angle_rad = math.radians(angle_deg)
        x_point = math.cos(angle_rad)
        y_point = math.sin(angle_rad)

        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale={self.scale}]
  % Axes
  \\draw[->] (-1.3,0) -- (1.3,0) node[right] {{$x$}};
  \\draw[->] (0,-1.3) -- (0,1.3) node[above] {{$y$}};

  % Cercle unitaire
  \\draw[thick, {couleur_cercle}] (0,0) circle (1);

  % Angle
  \\draw[very thick, {couleur_angle}] (0.5,0) arc (0:{angle_deg}:0.5);
  \\node[{couleur_angle}] at (0.6,0.2) {{$\\theta$}};

  % Rayon vers le point M
  \\draw[thick, blue] (0,0) -- ({x_point:.3f},{y_point:.3f});
  \\fill[blue] ({x_point:.3f},{y_point:.3f}) circle (0.03);
  \\node[blue, above right] at ({x_point:.3f},{y_point:.3f}) {{$M$}};
"""

        if afficher_projections:
            # Projection verticale (pour sin)
            code += f"""
  % Projection verticale (ligne en pointillés)
  \\draw[very thick, {couleur_angle}, dashed] ({x_point:.3f},0) -- ({x_point:.3f},{y_point:.3f});
"""

            if afficher_cos:
                # Segment cos (horizontal)
                code += f"""
  % Cosinus (segment horizontal)
  \\draw[very thick, {couleur_cos}] (0,0) -- ({x_point:.3f},0);
  \\node[{couleur_cos}, below] at ({x_point/2:.3f},0) {{$\\cos(\\theta)$}};
"""

            if afficher_sin:
                # Segment sin (vertical)
                code += f"""
  % Sinus (segment vertical)
  \\draw[thick, {couleur_sin}] (0,0) -- (0,{y_point:.3f});
  \\node[{couleur_sin}, left] at (0,{y_point/2:.3f}) {{$\\sin(\\theta)$}};
"""

        code += f"""
  % Graduations
  \\node[below left] at (0,0) {{$O$}};
  \\node[below] at (1,0) {{$1$}};
  \\node[left] at (0,1) {{$1$}};
  \\node[below] at (-1,0) {{$-1$}};
  \\node[left] at (0,-1) {{$-1$}};
\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def cercle_trigo_multiple_angles(self, angles_deg=[30, 45, 60, 90]):
        """Cercle trigonométrique montrant plusieurs angles remarquables."""
        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale={self.scale}]
  % Axes
  \\draw[->] (-1.3,0) -- (1.3,0) node[right] {{$x$}};
  \\draw[->] (0,-1.3) -- (0,1.3) node[above] {{$y$}};

  % Cercle unitaire
  \\draw[thick] (0,0) circle (1);

  % Points remarquables
"""

        couleurs = ["red", "blue", "green!60!black", "purple", "orange"]

        for i, angle in enumerate(angles_deg):
            angle_rad = math.radians(angle)
            x = math.cos(angle_rad)
            y = math.sin(angle_rad)
            couleur = couleurs[i % len(couleurs)]

            code += f"""  \\draw[thick, {couleur}] (0,0) -- ({x:.3f},{y:.3f});
  \\fill[{couleur}] ({x:.3f},{y:.3f}) circle (0.03);
  \\node[{couleur}, anchor=south west] at ({x:.3f},{y:.3f}) {{${angle}°$}};
"""

        code += f"""
  % Graduations
  \\node[below left] at (0,0) {{$O$}};
  \\node[below] at (1,0) {{$1$}};
  \\node[left] at (0,1) {{$1$}};
\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def cercle_trigo_complet_valeurs(self):
        """
        Cercle trigonométrique avec TOUTES les valeurs remarquables:
        0°, 30°, 45°, 60°, 90°, 120°, 135°, 150°, 180°, etc.
        Affiche les coordonnées exactes (cos, sin) et radians.
        """
        # Valeurs remarquables avec leurs coordonnées exactes
        valeurs_remarquables = {
            0: ("1", "0", "0"),
            30: ("\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}", "\\frac{\\pi}{6}"),
            45: ("\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}", "\\frac{\\pi}{4}"),
            60: ("\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}", "\\frac{\\pi}{3}"),
            90: ("0", "1", "\\frac{\\pi}{2}"),
            120: ("-\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}", "\\frac{2\\pi}{3}"),
            135: ("-\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}", "\\frac{3\\pi}{4}"),
            150: ("-\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}", "\\frac{5\\pi}{6}"),
            180: ("-1", "0", "\\pi"),
            210: ("-\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}", "\\frac{7\\pi}{6}"),
            225: ("-\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{2}}{2}", "\\frac{5\\pi}{4}"),
            240: ("-\\frac{1}{2}", "-\\frac{\\sqrt{3}}{2}", "\\frac{4\\pi}{3}"),
            270: ("0", "-1", "\\frac{3\\pi}{2}"),
            300: ("\\frac{1}{2}", "-\\frac{\\sqrt{3}}{2}", "\\frac{5\\pi}{3}"),
            315: ("\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{2}}{2}", "\\frac{7\\pi}{4}"),
            330: ("\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}", "\\frac{11\\pi}{6}"),
        }

        code = f"""```tikz
\\usepackage{{tikz}}
\\begin{{document}}
\\begin{{tikzpicture}}[scale=5]
  % Axes
  \\draw[->] (-1.4,0) -- (1.4,0) node[right] {{$x$}};
  \\draw[->] (0,-1.4) -- (0,1.4) node[above] {{$y$}};

  % Cercle unitaire
  \\draw[very thick, blue] (0,0) circle (1);

  % Centre
  \\node[below left] at (0,0) {{$O$}};

"""

        couleurs = ["red", "blue!60", "green!60!black", "purple", "orange", "brown"]

        for i, (angle, (cos_val, sin_val, rad_val)) in enumerate(valeurs_remarquables.items()):
            angle_rad = math.radians(angle)
            x = math.cos(angle_rad)
            y = math.sin(angle_rad)
            couleur = couleurs[i % len(couleurs)]

            # Position du label (décalé vers l'extérieur)
            label_distance = 1.3
            label_x = label_distance * x
            label_y = label_distance * y

            # Anchor selon position
            if x > 0 and y > 0:
                anchor = "south west"
            elif x < 0 and y > 0:
                anchor = "south east"
            elif x < 0 and y < 0:
                anchor = "north east"
            elif x > 0 and y < 0:
                anchor = "north west"
            else:
                anchor = "center"

            code += f"""  % Angle {angle}^\\circ = {rad_val}
  \\draw[{couleur}] (0,0) -- ({x:.3f},{y:.3f});
  \\fill[{couleur}] ({x:.3f},{y:.3f}) circle (0.02);
  \\node[{couleur}, anchor={anchor}, fill=white] at ({label_x:.2f},{label_y:.2f}) {{${rad_val}$}};
  \\node[{couleur}, anchor={anchor}, fill=white, yshift=-8pt] at ({label_x:.2f},{label_y:.2f}) {{$({cos_val}, {sin_val})$}};

"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def cercle_trigo_angle_specifique(self, angle_deg=30):
        """
        Cercle trigonométrique montrant UN SEUL angle avec ses valeurs exactes.
        Idéal pour équations trigonométriques - affiche seulement l'angle calculé.
        """
        # Valeurs exactes pour angles remarquables
        valeurs_exactes = {
            0: ("1", "0", "0"),
            30: ("\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}", "\\frac{\\pi}{6}"),
            45: ("\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}", "\\frac{\\pi}{4}"),
            60: ("\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}", "\\frac{\\pi}{3}"),
            90: ("0", "1", "\\frac{\\pi}{2}"),
            120: ("-\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}", "\\frac{2\\pi}{3}"),
            135: ("-\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}", "\\frac{3\\pi}{4}"),
            150: ("-\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}", "\\frac{5\\pi}{6}"),
            180: ("-1", "0", "\\pi"),
            210: ("-\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}", "\\frac{7\\pi}{6}"),
            225: ("-\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{2}}{2}", "\\frac{5\\pi}{4}"),
            240: ("-\\frac{1}{2}", "-\\frac{\\sqrt{3}}{2}", "\\frac{4\\pi}{3}"),
            270: ("0", "-1", "\\frac{3\\pi}{2}"),
            300: ("\\frac{1}{2}", "-\\frac{\\sqrt{3}}{2}", "\\frac{5\\pi}{3}"),
            315: ("\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{2}}{2}", "\\frac{7\\pi}{4}"),
            330: ("\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}", "\\frac{11\\pi}{6}"),
        }

        angle_rad = math.radians(angle_deg)
        x = math.cos(angle_rad)
        y = math.sin(angle_rad)

        # Vérifier si c'est une valeur remarquable
        if angle_deg in valeurs_exactes:
            cos_val, sin_val, rad_val = valeurs_exactes[angle_deg]
        else:
            # Valeurs décimales pour angles non-remarquables
            cos_val = f"{x:.3f}"
            sin_val = f"{y:.3f}"
            rad_val = f"{angle_rad:.3f}"

        code = f"""```tikz
\\usepackage{{tikz}}
\\begin{{document}}
\\begin{{tikzpicture}}[scale=5]
  % Axes
  \\draw[->] (-1.3,0) -- (1.3,0) node[right] {{$x$}};
  \\draw[->] (0,-1.3) -- (0,1.3) node[above] {{$y$}};

  % Cercle unitaire
  \\draw[thick, black] (0,0) circle (1);

  % Rayon vers le point M
  \\draw[very thick, blue] (0,0) -- ({x:.3f},{y:.3f});
  \\fill[blue] ({x:.3f},{y:.3f}) circle (0.03);
  \\node[blue, above right, fill=white] at ({x:.3f},{y:.3f}) {{$M$}};

  % Arc d'angle
  \\draw[very thick, red] (0.4,0) arc (0:{angle_deg}:0.4);
  \\node[red, fill=white] at ({0.5*math.cos(angle_rad/2):.2f},{0.5*math.sin(angle_rad/2):.2f}) {{$\\theta$}};

  % Projections
  \\draw[dashed, red] ({x:.3f},0) -- ({x:.3f},{y:.3f});
  \\draw[dashed, red] (0,{y:.3f}) -- ({x:.3f},{y:.3f});

  % Valeurs cosinus et sinus
  \\draw[very thick, green!60!black] (0,0) -- ({x:.3f},0);
  \\node[green!60!black, below, fill=white] at ({x/2:.3f},-0.05) {{$\\cos(\\theta) = {cos_val}$}};

  \\draw[very thick, orange] (0,0) -- (0,{y:.3f});
  \\node[orange, left, fill=white] at (-0.05,{y/2:.3f}) {{$\\sin(\\theta) = {sin_val}$}};

  % Affichage radian et degré
  \\node[above, fill=white] at (0,1.25) {{$\\theta = {rad_val}$ rad $= {angle_deg}^\\circ$}};

  % Coordonnées du point M
  \\node[below, fill=white] at (0,-1.25) {{$M({cos_val}, {sin_val})$}};

  % Graduations
  \\node[below left] at (0,0) {{$O$}};
  \\node[below] at (1,0) {{$1$}};
  \\node[left] at (0,1) {{$1$}};
  \\node[below] at (-1,0) {{$-1$}};
  \\node[left] at (0,-1) {{$-1$}};
\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    # ==================== TRIANGLES ====================

    def triangle_rectangle(self, angle_deg=30, afficher_formules=True,
                          type_formule="sin"):
        """
        Triangle rectangle pour illustrer les définitions trigonométriques.

        Args:
            angle_deg: Angle à illustrer
            afficher_formules: Afficher les formules
            type_formule: "sin", "cos", ou "tan"
        """
        angle_rad = math.radians(angle_deg)

        # Dimensions du triangle (hypoténuse = 3)
        hypotenuse = 3
        adjacent = hypotenuse * math.cos(angle_rad)
        oppose = hypotenuse * math.sin(angle_rad)

        code = f"""```tikz
\\usepackage{{tikz}}
\\begin{{document}}
\\begin{{tikzpicture}}[scale=2]
  % Triangle rectangle
  \\draw[very thick] (0,0) -- ({adjacent:.2f},0) -- ({adjacent:.2f},{oppose:.2f}) -- cycle;

  % Angle droit
  \\draw ({adjacent:.2f},0) -- ({adjacent-0.2:.2f},0) -- ({adjacent-0.2:.2f},0.2) -- ({adjacent:.2f},0.2);

  % Arc pour l'angle θ
  \\draw[very thick, red] (0.6,0) arc (0:{angle_deg}:0.6);
  \\node[red] at (0.8,0.15) {{$\\theta$}};

  % Labels des côtés
  \\node[below] at ({adjacent/2:.2f},0) {{adjacent}};
  \\node[right] at ({adjacent:.2f},{oppose/2:.2f}) {{opposé}};
  \\node[above left] at ({adjacent/2:.2f},{oppose/2:.2f}) {{hypoténuse}};
"""

        if afficher_formules:
            if type_formule == "sin":
                code += f"""
  % Formule sinus
  \\node[below, text width=5cm, align=center] at ({adjacent/2:.2f},-0.8) {{$\\sin(\\theta) = \\frac{{\\text{{opposé}}}}{{\\text{{hypoténuse}}}}$}};
"""
            elif type_formule == "cos":
                code += f"""
  % Formule cosinus
  \\node[below, text width=5cm, align=center] at ({adjacent/2:.2f},-0.8) {{$\\cos(\\theta) = \\frac{{\\text{{adjacent}}}}{{\\text{{hypoténuse}}}}$}};
"""
            elif type_formule == "tan":
                code += f"""
  % Formule tangente
  \\node[below, text width=5cm, align=center] at ({adjacent/2:.2f},-0.8) {{$\\tan(\\theta) = \\frac{{\\text{{opposé}}}}{{\\text{{adjacent}}}}$}};
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def triangle_quelconque(self, a=3, b=4, c=5, afficher_angles=True):
        """Triangle quelconque avec notation standard."""
        # Utiliser le théorème de Héron pour placer les points
        # Point A à l'origine, B sur l'axe x
        Ax, Ay = 0, 0
        Bx, By = c, 0

        # Calculer position de C avec loi des cosinus
        angle_A_rad = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
        Cx = b * math.cos(angle_A_rad)
        Cy = b * math.sin(angle_A_rad)

        # Calculer les trois angles en degrés
        angle_A_deg = math.degrees(angle_A_rad)
        angle_B_rad = math.acos((a**2 + c**2 - b**2) / (2 * a * c))
        angle_B_deg = math.degrees(angle_B_rad)
        angle_C_deg = 180 - angle_A_deg - angle_B_deg

        # Échelle adaptative pour éviter triangles trop grands
        max_dim = max(a, b, c)
        if max_dim > 10:
            scale = 0.5
        elif max_dim > 7:
            scale = 0.8
        else:
            scale = 1.5

        code = f"""```tikz
\\usepackage{{tikz}}
\\begin{{document}}
\\begin{{tikzpicture}}[scale={scale}]
  % Triangle
  \\draw[very thick] ({Ax},{Ay}) -- ({Bx},{By}) -- ({Cx:.2f},{Cy:.2f}) -- cycle;

  % Points
  \\fill ({Ax},{Ay}) circle (0.05);
  \\fill ({Bx},{By}) circle (0.05);
  \\fill ({Cx:.2f},{Cy:.2f}) circle (0.05);

  % Labels des sommets
  \\node[below left] at ({Ax},{Ay}) {{$A$}};
  \\node[below right] at ({Bx},{By}) {{$B$}};
  \\node[above] at ({Cx:.2f},{Cy:.2f}) {{$C$}};

  % Labels des côtés
  \\node[below] at ({c/2},{0}) {{$c = {c}$}};
  \\node[left] at ({Cx/2:.2f},{Cy/2:.2f}) {{$b = {b}$}};
  \\node[right] at ({(Bx+Cx)/2:.2f},{Cy/2:.2f}) {{$a = {a}$}};
"""

        if afficher_angles:
            # Calculer les angles de direction pour les arcs (méthode uniforme pour A, B, C)

            # Angle A: arc de 0 à angle_AC
            angle_AC = math.degrees(math.atan2(Cy, Cx))
            angle_A_start = 0
            angle_A_end = angle_AC

            # Angle B: calculer l'angle de départ (vers C)
            angle_BC_direction = math.degrees(math.atan2(Cy - By, Cx - Bx))
            angle_B_start = angle_BC_direction
            angle_B_end = angle_BC_direction + angle_B_deg

            # Angle C: calculer l'angle de départ (vers A)
            angle_CA_direction = math.degrees(math.atan2(Ay - Cy, Ax - Cx))
            angle_C_start = angle_CA_direction
            angle_C_end = angle_CA_direction + angle_C_deg

            # Assigner couleurs selon la mesure exacte de l'angle
            # Arrondir les angles pour éviter les problèmes d'arrondis numériques
            angle_A_rounded = round(angle_A_deg)
            angle_B_rounded = round(angle_B_deg)
            angle_C_rounded = round(angle_C_deg)

            # Créer un mapping: angle arrondi -> couleur
            angles_uniques = {}
            couleurs_dispo = ["blue!40", "yellow!60", "green!40", "red!40", "purple!40", "orange!40"]
            color_index = 0

            # Assigner les couleurs en fonction des angles arrondis
            for angle_val in sorted([angle_A_rounded, angle_B_rounded, angle_C_rounded]):
                if angle_val not in angles_uniques:
                    angles_uniques[angle_val] = couleurs_dispo[color_index % len(couleurs_dispo)]
                    color_index += 1

            color_A = angles_uniques[angle_A_rounded]
            color_B = angles_uniques[angle_B_rounded]
            color_C = angles_uniques[angle_C_rounded]

            # Position du texte à l'intérieur de l'arc (au milieu de l'angle)
            mid_angle_A = angle_A_start + angle_A_deg / 2
            mid_angle_B = angle_B_start + angle_B_deg / 2
            mid_angle_C = angle_C_start + angle_C_deg / 2

            text_pos_A_x = Ax + 0.5 * math.cos(math.radians(mid_angle_A))
            text_pos_A_y = Ay + 0.5 * math.sin(math.radians(mid_angle_A))
            text_pos_B_x = Bx + 0.5 * math.cos(math.radians(mid_angle_B))
            text_pos_B_y = By + 0.5 * math.sin(math.radians(mid_angle_B))
            text_pos_C_x = Cx + 0.5 * math.cos(math.radians(mid_angle_C))
            text_pos_C_y = Cy + 0.5 * math.sin(math.radians(mid_angle_C))

            # Calculer les points de départ des arcs (méthode uniforme)
            arc_A_start_x = Ax + 0.9 * math.cos(math.radians(angle_A_start))
            arc_A_start_y = Ay + 0.9 * math.sin(math.radians(angle_A_start))

            arc_B_start_x = Bx + 0.9 * math.cos(math.radians(angle_B_start))
            arc_B_start_y = By + 0.9 * math.sin(math.radians(angle_B_start))

            arc_C_start_x = Cx + 0.9 * math.cos(math.radians(angle_C_start))
            arc_C_start_y = Cy + 0.9 * math.sin(math.radians(angle_C_start))

            code += f"""
  % Arc d'angle en A
  \\fill[{color_A}] ({Ax},{Ay}) -- ({arc_A_start_x:.2f},{arc_A_start_y:.2f}) arc ({angle_A_start:.1f}:{angle_A_end:.1f}:0.9) -- cycle;
  \\node at ({text_pos_A_x:.2f},{text_pos_A_y:.2f}) {{${angle_A_deg:.0f}^\\circ$}};

  % Arc d'angle en B
  \\fill[{color_B}] ({Bx},{By}) -- ({arc_B_start_x:.2f},{arc_B_start_y:.2f}) arc ({angle_B_start:.1f}:{angle_B_end:.1f}:0.9) -- cycle;
  \\node at ({text_pos_B_x:.2f},{text_pos_B_y:.2f}) {{${angle_B_deg:.0f}^\\circ$}};

  % Arc d'angle en C
  \\fill[{color_C}] ({Cx:.2f},{Cy:.2f}) -- ({arc_C_start_x:.2f},{arc_C_start_y:.2f}) arc ({angle_C_start:.1f}:{angle_C_end:.1f}:0.9) -- cycle;
  \\node at ({text_pos_C_x:.2f},{text_pos_C_y:.2f}) {{${angle_C_deg:.0f}^\\circ$}};
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    # ==================== FORMES 2D ====================

    def polygone_regulier(self, n_cotes=6, rayon=2, afficher_centre=True):
        """Polygone régulier à n côtés."""
        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1.5]
  % Polygone régulier à {n_cotes} côtés
"""

        # Calculer les sommets
        sommets = []
        for i in range(n_cotes):
            angle = 2 * math.pi * i / n_cotes - math.pi/2  # Commence en haut
            x = rayon * math.cos(angle)
            y = rayon * math.sin(angle)
            sommets.append((x, y))

        # Dessiner les arêtes
        for i in range(n_cotes):
            x1, y1 = sommets[i]
            x2, y2 = sommets[(i+1) % n_cotes]
            code += f"""  \\draw[very thick] ({x1:.2f},{y1:.2f}) -- ({x2:.2f},{y2:.2f});
"""

        # Dessiner les sommets
        for i, (x, y) in enumerate(sommets):
            code += f"""  \\fill ({x:.2f},{y:.2f}) circle (0.05);
  \\node[anchor=center] at ({x*1.2:.2f},{y*1.2:.2f}) {{$S_{{{i+1}}}$}};
"""

        if afficher_centre:
            code += f"""
  % Centre
  \\fill[red] (0,0) circle (0.05);
  \\node[red, below right] at (0,0) {{$O$}};

  % Rayon (exemple)
  \\draw[dashed, red] (0,0) -- ({sommets[0][0]:.2f},{sommets[0][1]:.2f});
  \\node[red, midway, right] at (0,{rayon/2:.2f}) {{$r = {rayon}$}};
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def cercle_avec_points(self, rayon=2, points=[(0, 2), (1.41, 1.41), (2, 0)],
                          labels=["A", "B", "C"]):
        """Cercle avec points marqués et labels."""
        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1.5]
  % Cercle
  \\draw[thick] (0,0) circle ({rayon});

  % Centre
  \\fill (0,0) circle (0.05);
  \\node[below left] at (0,0) {{$O$}};

  % Points sur le cercle
"""

        for (x, y), label in zip(points, labels):
            angle = math.atan2(y, x) * 1.3  # Décalage pour label
            label_x = (rayon + 0.3) * math.cos(angle)
            label_y = (rayon + 0.3) * math.sin(angle)

            code += f"""  \\fill ({x:.2f},{y:.2f}) circle (0.05);
  \\node at ({label_x:.2f},{label_y:.2f}) {{${label}$}};
  \\draw[dashed] (0,0) -- ({x:.2f},{y:.2f});
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    # ==================== FORMES 3D ====================

    def cube_3d(self, taille=2, perspective=True):
        """Cube en 3D avec perspective."""
        t = taille

        # Facteur de perspective
        if perspective:
            dx, dy = 0.4, 0.4
        else:
            dx, dy = 0, 0

        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1.5]
  % Face avant
  \\draw[very thick] (0,0) -- ({t},0) -- ({t},{t}) -- (0,{t}) -- cycle;

  % Face arrière (avec perspective)
  \\draw[very thick] ({dx},{t+dy}) -- ({t+dx},{t+dy}) -- ({t+dx},{dy}) -- ({dx},{dy}) -- cycle;

  % Arêtes reliant avant et arrière
  \\draw[very thick] (0,0) -- ({dx},{dy});
  \\draw[very thick] ({t},0) -- ({t+dx},{dy});
  \\draw[very thick] ({t},{t}) -- ({t+dx},{t+dy});
  \\draw[very thick] (0,{t}) -- ({dx},{t+dy});

  % Labels des sommets - Face avant (ABCD)
  \\node[below left] at (0,0) {{$A$}};
  \\node[below right] at ({t},0) {{$B$}};
  \\node[above right] at ({t},{t}) {{$C$}};
  \\node[above left] at (0,{t}) {{$D$}};

  % Labels des sommets - Face arrière (EFGH)
  \\node[below left] at ({dx},{dy}) {{$E$}};
  \\node[below right] at ({t+dx},{dy}) {{$F$}};
  \\node[above right] at ({t+dx},{t+dy}) {{$G$}};
  \\node[above left] at ({dx},{t+dy}) {{$H$}};
\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def pyramide_3d(self, base=2, hauteur=3):
        """Pyramide à base carrée en 3D."""
        b = base
        h = hauteur

        # Sommet de la pyramide (projection)
        sx, sy = b/2, b + h*0.5

        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1.5]
  % Base de la pyramide
  \\draw[very thick] (0,0) -- ({b},0) -- ({b},{b}) -- (0,{b}) -- cycle;

  % Arêtes vers le sommet
  \\draw[very thick] (0,0) -- ({sx},{sy});
  \\draw[very thick] ({b},0) -- ({sx},{sy});
  \\draw[very thick] ({b},{b}) -- ({sx},{sy});
  \\draw[very thick] (0,{b}) -- ({sx},{sy});

  % Sommet
  \\fill ({sx},{sy}) circle (0.05);
  \\node[above] at ({sx},{sy}) {{$S$}};

  % Labels de la base
  \\node[below left] at (0,0) {{$A$}};
  \\node[below right] at ({b},0) {{$B$}};
  \\node[above right] at ({b},{b}) {{$C$}};
  \\node[above left] at (0,{b}) {{$D$}};
\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    # ==================== VECTEURS ====================

    def vecteur_2d(self, vecteurs=[(2, 3, "\\vec{u}"), (1, -1, "\\vec{v}")],
                   origine=(0, 0), afficher_composantes=True):
        """Vecteurs en 2D avec origine commune."""
        ox, oy = origine

        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1.2]
  % Axes
  \\draw[->] (-1,0) -- (4,0) node[right] {{$x$}};
  \\draw[->] (0,-2) -- (0,4) node[above] {{$y$}};

  % Origine
  \\fill ({ox},{oy}) circle (0.05);
  \\node[below left] at ({ox},{oy}) {{$O$}};

"""

        couleurs = ["red", "blue", "green!60!black", "purple", "orange"]

        for i, (vx, vy, label) in enumerate(vecteurs):
            couleur = couleurs[i % len(couleurs)]
            ex, ey = ox + vx, oy + vy

            code += f"""  % Vecteur {label}
  \\draw[->, very thick, {couleur}] ({ox},{oy}) -- ({ex},{ey});
  \\node[{couleur}] at ({ex+0.2},{ey+0.2}) {{${label}$}};
"""

            if afficher_composantes:
                code += f"""  \\node[{couleur}, anchor=west] at (4.5,{3-i*0.5}) {{${label} = ({vx}, {vy})$}};
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def addition_vecteurs(self, u=(2, 1), v=(1, 2), methode="parallelogramme"):
        """
        Illustration de l'addition vectorielle.

        Args:
            methode: "parallelogramme" ou "bout_a_bout"
        """
        ux, uy = u
        vx, vy = v

        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1.5]
  % Axes
  \\draw[->] (-0.5,0) -- ({ux+vx+1},0) node[right] {{$x$}};
  \\draw[->] (0,-0.5) -- (0,{uy+vy+1}) node[above] {{$y$}};

  % Origine
  \\fill (0,0) circle (0.05);
  \\node[below left] at (0,0) {{$O$}};

"""

        if methode == "parallelogramme":
            code += f"""  % Vecteur u
  \\draw[->, very thick, red] (0,0) -- ({ux},{uy});
  \\node[red] at ({ux/2-0.2},{uy/2}) {{$\\vec{{u}}$}};

  % Vecteur v
  \\draw[->, very thick, blue] (0,0) -- ({vx},{vy});
  \\node[blue] at ({vx/2+0.3},{vy/2}) {{$\\vec{{v}}$}};

  % Parallélogramme (pointillés)
  \\draw[dashed, gray] ({ux},{uy}) -- ({ux+vx},{uy+vy});
  \\draw[dashed, gray] ({vx},{vy}) -- ({ux+vx},{uy+vy});

  % Vecteur somme u + v
  \\draw[->, very thick, green!60!black] (0,0) -- ({ux+vx},{uy+vy});
  \\node[green!60!black] at ({(ux+vx)/2+0.5},{(uy+vy)/2}) {{$\\vec{{u}} + \\vec{{v}}$}};
"""
        else:  # bout_a_bout
            code += f"""  % Vecteur u
  \\draw[->, very thick, red] (0,0) -- ({ux},{uy});
  \\node[red] at ({ux/2-0.2},{uy/2}) {{$\\vec{{u}}$}};

  % Vecteur v (déplacé à l'extrémité de u)
  \\draw[->, very thick, blue] ({ux},{uy}) -- ({ux+vx},{uy+vy});
  \\node[blue] at ({ux+vx/2+0.3},{uy+vy/2}) {{$\\vec{{v}}$}};

  % Vecteur somme u + v
  \\draw[->, very thick, green!60!black, dashed] (0,0) -- ({ux+vx},{uy+vy});
  \\node[green!60!black] at ({(ux+vx)/2-0.5},{(uy+vy)/2+0.3}) {{$\\vec{{u}} + \\vec{{v}}$}};
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    # ==================== REPÈRES ====================

    def repere_2d(self, xmin=-3, xmax=3, ymin=-3, ymax=3, grille=True):
        """Repère 2D avec ou sans grille."""
        code = f"""```tikz
\\begin{{document}}
\\begin{{tikzpicture}}[scale=1]
"""

        if grille:
            code += f"""  % Grille
  \\draw[very thin, color=gray!30] ({xmin},{ymin}) grid ({xmax},{ymax});

"""

        code += f"""  % Axes
  \\draw[->, thick] ({xmin-0.5},0) -- ({xmax+0.5},0) node[right] {{$x$}};
  \\draw[->, thick] (0,{ymin-0.5}) -- (0,{ymax+0.5}) node[above] {{$y$}};

  % Origine
  \\fill (0,0) circle (0.05);
  \\node[below left] at (0,0) {{$O$}};

  % Graduations
"""

        # Graduations sur x
        for i in range(xmin, xmax+1):
            if i != 0:
                code += f"""  \\draw ({{i}},0.1) -- ({{i}},-0.1) node[below] {{${i}$}};
"""

        # Graduations sur y
        for i in range(ymin, ymax+1):
            if i != 0:
                code += f"""  \\draw (0.1,{{i}}) -- (-0.1,{{i}}) node[left] {{${i}$}};
"""

        code += f"""\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code

    def repere_3d(self, longueur_axes=3):
        """Repère 3D en perspective."""
        l = longueur_axes

        code = f"""```tikz
\\usepackage{{tikz-3dplot}}
\\begin{{document}}

\\tdplotsetmaincoords{{60}}{{120}}

\\begin{{tikzpicture}}[scale=1.5, tdplot_main_coords]
  % Axes
  \\draw[->, thick] (0,0,0) -- ({l},0,0) node[anchor=north east] {{$x$}};
  \\draw[->, thick] (0,0,0) -- (0,{l},0) node[anchor=north west] {{$y$}};
  \\draw[->, thick] (0,0,0) -- (0,0,{l}) node[anchor=south] {{$z$}};

  % Origine
  \\fill (0,0,0) circle (0.05);
  \\node[anchor=north] at (0,0,0) {{$O$}};

  % Plans (optionnel, semi-transparent)
  \\draw[opacity=0.2, fill=blue!20] (0,0,0) -- ({l},0,0) -- ({l},{l},0) -- (0,{l},0) -- cycle;
  \\draw[opacity=0.2, fill=red!20] (0,0,0) -- ({l},0,0) -- ({l},0,{l}) -- (0,0,{l}) -- cycle;
  \\draw[opacity=0.2, fill=green!20] (0,0,0) -- (0,{l},0) -- (0,{l},{l}) -- (0,0,{l}) -- cycle;
\\end{{tikzpicture}}
\\end{{document}}
```"""

        return code


# ==================== TESTS ====================

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    gen = GenerateurFormesGeometriques()

    print("=" * 80)
    print("GÉNÉRATEUR DE FORMES GÉOMÉTRIQUES TIKZ")
    print("=" * 80)

    # Test 1: Cercle trigonométrique
    print("\n1️⃣ Cercle Trigonométrique (angle 40°)")
    print("-" * 80)
    resultat = gen.cercle_trigonometrique(angle_deg=40)
    print(resultat)

    # Test 2: Triangle rectangle
    print("\n2️⃣ Triangle Rectangle (angle 30°)")
    print("-" * 80)
    resultat = gen.triangle_rectangle(angle_deg=30, type_formule="sin")
    print(resultat)

    # Test 3: Polygone régulier
    print("\n3️⃣ Hexagone Régulier")
    print("-" * 80)
    resultat = gen.polygone_regulier(n_cotes=6)
    print(resultat)

    # Test 4: Vecteurs
    print("\n4️⃣ Addition de Vecteurs")
    print("-" * 80)
    resultat = gen.addition_vecteurs(u=(2, 1), v=(1, 2), methode="parallelogramme")
    print(resultat)

    # Test 5: Cube 3D
    print("\n5️⃣ Cube 3D")
    print("-" * 80)
    resultat = gen.cube_3d(taille=2)
    print(resultat)

    print("\n" + "=" * 80)
    print("✅ Tests terminés!")
    print("=" * 80)
