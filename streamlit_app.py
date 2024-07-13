import streamlit as st

def obtenir_entree_utilisateur(message, type_conversion, default_value=None):
    user_input = st.text_input(message, default_value)
    if user_input:  # Vérifie si l'entrée utilisateur n'est pas vide
        try:
            return type_conversion(user_input)
        except ValueError:
            st.error(f"Erreur : Veuillez entrer une valeur numérique valide pour {message}")
            st.stop()
    else:
        st.error(f"Erreur : Veuillez entrer une valeur pour {message}")
        st.stop()

def afficher_resultat_cadre(titre, resultat, explication):
    st.subheader(titre)
    st.write(resultat)
    st.text(explication)

def main():
    st.title("Calculateur d'analyse financière")

    # Définition des produits
    produits = {
        "diamicron": "Diamicron",
        "natrixam": "Natrixam",
        "fludex LP": "Fludex LP"
    }

    # Choix du produit
    choix_produit = st.selectbox("Choisissez un produit", list(produits.values()))
    nom_produit = [key for key, value in produits.items() if value == choix_produit][0]

    # Saisie des ventes totales par mois avant l'implémentation (T0)
    ventes_initiales_par_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0) :", float)

    # Saisie de la période de mesure
    periode_mesure = st.number_input("Entrez la période de mesure (en mois) :", min_value=1, step=1, key='periode_mesure')

    # Saisie des ventes mensuelles pour chaque mois de la période de mesure
    ventes_mensuelles = []
    for mois in range(1, periode_mesure + 1):
        ventes_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales pour le mois {mois} (en boîtes) :", int)
        ventes_mensuelles.append(ventes_mois)

    # Calcul des boîtes supplémentaires (uplift)
    if ventes_mensuelles:
        boites_supplementaires = sum(ventes_mensuelles) - (ventes_initiales_par_mois * periode_mesure)
        afficher_resultat_cadre(
            "Boîtes supplémentaires vendues =",
            boites_supplementaires,
            "Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)"
        )

        # Demander le prix hors taxe par boîte
        prix_ht_par_boite = obtenir_entree_utilisateur(f"Entrez le prix hors taxe par boîte de {nom_produit} (en DT) : ", float)

        # Demander le coût de production par boîte
        cout_production_par_boite = obtenir_entree_utilisateur(f"Entrez le coût de production par boîte de {nom_produit} (en DT) : ", float)

        # Calcul du coût des marchandises vendues (COGS)
        cout_total_supplementaire = cout_production_par_boite * boites_supplementaires
        afficher_resultat_cadre(
            "Coût des marchandises vendues (COGS) =",
            f"{cout_total_supplementaire:.2f} DT",
            "COGS = Coût de production par boîte * Boîtes supplémentaires vendues"
        )

        # Demander le coût de l'investissement
        cout_investissement = obtenir_entree_utilisateur("Entrez le coût de l'investissement pour la période concernée (en DT) : ", float)

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
            st.warning("Le seuil de rentabilité n'est pas atteint dans la période donnée.")

if __name__ == "__main__":
    main()
