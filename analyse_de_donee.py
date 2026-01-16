import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ===== VARIABLE GLOBALE POUR COMPTER LES ERREURS =====
compteur_erreurs = {"total": 0}
fenetre_erreurs = None

# ===== FONCTIONS MATHÉMATIQUES =====

def addition(a, b): 
    return a + b

def soustraction(a, b): 
    return a - b

def multiplication(a, b): 
    return a * b

def division(a, b): 
    return "Erreur : division par zéro" if b == 0 else a / b

def puissance(base, exposant):
    if exposant == 0: 
        return 1
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
        return -puissance(-n, 1/3)
    else:
        return puissance(n, 1/3)

def factorielle(n):
    if n < 0: 
        return "Erreur : factorielle d'un nombre négatif"
    result = 1
    for i in range(2, n+1): 
        result *= i
    return result

def cosinus(x, termes=15):
    pi = 3.14159265358979323846
    while x > pi:
        x -= 2 * pi
    while x < -pi:
        x += 2 * pi
    res = 0
    for n in range(termes):
        signe = puissance(-1, n)
        numerateur = puissance(x, 2*n)
        denominateur = factorielle(2*n)
        res += signe * numerateur / denominateur
    return res

def sinus(x, termes=15):
    pi = 3.14159265358979323846
    while x > pi:
        x -= 2 * pi
    while x < -pi:
        x += 2 * pi
    res = 0
    for n in range(termes):
        signe = puissance(-1, n)
        numerateur = puissance(x, 2*n + 1)
        denominateur = factorielle(2*n + 1)
        res += signe * numerateur / denominateur
    return res

def tangente(x): 
    c = cosinus(x)
    if abs(c) < 1e-5: 
        return "Tangente indéfinie"
    return sinus(x) / c

def equation_premier_degre(a, b):
    return ("Infinité de solutions" if a == 0 and b == 0
            else "Pas de solution" if a == 0
            else -b / a)

def equation_second_degre(a, b, c):
    if a == 0: 
        return "Pas un second degré"
    delta = b*b - 4*a*c
    if delta > 0:
        d = racine_carree(delta)
        return f"x1={(-b-d)/(2*a):.4f}, x2={(-b+d)/(2*a):.4f}"
    if delta == 0:
        return f"Solution double: x={-b/(2*a):.4f}"
    return "Pas de solution réelle"

# ===== FONCTION POUR INCRÉMENTER ET AFFICHER LES ERREURS =====

def incrementer_erreur():
    compteur_erreurs["total"] += 1
    if fenetre_erreurs is not None:
        mettre_a_jour_affichage_erreurs()

def mettre_a_jour_affichage_erreurs():
    global fenetre_erreurs
    if fenetre_erreurs is not None and fenetre_erreurs.winfo_exists():
        for widget in fenetre_erreurs.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and "total" in child.cget("text").lower():
                        child.config(text=f"Nombre total d'erreurs : {compteur_erreurs['total']}")

