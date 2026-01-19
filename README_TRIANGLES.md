# 📐 Générateur de Triangles TikZ

## 📝 Types de Triangles Disponibles

### 1. Triangle Rectangle (pour définitions trigonométriques)
### 2. Triangle Quelconque (géométrie générale)

---

## 1️⃣ Triangle Rectangle

### `triangle_rectangle(angle_deg=30, afficher_formules=True, type_formule="sin")`

**Usage:** Illustrer les définitions trigonométriques (sin, cos, tan)

#### Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `angle_deg` | int | 30 | Angle θ en degrés |
| `afficher_formules` | bool | True | Afficher la formule trigonométrique |
| `type_formule` | str | "sin" | Formule à afficher: "sin", "cos", ou "tan" |

#### Caractéristiques

- **Hypoténuse fixe:** 3 unités
- **Dimensions calculées:** Adjacent et opposé calculés selon l'angle
- **Angle droit marqué:** Petit carré à l'angle droit
- **Arc d'angle:** Arc rouge pour θ
- **Labels des côtés:** "adjacent", "opposé", "hypoténuse"
- **Formule affichée:** Selon le type choisi

#### Formules Disponibles

**"sin":**
```latex
sin(θ) = opposé / hypoténuse
```

**"cos":**
```latex
cos(θ) = adjacent / hypoténuse
```

**"tan":**
```latex
tan(θ) = opposé / adjacent
```

#### Exemples

```python
from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

# Triangle 30° avec formule sinus
tri_30_sin = gen.triangle_rectangle(angle_deg=30, type_formule="sin")

# Triangle 45° avec formule cosinus
tri_45_cos = gen.triangle_rectangle(angle_deg=45, type_formule="cos")

# Triangle 60° avec formule tangente
tri_60_tan = gen.triangle_rectangle(angle_deg=60, type_formule="tan")

# Sans formule
tri_simple = gen.triangle_rectangle(angle_deg=30, afficher_formules=False)
```

#### Résultats selon l'angle

| Angle | Adjacent | Opposé | Résultat |
|-------|----------|--------|----------|
| 30° | 2.60 | 1.50 | Triangle allongé horizontalement |
| 45° | 2.12 | 2.12 | Triangle isocèle rectangle |
| 60° | 1.50 | 2.60 | Triangle allongé verticalement |

#### Code TikZ Généré

```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=2]
  % Triangle rectangle
  \draw[very thick] (0,0) -- (2.60,0) -- (2.60,1.50) -- cycle;

  % Angle droit (petit carré)
  \draw (2.60,0) -- (2.40,0) -- (2.40,0.2) -- (2.60,0.2);

  % Arc pour l'angle θ
  \draw[very thick, red] (0.6,0) arc (0:30:0.6);
  \node[red] at (0.8,0.15) {$\theta$};

  % Labels des côtés
  \node[below] at (1.30,0) {adjacent};
  \node[right] at (2.60,0.75) {opposé};
  \node[above left] at (1.30,0.75) {hypoténuse};

  % Formule sinus
  \node[below] at (1.30,-0.8) {$\sin(\theta) = \frac{\text{opposé}}{\text{hypoténuse}}$};
\end{tikzpicture}
\end{document}
```

---

## 2️⃣ Triangle Quelconque

### `triangle_quelconque(a=3, b=4, c=5, afficher_angles=True)`

**Usage:** Géométrie générale, triplets pythagoriciens, loi des cosinus

#### Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `a` | int/float | 3 | Longueur côté BC |
| `b` | int/float | 4 | Longueur côté AC |
| `c` | int/float | 5 | Longueur côté AB |
| `afficher_angles` | bool | True | Afficher les angles α, β, γ |

#### Caractéristiques

- **Sommets:** A (origine), B (sur axe x), C (calculé)
- **Position C:** Calculée avec loi des cosinus
- **Points marqués:** Cercles aux 3 sommets
- **Labels sommets:** A, B, C
- **Labels côtés:** a, b, c avec longueurs
- **Angles:** α (en A), β (en B), γ (en C) en rouge

#### Notation Standard

```
Côté a = BC (opposé à A)
Côté b = AC (opposé à B)
Côté c = AB (opposé à C)

Angle α en A
Angle β en B
Angle γ en C
```

#### Exemples

```python
from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

# Triangle 3-4-5 (rectangle classique)
tri_345 = gen.triangle_quelconque(a=3, b=4, c=5)

# Triangle 5-12-13 (triplet pythagoricien)
tri_51213 = gen.triangle_quelconque(a=5, b=12, c=13)

# Triangle 7-8-9 (quelconque)
tri_789 = gen.triangle_quelconque(a=7, b=8, c=9)

# Sans angles
tri_simple = gen.triangle_quelconque(a=3, b=4, c=5, afficher_angles=False)
```

#### Triplets Pythagoriciens Classiques

| a | b | c | Type |
|---|---|---|------|
| 3 | 4 | 5 | Rectangle (a² + b² = c²) |
| 5 | 12 | 13 | Rectangle |
| 8 | 15 | 17 | Rectangle |
| 7 | 24 | 25 | Rectangle |
| 6 | 8 | 10 | Multiple de 3-4-5 |

#### Code TikZ Généré

