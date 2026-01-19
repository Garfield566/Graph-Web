from sympy import symbols, diff, solve, lambdify, parse_expr, sin, cos, oo, tan, log, sqrt, exp, Integral, limit, pi, E, I
import numpy as np
import datetime
from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication,
    convert_xor,
    function_exponentiation,
)

def parse_latex_fallback(latex_expr):
    """Fonction de repli pour parser les expressions LaTeX."""
    try:
        from sympy.parsing.latex import parse_latex
        return parse_latex(latex_expr)
    except:
        # Remplacement des commandes LaTeX par leur équivalent SymPy
        latex_to_sympy = {
            r"\sin": "sin",
            r"\cos": "cos",
            r"\tan": "tan",
            r"\ln": "log",
            r"\log": "log",
            r"\sqrt": "sqrt",
            r"\cdot": "*",
            r"\exp": "exp",
        }

        for latex_cmd, sympy_cmd in latex_to_sympy.items():
            latex_expr = latex_expr.replace(latex_cmd, sympy_cmd)

        transformations = standard_transformations + (implicit_multiplication, convert_xor, function_exponentiation)
        return parse_expr(latex_expr, transformations=transformations)

class FonctionAnalyzer:
    def __init__(self):
        pass

    def _detecter_variables(self, fonction_latex):
        """Détecte les variables dans une fonction LaTeX."""
        try:
            x, y, z, t = symbols('x y z t')
            expr = parse_latex_fallback(fonction_latex)
            variables_brutes = expr.free_symbols
            variables_valides = {'x', 'y', 'z', 't'}
            variables = [str(var) for var in variables_brutes if str(var) in variables_valides]
            
            if not variables:
                return ['x']
            
            return sorted(variables)
        except Exception as e:
            print(f"Erreur lors de la détection des variables: {e}")
            return ['x']

    def _extract_integrals(self, expr):
        """Extrait récursivement toutes les intégrales d'une expression."""
        integrals = []
        
        if isinstance(expr, Integral):
            integrals.append(expr)
        
        # Chercher dans les arguments de l'expression
        if hasattr(expr, 'args'):
            for arg in expr.args:
                integrals.extend(self._extract_integrals(arg))
        
        return integrals

    def _compute_domain(self, expr, var):
        """Calcule le domaine de définition d'une expression."""
        from sympy import solveset, S, Union, Interval, FiniteSet

        domain = S.Reals
        restrictions = []

        try:
            # 1. Détection des logarithmes (argument > 0)
            for log_term in expr.atoms(log):
                arg = log_term.args[0]
                try:
                    positive_set = solveset(arg > 0, var, domain=S.Reals)
                    domain = domain.intersect(positive_set)
                    restrictions.append(f"log: {arg} > 0")
                except:
                    pass

            # 2. Détection des racines paires (argument >= 0)
            for pow_term in expr.atoms(sqrt):
                arg = pow_term.args[0]
                try:
                    non_negative = solveset(arg >= 0, var, domain=S.Reals)
                    domain = domain.intersect(non_negative)
                    restrictions.append(f"sqrt: {arg} >= 0")
                except:
                    pass

            # 3. Détection des divisions (dénominateur != 0)
            numer, denom = expr.as_numer_denom()
            if denom != 1:
                try:
                    zeros = solveset(denom, var, domain=S.Reals)
                    if zeros != S.EmptySet:
                        domain = domain - zeros
                        restrictions.append(f"division: {denom} ≠ 0")
                except:
                    pass

            # 4. Arcsin/Arccos: argument dans [-1, 1]
            from sympy import asin, acos
            for trig_term in list(expr.atoms(asin)) + list(expr.atoms(acos)):
                arg = trig_term.args[0]
                try:
                    bounded = solveset((arg >= -1) & (arg <= 1), var, domain=S.Reals)
                    domain = domain.intersect(bounded)
                    restrictions.append(f"arcsin/cos: -1 <= {arg} <= 1")
                except:
                    pass

        except Exception as e:
            print(f"Erreur calcul domaine: {e}")

        return {
            'domain': domain,
            'restrictions': restrictions,
            'is_all_reals': domain == S.Reals
        }

    def _detect_singularities(self, integrand, var, lower, upper):
        """Détecte toutes les singularités dans l'intervalle [lower, upper]."""
        from sympy import solveset, S

        singularities = {
            'poles': [],           # Pôles (division par zéro)
            'log_singularities': [],  # Singularités de log
            'sqrt_singularities': [], # Singularités de racines
            'discontinuities': [],    # Autres discontinuités
            'all': []
        }

        try:
            # 1. Pôles (zéros du dénominateur)
            numer, denom = integrand.as_numer_denom()
            if denom != 1:
                poles = solveset(denom, var, domain=S.Reals)
                # Vérifier si poles est un ensemble itérable (pas un ConditionSet)
                from sympy import ConditionSet
                if not isinstance(poles, ConditionSet) and hasattr(poles, '__iter__'):
                    for pole in poles:
                        if pole.is_real:
                            pole_val = float(pole.evalf())
                            # Vérifier si dans l'intervalle (ouvert ou bornes)
                            in_interval = False
                            if lower == -oo and upper == oo:
                                in_interval = True
                            elif lower == -oo:
                                in_interval = pole_val <= upper
                            elif upper == oo:
                                in_interval = pole_val >= lower
                            else:
                                in_interval = float(lower) <= pole_val <= float(upper)

                            if in_interval:
                                singularities['poles'].append(pole_val)
                                singularities['all'].append(('pole', pole_val))

            # 2. Singularités des logarithmes (argument = 0)
            for log_term in integrand.atoms(log):
                arg = log_term.args[0]
                zeros = solveset(arg, var, domain=S.Reals)
                # Vérifier si zeros est un ensemble itérable
                from sympy import ConditionSet
                if not isinstance(zeros, ConditionSet) and hasattr(zeros, '__iter__'):
                    for zero in zeros:
                        if zero.is_real:
                            zero_val = float(zero.evalf())
                            in_interval = self._in_interval(zero_val, lower, upper)
                            if in_interval:
                                singularities['log_singularities'].append(zero_val)
                                singularities['all'].append(('log', zero_val))

            # 3. Singularités des racines (argument = 0 pour racines impaires)
            for sqrt_term in integrand.atoms(sqrt):
                arg = sqrt_term.args[0]
                zeros = solveset(arg, var, domain=S.Reals)
                # Vérifier si zeros est un ensemble itérable
                from sympy import ConditionSet
                if not isinstance(zeros, ConditionSet) and hasattr(zeros, '__iter__'):
                    for zero in zeros:
                        if zero.is_real:
                            zero_val = float(zero.evalf())
                            in_interval = self._in_interval(zero_val, lower, upper)
                            if in_interval:
                                singularities['sqrt_singularities'].append(zero_val)
                                singularities['all'].append(('sqrt', zero_val))

        except Exception as e:
            print(f"Erreur détection singularités: {e}")

        return singularities

    def _in_interval(self, value, lower, upper):
        """Vérifie si une valeur est dans l'intervalle [lower, upper]."""
        try:
            if lower == -oo and upper == oo:
                return True
            elif lower == -oo:
                return value <= float(upper)
            elif upper == oo:
                return value >= float(lower)
            else:
                return float(lower) <= value <= float(upper)
        except:
            return False

    def _asymptotic_behavior(self, integrand, var, point):
        """Analyse le comportement asymptotique de l'intégrande près d'un point."""
        from sympy import series, Order

        try:
            # Développement en série autour du point
            if point == oo:
                # Substitution x = 1/t pour analyser en +∞
                t = symbols('t')
                substituted = integrand.subs(var, 1/t)
                behavior = series(substituted, t, 0, n=3)
            elif point == -oo:
                # Substitution x = -1/t pour analyser en -∞
                t = symbols('t')
                substituted = integrand.subs(var, -1/t)
                behavior = series(substituted, t, 0, n=3)
            else:
                behavior = series(integrand, var, point, n=3)

            # Extraire le terme dominant
            behavior_str = str(behavior.removeO())

            return {
                'series': behavior_str,
                'order': behavior
            }
        except:
            return None

    def _check_convergence(self, integrand, var, lower, upper):
        """Vérifie la convergence d'une intégrale avec analyse complète."""
        convergence_info = {
            'status': 'convergent',  # 'convergent', 'divergent', 'conditional', 'unknown'
            'type': 'proper',  # 'proper', 'improper_infinite', 'improper_singularity', 'improper_both'
            'issues': [],
            'warnings': [],
            'singularities': {},
            'domain_info': {}
        }

        try:
            # 1. CALCUL DU DOMAINE DE DÉFINITION
            domain_info = self._compute_domain(integrand, var)
            convergence_info['domain_info'] = domain_info

            # 2. DÉTECTION DES SINGULARITÉS
            singularities = self._detect_singularities(integrand, var, lower, upper)
            convergence_info['singularities'] = singularities

            # 3. CLASSIFICATION DE L'INTÉGRALE
            has_infinite_bounds = (lower == -oo or upper == oo)
            has_singularities = len(singularities['all']) > 0

            if has_infinite_bounds and has_singularities:
                convergence_info['type'] = 'improper_both'
            elif has_infinite_bounds:
                convergence_info['type'] = 'improper_infinite'
            elif has_singularities:
                convergence_info['type'] = 'improper_singularity'
            else:
                convergence_info['type'] = 'proper'

            # 4. VÉRIFICATION DES BORNES INFINIES avec tests de convergence
            if lower == -oo:
                behavior = self._asymptotic_behavior(integrand, var, -oo)
                lim = limit(integrand, var, -oo)

                if lim != 0:
                    # Test de comparaison pour 1/x^p
                    convergence_info['warnings'].append(
                        f"Borne -∞: l'intégrande ne tend pas vers 0 (limite = {lim})"
                    )
                    # Vérifier si décroissance assez rapide
                    try:
                        # Test si l'intégrande ~ 1/|x|^p avec p > 1
                        test_expr = integrand * var**2
                        test_lim = limit(test_expr, var, -oo)
                        if test_lim == 0:
                            convergence_info['warnings'].append(
                                "Mais décroissance assez rapide détectée (type 1/x^p, p>1)"
                            )
                        else:
                            convergence_info['status'] = 'divergent'
                            convergence_info['issues'].append(
                                "Divergence en -∞: décroissance trop lente"
                            )
                    except:
                        convergence_info['status'] = 'unknown'

            if upper == oo:
                behavior = self._asymptotic_behavior(integrand, var, oo)
                try:
                    from sympy import E
                    # Remplacer e par E (la constante de SymPy)
                    integrand_simplified = integrand.subs(symbols('e'), E)
                    lim = limit(integrand_simplified, var, oo)

                    # Essayer d'évaluer numériquement si la limite est symbolique
                    if lim.has(oo) or lim.has(-oo):
                        lim_numeric = oo
                    else:
                        try:
                            lim_numeric = lim.evalf()
                        except:
                            lim_numeric = lim
                except:
                    lim_numeric = None

                # Tester la convergence même si la limite est 0 (cas des fonctions à décroissance lente)
                if lim_numeric is not None:
                    # D'abord vérifier si la fonction croît vers l'infini
                    if lim_numeric == oo or lim_numeric.has(oo) or (hasattr(lim_numeric, 'is_infinite') and lim_numeric.is_infinite):
                        convergence_info['status'] = 'divergent'
                        convergence_info['issues'].append(
                            "Divergence en +∞: l'intégrande croît vers l'infini"
                        )
                    # Test de convergence pour fonctions décroissantes
                    else:
                        try:
                            # Cas exponentielle décroissante: e^(-x)
                            if integrand.has(exp):
                                # Test si décroissance exponentielle
                                test_expr = integrand * exp(var)
                                test_lim = limit(test_expr, var, oo)

                                # Si test_lim est fini et non infini, c'est une décroissance exponentielle
                                try:
                                    test_lim_val = test_lim.evalf()
                                    if test_lim_val.is_finite and test_lim_val != oo:
                                        # Convergent par décroissance exponentielle
                                        convergence_info['status'] = 'convergent'
                                    else:
                                        # Test algébrique
                                        test_expr2 = integrand * var**2
                                        test_lim2 = limit(test_expr2, var, oo)
                                        if test_lim2 == 0:
                                            convergence_info['status'] = 'convergent'
                                        else:
                                            convergence_info['status'] = 'divergent'
                                            convergence_info['issues'].append(
                                                "Divergence en +∞: décroissance trop lente"
                                            )
                                except:
                                    # En cas d'erreur, tester de manière algébrique
                                    test_expr2 = integrand * var**2
                                    test_lim2 = limit(test_expr2, var, oo)
                                    if test_lim2 == 0:
                                        convergence_info['status'] = 'convergent'
                            else:
                                # Test algébrique standard pour 1/x^p
                                # Pour les intégrales multiples, isoler la partie qui dépend de var
                                # Exemple: pour f(x,y) = 1/(x²y²), si var=y, extraire 1/y²
                                integrand_for_test = integrand

                                # Pour les intégrales multiples, isoler la partie qui dépend de var
                                # En substituant les autres variables d'intégration par 1
                                # (Ne pas toucher aux constantes symboliques comme pi, E, etc.)
                                try:
                                    from sympy import separatevars
                                    from sympy.core.numbers import NumberSymbol

                                    # Identifier les autres variables (pas des constantes)
                                    other_vars = integrand.free_symbols - {var}
                                    # Exclure les constantes mathématiques
                                    # Note: pi, E, I sont déjà importés au début de la méthode
                                    const_symbols = {pi, E, I, oo}
                                    other_vars = {v for v in other_vars
                                                 if v not in const_symbols
                                                 and not isinstance(v, NumberSymbol)}

                                    # Seulement pour les intégrales multiples (d'autres variables existent)
                                    if other_vars:
                                        separated = separatevars(integrand, symbols=var)
                                        # Si séparable, separated = g(autres vars) * h(var)
                                        if separated != integrand:
                                            # Substituer les autres variables par 1
                                            subs_dict = {v: 1 for v in other_vars}
                                            integrand_for_test = integrand.subs(subs_dict)
                                except:
                                    # Si la séparation échoue, utiliser l'intégrande complet
                                    pass

                                # Stratégie: tester avec x * f(x) pour déterminer l'exposant p
                                test_1x = integrand_for_test * var
                                test_1x_lim = limit(test_1x, var, oo)

                                # Évaluer numériquement pour éviter les problèmes symboliques
                                try:
                                    test_1x_val = test_1x_lim.evalf()

                                    # Si x * f(x) → ∞, alors f(x) décroît moins vite que 1/x (p < 1, diverge)
                                    if test_1x_lim.has(oo) or test_1x_lim == oo or (hasattr(test_1x_val, 'is_infinite') and test_1x_val.is_infinite):
                                        convergence_info['status'] = 'divergent'
                                        convergence_info['issues'].append(
                                            "Divergence en +∞: décroissance trop lente (p < 1)"
                                        )
                                    # Si x * f(x) → constante ≠ 0, alors f(x) ~ 1/x (p=1, diverge)
                                    elif test_1x_val.is_finite and abs(test_1x_val) > 0.001:
                                        convergence_info['status'] = 'divergent'
                                        convergence_info['issues'].append(
                                            "Divergence en +∞: 1/x (cas limite p=1)"
                                        )
                                    else:
                                        # Sinon, tester avec x^2 * f(x)
                                        # Si x^2 * f(x) → 0, alors p > 2 (convergent)
                                        # Si x^2 * f(x) → constante, alors p = 2 (convergent)
                                        # Si x^2 * f(x) → ∞, alors p < 2
                                        test_expr = integrand_for_test * var**2
                                        test_lim = limit(test_expr, var, oo)
                                        test_lim_val = test_lim.evalf() if hasattr(test_lim, 'evalf') else test_lim

                                        if test_lim == 0 or (hasattr(test_lim_val, 'is_finite') and test_lim_val.is_finite):
                                            convergence_info['status'] = 'convergent'
                                        elif test_lim.has(oo) or test_lim == oo:
                                            # x^2 * f → ∞, donc p < 2
                                            # Tester x^1.5 pour raffiner (entre p=1 et p=2)
                                            from sympy import Rational
                                            test_15 = integrand_for_test * var**Rational(3, 2)
                                            lim_15 = limit(test_15, var, oo)
                                            try:
                                                lim_15_val = lim_15.evalf()
                                                # Si x^1.5 * f → constante, alors p = 1.5 (convergent car > 1)
                                                if lim_15_val.is_finite and abs(lim_15_val) > 0.001:
                                                    convergence_info['status'] = 'convergent'
                                                # Si x^1.5 * f → ∞, alors p < 1.5, tester si < 1
                                                elif lim_15.has(oo) or lim_15 == oo:
                                                    # Déjà testé x * f = 0, donc 1 < p < 1.5 (convergent)
                                                    convergence_info['status'] = 'convergent'
                                                # Si x^1.5 * f → 0, alors p > 1.5 (convergent)
                                                else:
                                                    convergence_info['status'] = 'convergent'
                                            except:
                                                # En cas d'erreur, considérer convergent si entre 1 et 2
                                                convergence_info['status'] = 'convergent'
                                        else:
                                            convergence_info['status'] = 'divergent'
                                            convergence_info['issues'].append(
                                                "Divergence en +∞: décroissance trop lente (p < 1)"
                                            )
                                except:
                                    # En cas d'erreur, utiliser le test x^2
                                    test_expr = integrand_for_test * var**2
                                    test_lim = limit(test_expr, var, oo)
                                    if test_lim == 0:
                                        convergence_info['status'] = 'convergent'
                                    else:
                                        convergence_info['status'] = 'divergent'
                                        convergence_info['issues'].append(
                                            "Divergence en +∞: décroissance trop lente"
                                        )
                        except Exception as e:
                            convergence_info['status'] = 'unknown'
                            convergence_info['warnings'].append(
                                f"Impossible de déterminer la convergence en +∞"
                            )

            # 5. VÉRIFICATION DES SINGULARITÉS AUX BORNES avec tests de convergence
            # Ne vérifier que si les bornes sont des valeurs numériques (pas des constantes comme pi, e)
            # NOTE: Pour les bornes finies, utiliser integrand complet, pas integrand_for_test
            if lower != -oo:
                try:
                    # Évaluer numériquement la borne pour vérifier si c'est un nombre
                    lower_numeric = lower.evalf()
                    if lower_numeric.is_real and lower_numeric.is_finite:
                        val_lower = limit(integrand, var, lower, '+')
                        if val_lower.has(oo) or val_lower.has(-oo) or not val_lower.is_finite:
                            convergence_info['issues'].append(
                                f"Singularité à la borne inférieure {lower}"
                            )

                            # Test de convergence pour singularité à la borne inférieure
                            # Règle: ∫ₐᵇ (x-a)^α dx converge ssi α > -1
                            try:
                                if lower.is_number:
                                    from sympy import Rational

                                    # CAS SPÉCIAL: logarithme
                                    # log(x) seul est convergent en 0, mais 1/x * log(x) diverge
                                    if integrand.has(log):
                                        # Vérifier si c'est log(x-a) seul ou avec d'autres termes
                                        for log_term in integrand.atoms(log):
                                            arg = log_term.args[0]
                                            # Si log(x-a) où a est la borne
                                            if arg.has(var):
                                                arg_at_lower = arg.subs(var, lower)
                                                if arg_at_lower == 0 or not arg_at_lower.is_finite:
                                                    # log(x) seul converge en 0
                                                    # Mais log(x)/x ou log(x)/(x-a) diverge
                                                    # Tester si l'intégrande = log(x) * (autre chose)
                                                    test_log_only = integrand / log_term
                                                    if test_log_only.has(var):
                                                        # Il y a d'autres termes en x, potentiellement divergent
                                                        # Tester la convergence
                                                        test_conv_log = integrand * (var - lower)
                                                        lim_conv_log = limit(test_conv_log, var, lower, '+')
                                                        if lim_conv_log != 0 and lim_conv_log.is_finite:
                                                            convergence_info['status'] = 'divergent'
                                                    # Sinon, log(x-a) seul converge
                                                    break

                                    # CAS GÉNÉRAL: test de puissance
                                    # Stratégie: tester (x-a)^β * f(x) pour différents β

                                    # Test 1: (x-a)^(1/2) * f(x)
                                    test_half = integrand * (var - lower)**Rational(1, 2)
                                    lim_half = limit(test_half, var, lower, '+')

                                    # Test 2: (x-a) * f(x)
                                    test_one = integrand * (var - lower)
                                    lim_one = limit(test_one, var, lower, '+')

                                    # Déterminer α et la convergence
                                    # Si (x-a) * f → constante ≠ 0, alors α = -1 (diverge)
                                    if lim_one != 0 and lim_one.is_finite:
                                        convergence_info['status'] = 'divergent'
                                    # Si (x-a)^(1/2) * f → constante ≠ 0, alors α = -1/2 (converge car α > -1)
                                    elif lim_half != 0 and lim_half.is_finite:
                                        # α = -1/2, donc convergent
                                        pass  # Garder le statut actuel (pas de problème)
                                    # Si (x-a)^(1/2) * f → ∞, alors α < -1/2
                                    elif lim_half.has(oo) or lim_half == oo:
                                        # Tester si α < -1 ou -1 < α < -1/2
                                        if lim_one.has(oo) or lim_one == oo:
                                            # α < -1, diverge
                                            convergence_info['status'] = 'divergent'
                                        # Sinon, -1 < α < -1/2, converge
                                    # Si (x-a)^(1/2) * f → 0, alors α > -1/2, donc converge

                                behavior = self._asymptotic_behavior(integrand, var, lower)
                                if behavior:
                                    convergence_info['warnings'].append(
                                        f"Comportement près de {lower}: {behavior['series']}"
                                    )
                            except:
                                pass
                except Exception as e:
                    pass  # Ignorer les erreurs d'évaluation

            if upper != oo and upper != -oo:
                try:
                    # Évaluer numériquement la borne pour vérifier si c'est un nombre
                    upper_numeric = upper.evalf()
                    if upper_numeric.is_real and upper_numeric.is_finite:
                        val_upper = limit(integrand, var, upper, '-')
                        if val_upper.has(oo) or val_upper.has(-oo) or not val_upper.is_finite:
                            convergence_info['issues'].append(
                                f"Singularité à la borne supérieure {upper}"
                            )
                            behavior = self._asymptotic_behavior(integrand, var, upper)
                            if behavior:
                                convergence_info['warnings'].append(
                                    f"Comportement près de {upper}: {behavior['series']}"
                                )
                except Exception as e:
                    pass  # Ignorer les erreurs d'évaluation

            # 6. ANALYSE DES SINGULARITÉS INTERNES
            # IMPORTANT: Ne pas forcer divergent pour les singularités aux bornes
            # car le test de convergence (section 5) a déjà déterminé le statut
            for sing_type, sing_val in singularities['all']:
                # Vérifier si à l'intérieur strict de l'intervalle (pas sur les bornes)
                is_interior = False
                at_lower_bound = False
                at_upper_bound = False

                try:
                    lower_val = float(lower) if lower != -oo and lower != oo else None
                    upper_val = float(upper) if upper != -oo and upper != oo else None

                    # Tolérance pour considérer qu'un point est sur la borne
                    tol = 1e-10

                    if lower_val is not None:
                        at_lower_bound = abs(sing_val - lower_val) < tol
                    if upper_val is not None:
                        at_upper_bound = abs(sing_val - upper_val) < tol

                    # Intérieur strict: pas aux bornes
                    if lower_val is not None and upper_val is not None:
                        is_interior = lower_val < sing_val < upper_val and not at_lower_bound and not at_upper_bound
                    elif lower_val is not None:
                        is_interior = sing_val > lower_val and not at_lower_bound
                    elif upper_val is not None:
                        is_interior = sing_val < upper_val and not at_upper_bound
                except:
                    pass

                if is_interior:
                    # Singularité INTERNE: toujours divergent
                    convergence_info['issues'].append(
                        f"Singularité {sing_type} dans l'intervalle: {var} = {sing_val:.6f}"
                    )
                    convergence_info['status'] = 'divergent'
                elif at_lower_bound or at_upper_bound:
                    # Singularité sur une borne: le statut a été déterminé par le test de convergence
                    convergence_info['warnings'].append(
                        f"Singularité {sing_type} sur la borne: {var} = {sing_val:.6f}"
                    )

            # 7. DÉCISION FINALE
            # Ne marquer comme divergent que si on a des vraies singularités ou problèmes de convergence
            # Ignorer les fausses alertes sur les bornes symboliques
            real_issues = [issue for issue in convergence_info['issues']
                          if 'Singularité' in issue or 'Divergence' in issue]

            # Séparer les singularités internes (divergent) des singularités aux bornes (dépend du test)
            internal_singularities = [issue for issue in real_issues if 'dans l\'intervalle' in issue]
            bound_singularities = [issue for issue in real_issues if 'borne inférieure' in issue or 'borne supérieure' in issue]
            divergence_issues = [issue for issue in real_issues if 'Divergence' in issue]

            # Pour les intégrales propres sans singularités, le statut reste convergent
            if convergence_info['type'] == 'proper' and not real_issues:
                convergence_info['status'] = 'convergent'
            # Singularités INTERNES ou problèmes de divergence → toujours divergent
            elif len(internal_singularities) > 0 or len(divergence_issues) > 0:
                convergence_info['status'] = 'divergent'
            # Singularités aux BORNES seulement → le statut a déjà été déterminé par le test de convergence
            # Ne pas écraser le statut si convergent
            elif len(bound_singularities) > 0 and convergence_info['status'] == 'convergent':
                # Garder le statut convergent (le test de convergence a conclu que α > -1)
                pass

        except Exception as e:
            convergence_info['issues'].append(f"Erreur lors de la vérification: {str(e)}")
            convergence_info['status'] = 'unknown'

        return convergence_info

    def _analyze_integral(self, integral_expr):
        """Analyse une intégrale SymPy avec ses particularités."""
        try:
            # Extraire l'intégrande et les limites
            integrand = integral_expr.function
            integration_vars = integral_expr.limits
            
            integral_info = []
            
            for var, *limits in integration_vars:
                var_name = str(var)
                
                if len(limits) == 2:
                    lower, upper = limits
                    lower_str = str(lower) if lower != -oo else '-∞'
                    upper_str = str(upper) if upper != oo else '∞'
                    
                    # Vérifier la convergence
                    convergence = self._check_convergence(integrand, var, lower, upper)
                    
                    # Déterminer si les limites sont numériques
                    lower_numeric = None
                    upper_numeric = None
                    
                    try:
                        if lower != -oo and lower != oo:
                            lower_numeric = float(lower.evalf())
                    except:
                        pass
                    
                    try:
                        if upper != -oo and upper != oo:
                            upper_numeric = float(upper.evalf())
                    except:
                        pass
                    
                else:
                    lower_str, upper_str = None, None
                    lower_numeric, upper_numeric = None, None
                    convergence = {'convergent': True, 'issues': []}
                
                integral_info.append({
                    'integration_variable': var_name,
                    'lower_limit': lower_str,
                    'upper_limit': upper_str,
                    'lower_value': lower_numeric,
                    'upper_value': upper_numeric,
                    'convergence': convergence
                })
            
            return {
                'integrand': integrand,
                'integral_info': integral_info,
                'expr': integral_expr
            }
            
        except Exception as e:
            print(f"Erreur lors de l'analyse de l'intégrale: {e}")
            return None

    def analyser_fonction(self, fonction_latex):
        """Analyse une fonction mathématique ou une intégrale."""
        try:
            expr = parse_latex_fallback(fonction_latex)
            
            # Vérifier si l'expression contient des intégrales
            integrals = self._extract_integrals(expr)
            
            if integrals:
                return self._analyser_integrales(integrals, expr)
            
            # Sinon, analyser comme une fonction normale
            variables = self._detecter_variables(fonction_latex)
            n = len(variables)
            
            var_symbols = [symbols(var) for var in variables]
            f_num = lambdify(var_symbols, expr, modules=['numpy', 'math'])
            
            if n == 1:
                return self._analyser_fonction_1d(f_num, expr, variables, None)
            elif n == 2:
                return self._analyser_fonction_2d(f_num, expr, variables, None)
            elif n == 3:
                return self._analyser_fonction_3d(f_num, expr, variables, None)
            else:
                return self._analyser_fonction_nd(f_num, expr, variables, None)
                
        except Exception as e:
            print(f"Erreur lors de l'analyse : {e}")
            return None
    def flatten_integral(integral):
        integrand = integral.function
        limits = list(integral.limits)

        while isinstance(integrand, Integral):
            limits = list(integrand.limits) + limits
            integrand = integrand.function
        
        return integrand, limits

    def _validate_dependent_bounds(self, lower, upper, var, previous_vars):
        """Valide les bornes dépendantes par rapport aux variables précédentes."""
        from sympy import pi, E

        validation = {
            'valid': True,
            'issues': [],
            'dependencies': []
        }

        try:
            # Vérifier si les bornes dépendent de variables précédentes
            lower_vars = lower.free_symbols if hasattr(lower, 'free_symbols') else set()
            upper_vars = upper.free_symbols if hasattr(upper, 'free_symbols') else set()

            dependent_vars = (lower_vars | upper_vars) - {var}

            # Filtrer les constantes symboliques (pi, e, etc.)
            # Ne considérer que les vraies variables
            constants_symboliques = {pi, E, symbols('pi'), symbols('e')}
            dependent_vars = {v for v in dependent_vars if v not in constants_symboliques}

            for dep_var in dependent_vars:
                validation['dependencies'].append(str(dep_var))

                # Vérifier que la variable dépendante a été intégrée avant
                if dep_var not in previous_vars:
                    validation['valid'] = False
                    validation['issues'].append(
                        f"Variable {dep_var} utilisée dans les bornes mais pas encore intégrée"
                    )

            # Vérifier la cohérence mathématique: lower <= upper
            if lower != -oo and upper != oo:
                try:
                    # Pour des bornes numériques simples
                    if not lower.free_symbols and not upper.free_symbols:
                        lower_val = float(lower.evalf())
                        upper_val = float(upper.evalf())
                        if lower_val > upper_val:
                            validation['valid'] = False
                            validation['issues'].append(
                                f"Borne inférieure ({lower_val}) > borne supérieure ({upper_val})"
                            )
                except:
                    # Pour des bornes symboliques, on ne peut pas toujours vérifier
                    pass

        except Exception as e:
            validation['issues'].append(f"Erreur validation: {e}")

        return validation

    def _analyze_integral(self, integral_expr):
        """Analyse une intégrale SymPy avec ses particularités."""
        try:
            # --- 1. Aplatir les intégrales imbriquées ---
            def flatten_integral(integral):
                integrand = integral.function
                limits = list(integral.limits)

                while isinstance(integrand, Integral):
                    limits = list(integrand.limits) + limits
                    integrand = integrand.function

                return integrand, limits

            integrand, limits = flatten_integral(integral_expr)

            integral_info = []
            previous_vars = set()

            # --- 2. Analyse de chaque variable d'intégration ---
            # IMPORTANT: Inverser l'ordre pour correspondre à l'ordre mathématique d'intégration
            # SymPy stocke [(y, 0, x), (x, 0, 1)] pour ∫∫ dy dx
            # Mais on intègre d'abord par y (intérieur), donc x doit déjà être disponible
            # Solution: parcourir de la fin vers le début
            for var, *bounds in reversed(limits):
                var_name = str(var)

                lower = upper = None
                lower_str = upper_str = None
                lower_numeric = upper_numeric = None
                bounds_validation = None

                if len(bounds) == 2:
                    lower, upper = bounds
                    lower_str = str(lower) if lower != -oo else "-∞"
                    upper_str = str(upper) if upper != oo else "∞"

                    # Validation des bornes dépendantes
                    bounds_validation = self._validate_dependent_bounds(
                        lower, upper, var, previous_vars
                    )

                    # Numérisation si possible
                    try:
                        if lower not in (-oo, oo):
                            lower_numeric = float(lower.evalf())
                    except:
                        pass

                    try:
                        if upper not in (-oo, oo):
                            upper_numeric = float(upper.evalf())
                    except:
                        pass

                    # Vérification de convergence AMÉLIORÉE
                    convergence = self._check_convergence(
                        integrand, var, lower, upper
                    )
                else:
                    convergence = {
                        "status": "unknown",
                        "type": "indefinite",
                        "issues": [],
                        "warnings": []
                    }
                    bounds_validation = {"valid": True, "issues": [], "dependencies": []}

                integral_info.append({
                    "integration_variable": var_name,
                    "lower_limit": lower_str,
                    "upper_limit": upper_str,
                    "lower_value": lower_numeric,
                    "upper_value": upper_numeric,
                    "convergence": convergence,
                    "bounds_validation": bounds_validation
                })

                # Ajouter la variable aux variables précédentes
                previous_vars.add(var)

            # --- 3. Résumé global de l'intégrale ---
            overall_status = "convergent"
            all_issues = []
            all_warnings = []

            for info in integral_info:
                conv = info['convergence']
                if conv.get('status') == 'divergent':
                    overall_status = 'divergent'
                elif conv.get('status') == 'unknown' and overall_status != 'divergent':
                    overall_status = 'unknown'

                all_issues.extend(conv.get('issues', []))
                all_warnings.extend(conv.get('warnings', []))

                # Ajouter les problèmes de validation
                bounds_val = info.get('bounds_validation', {})
                if not bounds_val.get('valid', True):
                    all_issues.extend(bounds_val.get('issues', []))
                    overall_status = 'invalid'

            return {
                "integrand": integrand,
                "integral_info": integral_info,
                "expr": integral_expr,
                "dimension": len(limits),
                "overall_status": overall_status,
                "all_issues": all_issues,
                "all_warnings": all_warnings
            }

        except Exception as e:
            print(f"Erreur lors de l'analyse de l'intégrale: {e}")
            import traceback
            traceback.print_exc()
            return None



    def _analyser_integrand_1d(self, f_num, expr, variables, domain, integral_info):
        """Analyse l'intégrande 1D en tenant compte des limites d'intégration."""
        x = symbols(variables[0])
        var_name = variables[0]
        
        # PARTICULARITÉ: Utiliser le domaine d'intégration
        x_min, x_max = domain.get(var_name, (-8, 8))
        bounds = {"y": (-4, 4)}
        
        # Points critiques de l'intégrande sur [a, b]
        critical_points = []
        try:
            f_prime = diff(expr, x)
            critical_candidates = solve(f_prime, x)
            for cp in critical_candidates:
                if cp.is_real:
                    cp_val = float(cp.evalf())
                    # PARTICULARITÉ: Ne garder que les points dans [a, b]
                    if x_min <= cp_val <= x_max:
                        critical_points.append(cp_val)
        except:
            pass
        
        # Racines dans [a, b]
        roots = []
        try:
            root_candidates = solve(expr, x)
            for root in root_candidates:
                if root.is_real:
                    root_val = float(root.evalf())
                    if x_min <= root_val <= x_max:
                        roots.append(root_val)
        except:
            pass
        
        # Singularités dans [a, b]
        singularities = []
        convergence_issues = integral_info.get('convergence', {}).get('issues', [])
        
        try:
            denominators = expr.as_numer_denom()[1]
            sing_candidates = solve(denominators, x)
            for sing in sing_candidates:
                if sing.is_real:
                    sing_val = float(sing.evalf())
                    if x_min < sing_val < x_max:
                        singularities.append(sing_val)
        except:
            pass
        
        # Échantillonnage sur [a, b]
        xs = np.linspace(x_min, x_max, 600)
        ys = []
        for xi in xs:
            try:
                yi = f_num(xi)
                if np.isfinite(yi):
                    ys.append(yi)
            except:
                pass
        
        # Calcul des bornes y adaptatives
        if ys:
            y_min, y_max = np.min(ys), np.max(ys)
            y_span = y_max - y_min
            y_margin = max(0.5, 0.1 * y_span)
            bounds["y"] = (y_min - y_margin, y_max + y_margin)
        
        # Vérification que les bornes ne sont pas trop étroites
        if bounds["y"][1] - bounds["y"][0] < 1:
            y_center = (bounds["y"][0] + bounds["y"][1]) / 2
            bounds["y"] = (y_center - 0.5, y_center + 0.5)
        
        return {
            "variables": variables,
            "render_type": "1D",
            "domain": {var_name: (x_min, x_max)},
            "bounds": bounds,
            "samples": 200,
            "critical_points": critical_points,
            "roots": roots,
            "singularities": singularities,
            "convergence_issues": convergence_issues
        }

    def _analyser_integrand_2d(self, f_num, expr, variables, domain):
        """Analyse l'intégrande 2D sur le domaine d'intégration."""
        x, y = symbols(variables[0]), symbols(variables[1])
        bounds = {"z": (-4, 4)}
        
        # Utiliser le domaine d'intégration
        x_min, x_max = domain.get(variables[0], (-8, 8))
        y_min, y_max = domain.get(variables[1], (-8, 8))
        
        # Échantillonnage sur le domaine d'intégration
        base_xs = np.linspace(x_min, x_max, 30)
        base_ys = np.linspace(y_min, y_max, 30)
        zs = []
        
        for xi in base_xs:
            for yi in base_ys:
                try:
                    zi = f_num(xi, yi)
                    if np.isfinite(zi):
                        zs.append(zi)
                except:
                    pass
        
        # Calcul des bornes z
        if zs:
            z_min, z_max = np.min(zs), np.max(zs)
            z_span = z_max - z_min
            z_margin = max(0.5, 0.1 * z_span)
            bounds["z"] = (z_min - z_margin, z_max + z_margin)
        
        if bounds["z"][1] - bounds["z"][0] < 1:
            z_center = (bounds["z"][0] + bounds["z"][1]) / 2
            bounds["z"] = (z_center - 0.5, z_center + 0.5)
        
        return {
            "variables": variables,
            "render_type": "SURFACE",
            "domain": {variables[0]: (x_min, x_max), variables[1]: (y_min, y_max)},
            "bounds": bounds,
            "samples": 50,
            "z_range": z_span if zs else None
        }

    def _analyser_integrand_3d(self, f_num, expr, variables, domain):
        """Analyse l'intégrande 3D sur le domaine d'intégration."""
        bounds = {"w": (-4, 4)}
        
        x_min, x_max = domain.get(variables[0], (-8, 8))
        y_min, y_max = domain.get(variables[1], (-8, 8))
        z_min, z_max = domain.get(variables[2], (-8, 8))
        
        samples = 15
        xs = np.linspace(x_min, x_max, samples)
        ys = np.linspace(y_min, y_max, samples)
        zs = np.linspace(z_min, z_max, samples)
        ws = []
        
        for xi in xs:
            for yi in ys:
                for zi in zs:
                    try:
                        wi = f_num(xi, yi, zi)
                        if np.isfinite(wi):
                            ws.append(wi)
                    except:
                        pass
        
        if ws:
            ws_array = np.array(ws)
            w_min = float(np.min(ws_array))
            w_max = float(np.max(ws_array))
            w_span = w_max - w_min
            w_margin = max(0.5, 0.1 * w_span)
            bounds["w"] = (w_min - w_margin, w_max + w_margin)
        
        return {
            "variables": variables,
            "render_type": "SURFACE_COLOR",
            "domain": {
                variables[0]: (x_min, x_max),
                variables[1]: (y_min, y_max),
                variables[2]: (z_min, z_max)
            },
            "bounds": bounds,
            "samples": 15,
            "w_range": w_span if ws else None
        }

    def _evaluate_integral(self, integral_expr, var, lower, upper, samples=100):
        """Évalue numériquement une intégrale."""
        try:
            f = lambdify(var, integral_expr.function, modules=['numpy', 'math'])
            x_vals = np.linspace(float(lower), float(upper), samples)
            y_vals = [f(x) for x in x_vals]
            integral_value = np.trapz(y_vals, x_vals)

            return {
                "value": float(integral_value),
                "samples": samples,
                "x_range": (float(lower), float(upper)),
                "y_values": y_vals
            }
        except Exception as e:
            print(f"Erreur lors de l'évaluation de l'intégrale: {e}")
            return None

    def _compute_adaptive_domain_1d(self, f_num, expr, x, initial_domain=(-8, 8)):
        """Calcule un domaine adaptatif pour une fonction 1D en tenant compte de sa croissance."""
        
        # 1. Détecter le type de fonction
        is_exponential = expr.has(exp) or any(term.func.__name__ == 'Pow' and term.exp.is_number and abs(float(term.exp)) > 2 for term in expr.atoms() if hasattr(term, 'exp'))
        is_periodic = expr.has(sin, cos, tan)
        has_log = expr.has(log)
        
        # 2. Échantillonnage initial pour détecter la croissance
        test_points = np.linspace(initial_domain[0], initial_domain[1], 50)
        y_values = []
        valid_x = []
        
        for xi in test_points:
            try:
                yi = f_num(xi)
                if np.isfinite(yi) and abs(yi) < 1e10:
                    y_values.append(yi)
                    valid_x.append(xi)
            except:
                pass
        
        # 3. Analyser la croissance de la fonction
        growth_rate = 0
        if len(y_values) > 10:
            # Calculer le taux de croissance relatif
            y_array = np.array(y_values)
            y_range = np.max(y_array) - np.min(y_array)
            if y_range > 0:
                # Gradient de croissance
                gradients = np.abs(np.gradient(y_array))
                growth_rate = np.max(gradients) / (y_range + 1)
        
        # 4. Trouver tous les points d'intérêt
        interesting_points = []
        
        # Points critiques (extrema)
        try:
            f_prime = diff(expr, x)
            critical_points = solve(f_prime, x)
            for cp in critical_points:
                if cp.is_real:
                    cp_val = float(cp.evalf())
                    if abs(cp_val) < 100:
                        interesting_points.append(cp_val)
        except:
            pass
        
        # Racines
        try:
            roots = solve(expr, x)
            for root in roots:
                if root.is_real:
                    root_val = float(root.evalf())
                    if abs(root_val) < 100:
                        interesting_points.append(root_val)
        except:
            pass
        
        # Points d'inflexion
        try:
            f_double_prime = diff(expr, x, 2)
            inflection_points = solve(f_double_prime, x)
            for ip in inflection_points:
                if ip.is_real:
                    ip_val = float(ip.evalf())
                    if abs(ip_val) < 100:
                        interesting_points.append(ip_val)
        except:
            pass
        
        # Asymptotes verticales
        try:
            denominators = expr.as_numer_denom()[1]
            asymptotes = solve(denominators, x)
            for va in asymptotes:
                if va.is_real:
                    va_val = float(va.evalf())
                    if abs(va_val) < 100:
                        interesting_points.append(va_val)
        except:
            pass
        
        # 5. STRATÉGIE ADAPTATIVE selon le type de fonction
        domain = {"x": initial_domain}
        
        # CAS 1: Fonction exponentielle ou à croissance rapide
        if is_exponential or growth_rate > 10:
            # Restreindre fortement le domaine
            if interesting_points:
                x_center = np.mean(interesting_points)
            else:
                x_center = 0
            
            # Trouver un domaine où la fonction reste "visible"
            # Chercher le domaine où les valeurs sont entre 10^-3 et 10^3
            x_min, x_max = x_center - 5, x_center + 5
            
            # Affiner par échantillonnage
            test_range = np.linspace(x_min, x_max, 100)
            valid_range = []
            for xi in test_range:
                try:
                    yi = abs(f_num(xi))
                    if 1e-3 < yi < 1e3 and np.isfinite(yi):
                        valid_range.append(xi)
                except:
                    pass
            
            if valid_range:
                domain["x"] = (min(valid_range), max(valid_range))
                # Ajouter une petite marge
                span = domain["x"][1] - domain["x"][0]
                margin = 0.1 * span
                domain["x"] = (domain["x"][0] - margin, domain["x"][1] + margin)
            else:
                # Domaine très restreint par défaut pour exponentielle
                domain["x"] = (x_center - 3, x_center + 3)
        
        # CAS 2: Fonction avec logarithme
        elif has_log:
            # Le domaine doit être strictement positif (ou négatif selon le log)
            if interesting_points:
                x_min = max(0.01, min(interesting_points))
                x_max = max(interesting_points) + 2
            else:
                x_min, x_max = 0.01, 10
            
            domain["x"] = (x_min, x_max)
        
        # CAS 3: Fonction périodique
        elif is_periodic:
            period = 2 * np.pi
            
            for term in expr.atoms(sin, cos, tan):
                arg = term.args[0]
                if arg.has(x):
                    coeff = arg.coeff(x)
                    if coeff is not None and coeff != 0:
                        period = min(period, 2 * np.pi / abs(float(coeff)))
            
            # Afficher 2-3 périodes complètes
            if interesting_points:
                center = np.mean(interesting_points)
            else:
                center = 0
            
            domain["x"] = (center - 1.5 * period, center + 1.5 * period)
        
        # CAS 4: Fonction polynomiale ou "normale"
        else:
            if interesting_points:
                x_min = min(interesting_points)
                x_max = max(interesting_points)
                x_span = x_max - x_min
                
                # Adapter la marge selon la densité des points
                if x_span > 0:
                    margin = max(1, 0.3 * x_span)
                else:
                    margin = 2
                
                domain["x"] = (x_min - margin, x_max + margin)
            else:
                # Garder le domaine initial mais restreint
                domain["x"] = (-8, 8)
        
        # 6. Vérifications finales de sécurité
        # Domaine minimum
        if domain["x"][1] - domain["x"][0] < 0.5:
            center = (domain["x"][0] + domain["x"][1]) / 2
            domain["x"] = (center - 0.5, center + 0.5)
        
        # Domaine maximum (sauf pour les fonctions périodiques)
        if not is_periodic and domain["x"][1] - domain["x"][0] > 50:
            center = (domain["x"][0] + domain["x"][1]) / 2
            domain["x"] = (center - 25, center + 25)
        
        # Éviter les domaines trop décentrés pour les exponentielles
        if is_exponential:
            if domain["x"][1] - domain["x"][0] > 20:
                center = (domain["x"][0] + domain["x"][1]) / 2
                domain["x"] = (center - 10, center + 10)
        
        return domain, interesting_points

    def _analyser_fonction_1d(self, f_num, expr, variables, custom_domain=None):
        x = symbols(variables[0])
        
        # Utiliser un domaine personnalisé ou calculer un domaine adaptatif
        if custom_domain:
            domain = custom_domain
            interesting_points = []
        else:
            domain, interesting_points = self._compute_adaptive_domain_1d(f_num, expr, x)
        
        bounds = {"y": (-4, 4)}

        # Extraire les points d'intérêt (déjà calculés ou recalculer)
        critical_points = [p for p in interesting_points]
        roots = []
        inflection_points = []
        vertical_asymptotes = []
        horizontal_asymptotes = []
        
        # Calculer les caractéristiques détaillées si nécessaire
        try:
            f_prime = diff(expr, x)
            crit_pts = solve(f_prime, x)
            critical_points = [float(cp.evalf()) for cp in crit_pts if cp.is_real]
        except:
            pass

        try:
            root_pts = solve(expr, x)
            roots = [float(root.evalf()) for root in root_pts if root.is_real]
        except:
            pass

        try:
            f_double_prime = diff(expr, x, 2)
            infl_pts = solve(f_double_prime, x)
            inflection_points = [float(ip.evalf()) for ip in infl_pts if ip.is_real]
        except:
            pass

        try:
            if expr.has(x):
                denominators = expr.as_numer_denom()[1]
                asympt_pts = solve(denominators, x)
                vertical_asymptotes = [float(va.evalf()) for va in asympt_pts if va.is_real]
        except:
            pass

        try:
            limit_pos = expr.limit(x, oo)
            limit_neg = expr.limit(x, -oo)
            if limit_pos.is_finite:
                horizontal_asymptotes.append(float(limit_pos.evalf()))
            if limit_neg.is_finite:
                horizontal_asymptotes.append(float(limit_neg.evalf()))
        except:
            pass

        discontinuities = vertical_asymptotes
        is_periodic = expr.has(sin, cos)
        period = None

        xs = np.linspace(domain["x"][0], domain["x"][1], 600)
        ys = []
        for xi in xs:
            try:
                yi = f_num(xi)
                if np.isfinite(yi):
                    ys.append(yi)
            except:
                pass

        if ys:
            y_min, y_max = np.min(ys), np.max(ys)
            y_span = y_max - y_min
            y_margin = max(0.5, 0.1 * y_span)
            bounds["y"] = (y_min - y_margin, y_max + y_margin)

            if horizontal_asymptotes:
                bounds["y"] = (min(bounds["y"][0], min(horizontal_asymptotes) - 1),
                               max(bounds["y"][1], max(horizontal_asymptotes) + 1))

            if y_span > 100:
                bounds["y"] = (y_min - 0.1 * y_span, y_max + 0.1 * y_span)

        if bounds["y"][1] - bounds["y"][0] < 1:
            y_center = (bounds["y"][0] + bounds["y"][1]) / 2
            bounds["y"] = (y_center - 0.5, y_center + 0.5)

        return {
            "variables": variables,
            "render_type": "1D",
            "domain": domain,
            "bounds": bounds,
            "samples": 200,
            "asymptotes": {"vertical": vertical_asymptotes, "horizontal": horizontal_asymptotes},
            "discontinuities": discontinuities,
            "periodic": is_periodic,
            "period": period,
            "critical_points": critical_points,
            "roots": roots,
            "inflection_points": inflection_points
        }

    def _compute_adaptive_domain_2d(self, f_num, expr, variables, initial_domain=None):
        """Calcule un domaine adaptatif pour une fonction 2D en tenant compte de sa croissance."""
        x, y = symbols(variables[0]), symbols(variables[1])
        
        if initial_domain is None:
            domain = {variables[0]: (-8, 8), variables[1]: (-8, 8)}
        else:
            domain = initial_domain.copy()
        
        # 1. Détecter le type de fonction
        is_exponential = expr.has(exp)
        
        # 2. Échantillonnage pour analyser la croissance
        test_samples = 20
        x_test = np.linspace(domain[variables[0]][0], domain[variables[0]][1], test_samples)
        y_test = np.linspace(domain[variables[1]][0], domain[variables[1]][1], test_samples)
        
        z_values = []
        valid_points = []
        
        for xi in x_test:
            for yi in y_test:
                try:
                    zi = f_num(xi, yi)
                    if np.isfinite(zi) and abs(zi) < 1e8:
                        z_values.append(zi)
                        valid_points.append((xi, yi))
                except:
                    pass
        
        # 3. Trouver les points critiques
        interesting_points_x = []
        interesting_points_y = []
        
        try:
            f_grad = [diff(expr, x), diff(expr, y)]
            critical_points = solve(f_grad, (x, y), dict=True)
            
            for cp in critical_points:
                try:
                    x_val = float(cp[x].evalf())
                    y_val = float(cp[y].evalf())
                    
                    if abs(x_val) < 100 and abs(y_val) < 100:
                        interesting_points_x.append(x_val)
                        interesting_points_y.append(y_val)
                except:
                    continue
        except:
            pass
        
        # 4. STRATÉGIE ADAPTATIVE
        if is_exponential and z_values:
            # Pour les exponentielles, trouver la zone où z est "raisonnable"
            z_array = np.array(z_values)
            
            # Garder seulement les points où |z| est entre 1e-2 et 1e2
            good_indices = [i for i, z in enumerate(z_values) if 1e-2 < abs(z) < 1e2]
            
            if good_indices:
                good_points = [valid_points[i] for i in good_indices]
                xs = [p[0] for p in good_points]
                ys = [p[1] for p in good_points]
                
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)
                
                # Marge réduite pour exponentielles
                x_margin = 0.1 * max(x_max - x_min, 1)
                y_margin = 0.1 * max(y_max - y_min, 1)
                
                domain[variables[0]] = (x_min - x_margin, x_max + x_margin)
                domain[variables[1]] = (y_min - y_margin, y_max + y_margin)
            else:
                # Domaine très restreint
                domain[variables[0]] = (-3, 3)
                domain[variables[1]] = (-3, 3)
        
        # Fonction normale avec points critiques
        elif interesting_points_x and interesting_points_y:
            x_min, x_max = min(interesting_points_x), max(interesting_points_x)
            y_min, y_max = min(interesting_points_y), max(interesting_points_y)
            
            x_span = max(x_max - x_min, 2)
            y_span = max(y_max - y_min, 2)
            
            # Marge de 30%
            x_margin = 0.3 * x_span
            y_margin = 0.3 * y_span
            
            domain[variables[0]] = (x_min - x_margin, x_max + x_margin)
            domain[variables[1]] = (y_min - y_margin, y_max + y_margin)
        
        # Sinon garder le domaine initial mais restreint
        else:
            domain[variables[0]] = (-5, 5)
            domain[variables[1]] = (-5, 5)
        
        # 5. Limiter la taille du domaine
        for var in variables[:2]:
            span = domain[var][1] - domain[var][0]
            
            # Minimum
            if span < 1:
                center = (domain[var][0] + domain[var][1]) / 2
                domain[var] = (center - 0.5, center + 0.5)
            
            # Maximum
            if span > 50:
                center = (domain[var][0] + domain[var][1]) / 2
                domain[var] = (center - 25, center + 25)
            
            # Pour exponentielles, encore plus restreint
            if is_exponential and span > 20:
                center = (domain[var][0] + domain[var][1]) / 2
                domain[var] = (center - 10, center + 10)
        
        return domain

    def _analyser_fonction_2d(self, f_num, expr, variables, custom_domain=None):
        x, y = symbols(variables[0]), symbols(variables[1])
        
        # Calculer le domaine adaptatif
        if custom_domain:
            domain = custom_domain
        else:
            domain = self._compute_adaptive_domain_2d(f_num, expr, variables)
        
        bounds = {"z": (-4, 4)}

        # Recalculer les points critiques pour info détaillée
        critical_points_detail = []
        
        try:
            f_grad = [diff(expr, x), diff(expr, y)]
            critical_points = solve(f_grad, (x, y), dict=True)
        except:
            critical_points = []

        hessian_points = []
        for cp in critical_points:
            try:
                H = [[diff(expr, x, x), diff(expr, x, y)],
                     [diff(expr, y, x), diff(expr, y, y)]]
                H_val = [[h.subs(cp).evalf() for h in row] for row in H]
                det_H = H_val[0][0] * H_val[1][1] - H_val[0][1] * H_val[1][0]

                if det_H > 0:
                    hessian_points.append((float(cp[x]), float(cp[y]), "extremum"))
                elif det_H < 0:
                    hessian_points.append((float(cp[x]), float(cp[y]), "saddle"))
                else:
                    hessian_points.append((float(cp[x]), float(cp[y]), "undetermined"))
            except:
                continue

        base_xs = np.linspace(domain[variables[0]][0], domain[variables[0]][1], 30)
        base_ys = np.linspace(domain[variables[1]][0], domain[variables[1]][1], 30)
        zs = []

        for xi in base_xs:
            for yi in base_ys:
                try:
                    zi = f_num(xi, yi)
                    if np.isfinite(zi):
                        zs.append(zi)
                except:
                    pass

        if zs:
            z_min, z_max = np.min(zs), np.max(zs)
            z_span = z_max - z_min
            z_margin = max(0.5, 0.1 * z_span)
            bounds["z"] = (z_min - z_margin, z_max + z_margin)

            if z_span > 100:
                bounds["z"] = (z_min - 0.1 * z_span, z_max + 0.1 * z_span)

        if bounds["z"][1] - bounds["z"][0] < 1:
            z_center = (bounds["z"][0] + bounds["z"][1]) / 2
            bounds["z"] = (z_center - 0.5, z_center + 0.5)

        return {
            "variables": variables,
            "render_type": "SURFACE",
            "domain": domain,
            "bounds": bounds,
            "samples": 50,
            "critical_points": hessian_points,
            "z_range": z_span if zs else None
        }

    def _compute_adaptive_domain_3d(self, f_num, expr, variables, initial_domain=None):
        """Calcule un domaine adaptatif pour une fonction 3D en tenant compte de sa croissance."""
        if initial_domain is None:
            domain = {var: (-8, 8) for var in variables[:3]}
        else:
            domain = initial_domain.copy()
        
        # Détecter le type de fonction
        is_exponential = expr.has(exp)
        
        # Échantillonnage grossier pour analyser
        samples = 8 if is_exponential else 10
        ranges = [np.linspace(domain[var][0], domain[var][1], samples) for var in variables[:3]]
        
        w_values = []
        interesting_values = {var: [] for var in variables[:3]}
        
        for point in np.array(np.meshgrid(*ranges)).T.reshape(-1, 3):
            try:
                w_val = f_num(*point)
                if np.isfinite(w_val):
                    w_values.append(w_val)
                    
                    # Pour les exponentielles, garder seulement les valeurs raisonnables
                    if is_exponential:
                        if 1e-2 < abs(w_val) < 1e2:
                            for i, var in enumerate(variables[:3]):
                                interesting_values[var].append(point[i])
                    else:
                        if abs(w_val) > 0.01:  # Seuil pour filtrer le bruit
                            for i, var in enumerate(variables[:3]):
                                interesting_values[var].append(point[i])
            except:
                pass
        
        # Ajuster le domaine
        for var in variables[:3]:
            if interesting_values[var]:
                vals = interesting_values[var]
                v_min, v_max = min(vals), max(vals)
                v_span = max(v_max - v_min, 1)
                
                # Marge adaptative
                if is_exponential:
                    margin = 0.1 * v_span  # Marge réduite pour exponentielles
                else:
                    margin = 0.3 * v_span
                
                domain[var] = (v_min - margin, v_max + margin)
            else:
                # Domaine restreint si pas de valeurs intéressantes
                domain[var] = (-3, 3) if is_exponential else (-5, 5)
            
            # Limiter la taille
            span = domain[var][1] - domain[var][0]
            
            if span < 1:
                center = (domain[var][0] + domain[var][1]) / 2
                domain[var] = (center - 0.5, center + 0.5)
            
            if is_exponential and span > 15:
                center = (domain[var][0] + domain[var][1]) / 2
                domain[var] = (center - 7.5, center + 7.5)
            elif span > 50:
                center = (domain[var][0] + domain[var][1]) / 2
                domain[var] = (center - 25, center + 25)
        
        return domain

    def _analyser_fonction_3d(self, f_num, expr, variables, custom_domain=None):
        x, y, z = symbols(variables[0]), symbols(variables[1]), symbols(variables[2])
        
        # Calculer le domaine adaptatif
        if custom_domain:
            domain = custom_domain
        else:
            domain = self._compute_adaptive_domain_3d(f_num, expr, variables)
        
        bounds = {"w": (-4, 4)}
        
        samples = 15
        xs = np.linspace(domain[variables[0]][0], domain[variables[0]][1], samples)
        ys = np.linspace(domain[variables[1]][0], domain[variables[1]][1], samples)
        zs = np.linspace(domain[variables[2]][0], domain[variables[2]][1], samples)
        ws = []
        points = []
        
        for xi in xs:
            for yi in ys:
                for zi in zs:
                    try:
                        wi = f_num(xi, yi, zi)
                        if np.isfinite(wi):
                            ws.append(wi)
                            points.append((xi, yi, zi))
                    except:
                        pass
        
        if ws:
            ws_array = np.array(ws)
            w_min = float(np.min(ws_array))
            w_max = float(np.max(ws_array))
            w_span = w_max - w_min
            
            if w_span > 1e3:
                bounds["w"] = (w_min - 0.1 * abs(w_min), w_max + 0.1 * abs(w_max))
                bounds["echelle"] = "log"
            else:
                w_margin = max(0.5, 0.1 * w_span)
                bounds["w"] = (w_min - w_margin, w_max + w_margin)
                bounds["echelle"] = "lin"
            
            isosurfaces = []
            if w_span > 0:
                for level in np.linspace(w_min, w_max, 5):
                    isosurfaces.append(float(level))
            
            return {
                "variables": variables,
                "render_type": "VOLUME" if bounds.get("echelle") == "log" else "SURFACE_COLOR",
                "domain": domain,
                "bounds": bounds,
                "samples": min(20, 15 + len(ws)//100),
                "echelle": bounds.get("echelle", "lin"),
                "isosurfaces": isosurfaces,
                "w_range": w_span
            }
        else:
            return {
                "variables": variables,
                "render_type": "SURFACE_COLOR",
                "domain": domain,
                "bounds": bounds,
                "samples": 15,
                "echelle": "lin",
                "isosurfaces": [],
                "w_range": None
            }

    def _analyser_fonction_nd(self, f_num, expr, variables):
        n_dim = len(variables)
        domain = {var: (-8, 8) for var in variables}
        bounds = {"w": (-4, 4)}

        samples = max(10, min(20, 2 ** (n_dim - 1)))
        ranges = [np.linspace(domain[var][0], domain[var][1], samples) for var in variables]
        ws = []
        points = []

        for point in np.array(np.meshgrid(*ranges)).T.reshape(-1, n_dim):
            try:
                wi = f_num(*point)
                if np.isfinite(wi):
                    ws.append(wi)
                    points.append(point)
            except:
                pass

        if ws:
            ws_array = np.array(ws)
            w_min, w_max = np.min(ws_array), np.max(ws_array)
            w_span = w_max - w_min

            if w_span > 1e3:
                bounds["w"] = (np.log10(max(1e-10, abs(w_min))), np.log10(max(1e-10, abs(w_max))))
                bounds["echelle"] = "log"
            else:
                w_margin = max(0.5, 0.1 * w_span)
                bounds["w"] = (w_min - w_margin, w_max + w_margin)
                bounds["echelle"] = "lin"

        samples = min(25, 10 + len(variables) * 2)
        render_type = "SCATTER_3D" if n_dim <= 3 else "SCATTER_ND"

        return {
            "variables": variables,
            "render_type": render_type,
            "domain": domain,
            "bounds": bounds,
            "samples": samples,
            "echelle": bounds.get("echelle", "lin"),
            "dimension": n_dim
        }

# Test
from sympy import sin, cos, exp, log, sqrt, oo
from sympy.parsing.latex import parse_latex
import sys

# Forcer l'encodage UTF-8 pour la sortie
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# ===============================
# HARNAIS DE TEST GLOBAL
# ===============================

def run_integral_test(analyzer, latex_expr, description):
    print("\n" + "=" * 80)
    print(f"🧪 TEST : {description}")
    print(f"LaTeX : {latex_expr}")

    try:
        expr = parse_latex_fallback(latex_expr)
        integrals = analyzer._extract_integrals(expr)

        if not integrals:
            print("❌ Aucune intégrale détectée")
            return

        for idx, integral in enumerate(integrals, 1):
            print(f"\n🔍 Intégrale #{idx}")
            result = analyzer._analyze_integral(integral)

            if result is None:
                print("❌ Analyse échouée")
                continue

            # ---- Assertions structurelles ----
            assert isinstance(result, dict)
            assert "integrand" in result
            assert "integral_info" in result
            assert "dimension" in result
            assert "overall_status" in result
            assert isinstance(result["integral_info"], list)
            assert result["dimension"] == len(result["integral_info"])

            print(f"✅ Analyse réussie")
            print(f"   Dimension : {result['dimension']}")
            print(f"   Intégrande : {result['integrand']}")
            print(f"   Statut global : {result['overall_status']}")

            # Afficher les problèmes globaux
            if result.get('all_issues'):
                print(f"   ⚠️  PROBLÈMES ({len(result['all_issues'])}):")
                for issue in result['all_issues']:
                    print(f"      - {issue}")

            if result.get('all_warnings'):
                print(f"   ℹ️  AVERTISSEMENTS ({len(result['all_warnings'])}):")
                for warning in result['all_warnings']:
                    print(f"      - {warning}")

            # Détails par variable
            for info in result["integral_info"]:
                assert "integration_variable" in info
                assert "convergence" in info
                assert "bounds_validation" in info

                var = info['integration_variable']
                conv = info['convergence']
                bounds_val = info['bounds_validation']

                print(f"\n   📊 Variable d{var} [{info['lower_limit']}, {info['upper_limit']}]:")
                print(f"      • Type: {conv.get('type', 'N/A')}")
                print(f"      • Statut: {conv.get('status', 'N/A')}")

                # Domaine de définition
                domain_info = conv.get('domain_info', {})
                if not domain_info.get('is_all_reals', True):
                    print(f"      • Domaine: {domain_info.get('domain', 'N/A')}")
                    if domain_info.get('restrictions'):
                        print(f"      • Restrictions:")
                        for restriction in domain_info['restrictions']:
                            print(f"         - {restriction}")

                # Singularités
                singularities = conv.get('singularities', {})
                if singularities.get('all'):
                    print(f"      • Singularités détectées:")
                    for sing_type, sing_val in singularities['all']:
                        print(f"         - {sing_type}: {var} = {sing_val:.6f}")

                # Validation des bornes
                if bounds_val.get('dependencies'):
                    print(f"      • Bornes dépendantes de: {', '.join(bounds_val['dependencies'])}")
                if not bounds_val.get('valid', True):
                    print(f"      • ⚠️  Bornes invalides!")

    except AssertionError as ae:
        print(f"💥 Assertion échouée : {ae}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"💥 Crash total : {e}")
        import traceback
        traceback.print_exc()


# ===============================
# BATTERIE DE TESTS COMPLÈTE
# ===============================

TESTS = [

    # --- Intégrales simples ---
    (r"\int_0^1 x \, dx", "Polynôme degré 1 (convergent)"),
    (r"\int_0^1 x^7 \, dx", "Polynôme degré élevé (convergent)"),
    (r"\int_{-1}^1 x^3 \, dx", "Polynôme impair (convergent)"),

    # --- Fonctions classiques ---
    (r"\int_0^{\pi} \sin(x)\,dx", "Trigonométrique (convergent)"),
    (r"\int_0^{\pi/2} \cos(x)\,dx", "Trigonométrique cos (convergent)"),
    (r"\int_1^{e} \ln(x)\,dx", "Logarithme (convergent)"),
    (r"\int_0^{\infty} e^{-x}\,dx", "Exponentielle convergente (test décroissance exp)"),

    # --- Intégrales impropres DIVERGENTES ---
    (r"\int_0^{\infty} x\,dx", "Divergente simple (croissance linéaire)"),
    (r"\int_1^{\infty} \frac{1}{x}\,dx", "Divergente 1/x (cas limite p=1)"),
    (r"\int_1^{\infty} \frac{1}{x^{0.5}}\,dx", "Divergente 1/x^(1/2) (p<1)"),

    # --- Intégrales impropres CONVERGENTES ---
    (r"\int_1^{\infty} \frac{1}{x^2}\,dx", "Convergente 1/x^2 (p>1)"),
    (r"\int_1^{\infty} \frac{1}{x^3}\,dx", "Convergente 1/x^3 (p>1)"),
    (r"\int_{-\infty}^{\infty} e^{-x^2}\,dx", "Gaussienne (convergente)"),

    # --- Singularités en bornes ---
    (r"\int_0^1 \frac{1}{\sqrt{x}}\,dx", "Singularité en x=0 (borne inf)"),
    (r"\int_0^1 \frac{1}{x}\,dx", "Singularité log en x=0 (divergente)"),
    (r"\int_0^1 \ln(x)\,dx", "log(x) avec singularité en x=0 (convergente)"),

    # --- Singularités INTERNES (doivent être détectées) ---
    (r"\int_0^2 \frac{1}{x-1}\,dx", "Pôle INTERNE en x=1 (DIVERGENTE)"),
    (r"\int_{-1}^1 \frac{1}{x}\,dx", "Pôle INTERNE en x=0 (DIVERGENTE)"),
    (r"\int_0^2 \ln(x-1)\,dx", "Singularité log INTERNE en x=1 (DIVERGENTE)"),

    # --- Domaines de définition ---
    (r"\int_{-1}^1 \ln(x)\,dx", "ln(x) hors domaine (x>0) - INVALIDE"),
    (r"\int_{-2}^{-1} \frac{1}{\sqrt{x}}\,dx", "sqrt(x) hors domaine (x>=0) - INVALIDE"),

    # --- Intégrales imbriquées ---
    (r"\int_0^1 \int_0^1 x y \, dx \, dy", "Intégrale double imbriquée (convergente)"),
    (r"\int_0^1 \left( \int_0^x y\,dy \right) dx", "Bornes dépendantes VALIDES"),
    (r"\int_0^1 \left( \int_y^1 x\,dx \right) dy", "Bornes dépendantes (y intégré après)"),

    # --- Dimension élevée ---
    (
        r"\int_0^1 \int_0^1 \int_0^1 \int_0^1 x y z t \, dx\,dy\,dz\,dt",
        "Intégrale 4D (convergente)"
    ),

    # --- Fonctions pathologiques ---
    (r"\int_0^1 \sin\left(\frac{1}{x}\right)\,dx", "Oscillation forte (singularité essentielle)"),
    (r"\int_1^{\infty} \frac{\sin(x)}{x}\,dx", "Convergence conditionnelle"),
    (r"\int_0^1 \ln(\ln(\frac{1}{x}))\,dx", "Logarithme composé"),

    # --- Tests de décroissance exponentielle vs algébrique ---
    (r"\int_0^{\infty} x^2 e^{-x}\,dx", "x^2 * e^(-x) : exponentielle domine"),
    (r"\int_1^{\infty} \frac{e^{-x}}{x}\,dx", "e^(-x)/x : convergente"),
    (r"\int_1^{\infty} \frac{1}{x \ln(x)}\,dx", "1/(x*ln(x)) : divergente"),
]


# ===============================
# LANCEMENT DES TESTS
# ===============================
if __name__ == "__main__":
    analyzer = FonctionAnalyzer()
    for latex, desc in TESTS:
        run_integral_test(analyzer, latex, desc)
