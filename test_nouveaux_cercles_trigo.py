import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("TEST DES NOUVEAUX CERCLES TRIGONOMÉTRIQUES")
print("=" * 80)

# Test 1: Cercle complet avec toutes les valeurs
print("\n1️⃣ CERCLE TRIGONOMÉTRIQUE COMPLET")
print("   (Toutes les valeurs remarquables: 0° à 330°)")
print("=" * 80)
result = gen.cercle_trigo_complet_valeurs()
print(result)

# Test 2: Angle spécifique 30°
print("\n\n2️⃣ ANGLE SPÉCIFIQUE: 30°")
print("   (Avec valeurs exactes en radians)")
print("=" * 80)
result = gen.cercle_trigo_angle_specifique(angle_deg=30)
print(result)

# Test 3: Angle spécifique 45°
print("\n\n3️⃣ ANGLE SPÉCIFIQUE: 45°")
print("=" * 80)
result = gen.cercle_trigo_angle_specifique(angle_deg=45)
print(result)

# Test 4: Angle spécifique 60°
print("\n\n4️⃣ ANGLE SPÉCIFIQUE: 60°")
print("=" * 80)
result = gen.cercle_trigo_angle_specifique(angle_deg=60)
print(result)

# Test 5: Angle spécifique 120° (2ème quadrant)
print("\n\n5️⃣ ANGLE SPÉCIFIQUE: 120° (2ème quadrant)")
print("=" * 80)
result = gen.cercle_trigo_angle_specifique(angle_deg=120)
print(result)

# Test 6: Angle spécifique 240° (3ème quadrant)
print("\n\n6️⃣ ANGLE SPÉCIFIQUE: 240° (3ème quadrant)")
print("=" * 80)
result = gen.cercle_trigo_angle_specifique(angle_deg=240)
print(result)

print("\n" + "=" * 80)
print("✅ TESTS TERMINÉS")
print("=" * 80)
