import streamlit as st

def obtenir_entree_utilisateur(message, type_conversion):
    user_input = st.text_input(message)
    if user_input:
        try:
            return type_conversion(user_input)
        except ValueError:
            st.error(f"Erreur : Veuillez entrer une valeur valide pour {message}")
            st.stop()
    return None

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

    # Étape 1: Ventes initiales par mois avant l'implémentation
    if st.session_state.etape == 0:
        st.session_state.ventes_initiales_par_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0) :", float)
        if st.session_state.ventes_initiales_par_mois is not None:
            st.session_state.etape = 1

    # Étape 2: Période de mesure et ventes mensuelles
    elif st.session_state.etape == 1:
        periode_mesure = st.number_input("Entrez la période de mesure (en mois) :", min_value=1, step=1)

        ventes_mensuelles = []
        for mois in range(1, periode_mesure + 1):
            ventes_mois = obtenir_entree_utilisateur(f"Entrez les ventes totales pour le mois {mois} (en boîtes) :", int)
            ventes_mensuelles.append(ventes_mois)

        if len(ventes_mensuelles) == periode_mesure:
            st.session_state.ventes_mensuelles = ventes_mensuelles
            st.session_state.etape = 2

    # Étape 3: Autres calculs et résultats
    elif st.session_state.etape == 2:
        # Calcul des boîtes supplémentaires (uplift)
        boites_supplementaires = sum(st.session_state.ventes_mensuelles) - (st.session_state.ventes_initiales_par_mois * len(st.session_state.ventes_mensuelles))
        afficher_resultat_cadre(
            "Boîtes supplémentaires vendues =",
            boites_supplementaires,
            "Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)"
        )

        # Demander le prix hors taxe par boîte
        prix_ht_par_boite = obtenir_entree_utilisateur(f"Entrez le prix hors taxe par boîte de {nom_produit} (en DT) : ", float)

        # Demander le coût de production par boîte
        cout_production_par_boite = obtenir_entree_utilisateur(f"Entrez le coût de production par boîte de {nom_produit} (en DT) : ", float)

        # Calcul des coûts et des résultats finaux
        if prix_ht_par_boite is not None and cout_production_par_boite is not None:
            # Calcul des revenus supplémentaires
            revenus_supplementaires = prix_ht_par_boite * boites_supplementaires
            afficher_resultat_cadre(
                "Revenus supplémentaires =",
                f"{revenus_supplementaires:.2f} DT",
                "Revenus supplémentaires = Prix hors taxe par boîte * Boîtes supplémentaires vendues"
            )

            # Calcul de la marge brute
            if revenus_supplementaires > 0:
                marge_brute = ((revenus_supplementaires - (cout_production_par_boite * boites_supplementaires)) / revenus_supplementaires) * 100
                afficher_resultat_cadre(
                    "Marge Brute =",
                    f"{marge_brute:.2f}%",
                    "Marge Brute = ((Revenus supplémentaires - Coût des marchandises vendues) / Revenus supplémentaires) * 100"
                )

if __name__ == "__main__":
    main()
