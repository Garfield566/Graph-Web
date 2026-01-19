import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("🧮 CALCUL TRIGONOMÉTRIQUE - Résolution d'Équation")
print("=" * 80)

print("\n📝 Problème: Résoudre l'équation cos(θ) = 1/2 pour θ ∈ [0°, 360°]")
print()

print("💡 Solution mathématique:")
print("   cos(θ) = 1/2")
print("   Les solutions sont:")
print("   • θ₁ = 60° = π/3 rad")
print("   • θ₂ = 300° = 5π/3 rad")
print()

print("=" * 80)
print("1️⃣ SOLUTION 1: θ = 60°")
print("=" * 80)

solution1 = gen.cercle_trigo_angle_specifique(60)
print(solution1)

print("\n" + "=" * 80)
print("2️⃣ SOLUTION 2: θ = 300°")
print("=" * 80)

solution2 = gen.cercle_trigo_angle_specifique(300)
print(solution2)

print("\n" + "=" * 80)
print("📊 VÉRIFICATION")
print("=" * 80)

import math

# Solution 1: 60°
theta1 = 60
cos1 = math.cos(math.radians(theta1))
sin1 = math.sin(math.radians(theta1))

print(f"\n✅ Solution 1: θ = {theta1}°")
print(f"   cos(60°) = {cos1:.3f} ≈ 1/2 ✓")
print(f"   sin(60°) = {sin1:.3f} ≈ √3/2")
print(f"   Point M₁ = ({cos1:.3f}, {sin1:.3f})")

# Solution 2: 300°
theta2 = 300
cos2 = math.cos(math.radians(theta2))
sin2 = math.sin(math.radians(theta2))

print(f"\n✅ Solution 2: θ = {theta2}°")
print(f"   cos(300°) = {cos2:.3f} ≈ 1/2 ✓")
print(f"   sin(300°) = {sin2:.3f} ≈ -√3/2")
print(f"   Point M₂ = ({cos2:.3f}, {sin2:.3f})")

print("\n" + "=" * 80)
print("🎯 OBSERVATION")
print("=" * 80)
print("\nLes deux points M₁ et M₂ sont symétriques par rapport à l'axe des x.")
print("Ils ont la même abscisse (cos = 1/2) mais des ordonnées opposées.")
print("\n• M₁ est dans le 1er quadrant (cos > 0, sin > 0)")
print("• M₂ est dans le 4ème quadrant (cos > 0, sin < 0)")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ")
print("=" * 80)
