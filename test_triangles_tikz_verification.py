import sys
sys.stdout.reconfigure(encoding='utf-8')

from generateur_formes_geometriques import GenerateurFormesGeometriques

gen = GenerateurFormesGeometriques()

print("=" * 80)
print("🔍 VÉRIFICATION COMPLÈTE TikZJax - TRIANGLES")
print("=" * 80)

print("\n" + "=" * 80)
print("1️⃣ TRIANGLE RECTANGLE")
print("=" * 80)

# Test triangle rectangle avec différents angles et formules
angles = [30, 45, 60]
formules = ["sin", "cos", "tan"]

all_passed = True

for angle in angles:
    for formule in formules:
        result = gen.triangle_rectangle(angle_deg=angle, type_formule=formule)

        print(f"\n📐 Triangle rectangle {angle}° - Formule {formule}:")

        # Vérifications critiques
        checks = {
            "\\usepackage{tikz}": "Package TikZ",
            "\\begin{document}": "Document début",
            "\\end{document}": "Document fin",
            "\\begin{tikzpicture}": "TikzPicture début",
            "\\end{tikzpicture}": "TikzPicture fin",
            f"\\{formule}(\\theta)": f"Formule {formule}",
            "adjacent": "Label adjacent",
            "opposé": "Label opposé",
            "hypoténuse": "Label hypoténuse"
        }

        for pattern, description in checks.items():
            if pattern in result:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} MANQUANT!")
                all_passed = False

print("\n" + "=" * 80)
print("2️⃣ TRIANGLE QUELCONQUE")
print("=" * 80)

# Test triangle quelconque avec différents triplets
triplets = [
    (3, 4, 5, "3-4-5"),
    (5, 12, 13, "5-12-13"),
    (8, 15, 17, "8-15-17")
]

for a, b, c, nom in triplets:
    result = gen.triangle_quelconque(a=a, b=b, c=c)

    print(f"\n📐 Triangle quelconque {nom}:")

    # Vérifications critiques
    checks = {
        "\\usepackage{tikz}": "Package TikZ",
        "\\begin{document}": "Document début",
        "\\end{document}": "Document fin",
        "\\begin{tikzpicture}": "TikzPicture début",
        "\\end{tikzpicture}": "TikzPicture fin",
        "$A$": "Sommet A",
        "$B$": "Sommet B",
        "$C$": "Sommet C",
        f"$a = {a}$": f"Côté a={a}",
        f"$b = {b}$": f"Côté b={b}",
        f"$c = {c}$": f"Côté c={c}",
        "$\\alpha$": "Angle alpha",
        "$\\beta$": "Angle beta",
        "$\\gamma$": "Angle gamma"
    }

    for pattern, description in checks.items():
        if pattern in result:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} MANQUANT!")
            all_passed = False

print("\n" + "=" * 80)
print("3️⃣ VÉRIFICATIONS TIKZJAX SPÉCIFIQUES")
print("=" * 80)

# Test avec un triangle de chaque type
tri_rect = gen.triangle_rectangle(angle_deg=30, type_formule="sin")
tri_quelc = gen.triangle_quelconque(a=3, b=4, c=5)

print("\n🔍 Triangle Rectangle 30° (sin):")

# Vérifications des corrections TikZJax
tikzjax_checks = {
    "\\usepackage{tikz}": "❌→✅ Package TikZ (CRITIQUE)",
    "font=\\small": "Devrait être ABSENT (cause textes invisibles)",
    "°": "Devrait être ABSENT (utiliser ^\\circ)",
    "scale=": "Échelle définie"
}

for pattern, description in tikzjax_checks.items():
    if pattern == "font=\\small" or pattern == "°":
        # Ces patterns devraient être absents
        if pattern not in tri_rect:
            print(f"  ✅ {description}: NON présent ✓")
        else:
            print(f"  ❌ {description}: ENCORE présent!")
            all_passed = False
    else:
        # Ces patterns devraient être présents
        if pattern in tri_rect:
            print(f"  ✅ {description}: Présent ✓")
        else:
            print(f"  ❌ {description}: MANQUANT!")
            all_passed = False

print("\n🔍 Triangle Quelconque 3-4-5:")

for pattern, description in tikzjax_checks.items():
    if pattern == "font=\\small" or pattern == "°":
        # Ces patterns devraient être absents
        if pattern not in tri_quelc:
            print(f"  ✅ {description}: NON présent ✓")
        else:
            print(f"  ❌ {description}: ENCORE présent!")
            all_passed = False
    else:
        # Ces patterns devraient être présents
        if pattern in tri_quelc:
            print(f"  ✅ {description}: Présent ✓")
        else:
            print(f"  ❌ {description}: MANQUANT!")
            all_passed = False

print("\n" + "=" * 80)
print("📊 RÉSULTAT FINAL")
print("=" * 80)

if all_passed:
    print("\n✅ TOUS LES TESTS SONT PASSÉS!")
    print("\nLes triangles sont 100% compatibles TikZJax:")
    print("  • \\usepackage{tikz} présent")
    print("  • Pas de font=\\small")
    print("  • Pas de symbole ° direct")
    print("  • Structure document complète")
    print("  • Tous les labels présents")
else:
    print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
    print("\nVérifiez les erreurs ci-dessus.")

print("\n" + "=" * 80)
print("✅ TEST DE VÉRIFICATION TERMINÉ")
print("=" * 80)
