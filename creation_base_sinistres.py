import pandas as pd
import numpy as np
from datetime import timedelta

# Chargement de la base de données
# J'utilise le chemin vers ton fichier CSV
df = pd.read_csv('data/Donnees_souscription.csv')

# --- ÉTAPE 1 : Filtrer et Exploser la base ---

# On ne garde que les lignes ayant au moins 1 sinistre
# Note : la colonne dans le CSV est "N_SINISTRE" (singulier)
table_sinistres = df[df['N_SINISTRE'] > 0].copy()

# On "explose" la table : on duplique les lignes selon la valeur de N_SINISTRE
# Si N_SINISTRE = 2, la ligne est répétée 2 fois
table_sinistres = table_sinistres.loc[table_sinistres.index.repeat(table_sinistres['N_SINISTRE'])].reset_index(drop=True)

print(f"Nombre de lignes après explosion (doit correspondre au nombre total de sinistres) : {len(table_sinistres)}")

# --- ÉTAPE 2 : Simulation Actuarielle ---

# Conversion des colonnes dates en format datetime si ce n'est pas déjà fait
table_sinistres['date_debut_police'] = pd.to_datetime(table_sinistres['date_debut_police'])
table_sinistres['date_fin_police'] = pd.to_datetime(table_sinistres['date_fin_police'])

# 1. Simulation du COUT_SINISTRE (Loi Log-Normale)
# Paramètres de la loi normale sous-jacente (mu et sigma)
# Ces valeurs (mu=7, sigma=1.5) sont des exemples standards pour obtenir des montants réalistes.
# Tu peux les ajuster selon la sévérité moyenne désirée.
mu = 7.0 
sigma = 1.5

# Génération des coûts aléatoires
table_sinistres['COUT_SINISTRE'] = np.random.lognormal(mean=mu, sigma=sigma, size=len(table_sinistres))

# Arrondi à 2 décimales pour faire "monétaire"
table_sinistres['COUT_SINISTRE'] = table_sinistres['COUT_SINISTRE'].round(2)


# 2. Simulation de la DATE_SINISTRE (Aléatoire entre date_debut et date_fin)
# Calcul de la durée de couverture en jours pour chaque ligne
duree_couverture = (table_sinistres['date_fin_police'] - table_sinistres['date_debut_police']).dt.days

# Génération d'un nombre de jours aléatoire entre 0 et la durée de couverture
jours_aleatoires = np.random.randint(0, duree_couverture + 1, size=len(table_sinistres))

# Ajout de ces jours à la date de début pour obtenir la date du sinistre
table_sinistres['DATE_SINISTRE'] = table_sinistres['date_debut_police'] + pd.to_timedelta(jours_aleatoires, unit='D')


# --- Affichage et Vérification ---
print("\n--- Aperçu de la nouvelle table table_sinistres ---")
print(table_sinistres[['num_police', 'N_SINISTRE', 'date_debut_police', 'DATE_SINISTRE', 'COUT_SINISTRE']].head(10))

# Sauvegarde optionnelle
# table_sinistres.to_csv('data/table_sinistres_generee.csv', index=False)

