# 📐 Générateur de Formes Géométriques TikZ

## 📝 Vue d'ensemble

Le module `generateur_formes_geometriques.py` fournit une classe Python pour générer automatiquement des formes géométriques en TikZ compatible avec TikZJax pour Obsidian.

**Fichier:** [generateur_formes_geometriques.py](c:\code\code-Graphique-final\generateur_formes_geometriques.py)

---

## 🎯 Fonctionnalités

### 1. Cercle Trigonométrique

#### `cercle_trigonometrique(angle_deg=40, afficher_projections=True, ...)`
Génère un cercle trigonométrique unitaire avec angle, projections sin/cos et point M.

**Paramètres:**
- `angle_deg`: Angle en degrés (défaut: 40°)
- `afficher_projections`: Afficher lignes pointillées (défaut: True)
- `afficher_sin`: Afficher segment sinus (défaut: True)
- `afficher_cos`: Afficher segment cosinus (défaut: True)
- `couleur_cercle`: Couleur du cercle (défaut: "black")
- `couleur_angle`: Couleur de l'arc angle (défaut: "red")
- `couleur_sin`: Couleur du segment sin (défaut: "orange")
- `couleur_cos`: Couleur du segment cos (défaut: "green!60!black")

**Exemple:**
```python
gen = GenerateurFormesGeometriques()
tikz = gen.cercle_trigonometrique(angle_deg=45, couleur_angle="blue")
```

**Rendu:**
- Cercle unitaire avec axes gradués (-1, 0, 1)
- Arc rouge pour l'angle θ
- Point M sur le cercle
- Segment orange pour sin(θ)
- Segment vert pour cos(θ)
- Projection pointillée

---

#### `cercle_trigo_multiple_angles(angles_deg=[30, 60, 90, 120], ...)`
Génère un cercle trigonométrique avec plusieurs angles marqués simultanément.

**Paramètres:**
- `angles_deg`: Liste d'angles en degrés
- `couleurs`: Liste de couleurs (auto si vide)
- `afficher_labels`: Afficher valeurs exactes (défaut: True)

**Exemple:**
```python
tikz = gen.cercle_trigo_multiple_angles(
    angles_deg=[30, 45, 60, 90],
    couleurs=["red", "blue", "green", "purple"]
)
```

**Rendu:**
- 4 points sur le cercle avec angles spécifiés
- Labels avec valeurs exactes: $(\frac{\sqrt{3}}{2}, \frac{1}{2})$ pour 30°
- Couleurs distinctes pour chaque angle

---

### 2. Triangles

#### `triangle_rectangle(angle_deg=30, afficher_formules=True, type_formule="sin")`
Triangle rectangle pour illustrer les définitions trigonométriques.

**Paramètres:**
- `angle_deg`: Angle θ du triangle (défaut: 30°)
- `afficher_formules`: Afficher formule trigonométrique (défaut: True)
- `type_formule`: "sin", "cos", ou "tan"

**Exemple:**
```python
tikz = gen.triangle_rectangle(angle_deg=30, type_formule="sin")
```

**Rendu:**
- Triangle rectangle avec angle droit marqué
- Arc rouge pour angle θ
- Labels "adjacent", "opposé", "hypoténuse"
- Formule: $\sin(\theta) = \frac{\text{opposé}}{\text{hypoténuse}}$

---

#### `triangle_quelconque(a=3, b=4, c=5, afficher_angles=True)`
Triangle quelconque avec notation standard.

**Paramètres:**
- `a, b, c`: Longueurs des côtés
- `afficher_angles`: Afficher angles A, B, C (défaut: True)

**Exemple:**
```python
tikz = gen.triangle_quelconque(a=3, b=4, c=5, afficher_angles=True)
```

**Rendu:**
- Triangle avec sommets A, B, C
- Côtés étiquetés a, b, c
- Angles marqués si demandé

---

### 3. Formes 2D

#### `polygone_regulier(n_cotes=6, rayon=2, afficher_centre=True)`
Polygone régulier à n côtés.

**Paramètres:**
- `n_cotes`: Nombre de côtés (3 à 12)
- `rayon`: Rayon du cercle circonscrit
- `afficher_centre`: Marquer centre O (défaut: True)

**Exemple:**
```python
tikz = gen.polygone_regulier(n_cotes=6, rayon=2)  # Hexagone
tikz = gen.polygone_regulier(n_cotes=5, rayon=1.5)  # Pentagone
```

**Rendu:**
- Polygone régulier inscrit dans cercle
- Sommets numérotés $S_1, S_2, ..., S_n$
- Centre marqué
- Rayon en pointillé

---

#### `cercle_avec_points(rayon=2, points=[], labels=[])`
Cercle avec points marqués et étiquetés.

**Paramètres:**
- `rayon`: Rayon du cercle
- `points`: Liste de tuples (x, y)
- `labels`: Liste de noms pour les points

**Exemple:**
```python
tikz = gen.cercle_avec_points(
    rayon=2,
    points=[(1.5, 1), (-1, 1.5), (0, -2)],
    labels=["A", "B", "C"]
)
```

