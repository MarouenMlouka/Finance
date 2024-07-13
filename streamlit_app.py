import streamlit as st

def obtenir_entree_utilisateur(message, type_conversion, default_value=None):
    user_input = st.text_input(message, default_value)
    if user_input is not None and user_input.strip():  # Vérifie si l'entrée utilisateur n'est pas vide
        try:
            return type_conversion(user_input)
        except ValueError:
            st.error(f"Erreur : Veuillez entrer une valeur numérique valide pour '{message}'")
            st.stop()
    else:
        st.error(f"Erreur : Veuillez entrer une valeur pour '{message}'")
        st.stop()

def afficher_resultat_cadre(titre, resultat, explication):
    st.subheader(titre)
    st.write(resultat)
    st.text(explication)

def calculer_boites_supplementaires(ventes_mensuelles, ventes_initiales_par_mois, periode_mesure):
    return sum(ventes_mensuelles) - (ventes_initiales_par_mois * periode_mesure)

def calculer_cout_total_supplementaire(cout_production_par_boite, boites_supplementaires):
    return cout_production_par_boite * boites_supplementaires

def calculer_revenus_supplementaires(prix_ht_par_boite, boites_supplementaires):
    return prix_ht_par_boite * boites_supplementaires

def main():
    st.title("Calculateur d'analyse financière")

    produits = {
        "diamicron": "Diamicron",
        "natrixam": "Natrixam",
        "fludex LP": "Fludex LP"
    }

    choix_produit = st.selectbox("Choisissez un produit", list(produits.values()))
    nom_produit = next(key for key, value in produits.items() if value == choix_produit)

    ventes_initiales_par_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0) :", float)
    periode_mesure = st.number_input("Entrez la période de mesure (en mois) :", min_value=1, step=1)

    ventes_mensuelles = []
    for mois in range(1, periode_mesure + 1):
        ventes_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales pour le mois {mois} (en boîtes) :", int)
        ventes_mensuelles.append(ventes_mois)

    boites_supplementaires = calculer_boites_supplementaires(ventes_mensuelles, ventes_initiales_par_mois, periode_mesure)
    afficher_resultat_cadre(
        "Boîtes supplémentaires vendues =",
        boites_supplementaires,
        "Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)"
    )

    prix_ht_par_boite = obtenir_entree_utilisateur(f"Entrez le prix hors taxe par boîte de {nom_produit} (en DT) : ", float)
    cout_production_par_boite = obtenir_entree_utilisateur(f"Entrez le coût de production par boîte de {nom_produit} (en DT) : ", float)

    cout_total_supplementaire = calculer_cout_total_supplementaire(cout_production_par_boite, boites_supplementaires)
    afficher_resultat_cadre(
        "Coût des marchandises vendues (COGS) =",
        f"{cout_total_supplementaire:.2f} DT",
        "COGS = Coût de production par boîte * Boîtes supplémentaires vendues"
    )

    cout_investissement = obtenir_entree_utilisateur("Entrez le coût de l'investissement pour la période concernée (en DT) : ", float)

    revenus_supplementaires = calculer_revenus_supplementaires(prix_ht_par_boite, boites_supplementaires)
    afficher_resultat_cadre(
        "Revenus supplémentaires =",
        f"{revenus_supplementaires:.2f} DT",
        "Revenus supplémentaires = Prix hors taxe par boîte * Boîtes supplémentaires vendues"
    )

    marge_brute = ((revenus_supplementaires - cout_total_supplementaire) / revenus_supplementaires) * 100
    afficher_resultat_cadre(
        "Marge Brute =",
        f"{marge_brute:.2f}%",
        "Marge Brute = ((Revenus supplémentaires - Coût des marchandises vendues) / Revenus supplémentaires) * 100"
    )

    revenus_total = sum(ventes_mensuelles) * prix_ht_par_boite
    afficher_resultat_cadre(
        "Revenus totaux =",
        f"{revenus_total:.2f} DT",
        "Revenus totaux = (Somme des ventes mensuelles) * Prix hors taxe par boîte"
    )

    cout_total = (ventes_initiales_par_mois * periode_mesure * cout_production_par_boite) + cout_total_supplementaire + cout_investissement
    afficher_resultat_cadre(
        "Coût total =",
        f"{cout_total:.2f} DT",
        "Coût total = (Ventes initiales par mois * Période de mesure * Coût de production par boîte) + Coût des marchandises vendues + Coût de l'investissement"
    )

    roi_complet = ((revenus_total - cout_total) / cout_investissement) * 100
    afficher_resultat_cadre(
        "Retour sur investissement (ROI) =",
        f"{roi_complet:.2f}%",
        "ROI = ((Revenus total - Coût total) / Coût de l'investissement) * 100"
    )

    bep = cout_investissement / (prix_ht_par_boite - cout_production_par_boite)
    afficher_resultat_cadre(
        "Seuil de rentabilité (BEP) =",
        f"{bep:.2f} boîtes",
        "BEP = Coût de l'investissement / (Prix hors taxe par boîte - Coût de production par boîte)"
    )

    ventes_cumulees = 0
    mois_bep = 0
    for mois, ventes in enumerate(ventes_mensuelles, start=1):
        ventes_cumulees += ventes
        revenu_cumule = ventes_cumulees * prix_ht_par_boite
        if revenu_cumule >= cout_investissement:
            mois_bep = mois
            break

    if mois_bep > 0:
        afficher_resultat_cadre(
            "Le seuil de rentabilité est atteint au mois :",
            mois_bep,
            "Le seuil de rentabilité est atteint quand les ventes cumulées couvrent le coût de l'investissement"
        )
    else:
        st.warning("Le seuil de rentabilité n'est pas atteint dans la période donnée.")

if __name__ == "__main__":
    main()
