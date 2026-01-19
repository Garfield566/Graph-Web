from sympy import symbols, sin, cos, ln, log, lambdify, Integral, Symbol, degree
from sympy.parsing.latex import parse_latex
from sympy.core.numbers import Rational
import sympy as sp
import math
import numpy as np
from analyseur_convergence import FonctionAnalyzer

class TikzGraphGenerator:
    def __init__(self, scale=0.9):
        self.scale = scale
        self.analyzer = FonctionAnalyzer()

    def _detecter_variables(self, fonction_latex):
        """Détecte les variables dans une fonction LaTeX."""
        try:
            x, y, z, t = symbols('x y z t')
            expr = parse_latex(fonction_latex)
            variables = expr.free_symbols
            return sorted([str(var) for var in variables])
        except:
            return ['x']

    def _est_integrale(self, fonction_latex):
        """Vérifie si l'expression contient une intégrale."""
        try:
            expr = parse_latex(fonction_latex)
            # Vérifier si l'expression contient des intégrales
            integrals = self.analyzer._extract_integrals(expr)
            return len(integrals) > 0, integrals
        except:
            return False, []

    def analyser_integrale(self, fonction_latex):
        """Analyse une intégrale et retourne les informations de convergence."""
        try:
            expr = parse_latex(fonction_latex)
            integrals = self.analyzer._extract_integrals(expr)

            if not integrals:
                return None

            # Analyser la première intégrale
            result = self.analyzer._analyze_integral(integrals[0])

            return result
        except Exception as e:
            return {"error": str(e)}

    def formater_analyse_convergence(self, result):
        """Formate l'analyse de convergence en texte lisible."""
        if result is None:
            return "Aucune intégrale détectée."

        if "error" in result:
            return f"Erreur lors de l'analyse: {result['error']}"

        lines = []
        lines.append("=" * 80)
        lines.append("ANALYSE DE CONVERGENCE DE L'INTÉGRALE")
        lines.append("=" * 80)
        lines.append("")

        # Statut global
        statut = result.get('overall_status', 'unknown').upper()
        emoji = "✅" if statut == "CONVERGENT" else "❌" if statut == "DIVERGENT" else "⚠️"
        lines.append(f"{emoji} STATUT: {statut}")
        lines.append("")

        # Dimension
        dimension = result.get('dimension', 1)
        lines.append(f"📊 Dimension: {dimension}D")
        lines.append(f"📝 Intégrande: {result.get('integrand', 'N/A')}")
        lines.append("")

        # Informations par variable
        if 'variables_info' in result:
            lines.append("=" * 80)
            lines.append("DÉTAILS PAR VARIABLE")
            lines.append("=" * 80)

            for var_info in result['variables_info']:
                var = var_info.get('variable', '?')
                lower = var_info.get('lower_bound', '?')
                upper = var_info.get('upper_bound', '?')

                lines.append("")
                lines.append(f"Variable: d{var} [{lower}, {upper}]")
                lines.append("-" * 40)

                conv_info = var_info.get('convergence_info', {})

                # Type d'intégrale
                type_integral = conv_info.get('type', 'proper')
                lines.append(f"  Type: {type_integral}")

                # Statut de convergence
                status = conv_info.get('status', 'unknown')
                lines.append(f"  Statut: {status}")

                # Domaine de définition
                if 'domain_info' in conv_info and conv_info['domain_info']:
                    domain = conv_info['domain_info'].get('domain', 'N/A')
                    lines.append(f"  Domaine: {domain}")

                    if conv_info['domain_info'].get('restrictions'):
                        lines.append("  Restrictions:")
                        for key, value in conv_info['domain_info']['restrictions'].items():
                            lines.append(f"    - {key}: {value}")

                # Singularités
                if 'singularities' in conv_info and conv_info['singularities'].get('all'):
                    lines.append("  Singularités détectées:")
                    for sing_type, sing_val in conv_info['singularities']['all']:
                        lines.append(f"    - {sing_type}: {var} = {sing_val:.6f}")

                # Bornes dépendantes
                if var_info.get('dependent_bounds'):
                    deps = var_info['dependent_bounds'].get('dependencies', [])
                    if deps:
                        lines.append(f"  Bornes dépendantes de: {', '.join(deps)}")

        # Problèmes détectés
        if 'all_issues' in result and result['all_issues']:
            lines.append("")
            lines.append("=" * 80)
            lines.append("⚠️  PROBLÈMES DÉTECTÉS")
            lines.append("=" * 80)
            for issue in result['all_issues']:
                lines.append(f"  - {issue}")

        # Avertissements
        if 'all_warnings' in result and result['all_warnings']:
            lines.append("")
            lines.append("=" * 80)
            lines.append("ℹ️  AVERTISSEMENTS")
            lines.append("=" * 80)
            for warning in result['all_warnings']:
                lines.append(f"  - {warning}")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def evaluer_fonction(self, fonction, x, y=None):
        """Évalue une fonction pour une valeur de x (et y si 3D)."""
        try:
            expr = fonction.replace('^', '**') \
                           .replace('cos(', 'math.cos(') \
                           .replace('sin(', 'math.sin(') \
                           .replace('tan(', 'math.tan(') \
                           .replace('ln(', 'math.log(') \
                           .replace('log(', 'math.log10(') \
                           .replace('sqrt(', 'math.sqrt(') \
                           .replace('e^', 'math.exp(')

            if y is not None:
                expr = expr.replace('y', str(y))
            return eval(expr, {'math': math, 'x': x})
        except:
            return None

    def calculer_domaine_adaptatif(self, fonction_latex):
        """Calcule un domaine X adaptatif en analysant les contraintes mathématiques."""
        try:
            # Parser l'expression
            expr = parse_latex(fonction_latex)
            x_sym = sp.Symbol('x', real=True)
            func_str = str(expr)

            # Domaine par défaut
            dom_min, dom_max = -5, 5

            # 1. CONTRAINTES DE DOMAINE (priorité haute)

            # Logarithme: x > 0
            if 'log' in func_str.lower():
                dom_min, dom_max = 0.1, 10

            # Racine carrée
            elif 'sqrt' in func_str:
                if 'sqrt(-x)' in func_str:
                    # sqrt(-x) => x <= 0
                    dom_min, dom_max = -10, -0.01
                else:
                    # sqrt(x) ou sqrt(f(x)) => généralement x >= 0
                    dom_min, dom_max = 0, 10

            # Division par x: 1/x
            elif (func_str == '1/x' or '/x' in func_str) and 'log' not in func_str.lower():
                # TikZ gère la discontinuité
                dom_min, dom_max = -5, 5

            # 2. AJUSTEMENTS SELON COMPORTEMENT (si pas de contrainte forte)

            # Exponentielle avec coefficient: e^(nx)
            elif 'exp' in func_str or 'e**' in func_str or 'E**' in func_str:
                import re
                # Chercher e^(10*x) ou exp(10*x)
                match = re.search(r'(\d+)\*x', func_str)
                if match:
                    coeff = int(match.group(1))
                    if coeff >= 10:
                        dom_min, dom_max = -0.3, 0.3
                    elif coeff >= 5:
                        dom_min, dom_max = -0.5, 0.5
                    elif coeff >= 3:
                        dom_min, dom_max = -1, 1
                    else:
                        dom_min, dom_max = -2, 2
                elif '-x' in func_str:
                    # e^(-x)
                    dom_min, dom_max = 0, 5
                else:
                    # e^x
                    dom_min, dom_max = -3, 3

            # Trigonométrie avec coefficient: sin(nx), cos(nx)
            elif 'sin' in func_str or 'cos' in func_str:
                import re
                match = re.search(r'(\d+)\*x', func_str)
                if match:
                    coeff = int(match.group(1))
                    # Montrer ~2 périodes: 2*2π/n
                    periodes = 2
                    amplitude = periodes * 3.14159 / coeff
                    dom_min, dom_max = -amplitude, amplitude
                else:
                    # 2 périodes complètes
                    dom_min, dom_max = -6.28, 6.28

            # Tangente: asymptotes à ±π/2
            elif 'tan' in func_str:
                dom_min, dom_max = -1.4, 1.4

            # Polynômes avec gros coefficients
            elif expr.is_polynomial(x_sym):
                import re
                # Chercher grands coefficients comme 100*x^2
                coeffs = re.findall(r'(\d+)\*', func_str)
                if coeffs:
                    max_coeff = max(int(c) for c in coeffs)
                    if max_coeff >= 100:
                        dom_min, dom_max = -1, 1
                    elif max_coeff >= 10:
                        dom_min, dom_max = -2, 2

                # Ajuster selon degré
                try:
                    degree = sp.degree(expr, x_sym)
                    if degree >= 5:
                        dom_min, dom_max = max(dom_min, -2), min(dom_max, 2)
                    elif degree >= 3:
                        dom_min, dom_max = max(dom_min, -3), min(dom_max, 3)
                except:
                    pass

            return (dom_min, dom_max)

        except Exception as e:
            # En cas d'erreur, retourner domaine par défaut
            return (-5, 5)

    def calculer_domaine_3d_adaptatif(self, fonction_latex):
        """Calcule un domaine 3D adaptatif en testant plusieurs plages."""
        try:
            # Parser l'expression
            expr = parse_latex(fonction_latex)
            x_sym, y_sym = sp.Symbol('x'), sp.Symbol('y')

            # Convertir en fonction Python évaluable
            try:
                func_lambda = sp.lambdify((x_sym, y_sym), expr, modules=['numpy', 'math'])
            except:
                return (-3, 3)

            # Tester plusieurs domaines candidats
            domaines_candidats = [
                (-5, 5),
                (-3, 3),
                (-2, 2),
                (-1, 1),
            ]

            meilleur_domaine = None
            meilleur_score = -1

            for dom_min, dom_max in domaines_candidats:
                try:
                    # Tester une grille 10x10
                    xs = np.linspace(dom_min, dom_max, 10)
                    ys_vals = np.linspace(dom_min, dom_max, 10)
                    zs = []
                    points_valides = 0

                    for x_val in xs:
                        for y_val in ys_vals:
                            try:
                                z = func_lambda(x_val, y_val)
                                if isinstance(z, (int, float)) and not math.isnan(z) and not math.isinf(z):
                                    if abs(z) < 1e10:
                                        zs.append(z)
                                        points_valides += 1
                            except:
                                pass

                    if points_valides < 50:  # Moins de 50% valides
                        continue

                    if not zs:
                        continue

                    # Calculer score
                    z_min, z_max = min(zs), max(zs)
                    plage_z = z_max - z_min

                    if plage_z > 1e6:
                        score = 0
                    elif plage_z < 0.01:
                        score = points_valides * 0.1
                    else:
                        score = min(plage_z, 1000) * (points_valides / 100)

                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_domaine = (dom_min, dom_max)

                except:
                    continue

            if meilleur_domaine:
                return meilleur_domaine
            else:
                return (-3, 3)

        except:
            return (-3, 3)

    def calculer_bornes(self, fonction, domaine_min=-8, domaine_max=8):
        """Calcule les bornes de l'axe y pour une fonction 2D."""
        xs = np.linspace(domaine_min, domaine_max, 500)
        ys = []
        for x in xs:
            y = self.evaluer_fonction(fonction, x)
            if y is not None and not math.isnan(y) and abs(y) < 1e10:
                ys.append(y)

        if not ys:
            return (-4, 4)

        y_min, y_max = min(ys), max(ys)
        plage = y_max - y_min

        if plage < 4:
            centre = (y_min + y_max) / 2
            y_min = centre - 4
            y_max = centre + 4
        else:
            marge = 0.2 * plage
            y_min -= marge
            y_max += marge

        if y_max > 12:
            y_max = 12
        if y_min < -12:
            y_min = -12

        return (y_min, y_max)

    @staticmethod
    def expr_to_tikz(expr):
        """Convertit une expression SymPy en syntaxe TikZ."""
        from sympy import Pow, Mul, Add, sqrt as sympy_sqrt

        # Exponentielle e^x
        if expr.is_Pow and str(expr.base) == 'e':
            return f"exp({TikzGraphGenerator.expr_to_tikz(expr.exp)})"

        # Racine carrée √x
        if expr.is_Pow and isinstance(expr.exp, Rational) and expr.exp == Rational(1, 2):
            return f"sqrt({TikzGraphGenerator.expr_to_tikz(expr.base)})"

        # Puissance négative: x^-n → 1/x^n
        if expr.is_Pow and expr.exp.is_Number and expr.exp < 0:
            base_str = TikzGraphGenerator.expr_to_tikz(expr.base)
            exp_str = TikzGraphGenerator.expr_to_tikz(-expr.exp)

            # Cas spéciaux sans parenthèses
            if expr.base.is_Symbol:
                # x^-1 → 1/x
                if exp_str == "1":
                    return f"1/{base_str}"
                # x^-2 → 1/(x^2)
                else:
                    return f"1/({base_str}^{exp_str})"
            # Fonction (comme sqrt) - pas de parenthèses autour
            elif 'sqrt' in base_str:
                # sqrt(x)^-1 → 1/sqrt(x)
                return f"1/{base_str}"
            # Autre expression composée
            else:
                if exp_str == "1":
                    return f"1/({base_str})"
                else:
                    return f"1/(({base_str})^{exp_str})"

        # Puissance positive
        if expr.is_Pow:
            base_str = TikzGraphGenerator.expr_to_tikz(expr.base)
            exp_str = TikzGraphGenerator.expr_to_tikz(expr.exp)

            # Simplifier: x^2 au lieu de (x)^2
            if expr.base.is_Symbol:
                return f"{base_str}^{exp_str}"
            else:
                return f"({base_str})^{exp_str}"

        # Multiplication
        if expr.is_Mul:
            facteurs = [TikzGraphGenerator.expr_to_tikz(arg) for arg in expr.args]
            return "*".join(facteurs)

        # Addition
        if expr.is_Add:
            return "+".join(TikzGraphGenerator.expr_to_tikz(a) for a in expr.args)

        # Symbole (variable)
        if expr.is_Symbol:
            return str(expr)

        # Nombre
        if expr.is_Number:
            return str(expr)

        # Fonctions trigonométriques (utilise deg() pour compatibilité TikZJax)
        if expr.func == sin:
            return f"sin(deg({TikzGraphGenerator.expr_to_tikz(expr.args[0])}))"
        if expr.func == cos:
            return f"cos(deg({TikzGraphGenerator.expr_to_tikz(expr.args[0])}))"

        # Logarithme
        if expr.func == ln or expr.func.__name__ == "log":
            return f"ln({TikzGraphGenerator.expr_to_tikz(expr.args[0])})"

        return str(expr)

    @staticmethod
    def latex_to_tikz(expr_latex):
        """Convertit une expression LaTeX en syntaxe TikZ."""
        x, y, z = symbols('x y z')
        expr = parse_latex(expr_latex)
        return TikzGraphGenerator.expr_to_tikz(expr)

    def _plot_1d_avec_bornes(self, integrand_expr, var, lower, upper):
        """Génère un graphique 1D avec des bornes spécifiques."""
        try:
            # Convertir l'intégrande (expression SymPy) en syntaxe TikZ
            from sympy import sympify
            if isinstance(integrand_expr, str):
                # Si c'est une chaîne, essayer de la parser
                integrand_expr = sympify(integrand_expr)
            f = self.expr_to_tikz(integrand_expr)
        except Exception as e:
            # Si la conversion échoue, utiliser l'expression telle quelle
            f = str(integrand_expr).replace('**', '^')

        # Limiter les bornes à un intervalle raisonnable pour l'affichage
        lower_display = max(lower, -10)
        upper_display = min(upper, 10)

        # Éviter division par zéro: si lower_display == 0 et qu'il y a une division, commencer à 0.1
        if lower_display == 0.0:
            # Vérifier s'il y a une division ou racine carrée dans l'expression
            f_str = str(integrand_expr)
            if '/' in f_str or 'sqrt' in f_str or '**-' in f_str or 'Pow' in f_str:
                lower_display = 0.1

        return f"""```tikz
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.16}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    axis lines=middle,
    grid=both,
    domain={lower_display}:{upper_display},
    samples=200,
    xlabel={{${var}$}},
    ylabel={{$f({var})$}},
    title={{Intégrande sur [{lower}, {upper}]}},
]
\\addplot[blue, thick] {{{f}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
```"""

    def _plot_1d(self, fonction_latex, variables):
        """Génère un graphique 1D."""
        f = self.latex_to_tikz(fonction_latex)

        # Calcul du domaine adaptatif
        domain_min, domain_max = self.calculer_domaine_adaptatif(fonction_latex)

        return f"""```tikz
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.16}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    axis lines=middle,
    grid=both,
    domain={domain_min}:{domain_max},
    samples=200,
    xlabel={{${variables[0]}$}},
    ylabel={{$f({variables[0]})$}},
    width=10cm,
    height=8cm
]
\\addplot[blue, thick] {{{f}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
```"""

    def _plot_2d_surface(self, fonction_latex, variables):
        """Génère une surface 3D pour 2 variables."""
        f = self.latex_to_tikz(fonction_latex)

        # Calcul du domaine 3D adaptatif
        domain_min, domain_max = self.calculer_domaine_3d_adaptatif(fonction_latex)

        # Calculer les limites Z en évaluant la fonction
        try:
            expr = parse_latex(fonction_latex)
            x_sym, y_sym = sp.Symbol('x'), sp.Symbol('y')
            func_lambda = sp.lambdify((x_sym, y_sym), expr, modules=['numpy', 'math'])

            # Évaluer sur une grille pour trouver zmin, zmax
            xs = np.linspace(domain_min, domain_max, 20)
            ys = np.linspace(domain_min, domain_max, 20)
            zs = []

            for x_val in xs:
                for y_val in ys:
                    try:
                        z = func_lambda(x_val, y_val)
                        if isinstance(z, (int, float)) and not math.isnan(z) and not math.isinf(z):
                            zs.append(z)
                    except:
                        pass

            if zs:
                z_min = min(zs)
                z_max = max(zs)
                # Ajouter une petite marge
                z_range = z_max - z_min
                if z_range > 0:
                    z_min -= 0.1 * z_range
                    z_max += 0.1 * z_range
            else:
                z_min, z_max = -10, 10
        except:
            z_min, z_max = -10, 10

        return f"""```tikz
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.16}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    view={{60}}{{30}},
    xlabel=${variables[0]}$,
    ylabel=${variables[1]}$,
    zlabel=$z$,
    colormap/cool,
    width=12cm,
    height=10cm,
    xmin={domain_min}, xmax={domain_max},
    ymin={domain_min}, ymax={domain_max},
    zmin={z_min}, zmax={z_max}
]
\\addplot3[
    surf,
    samples=13,
    domain={domain_min}:{domain_max},
    y domain={domain_min}:{domain_max}
] {{{f}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
```"""

    def _plot_3d_colored(self, fonction_latex, variables):
        """Génère une surface 3D colorée pour 3 variables."""
        f = self.latex_to_tikz(fonction_latex)

        # Calcul du domaine 3D adaptatif
        domain_min, domain_max = self.calculer_domaine_3d_adaptatif(fonction_latex)

        # Calculer les limites Z en évaluant la fonction
        try:
            expr = parse_latex(fonction_latex)
            x_sym, y_sym = sp.Symbol('x'), sp.Symbol('y')
            func_lambda = sp.lambdify((x_sym, y_sym), expr, modules=['numpy', 'math'])

            # Évaluer sur une grille pour trouver zmin, zmax
            xs = np.linspace(domain_min, domain_max, 20)
            ys = np.linspace(domain_min, domain_max, 20)
            zs = []

            for x_val in xs:
                for y_val in ys:
                    try:
                        z = func_lambda(x_val, y_val)
                        if isinstance(z, (int, float)) and not math.isnan(z) and not math.isinf(z):
                            zs.append(z)
                    except:
                        pass

            if zs:
                z_min = min(zs)
                z_max = max(zs)
                # Ajouter une petite marge
                z_range = z_max - z_min
                if z_range > 0:
                    z_min -= 0.1 * z_range
                    z_max += 0.1 * z_range
            else:
                z_min, z_max = -10, 10
        except:
            z_min, z_max = -10, 10

        return f"""```tikz
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.16}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    view={{60}}{{30}},
    xlabel=${variables[0]}$,
    ylabel=${variables[1]}$,
    zlabel=$z$,
    colormap/cool,
    width=12cm,
    height=10cm,
    xmin={domain_min}, xmax={domain_max},
    ymin={domain_min}, ymax={domain_max},
    zmin={z_min}, zmax={z_max}
]
\\addplot3[
    surf,
    samples=13,
    domain={domain_min}:{domain_max},
    y domain={domain_min}:{domain_max}
] {{{f}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
```"""

    def _plot_scatter_nd(self, fonction_latex, variables):
        """Génère un nuage de points 4D avec couleur pour la 4ème dimension."""
        # Convertir LaTeX en fonction Python
        try:
            expr = parse_latex(fonction_latex)

            # Créer les symboles pour les variables
            var_symbols = [sp.Symbol(v) for v in variables[:4]]  # Max 4 variables (x,y,z,w)

            # Créer la fonction lambda
            func_lambda = sp.lambdify(var_symbols, expr, modules=['numpy', 'math'])

            # Générer une grille de points 3D
            samples_per_axis = 5  # 5×5×5 = 125 points (performant pour TikZJax)
            domain_min, domain_max = -2, 2

            # Créer la grille
            x_vals = np.linspace(domain_min, domain_max, samples_per_axis)
            y_vals = np.linspace(domain_min, domain_max, samples_per_axis)
            z_vals = np.linspace(domain_min, domain_max, samples_per_axis)

            # Générer les points et calculer w
            points_data = []
            for x in x_vals:
                for y in y_vals:
                    for z in z_vals:
                        try:
                            # Évaluer la fonction f(x,y,z,...) = w
                            if len(variables) == 4:
                                # Pour 4 variables, on suppose que la fonction donne w
                                # On évalue avec des valeurs fixes pour les variables supplémentaires si nécessaire
                                w = func_lambda(x, y, z, 0)  # 4ème var à 0 par défaut
                            else:
                                # Pour 4+ variables, utiliser x,y,z et mettre les autres à 0
                                args = [x, y, z] + [0] * (len(variables) - 3)
                                w = func_lambda(*args)

                            if isinstance(w, (int, float)) and not math.isnan(w) and not math.isinf(w):
                                points_data.append((x, y, z, w))
                        except:
                            pass

            # Si on a des points, générer le graphique
            if points_data:
                # Formater les données pour TikZ
                table_data = "x y z w\n"
                for x, y, z, w in points_data:
                    table_data += f"{x:.3f} {y:.3f} {z:.3f} {w:.3f}\n"

                return f"""```tikz
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.16}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    view={{60}}{{30}},
    xlabel=$x$,
    ylabel=$y$,
    zlabel=$z$,
    colorbar,
    colorbar style={{ylabel=$w$ (4ème dim)}},
    colormap/viridis,
    width=12cm,
    height=10cm
]
\\addplot3[
    scatter,
    only marks,
    mark=*,
    mark size=2pt,
    point meta=explicit,
    scatter/use mapped color={{draw=mapped color, fill=mapped color}}
] table[meta=w] {{
{table_data}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
```"""
        except:
            pass

        # Fallback si échec
        return f"""```tikz
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.16}}

\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    view={{60}}{{30}},
    xlabel=$x$,
    ylabel=$y$,
    zlabel=$z$,
    colorbar,
    colorbar style={{ylabel=$w$}},
    colormap/viridis
]
\\addplot3[
    scatter,
    only marks,
    mark=*,
    mark size=2pt,
    point meta=explicit,
    scatter/use mapped color={{draw=mapped color, fill=mapped color}}
] table[meta=w] {{
x y z w
0 0 0 0
1 0 0 1
0 1 0 1
0 0 1 1
1 1 0 2
1 0 1 2
0 1 1 2
1 1 1 3
-1 0 0 1
0 -1 0 1
0 0 -1 1
}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
```"""

    def generer_fonction(self, fonction_latex):
        """Génère le graphique et/ou l'analyse selon le type d'expression."""
        # Vérifier si c'est une intégrale
        est_int, integrals = self._est_integrale(fonction_latex)

        if est_int:
            # C'est une intégrale, faire l'analyse de convergence
            print("\n🔍 INTÉGRALE DÉTECTÉE - Analyse de convergence en cours...\n")
            result = self.analyser_integrale(fonction_latex)

            # Extraire l'intégrande et les bornes pour tracer le graphique
            if result and 'integral_info' in result and result['integral_info']:
                var_info = result['integral_info'][0]  # Première variable d'intégration
                integrand_expr = result.get('integrand', '')

                # Récupérer les bornes
                var = var_info.get('integration_variable', 'x')
                lower_numeric = var_info.get('lower_value')
                upper_numeric = var_info.get('upper_value')

                # Convertir les bornes en numériques
                try:
                    from sympy import oo, N, sympify

                    # Si lower_value est None, utiliser lower_limit
                    if lower_numeric is None:
                        lower_limit = var_info.get('lower_limit', -8)
                        if str(lower_limit) in ['oo', 'inf']:
                            lower_numeric = 8
                        elif str(lower_limit) in ['-oo', '-inf']:
                            lower_numeric = -8
                        else:
                            try:
                                lower_numeric = float(N(sympify(str(lower_limit))))
                            except:
                                lower_numeric = -8
                    # Gérer l'infini pour lower si déjà une valeur
                    elif lower_numeric == float('inf') or str(lower_numeric) == 'oo':
                        lower_numeric = 8
                    elif lower_numeric == float('-inf') or str(lower_numeric) == '-oo':
                        lower_numeric = -8

                    # Si upper_value est None, utiliser upper_limit
                    if upper_numeric is None:
                        upper_limit = var_info.get('upper_limit', 8)
                        if str(upper_limit) in ['oo', 'inf']:
                            upper_numeric = 8
                        elif str(upper_limit) in ['-oo', '-inf']:
                            upper_numeric = -8
                        else:
                            try:
                                upper_numeric = float(N(sympify(str(upper_limit))))
                            except:
                                upper_numeric = 8
                    # Gérer l'infini pour upper si déjà une valeur
                    elif upper_numeric == float('inf') or str(upper_numeric) == 'oo':
                        upper_numeric = 8
                    elif upper_numeric == float('-inf') or str(upper_numeric) == '-oo':
                        upper_numeric = -8

                    # Générer le graphique de l'intégrande avec les bornes calculées
                    tikz_code = self._plot_1d_avec_bornes(integrand_expr, var, lower_numeric, upper_numeric)

                    # Retourner l'analyse ET le graphique
                    analyse_text = self.formater_analyse_convergence(result)
                    return analyse_text + "\n\n" + tikz_code
                except Exception as e:
                    # Si erreur, retourner seulement l'analyse
                    return self.formater_analyse_convergence(result)
            else:
                return self.formater_analyse_convergence(result)
        else:
            # C'est une fonction normale, générer le graphique
            variables = self._detecter_variables(fonction_latex)
            n = len(variables)

            if n == 1:
                return self._plot_1d(fonction_latex, variables)
            elif n == 2:
                return self._plot_2d_surface(fonction_latex, variables)
            else:
                # 3+ variables → Nuage de points 4D (points 3D colorés)
                return self._plot_scatter_nd(fonction_latex, variables)


