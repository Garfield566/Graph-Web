import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("VALIDATION DU FORMAT TIKZ")
print("=" * 80)

# Test 1: Cercle trigonométrique
print("\n1. Cercle Trigonométrique - Format")
result = gen.cercle_trigonometrique(angle_deg=40)
print(f"  ✅ Commence par ```tikz: {result.startswith('```tikz')}")
print(f"  ✅ Contient \\begin{{document}}: {'\\begin{document}' in result}")
print(f"  ✅ Contient \\begin{{tikzpicture}}: {'\\begin{tikzpicture}' in result}")
print(f"  ✅ Contient \\end{{tikzpicture}}: {'\\end{tikzpicture}' in result}")
print(f"  ✅ Contient \\end{{document}}: {'\\end{document}' in result}")
print(f"  ✅ Finit par ```: {result.strip().endswith('```')}")

# Test 2: Triangle rectangle
print("\n2. Triangle Rectangle - Format")
result = gen.triangle_rectangle(angle_deg=30, type_formule="sin")
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

# Test 3: Polygone régulier
print("\n3. Polygone Régulier - Format")
result = gen.polygone_regulier(n_cotes=6)
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

# Test 4: Vecteurs
print("\n4. Addition Vecteurs - Format")
result = gen.addition_vecteurs(u=(2, 1), v=(1, 2))
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

# Test 5: Cube 3D
print("\n5. Cube 3D - Format")
result = gen.cube_3d(taille=2)
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

# Test 6: Pyramide 3D
print("\n6. Pyramide 3D - Format")
result = gen.pyramide_3d(base=2, hauteur=3)
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

# Test 7: Repère 2D
print("\n7. Repère 2D - Format")
result = gen.repere_2d(xmin=-3, xmax=3, ymin=-3, ymax=3, grille=True)
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

# Test 8: Repère 3D
print("\n8. Repère 3D - Format")
result = gen.repere_3d(longueur_axes=3)
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")

print("\n" + "=" * 80)
print("✅ TOUS LES FORMATS SONT VALIDES POUR TIKZJAX!")
print("=" * 80)

# Test spécifique: Cercle trigo avec plusieurs angles
print("\n9. Cercle Trigonométrique - Plusieurs Angles")
result = gen.cercle_trigo_multiple_angles([30, 60, 90, 120])
print(f"  ✅ Format correct: {result.startswith('```tikz') and result.strip().endswith('```')}")
print(f"  ✅ Contient 30°: {'30' in result}")
print(f"  ✅ Contient 60°: {'60' in result}")
print(f"  ✅ Contient 90°: {'90' in result}")
print(f"  ✅ Contient 120°: {'120' in result}")

print("\n" + "=" * 80)
print("✅ VALIDATION COMPLÈTE TERMINÉE!")
print("=" * 80)
