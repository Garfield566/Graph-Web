import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques
import math

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("TEST DE GÉNÉRATION RÉELLE - Vérification des Calculs")
print("=" * 80)

# ============= TEST 1: Cercle Trigonométrique - Différents Angles =============
print("\n" + "=" * 80)
print("TEST 1: Cercle Trigonométrique - Vérification Calculs")
print("=" * 80)

angles_test = [30, 45, 60, 90]
for angle in angles_test:
    result = gen.cercle_trigonometrique(angle_deg=angle)

    # Calculer les valeurs attendues
    angle_rad = math.radians(angle)
    cos_attendu = math.cos(angle_rad)
    sin_attendu = math.sin(angle_rad)

    print(f"\n📐 Angle: {angle}°")
    print(f"  Attendu: cos({angle}°) = {cos_attendu:.3f}, sin({angle}°) = {sin_attendu:.3f}")

    # Chercher les coordonnées dans le code généré
    lines = result.split('\n')
    for line in lines:
        if "Rayon vers le point M" in line:
            # Ligne suivante contient les coordonnées
            idx = lines.index(line)
            coord_line = lines[idx + 1]
            print(f"  Généré: {coord_line.strip()}")

            # Vérifier si les valeurs sont présentes
            if f"{cos_attendu:.3f}" in result or f"{cos_attendu:.2f}" in result:
                print(f"  ✅ Cosinus trouvé dans le code")
            if f"{sin_attendu:.3f}" in result or f"{sin_attendu:.2f}" in result:
                print(f"  ✅ Sinus trouvé dans le code")

# ============= TEST 2: Triangle Rectangle - Différents Angles =============
print("\n" + "=" * 80)
print("TEST 2: Triangle Rectangle - Différents Angles et Formules")
print("=" * 80)

angles_triangle = [30, 45, 60]
formules = ["sin", "cos", "tan"]

for angle in angles_triangle:
    print(f"\n📐 Triangle avec angle {angle}°")

    for formule in formules:
        result = gen.triangle_rectangle(angle_deg=angle, type_formule=formule)

        # Calculer dimensions attendues
        hypotenuse = 3.0
        angle_rad = math.radians(angle)
        adjacent = hypotenuse * math.cos(angle_rad)
        oppose = hypotenuse * math.sin(angle_rad)

        print(f"\n  📝 Formule: {formule}")
        print(f"    Attendu: adjacent={adjacent:.2f}, opposé={oppose:.2f}, hypoténuse={hypotenuse:.2f}")

        # Vérifier que la formule correcte est présente
        if formule == "sin" and "sin(\\theta) = \\frac{\\text{opposé}}{\\text{hypoténuse}}" in result:
            print(f"    ✅ Formule sin correcte")
        elif formule == "cos" and "cos(\\theta) = \\frac{\\text{adjacent}}{\\text{hypoténuse}}" in result:
            print(f"    ✅ Formule cos correcte")
        elif formule == "tan" and "tan(\\theta) = \\frac{\\text{opposé}}{\\text{adjacent}}" in result:
            print(f"    ✅ Formule tan correcte")

        # Afficher un extrait du triangle généré
        lines = result.split('\n')
        for i, line in enumerate(lines):
            if "Triangle rectangle" in line and i + 1 < len(lines):
                print(f"    Code: {lines[i+1].strip()}")
                break

# ============= TEST 3: Triangle Quelconque - Différentes Dimensions =============
print("\n" + "=" * 80)
print("TEST 3: Triangle Quelconque - Différentes Dimensions")
print("=" * 80)

triangles = [
    (3, 4, 5, "Triangle 3-4-5 (rectangle)"),
    (5, 6, 7, "Triangle 5-6-7"),
    (2, 3, 4, "Triangle 2-3-4"),
]

