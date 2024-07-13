import streamlit as st
from termcolor import colored

# Fonction pour obtenir les entrées de l'utilisateur avec vérification
def obtenir_entree_utilisateur(message, type_donnee=float):
    while True:
        try:
            return type_donnee(st.text_input(message))
        except ValueError:
            st.error(colored("Entrée invalide. Veuillez entrer un nombre.", 'red'))

def main():
    st.title("Calculateur d'analyse financière")

    # Définir les produits disponibles
    produits = {
        "diamicron": {
            "nom": "Diamicron",
            "indice": 0
        },
        "natrixam": {
            "nom": "Natrixam",
            "indice": 1
        },
        "fludex LP": {
            "nom": "Fludex LP",
            "indice": 2
        }
    }

    # Initialisation de l'état de session pour les ventes initiales
    if 'ventes_initiales' not in st.session_state:
        st.session_state['ventes_initiales'] = {}

    # Demander le nom du produit
    choix_produit_nom = st.selectbox("Choisissez un produit", list(produits.keys()))
    nom_produit = produits[choix_produit_nom]["nom"]

    # Demander les ventes totales par mois avant l'implémentation du projet (T0)
    if nom_produit not in st.session_state['ventes_initiales']:
        st.session_state['ventes_initiales'][nom_produit] = obtenir_entree_utilisateur(
            f"Entrez les ventes totales par mois de {nom_produit} avant l'implémentation du projet (T0) : ",
            int
        )

    # Demander la période de mesure
    periode_mesure = obtenir_entree_utilisateur("Entrez la période de mesure (en mois) : ", int)

    # Demander les ventes mensuelles pour chaque mois de la période de mesure
    ventes_mensuelles = []
    for mois in range(1, periode_mesure + 1):
        ventes_mensuelles.append(obtenir_entree_utilisateur(f"Entrez les ventes totales pour le mois {mois} (en boîtes) : ", int))

    # Calculer les boîtes supplémentaires (uplift)
    boites_supplementaires = sum(ventes_mensuelles) - (st.session_state['ventes_initiales'][nom_produit] * periode_mesure)
    st.subheader("Boîtes supplémentaires vendues =")
    st.write(boites_supplementaires)
    st.text("Formule : Boîtes supplémentaires vendues = Total des ventes après investissement - (Ventes initiales par mois * Période de mesure)")

if __name__ == "__main__":
    main()

