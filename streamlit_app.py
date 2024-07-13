# Importer la bibliothèque termcolor pour la coloration du texte
from termcolor import colored

# Fonction pour obtenir les entrées de l'utilisateur avec vérification
def obtenir_entree_utilisateur(message, type_donnee=float):
    while True:
        try:
            return type_donnee(input(message))
        except ValueError:
            print(colored("Entrée invalide. Veuillez entrer un nombre.", 'red'))

# Fonction pour afficher les résultats dans un cadre
def afficher_resultat_cadre(titre, valeur, formule):
    print(colored("="*50, 'cyan'))
    print(colored(titre, 'cyan'))
    print(f"{valeur}")
    print(colored(f"Formule : {formule}", 'grey'))
    print(colored("="*50, 'cyan'))

# Demander le nom du produit
produits = ["diamicron", "natrixam", "fludex LP"]
print("Choisissez un produit parmi les suivants :")
for i, produit in enumerate(produits, 1):
    print(f"{i}. {produit}")
    
while True:
    choix_produit = input("Entrez le numéro du produit choisi : ")
    if choix_produit.isdigit() and 1 <= int(choix_produit) <= len(produits):
        nom_produit = produits[int(choix_produit) - 1]
        break
    else:
        print(colored("Entrée invalide. Veuillez entrer un numéro valide.", 'red'))

# Demander les ventes totales par mois avant l'implémentation du projet
ventes_initiales_par_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0) : ", int)

# Demander la période de mesure
periode_mesure = obtenir_entree_utilisateur("Entrez la période de mesure (en mois) : ", int)

# Demander les ventes mensuelles pour chaque mois de la période de mesure
ventes_mensuelles = []
for mois in range(1, periode_mesure + 1):
    ventes_mensuelles.append(obtenir_entree_utilisateur(f"Entrez les ventes totales pour le mois {mois} (en boîtes) : ", int))

# Calculer les boîtes supplémentaires (uplift)
boites_supplementaires = sum(ventes_mensuelles) - (ventes_initiales_par_mois * periode_mesure)
afficher_resultat_cadre(
    "Boîtes supplémentaires vendues =",
    boites_supplementaires,
    "Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)"
)

# Demander le prix hors taxe par boîte
prix_ht_par_boite = obtenir_entree_utilisateur(f"Entrez le prix hors taxe par boîte de {nom_produit} (en DT) : ")

# Demander le coût de production par boîte
cout_production_par_boite = obtenir_entree_utilisateur(f"Entrez le coût de production par boîte de {nom_produit} (en DT) : ")

# Calcul du coût des marchandises vendues (COGS)
cout_total_supplementaire = cout_production_par_boite * boites_supplementaires
afficher_resultat_cadre(
    "Coût des marchandises vendues (COGS) =",
    f"{cout_total_supplementaire:.2f} DT",
    "COGS = Coût de production par boîte * Boîtes supplémentaires vendues"
)

# Demander le coût de l'investissement
cout_investissement = obtenir_entree_utilisateur("Entrez le coût de l'investissement pour la période concernée (en DT) : ")

# Calcul des revenus supplémentaires
revenus_supplementaires = prix_ht_par_boite * boites_supplementaires
afficher_resultat_cadre(
    "Revenus supplémentaires =",
    f"{revenus_supplementaires:.2f} DT",
    "Revenus supplémentaires = Prix hors taxe par boîte * Boîtes supplémentaires vendues"
)

# Calcul de la marge brute
marge_brute = ((revenus_supplementaires - cout_total_supplementaire) / revenus_supplementaires) * 100
afficher_resultat_cadre(
    "Marge Brute =",
    f"{marge_brute:.2f}%",
    "Marge Brute = ((Revenus supplémentaires - Coût des marchandises vendues) / Revenus supplémentaires) * 100"
)

# Calcul des revenus totaux
revenus_total = sum(ventes_mensuelles) * prix_ht_par_boite
afficher_resultat_cadre(
    "Revenus totaux =",
    f"{revenus_total:.2f} DT",
    "Revenus totaux = (Somme des ventes mensuelles) * Prix hors taxe par boîte"
)

# Calcul des coûts totaux
cout_total = (ventes_initiales_par_mois * periode_mesure * cout_production_par_boite) + cout_total_supplementaire + cout_investissement
afficher_resultat_cadre(
    "Coût total =",
    f"{cout_total:.2f} DT",
    "Coût total = (Ventes initiales par mois * Période de mesure * Coût de production par boîte) + Coût des marchandises vendues + Coût de l'investissement"
)

# Calcul du retour sur investissement (ROI)
roi_complet = ((revenus_total - cout_total) / cout_investissement) * 100
afficher_resultat_cadre(
    "Retour sur investissement (ROI) =",
    f"{roi_complet:.2f}%",
    "ROI = ((Revenus total - Coût total) / Coût de l'investissement) * 100"
)

# Calcul du seuil de rentabilité (BEP)
bep = cout_investissement / (prix_ht_par_boite - cout_production_par_boite)
afficher_resultat_cadre(
    "Seuil de rentabilité (BEP) =",
    f"{bep:.2f} boîtes",
    "BEP = Coût de l'investissement / (Prix hors taxe par boîte - Coût de production par boîte)"
)

# Calcul de la période exacte qui coïncide avec le BEP
ventes_cumulees = 0
mois_bep = 0
for mois, ventes in enumerate(ventes_mensuelles, start=1):
    ventes_cumulees += ventes
    revenu_cumule = ventes_cumulees * prix_ht_par_boite
    if revenu_cumule >= cout_investissement:
        mois_bep = mois
        break

# Afficher les résultats de la période BEP
if mois_bep > 0:
    afficher_resultat_cadre(
        "Le seuil de rentabilité est atteint au mois :",
        mois_bep,
        "Le seuil de rentabilité est atteint quand les ventes cumulées couvrent le coût de l'investissement"
    )
else:
    print(colored("Le seuil de rentabilité n'est pas atteint dans la période donnée.", 'red'))