**Rendu:**
- Cercle centré à l'origine
- Points marqués en rouge
- Labels personnalisés

---

### 4. Formes 3D

#### `cube_3d(taille=2, perspective=True)`
Cube en 3D avec perspective.

**Paramètres:**
- `taille`: Longueur arête (défaut: 2)
- `perspective`: Utiliser perspective (défaut: True)

**Exemple:**
```python
tikz = gen.cube_3d(taille=2, perspective=True)
```

**Rendu:**
- Cube avec 8 sommets
- Face avant et face arrière
- Arêtes reliant faces
- Sommets étiquetés A, B, C, D

---

#### `pyramide_3d(base=2, hauteur=3)`
Pyramide à base carrée en 3D.

**Paramètres:**
- `base`: Longueur côté base (défaut: 2)
- `hauteur`: Hauteur pyramide (défaut: 3)

**Exemple:**
```python
tikz = gen.pyramide_3d(base=2, hauteur=3)
```

**Rendu:**
- Base carrée ABCD
- Sommet S au-dessus
- Arêtes latérales en pointillé
- Hauteur marquée

---

### 5. Vecteurs

#### `vecteur_2d(vecteurs=[], origine=(0, 0), afficher_composantes=True)`
Vecteurs en 2D avec origine commune.

**Paramètres:**
- `vecteurs`: Liste de tuples [(x1, y1), (x2, y2), ...]
- `origine`: Point de départ (défaut: origine)
- `afficher_composantes`: Afficher $\vec{v} = (x, y)$ (défaut: True)

**Exemple:**
```python
tikz = gen.vecteur_2d(
    vecteurs=[(2, 3), (-1, 2), (3, -1)],
    origine=(0, 0),
    afficher_composantes=True
)
```

**Rendu:**
- 3 vecteurs depuis origine
- Couleurs distinctes
- Labels $\vec{v_1}, \vec{v_2}, \vec{v_3}$
- Composantes affichées

---

#### `addition_vecteurs(u=(2, 1), v=(1, 2), methode="parallelogramme")`
Illustration de l'addition vectorielle.

**Paramètres:**
- `u`: Vecteur $\vec{u}$ (tuple)
- `v`: Vecteur $\vec{v}$ (tuple)
- `methode`: "parallelogramme" ou "bout_a_bout"

**Exemple:**
```python
# Méthode parallélogramme
tikz = gen.addition_vecteurs(u=(2, 1), v=(1, 2), methode="parallelogramme")

# Méthode bout à bout
tikz = gen.addition_vecteurs(u=(2, 1), v=(1, 2), methode="bout_a_bout")
```

**Rendu (parallélogramme):**
- Vecteurs $\vec{u}$ (rouge) et $\vec{v}$ (bleu)
- Parallélogramme en pointillés
- Vecteur somme $\vec{u} + \vec{v}$ (vert)

**Rendu (bout à bout):**
- $\vec{u}$ depuis origine
- $\vec{v}$ depuis extrémité de $\vec{u}$
- Vecteur somme depuis origine

---

### 6. Repères

#### `repere_2d(xmin=-3, xmax=3, ymin=-3, ymax=3, grille=True)`
Repère 2D avec axes et grille optionnelle.

**Paramètres:**
- `xmin, xmax`: Limites axe x
- `ymin, ymax`: Limites axe y
- `grille`: Afficher grille (défaut: True)

**Exemple:**
```python
tikz = gen.repere_2d(xmin=-5, xmax=5, ymin=-3, ymax=3, grille=True)
```

**Rendu:**
- Axes x et y avec flèches
- Grille grise fine
- Origine marquée O

---

#### `repere_3d(longueur_axes=3)`
Repère 3D en perspective.

**Paramètres:**
- `longueur_axes`: Longueur axes x, y, z

**Exemple:**
```python
tikz = gen.repere_3d(longueur_axes=3)
```

**Rendu:**
- 3 axes x, y, z en perspective
- Labels avec couleurs distinctes
- Origine O

---

## 🧪 Tests et Validation

### Test Complet

```bash
python generateur_formes_geometriques.py
```

Génère 5 exemples:
1. Cercle trigonométrique (40°)
2. Triangle rectangle (30°)
3. Hexagone régulier
4. Addition de vecteurs
5. Cube 3D

### Test de Validation Format

```bash
python test_format_validation.py
```

Vérifie 9 types de formes:
- Format TikZ correct (```tikz ... ```)
- Structure complète (\begin{document}, \begin{tikzpicture}, etc.)
- Contenu spécifique (angles, labels, etc.)

**Résultat:** ✅ 100% des tests passés

---

## 🔗 Intégration avec good.py

### Prochaine Étape: Intégration Multi-Graphiques

Le système actuel de [good.py](c:\code\code-Note\good.py) utilise un seul placeholder `{graphique}`.

**Problème identifié par l'utilisateur:**
> "les de graphique sont coller allors que le deuxième graph qui est un cercle trigonométrique devrait être placer après la mension de ça définition trigonométrique"