def ouvrir_fenetre_erreurs():
    global fenetre_erreurs
    
    if fenetre_erreurs is not None and fenetre_erreurs.winfo_exists():
        fenetre_erreurs.lift()
        return
    
    fenetre_erreurs = tk.Toplevel()
    fenetre_erreurs.title("📊 Statistiques d'erreurs")
    fenetre_erreurs.geometry("400x300")
    fenetre_erreurs.configure(bg="#ecf0f1")
    
    # Titre
    titre_frame = tk.Frame(fenetre_erreurs, bg="#e74c3c", height=60)
    titre_frame.pack(fill=tk.X)
    titre_frame.pack_propagate(False)
    
    titre = tk.Label(titre_frame, text="⚠️ COMPTEUR D'ERREURS", 
                    font=("Arial", 16, "bold"), fg="white", bg="#e74c3c")
    titre.pack(expand=True)
    
    # Contenu
    content_frame = tk.Frame(fenetre_erreurs, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Affichage du compteur
    compteur_frame = tk.Frame(content_frame, bg="white")
    compteur_frame.pack(expand=True)
    
    icone_label = tk.Label(compteur_frame, text="❌", font=("Arial", 48), bg="white")
    icone_label.pack(pady=10)
    
    nombre_label = tk.Label(compteur_frame, 
                           text=f"Nombre total d'erreurs : {compteur_erreurs['total']}", 
                           font=("Arial", 14, "bold"), bg="white", fg="#e74c3c")
    nombre_label.pack(pady=10)
    
    description_label = tk.Label(compteur_frame, 
                                text="Ce compteur enregistre toutes les erreurs\nrencontrées lors de l'utilisation\nde la calculatrice.", 
                                font=("Arial", 10), bg="white", fg="#7f8c8d", justify=tk.CENTER)
    description_label.pack(pady=10)
    
    # Bouton de réinitialisation
    def reinitialiser():
        compteur_erreurs["total"] = 0
        nombre_label.config(text=f"Nombre total d'erreurs : {compteur_erreurs['total']}")
    
    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(side=tk.BOTTOM, pady=10)
    
    tk.Button(btn_frame, text="🔄 Réinitialiser", font=("Arial", 10, "bold"),
             bg="#95a5a6", fg="white", command=reinitialiser, padx=20, pady=5).pack()

# ===== INTERFACE TKINTER =====

def creer_interface():
    root = tk.Tk()
    root.title("Calculatrice Mathématique avec Graphiques")
    root.geometry("900x700")
    root.configure(bg="#ecf0f1")
    
    # Titre principal
    titre_frame = tk.Frame(root, bg="#2c3e50", height=60)
    titre_frame.pack(fill=tk.X)
    titre_frame.pack_propagate(False)
    
    titre_left = tk.Frame(titre_frame, bg="#2c3e50")
    titre_left.pack(side=tk.LEFT, expand=True)
    
    titre = tk.Label(titre_left, text="📊 CALCULATRICE & GRAPHIQUES", 
                    font=("Arial", 18, "bold"), fg="white", bg="#2c3e50")
    titre.pack(expand=True)
    
    # Bouton pour ouvrir les statistiques d'erreurs
    btn_erreurs = tk.Button(titre_frame, text="📊 Voir les erreurs", 
                           font=("Arial", 10, "bold"), bg="#e74c3c", fg="white",
                           command=ouvrir_fenetre_erreurs, padx=15, pady=5)
    btn_erreurs.pack(side=tk.RIGHT, padx=10)
    
    # Notebook (onglets)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Onglet 1 : Calculatrice
    tab_calc = tk.Frame(notebook, bg="white")
    notebook.add(tab_calc, text="  Calculatrice  ")
    creer_onglet_calculatrice(tab_calc)
    
    # Onglet 2 : Graphiques
    tab_graph = tk.Frame(notebook, bg="white")
    notebook.add(tab_graph, text="  Graphiques  ")
    creer_onglet_graphiques(tab_graph)
    
    root.mainloop()

# ===== ONGLET CALCULATRICE =====

def creer_onglet_calculatrice(parent):
    # Scroll canvas
    canvas = tk.Canvas(parent, bg="white")
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Opérations de base
    frame_ops = tk.LabelFrame(scrollable_frame, text="Opérations de base", 
                              font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
    frame_ops.pack(fill=tk.X, padx=20, pady=10)
    
    creer_operation_2_inputs(frame_ops, "Addition (+)", addition)
    creer_operation_2_inputs(frame_ops, "Soustraction (−)", soustraction)
    creer_operation_2_inputs(frame_ops, "Multiplication (×)", multiplication)
    creer_operation_2_inputs(frame_ops, "Division (÷)", division)
    creer_operation_2_inputs(frame_ops, "Puissance (^)", puissance)
    
    # Racines
    frame_racines = tk.LabelFrame(scrollable_frame, text="Racines & Factorielle", 
                                  font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
    frame_racines.pack(fill=tk.X, padx=20, pady=10)
    
    creer_operation_1_input(frame_racines, "Racine carrée (√)", racine_carree)
    creer_operation_1_input(frame_racines, "Racine cubique (∛)", racine_cubique)
    creer_operation_1_input(frame_racines, "Factorielle (n!)", factorielle)
    
    # Trigonométrie
    frame_trig = tk.LabelFrame(scrollable_frame, text="Trigonométrie (radians)", 
                               font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
    frame_trig.pack(fill=tk.X, padx=20, pady=10)
    
    creer_operation_1_input(frame_trig, "Cosinus", cosinus)
    creer_operation_1_input(frame_trig, "Sinus", sinus)
    creer_operation_1_input(frame_trig, "Tangente", tangente)
    
    # Équations
    frame_eq = tk.LabelFrame(scrollable_frame, text="Résolution d'équations", 
                            font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
    frame_eq.pack(fill=tk.X, padx=20, pady=10)
    
    creer_equation_1er_degre(frame_eq)
    creer_equation_2nd_degre(frame_eq)

def creer_operation_2_inputs(parent, nom, fonction):
    frame = tk.Frame(parent, bg="white")
    frame.pack(fill=tk.X, pady=5)
    
    tk.Label(frame, text=nom, font=("Arial", 10), bg="white", width=20, anchor="w").pack(side=tk.LEFT, padx=5)
    
    entry_a = tk.Entry(frame, font=("Arial", 10), width=10)
    entry_a.pack(side=tk.LEFT, padx=5)
    
    entry_b = tk.Entry(frame, font=("Arial", 10), width=10)
    entry_b.pack(side=tk.LEFT, padx=5)
    
    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"), bg="white", fg="#27ae60", width=20)
    result_label.pack(side=tk.LEFT, padx=5)
    
    def calculer():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            res = fonction(a, b)
            if isinstance(res, str):
                result_label.config(text=res, fg="#e74c3c")
                incrementer_erreur()
            else:
                result_label.config(text=f"= {res:.6f}", fg="#27ae60")
        except:
            result_label.config(text="Erreur", fg="#e74c3c")
            incrementer_erreur()
    
    tk.Button(frame, text="=", font=("Arial", 10, "bold"), bg="#3498db", fg="white", 
             width=3, command=calculer).pack(side=tk.LEFT, padx=5)

def creer_operation_1_input(parent, nom, fonction):
    frame = tk.Frame(parent, bg="white")
    frame.pack(fill=tk.X, pady=5)
    
    tk.Label(frame, text=nom, font=("Arial", 10), bg="white", width=20, anchor="w").pack(side=tk.LEFT, padx=5)
    
    entry = tk.Entry(frame, font=("Arial", 10), width=10)
    entry.pack(side=tk.LEFT, padx=5)
    
    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"), bg="white", fg="#27ae60", width=20)
    result_label.pack(side=tk.LEFT, padx=5)
    
    def calculer():
        try:
            val = float(entry.get())
            res = fonction(val)
            if isinstance(res, str):
                result_label.config(text=res, fg="#e74c3c")
                incrementer_erreur()
            else:
                result_label.config(text=f"= {res:.6f}", fg="#27ae60")
        except:
            result_label.config(text="Erreur", fg="#e74c3c")
            incrementer_erreur()
    
    tk.Button(frame, text="=", font=("Arial", 10, "bold"), bg="#3498db", fg="white", 
             width=3, command=calculer).pack(side=tk.LEFT, padx=5)

def creer_equation_1er_degre(parent):
    frame = tk.LabelFrame(parent, text="ax + b = 0", font=("Arial", 10, "bold"), 
                         bg="white", padx=10, pady=5)
    frame.pack(fill=tk.X, pady=5)
    
    input_frame = tk.Frame(frame, bg="white")
    input_frame.pack()
    
    tk.Label(input_frame, text="a =", bg="white").grid(row=0, column=0, padx=5)
    entry_a = tk.Entry(input_frame, width=10)
    entry_a.grid(row=0, column=1, padx=5)
    
    tk.Label(input_frame, text="b =", bg="white").grid(row=0, column=2, padx=5)
    entry_b = tk.Entry(input_frame, width=10)
    entry_b.grid(row=0, column=3, padx=5)
    
    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"), bg="white", fg="#27ae60")
    result_label.pack(pady=5)
    
    def resoudre():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            res = equation_premier_degre(a, b)
            if isinstance(res, str):
                result_label.config(text=res, fg="#e74c3c")
                incrementer_erreur()
            else:
                result_label.config(text=f"x = {res:.6f}", fg="#27ae60")
        except:
            result_label.config(text="Erreur", fg="#e74c3c")
            incrementer_erreur()
    
    tk.Button(frame, text="Résoudre", bg="#27ae60", fg="white", command=resoudre).pack()

def creer_equation_2nd_degre(parent):
    frame = tk.LabelFrame(parent, text="ax² + bx + c = 0", font=("Arial", 10, "bold"), 
                         bg="white", padx=10, pady=5)
    frame.pack(fill=tk.X, pady=5)
    
    input_frame = tk.Frame(frame, bg="white")
    input_frame.pack()
    
    tk.Label(input_frame, text="a =", bg="white").grid(row=0, column=0, padx=5)
    entry_a = tk.Entry(input_frame, width=8)
    entry_a.grid(row=0, column=1, padx=5)
    
    tk.Label(input_frame, text="b =", bg="white").grid(row=0, column=2, padx=5)
    entry_b = tk.Entry(input_frame, width=8)
    entry_b.grid(row=0, column=3, padx=5)
    
    tk.Label(input_frame, text="c =", bg="white").grid(row=0, column=4, padx=5)
    entry_c = tk.Entry(input_frame, width=8)
    entry_c.grid(row=0, column=5, padx=5)
    
    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"), bg="white", fg="#27ae60")
    result_label.pack(pady=5)
    
    def resoudre():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            c = float(entry_c.get())
            res = equation_second_degre(a, b, c)
            if "Erreur" in res or "Pas" in res:
                result_label.config(text=res, fg="#e74c3c")
                incrementer_erreur()
            else:
                result_label.config(text=res, fg="#27ae60")
        except:
            result_label.config(text="Erreur", fg="#e74c3c")
            incrementer_erreur()
    
    tk.Button(frame, text="Résoudre", bg="#27ae60", fg="white", command=resoudre).pack()

# ===== ONGLET GRAPHIQUES =====

def creer_onglet_graphiques(parent):
    # Frame gauche (contrôles)
    left_frame = tk.Frame(parent, bg="white", width=300)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    left_frame.pack_propagate(False)
    
    tk.Label(left_frame, text="Type de fonction", font=("Arial", 12, "bold"), 
            bg="white").pack(pady=10)
    
    type_var = tk.StringVar(value="lineaire")
    
    tk.Radiobutton(left_frame, text="Linéaire (y = ax + b)", variable=type_var, 
                  value="lineaire", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(left_frame, text="Quadratique (y = ax² + bx + c)", variable=type_var, 
                  value="quadratique", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(left_frame, text="Exponentielle (y = a^x)", variable=type_var, 
                  value="exponentielle", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(left_frame, text="Sinus", variable=type_var, 
                  value="sinus", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(left_frame, text="Cosinus", variable=type_var, 
                  value="cosinus", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(left_frame, text="Tangente", variable=type_var, 
                  value="tangente", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20)
    
    # Paramètres
    tk.Label(left_frame, text="Paramètres", font=("Arial", 12, "bold"), 
            bg="white").pack(pady=10)
    
    param_frame = tk.Frame(left_frame, bg="white")
    param_frame.pack(fill=tk.X, padx=20)
    
    tk.Label(param_frame, text="a =", bg="white").grid(row=0, column=0, pady=5)
    entry_a = tk.Entry(param_frame, width=10)
    entry_a.grid(row=0, column=1, pady=5, padx=5)
    entry_a.insert(0, "1")
    
    tk.Label(param_frame, text="b =", bg="white").grid(row=1, column=0, pady=5)
    entry_b = tk.Entry(param_frame, width=10)
    entry_b.grid(row=1, column=1, pady=5, padx=5)
    entry_b.insert(0, "0")
    
    tk.Label(param_frame, text="c =", bg="white").grid(row=2, column=0, pady=5)
    entry_c = tk.Entry(param_frame, width=10)
    entry_c.grid(row=2, column=1, pady=5, padx=5)
    entry_c.insert(0, "0")
    
    # Frame droite (graphique)
    right_frame = tk.Frame(parent, bg="white")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Créer figure matplotlib
    fig, ax = plt.subplots(figsize=(6, 5))
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def tracer():
        try:
            ax.clear()
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.8)
            ax.axvline(x=0, color='k', linewidth=0.8)
            
            # Générer x
            x_values = []
            for i in range(1000):
                x_values.append(-10 + i * 20 / 999)
            
            type_func = type_var.get()
            
            if type_func == "lineaire":
                a = float(entry_a.get())
                b = float(entry_b.get())
                y_values = [a * x + b for x in x_values]
                ax.plot(x_values, y_values, 'b-', linewidth=2, label=f"y = {a}x + {b}")
            
            elif type_func == "quadratique":
                a = float(entry_a.get())
                b = float(entry_b.get())
                c = float(entry_c.get())
                y_values = [a * x * x + b * x + c for x in x_values]
                ax.plot(x_values, y_values, 'r-', linewidth=2, label=f"y = {a}x² + {b}x + {c}")
            
            elif type_func == "exponentielle":
                a = float(entry_a.get())
                if a <= 0:
                    raise ValueError("Base doit être > 0")
                y_values = [puissance(a, x) if abs(puissance(a, x)) < 1000 else None for x in x_values]
                ax.plot(x_values, y_values, 'g-', linewidth=2, label=f"y = {a}^x")
            
            elif type_func == "sinus":
                y_values = [sinus(x) for x in x_values]
                ax.plot(x_values, y_values, 'm-', linewidth=2, label="y = sin(x)")
            
            elif type_func == "cosinus":
                y_values = [cosinus(x) for x in x_values]
                ax.plot(x_values, y_values, 'c-', linewidth=2, label="y = cos(x)")
            
            elif type_func == "tangente":
                y_values = []
                for x in x_values:
                    t = tangente(x)
                    if isinstance(t, str) or abs(t) > 10:
                        y_values.append(None)
                    else:
                        y_values.append(t)
                ax.plot(x_values, y_values, 'orange', linewidth=2, label="y = tan(x)")
            
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.legend()
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            canvas.draw()
            
        except Exception as e:
            print(f"Erreur: {e}")
            incrementer_erreur()
    
    tk.Button(left_frame, text="Tracer le graphique", font=("Arial", 12, "bold"),
             bg="#3498db", fg="white", command=tracer).pack(pady=20)

# ===== LANCEMENT =====

if __name__ == "__main__":
    creer_interface()
    