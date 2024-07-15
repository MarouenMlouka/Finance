import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def obtenir_entree_utilisateur(message, type_conversion, default_value=None):
    if default_value is not None:
        user_input = st.text_input(message, value=default_value)
    else:
        user_input = st.text_input(message)
    
    if user_input and user_input.strip():  # Vérifie si l'entrée utilisateur n'est pas vide
        try:
            return type_conversion(user_input)
        except ValueError:
            st.error(f"Erreur : Veuillez entrer une valeur numérique valide pour {message}")
            return None  # Retourner None en cas d'erreur de conversion
    else:
        return None  # Retourner None si l'entrée est vide ou None

def afficher_resultat_cadre(titre, resultat, explication):
    st.subheader(titre)
    st.write(resultat)
    st.text_area("Explication", explication, height=100)

def main():
    # URL du logo Servier
    url_logo_servier = "https://upload.wikimedia.org/wikipedia/fr/thumb/b/b0/Logo_Servier_2024.svg/2560px-Logo_Servier_2024.svg.png"

    st.title("Calculateur d'analyse financière")

    # Affichage du logo Servier en haut à droite
    st.image(url_logo_servier, width=150)  # Ajustez la largeur selon vos besoins

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
    ventes_initiales_par_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0) :", float, default_value=None)
    if ventes_initiales_par_mois is None:
        st.warning(f"Aucune valeur n'a été saisie pour les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0).")

    # Saisie de la période de mesure
    periode_mesure = st.number_input("Entrez la période de mesure (en mois) :", min_value=1, step=1, key='periode_mesure')

    # Saisie des ventes mensuelles pour chaque mois de la période de mesure
    ventes_mensuelles = []
    for mois in range(1, periode_mesure + 1):
        ventes_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales pour le mois {mois} (en boîtes) :", int)
        if ventes_mois is None:
            st.warning(f"Aucune valeur n'a été saisie pour les ventes totales du mois {mois}.")
        ventes_mensuelles.append(ventes_mois)

    # Vérifier si toutes les entrées nécessaires sont valides avant de procéder aux calculs
    if all(v is not None for v in ventes_mensuelles) and ventes_initiales_par_mois is not None:
        # Calcul des boîtes supplémentaires (uplift)
        boites_supplementaires = sum(ventes_mensuelles) - (ventes_initiales_par_mois * periode_mesure)
        afficher_resultat_cadre(
            "Boîtes supplémentaires vendues =",
            boites_supplementaires,
            "Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)"
        )

        # Demander le prix hors taxe par boîte
        prix_ht_par_boite = obtenir_entree_utilisateur(f"Entrez le prix hors taxe par boîte de {nom_produit} (en DT) : ", float)
        if prix_ht_par_boite is None:
            st.warning(f"Aucune valeur n'a été saisie pour le prix hors taxe par boîte de {nom_produit}.")

        # Demander le coût de production par boîte
        cout_production_par_boite = obtenir_entree_utilisateur(f"Entrez le coût de production par boîte de {nom_produit} (en DT) : ", float)
        if cout_production_par_boite is None:
            st.warning(f"Aucune valeur n'a été saisie pour le coût de production par boîte de {nom_produit}.")

        # Vérifier si toutes les entrées nécessaires sont valides avant de procéder aux calculs
        if prix_ht_par_boite is not None and cout_production_par_boite is not None:
            # Calcul du coût des marchandises vendues (COGS)
            cout_total_supplementaire = cout_production_par_boite * boites_supplementaires
            afficher_resultat_cadre(
                "Coût des marchandises vendues (COGS) =",
                f"{cout_total_supplementaire:.2f} DT",
                "COGS = Coût de production par boîte * Boîtes supplémentaires vendues"
            )

            # Demander le coût de l'investissement
            cout_investissement = obtenir_entree_utilisateur("Entrez le coût de l'investissement pour la période concernée (en DT) : ", float)
            if cout_investissement is None:
                st.warning("Aucune valeur n'a été saisie pour le coût de l'investissement.")

            # Vérifier si toutes les entrées nécessaires sont valides avant de procéder aux calculs
            if cout_investissement is not None:
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

                # Calcul du seuil de rentabilité (BEP)
                seuil_rentabilite = cout_total / revenus_total
                afficher_resultat_cadre(
                    "Seuil de rentabilité (BEP) =",
                    f"{seuil_rentabilite:.2%}",
                    "Seuil de rentabilité (BEP) = Coût total / Revenus totaux"
                )

                # Calcul de la période exacte pour atteindre le seuil de rentabilité (BEP)
                if marge_brute > 0:
                    periode_bep_exacte = (cout_investissement / marge_brute) * 100
                    afficher_resultat_cadre(
                        "Période exacte pour atteindre le seuil de rentabilité (BEP) =",
                        f"{periode_bep_exacte:.2f} mois",
                        "Période exacte pour atteindre le seuil de rentabilité (BEP) = (Coût de l'investissement / Marge Brute) * 100"
                    )
                else:
                    st.warning("La marge brute est inférieure ou égale à zéro, impossible de calculer la période exacte pour atteindre le seuil de rentabilité (BEP).")

    st.markdown("---")
    st.write("Merci d'utiliser notre calculateur d'analyse financière.")
    
if __name__ == "__main__":
    main()
