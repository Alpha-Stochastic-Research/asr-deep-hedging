# Rapport de révision du manuscrit

## Livrables

- `deep_hedging_revised.tex` : manuscrit LaTeX réécrit et compilable.
- `deep_hedging_revised.pdf` : version PDF vérifiée visuellement.

## Corrections de fond intégrées

1. **Repositionnement honnête de la contribution**
   - Le titre parle désormais d’une *partial replication* et non d’une reproduction intégrale.
   - Un tableau compare explicitement l’architecture, les instruments et les benchmarks à ceux de Bühler et al. (2019).

2. **Correction du raisonnement à coût nul**
   - Suppression de l’affirmation selon laquelle la delta Black–Scholes discrétisée serait nécessairement optimale pour la CVaR.
   - La contre-performance du réseau à coût nul est présentée comme un résultat empirique d’un run, non comme une prédiction théorique.

3. **Définition financière complète**
   - Introduction d’un P&L terminal avec cash initial `p0`.
   - Définition explicite de la perte, de l’autofinancement, des transactions et de la liquidation terminale.
   - La convention expérimentale `p0 = 0` et le coût terminal nul sont désormais déclarés.

4. **Correction de l’interprétation des pourcentages de CVaR**
   - Preuve que la politique optimale et les différences absolues sont invariantes par translation monétaire.
   - Explication que les pourcentages d’amélioration ne le sont pas.
   - Les écarts absolus deviennent les résultats principaux.

5. **CVaR empirique rigoureuse**
   - Distinction entre CVaR populationnelle, objectif empirique de batch et objectif profilé.
   - Suppression de l’affirmation incorrecte selon laquelle le quantile de chaque batch donnerait exactement le même objectif populationnel.
   - Formule exacte de l’Expected Shortfall empirique avec pondération fractionnaire de l’observation frontière.
   - Pour `B = 4096` et `alpha = 0.95`, la queue exacte contient 204 observations entières et 0,8 fois l’observation suivante.

6. **Correction du gradient des coûts**
   - Le coût suivant est correctement indexé par `S_{k+1}`.
   - Traitement séparé des dates initiale, intérieure et terminale.
   - Sous-gradient du coût proportionnel à zéro explicité.

7. **Correction de l’interprétation de l’architecture**
   - Le réseau actuel est qualifié de *state-only*, non de récurrent.
   - Le texte explique pourquoi le gradient de coût ne remplace pas l’inventaire comme variable d’état.
   - Le manuscrit ne prétend plus que le réseau apprend une véritable région de non-transaction.

8. **Expérience Heston requalifiée**
   - Elle est décrite comme une comparaison avec benchmark volontairement mal spécifié.
   - Suppression des affirmations de robustesse à la mauvaise spécification ou de comparaison équitable.
   - Ajout des ablations minimales nécessaires : réseau avec/sans variance, volatilité instantanée, volatilité fixe optimisée et delta Heston.

9. **Schéma Heston complètement spécifié**
   - Équations du full-truncation Euler et du log-Euler données.
   - Construction des Browniennes corrélées explicitée.
   - Distinction entre variable auxiliaire potentiellement négative et variance tronquée positive.
   - Violation de la condition de Feller signalée et besoin d’une étude de convergence expliqué.

10. **Interprétation statistique corrigée**
    - Les résultats sont qualifiés de point estimates mono-run.
    - Suppression des affirmations non démontrées sur la variance inter-runs.
    - Ajout d’un protocole multi-seed et bootstrap apparié.
    - Le contrôle de la moyenne non couverte est réévalué : l’écart au prix analytique est d’environ 3,1 erreurs standards Monte-Carlo.

11. **Benchmarks et calibration**
    - Ajout des benchmarks nécessaires : delta réduite, fréquence réduite, no-trade band et politique avec inventaire.
    - Les niveaux de coûts proportionnels élevés sont présentés comme stress tests.
    - La calibration quadratique approximative est explicitement reconnue comme non appariée.

12. **Reproductibilité**
    - Ajout d’un protocole de réplication confirmatoire.
    - Ajout d’une liste minimale des artefacts à archiver pour chaque tableau.
    - Ajout d’un test de gradient end-to-end recommandé.

## Ce qui ne peut pas être corrigé par réécriture seule

Une version réellement soumise à une revue de premier rang nécessite encore de relancer les expériences. Il serait scientifiquement incorrect d’inventer les résultats manquants. Les travaux empiriques indispensables sont :

1. régénérer tous les tableaux avec la CVaR empirique exacte et sa pondération frontière ;
2. réaliser au moins dix graines d’entraînement par configuration ;
3. construire des intervalles de confiance bootstrap appariés ;
4. ajouter des benchmarks classiques conscients des coûts ;
5. ajouter l’ablation avec la position précédente en entrée ;
6. équilibrer les ensembles d’information dans l’expérience Heston ;
7. tester la robustesse hors distribution ;
8. effectuer une étude de convergence du simulateur Heston ;
9. fournir le code, les graines, les configurations et les pertes individuelles ;
10. remplacer les cadres de figures par les fichiers graphiques originaux ou régénérés.

## Vérifications effectuées

- Compilation LaTeX sans erreur fatale.
- Références croisées et citations résolues.
- PDF de 17 pages généré.
- Rendu visuel des 17 pages contrôlé.
- Les figures manquantes sont remplacées automatiquement par des cadres explicites, afin que le fichier compile même sans le dossier `figures/`.
