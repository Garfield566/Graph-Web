import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("📐 TEST COMPLET DES TRIANGLES")
print("=" * 80)

# ============== TRIANGLES RECTANGLES ==============
print("\n" + "=" * 80)
print("1️⃣ TRIANGLES RECTANGLES - Différents Angles et Formules")
print("=" * 80)

angles_test = [30, 45, 60]
formules = ["sin", "cos", "tan"]

for angle in angles_test:
    print(f"\n{'='*80}")
    print(f"📐 ANGLE {angle}°")
    print("=" * 80)

    for formule in formules:
        print(f"\n🔹 Formule: {formule.upper()}")
        print("-" * 80)
        result = gen.triangle_rectangle(angle_deg=angle, type_formule=formule)
        print(result)
        print()

# ============== TRIANGLES QUELCONQUES ==============
print("\n" + "=" * 80)
print("2️⃣ TRIANGLES QUELCONQUES - Différentes Dimensions")
print("=" * 80)

triangles_test = [
    (3, 4, 5, "Triangle 3-4-5 (rectangle classique)"),
    (5, 12, 13, "Triangle 5-12-13 (triplet pythagoricien)"),
    (8, 15, 17, "Triangle 8-15-17 (triplet pythagoricien)"),
    (6, 8, 10, "Triangle 6-8-10 (multiple de 3-4-5)"),
    (5, 6, 7, "Triangle 5-6-7 (quelconque)"),
    (7, 8, 9, "Triangle 7-8-9 (quelconque)"),
]

for a, b, c, description in triangles_test:
    print(f"\n{'='*80}")
    print(f"📐 {description}")
    print(f"   Côtés: a={a}, b={b}, c={c}")
    print("=" * 80)
    result = gen.triangle_quelconque(a=a, b=b, c=c, afficher_angles=True)
    print(result)
    print()

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ")
print("=" * 80)

# Résumé
print("\n📊 RÉSUMÉ DES TESTS:")
print(f"  • Triangles rectangles: {len(angles_test) * len(formules)} variations")
print(f"  • Triangles quelconques: {len(triangles_test)} exemples")
print(f"  • Total graphiques générés: {len(angles_test) * len(formules) + len(triangles_test)}")