if __name__ == "__main__":
    generator = TikzGraphGenerator()

    # ========================================
    # LISTE DE FONCTIONS À GÉNÉRER
    # Modifiez cette liste pour générer automatiquement vos graphiques
    # ========================================
    FONCTIONS = [
        r"x^2",
        r"\sin(x)",
        r"x^2 + y^2",
        r"2x + 3y + z^2",

    ]
    # ========================================

    print("=" * 80)
    print("GÉNÉRATEUR DE GRAPHIQUES TIKZ POUR OBSIDIAN")
    print("=" * 80)
    print()
    print("Types de graphiques supportés:")
    print(r"  • 1D: x^2, sin(x), e^x, n(x), rac{1}{x}")
    print(r"  • 2D→3D: x^2 + y^2, x^2 - y^2, sin(x) + s(y)")
    print("  • 4D: x^2 + y^2 + z^2 + t^2 (points 3D colorés)")
    print(r"  • Intégrales: int_0^1 x^2 dx, int_1^{infty} rac{1}{x^2} dx")
    print()
    print("MODES:")
    print("  [Entrée] = Utiliser la liste FONCTIONS du code")
    print("  [i]      = Mode interactif (entrer fonctions manuellement)")
    print("=" * 80)
    print()

    mode = input("Choisir mode (Entrée ou i): ").strip().lower()

    if mode == 'i':
        # Mode interactif
        print("\n📝 Mode interactif - Entrez vos fonctions (ligne vide pour terminer)\n")
        fonctions_a_generer = []
        while True:
            fonction = input(f"Fonction #{len(fonctions_a_generer) + 1}: ").strip()
            if not fonction:
                break
            fonctions_a_generer.append(fonction)
    else:
        # Mode liste
        print(f"\n📋 Mode liste - Utilisation de {len(FONCTIONS)} fonction(s) prédéfinie(s)")
        fonctions_a_generer = FONCTIONS

    if not fonctions_a_generer:
        print("\n⚠️ Aucune fonction à générer")
        exit(0)

    # Générer les graphiques
    print(f"\n{'=' * 80}")
    print(f"🚀 GÉNÉRATION DE {len(fonctions_a_generer)} GRAPHIQUE(S)")
    print("=" * 80)

    for i, fonction in enumerate(fonctions_a_generer, 1):
        print(f"\n{'=' * 80}")
        print(f"📊 GRAPHIQUE {i}/{len(fonctions_a_generer)}: {fonction}")
        print("=" * 80)

        try:
            resultat = generator.generer_fonction(fonction)

            if resultat:
                print(resultat)

                if "```tikz" in resultat:
                    print(f"\n{'─' * 80}")
                    print("✓ Graphique généré! Copiez le bloc ```tikz``` dans Obsidian")
                    print("─" * 80)
        except Exception as e:
            print(f"❌ Erreur: {e}")

    print(f"\n{'=' * 80}")
    print(f"✅ {len(fonctions_a_generer)} graphique(s) généré(s) avec succès")
    print("=" * 80)