```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=1.5]
  % Triangle
  \draw[very thick] (0,0) -- (5,0) -- (3.20,2.40) -- cycle;

  % Points
  \fill (0,0) circle (0.05);
  \fill (5,0) circle (0.05);
  \fill (3.20,2.40) circle (0.05);

  % Labels des sommets
  \node[below left] at (0,0) {$A$};
  \node[below right] at (5,0) {$B$};
  \node[above] at (3.20,2.40) {$C$};

  % Labels des côtés
  \node[below] at (2.5,0) {$c = 5$};
  \node[left] at (1.60,1.20) {$b = 4$};
  \node[right] at (4.10,1.20) {$a = 3$};

  % Angles
  \node[red, right] at (0.3,0.1) {$\alpha$};
  \node[red, left] at (4.7,0.1) {$\beta$};
  \node[red, below] at (3.20,2.20) {$\gamma$};
\end{tikzpicture}
\end{document}
```

---

## 🎨 Comparaison Triangle Rectangle vs Quelconque

| Aspect | Triangle Rectangle | Triangle Quelconque |
|--------|-------------------|---------------------|
| **Usage** | Définitions trigonométriques | Géométrie générale |
| **Paramètres** | Angle θ + formule | 3 côtés a, b, c |
| **Dimensions** | Calculées (hyp=3) | Spécifiées par l'utilisateur |
| **Labels côtés** | Texte (adjacent, opposé) | Variables ($a$, $b$, $c$) |
| **Formule** | sin/cos/tan affichée | Pas de formule |
| **Angle droit** | Marqué avec carré | Peut ne pas exister |
| **Angles** | θ uniquement | α, β, γ (optionnel) |

---

## 🧪 Tests et Validation

### Test Triangle Rectangle

```bash
python -c "
from generateur_formes_geometriques import GenerateurFormesGeometriques
gen = GenerateurFormesGeometriques()
print(gen.triangle_rectangle(30, type_formule='sin'))
"
```

**Vérifications:**
- ✅ \usepackage{tikz} présent
- ✅ Dimensions: adjacent=2.60, opposé=1.50
- ✅ Formule sin correcte
- ✅ Angle droit marqué

### Test Triangle Quelconque

```bash
python -c "
from generateur_formes_geometriques import GenerateurFormesGeometriques
gen = GenerateurFormesGeometriques()
print(gen.triangle_quelconque(3, 4, 5))
"
```

**Vérifications:**
- ✅ \usepackage{tikz} présent
- ✅ Coordonnées: C(3.20, 2.40)
- ✅ 3 sommets A, B, C
- ✅ 3 côtés a=3, b=4, c=5
- ✅ 3 angles α, β, γ

---

## 📊 Cas d'Usage Pédagogiques

### 1. Cours de Trigonométrie

**Définition du sinus:**
```python
# Montrer plusieurs angles avec sinus
for angle in [30, 45, 60]:
    tikz = gen.triangle_rectangle(angle, type_formule="sin")
    # Insérer dans note Obsidian
```

**Les 3 rapports:**
```python
# Même angle, 3 formules différentes
angle = 30
tri_sin = gen.triangle_rectangle(angle, type_formule="sin")
tri_cos = gen.triangle_rectangle(angle, type_formule="cos")
tri_tan = gen.triangle_rectangle(angle, type_formule="tan")
```

### 2. Théorème de Pythagore

**Vérification visuelle:**
```python
# Triangle 3-4-5 rectangle
tri = gen.triangle_quelconque(3, 4, 5)
# On voit que c'est un triangle rectangle
# 3² + 4² = 9 + 16 = 25 = 5²
```

### 3. Loi des Cosinus

**Exemple:**
```python
# Triangle 7-8-9 quelconque
tri = gen.triangle_quelconque(7, 8, 9)
# c² = a² + b² - 2ab cos(γ)
# 81 = 49 + 64 - 2(7)(8) cos(γ)
# cos(γ) = 0.286 → γ ≈ 73.4°
```

---

## ✅ Corrections TikZ Appliquées

Toutes les corrections pour TikZJax ont été appliquées:

| Correction | Status |
|-----------|--------|
| \usepackage{tikz} | ✅ Ajouté |
| Format complet | ✅ \begin{document} ... \end{document} |
| Compatible Obsidian | ✅ TikZJax ready |

---

## 🚀 Utilisation dans Notes

### Note "Fonction Sinus"

```markdown
## Définition Trigonométrique

[Triangle rectangle 30° avec formule sin]

Le sinus d'un angle est le rapport entre
le côté opposé et l'hypoténuse.
```

### Note "Théorème de Pythagore"

```markdown
## Exemple: Triangle 3-4-5

[Triangle quelconque 3-4-5]

On vérifie: 3² + 4² = 9 + 16 = 25 = 5² ✓
```

---

**Date:** 2026-01-10
**Version:** 2.1 - Triangles Corrigés TikZJax
**Statut:** ✅ Testé et Validé
**Fichiers:**
- [generateur_formes_geometriques.py](c:\code\code-Graphique-final\generateur_formes_geometriques.py)
- [test_triangles_complet.py](c:\code\code-Graphique-final\test_triangles_complet.py)
