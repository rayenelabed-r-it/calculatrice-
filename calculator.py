def addition(a, b):
    return a + b


def soustraction(a, b):
    return a - b


def multiplication(a, b):
    return a * b


def division(a, b):
    if b == 0:
        return "Erreur : division par zéro"
    return a / b


def puissance(base, exposant):
    if exposant == 0:
        return 1
    
    resultat = 1
    exp_positif = abs(exposant)
    
    for i in range(exp_positif):
        resultat *= base
    
    if exposant < 0:
        return 1 / resultat
    return resultat


def racine_carree(n):
    """Calcule la racine carrée en utilisant la puissance 1/2.
    √n = n^(1/2)"""
    if n < 0:
        return "Erreur : racine d'un nombre négatif"
    if n == 0:
        return 0
    
    return puissance(n, 0.5)
#La racine cubique (racine triple) de 7 est : 7 a la puisance 1/3 


def factorielle(n): 
    #3!=3×2×1=6
    if n == 0 or n == 1:
        return 1
    resultat = 1
    for i in range(2, n + 1):
        resultat *= i
    return resultat


def cosinus(x, termes=15):
    """Calcule cos(x) par développement en série de Taylor.
    cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ..."""
    
    # Normaliser x dans [-π, π]
    pi = 3.14159265358979323846
    while x > pi:
        x -= 2 * pi
    while x < -pi:
        x += 2 * pi
    
    resultat = 0
    for n in range(termes):
        signe = puissance(-1, n)
        numerateur = puissance(x, 2 * n)
        denominateur = factorielle(2 * n)
        resultat += signe * numerateur / denominateur
    
    return resultat


def sinus(x, termes=15):
    """Calcule sin(x) par développement en série de Taylor.
    sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ..."""
    
    # Normaliser x dans [-π, π]
    pi = 3.14159265358979323846
    while x > pi:
        x -= 2 * pi
    while x < -pi:
        x += 2 * pi
    
    resultat = 0
    for n in range(termes):
        signe = puissance(-1, n)
        numerateur = puissance(x, 2 * n + 1)
        denominateur = factorielle(2 * n + 1)
        resultat += signe * numerateur / denominateur
    
    return resultat

def tangente(x, termes=15):
    """Calcule tan(x) en utilisant tan(x) = sin(x) / cos(x)."""
    cos_x = cosinus(x, termes)
    
    # Vérifier que cos(x) n'est pas zéro (division par zéro)
    if abs(cos_x) < 0.00001:
        return "Erreur : tangente indéfinie (cos = 0)"
    
    sin_x = sinus(x, termes)
    return sin_x / cos_x






# Menu de la calculatrice
def calculatrice():
    """Menu principal de la calculatrice."""
    print("=== CALCULATRICE ===")
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Puissance")
    print("6. Racine carrée")
    print("7. Cosinus")
    print("8. Sinus")
    print("0. Quitter")
    print("===================")
    
    while True:
        choix = input("\nChoisissez une opération (0-8) : ")
        
        if choix == "0":
            print("Au revoir !")
            break
        
        elif choix in ["1", "2", "3", "4", "5"]:
            a = float(input("Premier nombre : "))
            b = float(input("Deuxième nombre : "))
            
            if choix == "1":
                print(f"Résultat : {addition(a, b)}")
            elif choix == "2":
                print(f"Résultat : {soustraction(a, b)}")
            elif choix == "3":
                print(f"Résultat : {multiplication(a, b)}")
            elif choix == "4":
                print(f"Résultat : {division(a, b)}")
            elif choix == "5":
                print(f"Résultat : {puissance(a, int(b))}")
        
        elif choix == "6":
            n = float(input("Nombre : "))
            print(f"Résultat : {racine_carree(n)}")
        
        elif choix == "7":
            x = float(input("Angle en radians : "))
            print(f"Résultat : {cosinus(x)}")
        
        elif choix == "8":
            x = float(input("Angle en radians : "))
            print(f"Résultat : {sinus(x)}")
        
        else:
            print("Choix invalide !")


# Tests des fonctions
if __name__ == "__main__":
    print("Tests des fonctions :")
    print(f"5 + 3 = {addition(5, 3)}")
    print(f"10 - 4 = {soustraction(10, 4)}")
    print(f"6 × 7 = {multiplication(6, 7)}")
    print(f"20 ÷ 4 = {division(20, 4)}")
    print(f"2^10 = {puissance(2, 10)}")
    print(f"√16 = {racine_carree(16)}")
    print(f"cos(0) = {cosinus(0)}")
    print(f"sin(π/2) ≈ {sinus(3.14159/2)}")
    
    # Lancer la calculatrice interactive
    print("\n")
    calculatrice()