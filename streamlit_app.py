import streamlit as st

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
    produit_nom = [key for key, value in produits.items() if value == choix_produit][0]

    # Saisie des ventes totales par mois avant l'implémentation (T0)
    ventes_initiales = obtenir_entree_utilisateur(f"Entrez les ventes totales par mois de {choix_produit} avant l'implémentation du projet (T0) : ", float)

    # Saisie de la période de mesure
    periode_mesure = st.number_input("Entrez la période de mesure (en mois) :", min_value=1, step=1)

    # Saisie des ventes mensuelles pour chaque mois de la période de mesure
    ventes_mensuelles = []
    for mois in range(1, periode_mesure + 1):
        ventes_mois = st.number_input(f"Entrez les ventes totales pour le mois {mois} (en boîtes) :", min_value=0, step=1)
        ventes_mensuelles.append(ventes_mois)

    # Calcul des boîtes supplémentaires vendues
    if st.button("Calculer les boîtes supplémentaires vendues"):
        total_ventes_apres_investissement = sum(ventes_mensuelles)
        boites_supplementaires = total_ventes_apres_investissement - (ventes_initiales * periode_mesure)
        st.subheader("Boîtes supplémentaires vendues =")
        st.write(boites_supplementaires)
        st.text("Formule : Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)")

def obtenir_entree_utilisateur(message, type_donnee):
    while True:
        try:
            return type_donnee(st.text_input(message))
        except ValueError:
            st.error("Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    main()