for a, b, c, nom in triangles:
    result = gen.triangle_quelconque(a=a, b=b, c=c, afficher_angles=True)

    print(f"\n📐 {nom}")
    print(f"  Côtés: a={a}, b={b}, c={c}")

    # Vérifier présence des valeurs
    if f"({a},0)" in result or f"({a}," in result:
        print(f"  ✅ Côté a={a} trouvé dans coordonnées")

    # Afficher coordonnées trouvées
    lines = result.split('\n')
    for line in lines:
        if "\\draw[very thick]" in line and "--" in line:
            print(f"  Généré: {line.strip()}")
            break

# ============= TEST 4: Cube 3D - Vérification Points =============
print("\n" + "=" * 80)
print("TEST 4: Cube 3D - Vérification des 8 Sommets")
print("=" * 80)

result = gen.cube_3d(taille=2, perspective=True)

print("\n🎲 Cube 3D (taille=2)")
print("\nRecherche des 8 sommets (A, B, C, D, E, F, G, H):")

sommets_trouves = []
for lettre in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    if f"{{{lettre}}}$" in result or f"at (0,0) {{{lettre}}}" in result or f"{lettre}$" in result:
        sommets_trouves.append(lettre)

print(f"  Sommets trouvés: {sommets_trouves}")
if len(sommets_trouves) == 8:
    print(f"  ✅ SUCCÈS: Les 8 sommets sont présents!")
else:
    print(f"  ❌ PROBLÈME: Seulement {len(sommets_trouves)} sommets sur 8!")

# Afficher le code du cube
print("\n📄 Code généré pour le cube:")
lines = result.split('\n')
for line in lines:
    if "\\node" in line:
        print(f"  {line.strip()}")

# ============= TEST 5: Polygones - Différents Nombres de Côtés =============
print("\n" + "=" * 80)
print("TEST 5: Polygones Réguliers - Différents Nombres de Côtés")
print("=" * 80)

for n in [3, 4, 5, 6, 8]:
    result = gen.polygone_regulier(n_cotes=n, rayon=2)

    print(f"\n📐 Polygone à {n} côtés (rayon=2)")

    # Compter le nombre de lignes \draw
    nb_draw = result.count("\\draw[very thick]")
    print(f"  Nombre de segments tracés: {nb_draw}")

    if nb_draw == n:
        print(f"  ✅ Correct: {n} côtés tracés")
    else:
        print(f"  ❌ PROBLÈME: {nb_draw} segments au lieu de {n}")

    # Compter sommets
    nb_sommets = result.count("$S_{")
    print(f"  Nombre de sommets: {nb_sommets}")

    if nb_sommets == n:
        print(f"  ✅ Correct: {n} sommets")
    else:
        print(f"  ❌ PROBLÈME: {nb_sommets} sommets au lieu de {n}")

# ============= TEST 6: Vecteurs - Différentes Coordonnées =============
print("\n" + "=" * 80)
print("TEST 6: Addition Vecteurs - Différentes Coordonnées")
print("=" * 80)

tests_vecteurs = [
    ((2, 1), (1, 2), "u=(2,1) v=(1,2)"),
    ((3, 0), (0, 3), "u=(3,0) v=(0,3)"),
    ((1, 1), (1, 1), "u=(1,1) v=(1,1)"),
]

for u, v, nom in tests_vecteurs:
    result = gen.addition_vecteurs(u=u, v=v, methode="parallelogramme")

    somme = (u[0] + v[0], u[1] + v[1])

    print(f"\n📐 {nom}")
    print(f"  Somme attendue: u+v = ({somme[0]}, {somme[1]})")

    # Vérifier que la somme est dans le code
    if f"({u[0]},{u[1]})" in result:
        print(f"  ✅ Vecteur u trouvé")
    if f"({v[0]},{v[1]})" in result:
        print(f"  ✅ Vecteur v trouvé")
    if f"({somme[0]},{somme[1]})" in result:
        print(f"  ✅ Somme u+v trouvée")

print("\n" + "=" * 80)
print("FIN DES TESTS DE GÉNÉRATION RÉELLE")
print("=" * 80)