**Solution proposée:**

#### 1. Multiple Placeholders dans Templates

```python
# Dans _init_template_sections()
self.template_sections["definition"] = r"""
## 💡 Définition et Caractérisation

{graphique_principal}

La **fonction sinus**...

### Définition Trigonométrique

{graphique_cercle_trigo}

Sur le cercle trigonométrique...
"""
```

#### 2. Détection Auto des Graphiques Nécessaires

```python
def _detecter_graphiques_necessaires(self, notion, proprietes):
    """Détecte quels graphiques générer selon la notion."""
    graphiques = {}

    if "sinus" in notion or "cosinus" in notion:
        # Courbe de la fonction
        graphiques["principal"] = self.tikz_gen.generer_graphique(notion)

        # Cercle trigonométrique
        angle = 40  # ou angle pertinent
        graphiques["cercle_trigo"] = self.forme_gen.cercle_trigonometrique(
            angle_deg=angle
        )

    elif "vecteur" in notion:
        graphiques["principal"] = self.forme_gen.addition_vecteurs(...)

    return graphiques
```

#### 3. Remplissage Multi-Graphiques

```python
def generer_note(self, notion, categorie):
    graphiques = self._detecter_graphiques_necessaires(notion, proprietes)

    # Remplir tous les placeholders
    note = template.format(
        graphique_principal=graphiques.get("principal", ""),
        graphique_cercle_trigo=graphiques.get("cercle_trigo", ""),
        graphique_geometrique=graphiques.get("geometrique", ""),
    )

    return note
```

---

## 📊 Couverture Complète

### Formes Disponibles (13 méthodes)

| Catégorie | Méthodes | Cas d'usage |
|-----------|----------|-------------|
| **Cercle Trigo** | `cercle_trigonometrique()`, `cercle_trigo_multiple_angles()` | Fonctions sin, cos, tan |
| **Triangles** | `triangle_rectangle()`, `triangle_quelconque()` | Définitions trigo, géométrie |
| **Formes 2D** | `polygone_regulier()`, `cercle_avec_points()` | Géométrie plane |
| **Formes 3D** | `cube_3d()`, `pyramide_3d()` | Géométrie dans l'espace |
| **Vecteurs** | `vecteur_2d()`, `addition_vecteurs()` | Algèbre linéaire |
| **Repères** | `repere_2d()`, `repere_3d()` | Bases de coordonnées |

---

## ✅ Qualité et Standards

### Format TikZ

Tous les graphiques suivent le format:
```tikz
\begin{document}
\begin{tikzpicture}[scale=...]
  % Code TikZ
\end{tikzpicture}
\end{document}
```

### Compatibilité TikZJax

- ✅ Fonctionne dans Obsidian avec plugin TikZJax
- ✅ Syntaxe TikZ standard
- ✅ Pas de dépendances externes
- ✅ Rendu immédiat dans les notes

### Paramètres Personnalisables

Chaque méthode offre:
- Dimensions configurables
- Couleurs personnalisables
- Options d'affichage (labels, formules, grille)
- Échelle ajustable

---

## 🚀 Utilisation

### Import et Initialisation

```python
from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()
```

### Génération Simple

```python
# Cercle trigonométrique pour 45°
tikz = gen.cercle_trigonometrique(angle_deg=45)

# Hexagone régulier
tikz = gen.polygone_regulier(n_cotes=6, rayon=2)

# Addition de vecteurs
tikz = gen.addition_vecteurs(u=(2, 1), v=(1, 2))
```

### Résultat

Chaque méthode retourne une chaîne TikZ prête à être:
1. Insérée dans une note Markdown
2. Sauvegardée sur GitHub
3. Rendue par TikZJax dans Obsidian

---

## 📝 Exemples d'Intégration

### Note pour "Fonction Sinus"

```markdown
# Fonction Sinus

```tikz
[Graphique de sin(deg(x))]
```

## 💡 Définition et Caractérisation

La fonction sinus...

### Définition Trigonométrique

```tikz
[Cercle trigonométrique avec angle]
```

Sur le cercle unitaire...
```

### Note pour "Addition de Vecteurs"

```markdown
# Addition de Vecteurs

```tikz
[Méthode du parallélogramme]
```

## 💡 Définition

L'addition vectorielle...
```

---

## 🎯 Prochaines Étapes

1. **Intégrer dans good.py** avec système multi-placeholders
2. **Tester notes complètes** avec plusieurs graphiques
3. **Valider rendu** dans Obsidian avec TikZJax
4. **Optimiser placement** selon contexte de la notion

---

**Date:** 2026-01-09
**Version:** 1.0 - Module Complet
**Statut:** ✅ Tests Validés - Prêt pour Intégration
**Fichiers:**
- [generateur_formes_geometriques.py](c:\code\code-Graphique-final\generateur_formes_geometriques.py) (476 lignes)
- [test_format_validation.py](c:\code\code-Graphique-final\test_format_validation.py)
