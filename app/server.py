"""
Serveur Flask pour le Générateur de Graphiques TikZ
Lance une interface web pour générer des graphiques mathématiques
"""

import sys
import os
import re
import webbrowser
from threading import Timer

# Ajouter le dossier parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify

# Importer les générateurs
from generateur_graphiques import TikzGraphGenerator
from generateur_formes_geometriques import GenerateurFormesGeometriques

app = Flask(__name__)

# Initialiser les générateurs
graph_generator = TikzGraphGenerator()
forme_generator = GenerateurFormesGeometriques()


def parse_forme_geometrique(ligne):
    """
    Parse une commande de forme géométrique et retourne le code TikZ.

    Formats supportés:
    - cercle_trigo(angle) ou cercle_trigo(45)
    - cercle_trigo_complet()
    - cercle_trigo_multiple(30,45,60,90)
    - cercle_trigo_angle(30)
    - triangle_rectangle(angle, formule) ou triangle_rectangle(30, sin)
    - triangle(a, b, c) ou triangle(3, 4, 5)
    - polygone(n) ou polygone(6)
    - cube() ou cube(taille)
    - pyramide() ou pyramide(base, hauteur)
    - vecteur(x, y) ou vecteur(2, 3)
    - addition_vecteurs(ux, uy, vx, vy)
    - repere_2d() ou repere_3d()
    """
    ligne = ligne.strip().lower()

    # Cercle trigonométrique simple
    match = re.match(r'cercle_trigo\s*\(\s*(\d+)\s*\)', ligne)
    if match:
        angle = int(match.group(1))
        return forme_generator.cercle_trigonometrique(angle_deg=angle)

    # Cercle trigonométrique complet
    if 'cercle_trigo_complet' in ligne:
        return forme_generator.cercle_trigo_complet_valeurs()

    # Cercle trigonométrique avec angle spécifique et valeurs
    match = re.match(r'cercle_trigo_angle\s*\(\s*(\d+)\s*\)', ligne)
    if match:
        angle = int(match.group(1))
        return forme_generator.cercle_trigo_angle_specifique(angle_deg=angle)

    # Cercle trigonométrique multiple angles
    match = re.match(r'cercle_trigo_multiple\s*\(\s*([\d,\s]+)\s*\)', ligne)
    if match:
        angles_str = match.group(1)
        angles = [int(a.strip()) for a in angles_str.split(',')]
        return forme_generator.cercle_trigo_multiple_angles(angles_deg=angles)

    # Triangle rectangle
    match = re.match(r'triangle_rectangle\s*\(\s*(\d+)\s*(?:,\s*(\w+))?\s*\)', ligne)
    if match:
        angle = int(match.group(1))
        formule = match.group(2) if match.group(2) else 'sin'
        return forme_generator.triangle_rectangle(angle_deg=angle, type_formule=formule)

    # Triangle quelconque
    match = re.match(r'triangle\s*\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)', ligne)
    if match:
        a = float(match.group(1))
        b = float(match.group(2))
        c = float(match.group(3))
        return forme_generator.triangle_quelconque(a=a, b=b, c=c)

    # Polygone régulier
    match = re.match(r'polygone\s*\(\s*(\d+)\s*\)', ligne)
    if match:
        n = int(match.group(1))
        return forme_generator.polygone_regulier(n_cotes=n)

    # Cube
    match = re.match(r'cube\s*\(\s*(\d+(?:\.\d+)?)?\s*\)', ligne)
    if match:
        taille = float(match.group(1)) if match.group(1) else 2
        return forme_generator.cube_3d(taille=taille)

    # Pyramide
    match = re.match(r'pyramide\s*\(\s*(?:(\d+(?:\.\d+)?)\s*(?:,\s*(\d+(?:\.\d+)?))?)?\s*\)', ligne)
    if match:
        base = float(match.group(1)) if match.group(1) else 2
        hauteur = float(match.group(2)) if match.group(2) else 3
        return forme_generator.pyramide_3d(base=base, hauteur=hauteur)

    # Vecteur 2D
    match = re.match(r'vecteur\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)', ligne)
    if match:
        vx = float(match.group(1))
        vy = float(match.group(2))
        return forme_generator.vecteur_2d(vecteurs=[(vx, vy, r"\vec{u}")])

    # Addition de vecteurs
    match = re.match(r'addition_vecteurs\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)', ligne)
    if match:
        ux = float(match.group(1))
        uy = float(match.group(2))
        vx = float(match.group(3))
        vy = float(match.group(4))
        return forme_generator.addition_vecteurs(u=(ux, uy), v=(vx, vy))

    # Repère 2D
    if 'repere_2d' in ligne or 'repere2d' in ligne:
        return forme_generator.repere_2d()

    # Repère 3D
    if 'repere_3d' in ligne or 'repere3d' in ligne:
        return forme_generator.repere_3d()

    return None


def generate_single(ligne):
    """Génère le code TikZ pour une seule ligne d'entrée."""
    ligne = ligne.strip()
    if not ligne:
        return None

    # Vérifier si c'est une forme géométrique
    forme_result = parse_forme_geometrique(ligne)
    if forme_result:
        return forme_result

    # Sinon, c'est une fonction mathématique
    try:
        return graph_generator.generer_fonction(ligne)
    except Exception as e:
        return f"% Erreur pour '{ligne}': {str(e)}"


@app.route('/')
def index():
    """Page principale."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint pour générer les graphiques."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Pas de données reçues'})

        functions_text = data.get('functions', '')
        if not functions_text:
            return jsonify({'success': False, 'error': 'Aucune fonction fournie'})

        # Séparer les lignes
        lignes = functions_text.strip().split('\n')

        # Générer chaque graphique
        results = []
        errors = []
        for ligne in lignes:
            ligne = ligne.strip()
            if ligne and not ligne.startswith('#') and not ligne.startswith('//'):
                try:
                    result = generate_single(ligne)
                    if result:
                        results.append(f"% === {ligne} ===\n{result}")
                except Exception as e:
                    errors.append(f"% Erreur pour '{ligne}': {str(e)}")

        if results:
            final_result = '\n\n'.join(results)
            if errors:
                final_result += '\n\n% === ERREURS ===\n' + '\n'.join(errors)
            return jsonify({'success': True, 'result': final_result})
        elif errors:
            return jsonify({'success': False, 'error': '\n'.join(errors)})
        else:
            return jsonify({'success': False, 'error': 'Aucune fonction valide trouvée'})

    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': f'{str(e)}\n{traceback.format_exc()}'})


def open_browser():
    """Ouvre le navigateur après un court délai."""
    webbrowser.open('http://127.0.0.1:5000')


if __name__ == '__main__':
    print("=" * 60)
    print("  GÉNÉRATEUR DE GRAPHIQUES TIKZ")
    print("  Interface Web")
    print("=" * 60)
    print()
    print("Démarrage du serveur...")
    print("L'application s'ouvrira dans votre navigateur.")
    print()
    print("URL: http://127.0.0.1:5000")
    print()
    print("Pour arrêter le serveur, appuyez sur Ctrl+C")
    print("=" * 60)

    # Ouvrir le navigateur après 1.5 secondes
    Timer(1.5, open_browser).start()

    # Lancer le serveur Flask
    app.run(host='127.0.0.1', port=5000, debug=False)
