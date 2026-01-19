import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques
import math

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("🧮 ÉQUATION TRIGONOMÉTRIQUE SUR [0, 4π]")
print("=" * 80)

print("\n📝 Problème: Résoudre sin(θ) = √2/2 pour θ ∈ [0, 4π] (2 tours complets)")
print()

print("💡 Solution mathématique:")
print("   sin(θ) = √2/2")
print()
print("   Sur [0, 2π], les solutions sont:")
print("   • θ₁ = 45° = π/4 rad")
print("   • θ₂ = 135° = 3π/4 rad")
print()
print("   Sur [2π, 4π] (2ème tour), on ajoute 2π = 360°:")
print("   • θ₃ = 405° = 45° + 360° = 9π/4 rad")
print("   • θ₄ = 495° = 135° + 360° = 11π/4 rad")
print()
print("   TOTAL: 4 solutions sur [0, 4π]")

print("\n" + "=" * 80)
print("📊 VISUALISATION DES 4 SOLUTIONS")
print("=" * 80)

solutions = [
    (45, "π/4", "1er tour - 1er quadrant"),
    (135, "3π/4", "1er tour - 2ème quadrant"),
]

# Pour visualiser, on montre les angles équivalents dans [0, 360°]
# car le cercle trigo se répète
solutions_equivalentes = [
    (45, "9π/4 ≡ π/4 (mod 2π)", "2ème tour - même position que 45°"),
    (135, "11π/4 ≡ 3π/4 (mod 2π)", "2ème tour - même position que 135°"),
]

print("\n🔵 PREMIER TOUR [0, 2π]:")
print("=" * 80)

for i, (angle, radian, desc) in enumerate(solutions, 1):
    print(f"\n{i}️⃣ Solution {i}: θ = {angle}° = {radian}")
    print(f"   Description: {desc}")
    print("-" * 80)
    result = gen.cercle_trigo_angle_specifique(angle)
    print(result)

print("\n\n🟢 DEUXIÈME TOUR [2π, 4π]:")
print("=" * 80)
print("\nNote: Sur le cercle trigonométrique, les positions sont identiques")
print("car sin(θ + 2π) = sin(θ) (périodicité)")
print()

for i, (angle, radian, desc) in enumerate(solutions_equivalentes, 3):
    print(f"\n{i}️⃣ Solution {i}: θ = {radian}")
    print(f"   Angle équivalent sur [0, 360°]: {angle}°")
    print(f"   Description: {desc}")
    print("-" * 80)
    # On affiche le même graphique car c'est la même position
    result = gen.cercle_trigo_angle_specifique(angle)
    # Remplacer le label pour montrer qu'on est au 2ème tour
    if angle == 45:
        result = result.replace("\\frac{\\pi}{4}", "\\frac{9\\pi}{4}")
        result = result.replace("= 45^\\circ", "= 405^\\circ (\\equiv 45^\\circ)")
    elif angle == 135:
        result = result.replace("\\frac{3\\pi}{4}", "\\frac{11\\pi}{4}")
        result = result.replace("= 135^\\circ", "= 495^\\circ (\\equiv 135^\\circ)")
    print(result)

print("\n" + "=" * 80)
print("📊 VÉRIFICATION NUMÉRIQUE")
print("=" * 80)

solutions_radians = [
    (math.pi/4, "π/4", 45),
    (3*math.pi/4, "3π/4", 135),
    (9*math.pi/4, "9π/4", 405),
    (11*math.pi/4, "11π/4", 495),
]

for theta_rad, nom, deg in solutions_radians:
    sin_val = math.sin(theta_rad)
    sqrt2_2 = math.sqrt(2)/2
    print(f"\n✅ θ = {nom} rad = {deg}°")
    print(f"   sin({nom}) = {sin_val:.6f}")
    print(f"   √2/2 = {sqrt2_2:.6f}")
    print(f"   Égalité: {abs(sin_val - sqrt2_2) < 1e-10} ✓")

print("\n" + "=" * 80)
print("🎯 CONCLUSION")
print("=" * 80)
print("\nL'équation sin(θ) = √2/2 sur [0, 4π] a bien 4 solutions:")
print()
print("• 2 solutions sur le 1er tour [0, 2π]:")
print("  - θ₁ = π/4 (45°)")
print("  - θ₂ = 3π/4 (135°)")
print()
print("• 2 solutions sur le 2ème tour [2π, 4π]:")
print("  - θ₃ = 9π/4 (405°) = π/4 + 2π")
print("  - θ₄ = 11π/4 (495°) = 3π/4 + 2π")
print()
print("Sur le cercle trigonométrique, θ₃ et θ₁ sont au même point")
print("(de même pour θ₄ et θ₂) à cause de la périodicité 2π.")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ")
print("=" * 80)
