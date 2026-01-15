import matplotlib.pyplot as plt
import numpy as np

#fonctions mathématiques

def addition(a, b): return a + b
def soustraction(a, b): return a - b
def multiplication(a, b): return a * b
def division(a, b): return "Erreur : division par zéro" if b == 0 else a / b

def puissance(base, exposant):
    if exposant == 0: return 1
    if exposant == int(exposant):
        resultat = 1
        for i in range(abs(int(exposant))):
            resultat *= base
        return 1 / resultat if exposant < 0 else resultat
    return base ** exposant

def racine_carree(n):
    if n < 0:
        return "Erreur : racine d'un nombre négatif"
    elif n == 0:
        return 0
    else:
        return puissance(n, 0.5)

def racine_cubique(n):
    if n == 0:
        return 0
    elif n < 0:
        # La racine cubique d'un nombre négatif existe
        # ∛(-8) = -2 car (-2)×(-2)×(-2) = -8
        return -puissance(-n, 1/3)
    else:
        return puissance(n, 1/3)

def factorielle(n):
    if n < 0: return "Erreur : factorielle d'un nombre négatif"
    result = 1
    for i in range(2, n+1): result *= i
    return result

#fonctions trigonométriques 

def cosinus(x, termes=15):
    pi = np.pi
    x = ((x + pi) % (2*pi)) - pi
    res = 0
    for n in range(termes):
        res += ((-1)**n) * (x**(2*n)) / factorielle(2*n)
    return res

def sinus(x, termes=15):
    pi = np.pi
    x = ((x + pi) % (2*pi)) - pi
    res = 0
    for n in range(termes):
        res += ((-1)**n) * (x**(2*n + 1)) / factorielle(2*n + 1)
    return res

def tangente(x): 
    c = cosinus(x)
    if abs(c) < 1e-5: return "Tangente indéfinie"
    return sinus(x) / c

#solveurs d’équations

def equation_premier_degre(a, b):
    return ("Infinité de solutions" if a == 0 and b == 0
            else "Pas de solution" if a == 0
            else -b / a)

def equation_second_degre(a, b, c):
    if a == 0: return "Pas un second degré"
    delta = b*b - 4*a*c
    if delta > 0:
        d = racine_carree(delta)
        return f"x1={(-b-d)/(2*a):.4f}, x2={(-b+d)/(2*a):.4f}"
    if delta == 0:
        return f"Solution double: x={-b/(2*a):.4f}"
    return "Pas de solution réelle"

#mode graphique interactif 

def plot_function():
    plt.ion()  # active le mode interactif
    fig, ax = plt.subplots(figsize=(8, 5))

    while True:
        print("\n=== MODE GRAPHIQUE ===")
        print("1. Linéaire y=ax+b")
        print("2. Quadratique y=ax²+bx+c")
        print("3. Exponentielle y=a^x")
        print("4. Sinus/Cosinus/Tangente")
        print("0. Retour menu")
        c = input("Choix: ").strip()
        
        if c == "0":
            plt.close(fig)
            break
        
        x = np.linspace(-10, 10, 1000)
        y = None

        try:
            if c == "1":
                a = float(input("a: "))
                b = float(input("b: "))
                y = a*x + b

            elif c == "2":
                a = float(input("a: "))
                b = float(input("b: "))
                cst = float(input("c: "))
                y = a*x**2 + b*x + cst

            elif c == "3":
                base = float(input("Base > 0: "))
                if base <= 0: raise ValueError("Base doit être > 0")
                y = base**x

            elif c == "4":
                trig = input("sin/cos/tan: ").lower()
                if trig == "sin": y = np.sin(x)
                elif trig == "cos": y = np.cos(x)
                elif trig == "tan":
                    y = np.tan(x)
                    y[np.abs(y) > 20] = np.nan

            else:
                print("Choix invalide!")
                continue

            ax.clear()
            ax.plot(x, y, linewidth=2)
            ax.grid(True)
            ax.set_title("Graphique de la fonction")
            plt.draw()
            plt.pause(0.1)

        except Exception as e:
            print("Erreur:", e)

#menu principal

def main():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Mode Graphique")
        print("2. Calculatrice simple")
        print("0. Quitter")
        choix = input("Choix: ").strip()

        if choix == "0":
            print("Bye!")
            break
        elif choix == "1":
            plot_function()
        elif choix == "2":
            print("Sélectionne une opération mathématique dans ton ancien menu.")
        else:
            print("Entrée invalide!")

if __name__ == "__main__":
    main()

