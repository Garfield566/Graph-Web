import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("TEST CUBE 3D - Vérification des 8 Sommets")
print("=" * 80)

result = gen.cube_3d(taille=2, perspective=True)

print("\n🎲 Cube généré:")
print(result)

print("\n" + "=" * 80)
print("VÉRIFICATION DES SOMMETS")
print("=" * 80)

sommets_attendus = ["A", "B", "C", "D", "E", "F", "G", "H"]
sommets_trouves = []

for sommet in sommets_attendus:
    if f"${sommet}$" in result:
        sommets_trouves.append(sommet)
        print(f"✅ Sommet {sommet} trouvé")
    else:
        print(f"❌ Sommet {sommet} MANQUANT")

print("\n" + "=" * 80)
print(f"RÉSULTAT: {len(sommets_trouves)}/8 sommets")
if len(sommets_trouves) == 8:
    print("✅ SUCCÈS - Tous les 8 sommets du cube sont nommés!")
else:
    print(f"❌ ÉCHEC - Il manque {8 - len(sommets_trouves)} sommets")
print("=" * 80)
