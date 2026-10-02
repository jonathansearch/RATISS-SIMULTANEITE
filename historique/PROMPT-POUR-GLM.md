# 🛰️ PROMPT POUR GLM — renfort sur RATISS-SIMULTANEITE

Salut GLM 👋 Ici l'agent Arena, sur ordre de Jonathan, le chef de **RATISS Labs** (labo indépendant, Cameroun).
Tu rejoins l'équipe : **Jonathan · Arena · RATISS · Qwen Coder · GLM · Dola**. Bienvenue 🔥

Dépôt public : **https://github.com/jonathansearch/RATISS-SIMULTANEITE**
Lis `README.md` puis `JOURNAL.md` (5 min), c'est tout le contexte.

## Le projet en 5 lignes
- Idée du chef : une « matrice de simultanéité », des portes coordonnées par le bruit, nos portes et nos micro-ondes.
- Juge CHSH déjà en place : un modèle classique sans canal A↔B ne dépasse pas S = 2 (Bell). On ne cherche pas à le battre.
- Trois versions ont échoué pour des raisons documentées (instrument aveugle, témoin injuste, identité du modèle).
- `simmat_v3_opt.py` : Kuramoto forcé sur anneau (drive A·sin(ω_d t − φ_i), bruit local, désordre de fréquence),
  observables **Rd** (verrouillage collectif dans le repère du drive) et **Pgl** (cohérence de la phase totale).
- Scan exploratoire (non scellé) : le couplage aide fortement le verrouillage sur le drive (N=16 : 0,42 / 0,48 / **0,81**) ;
  l'effet sur Pgl n'est significatif qu'à N=4.

## Les règles du labo (non négociables)
- R4 : aucun chiffre non calculé, aucune prédiction chiffrée inventée.
- R5 : critères scellés (SHA-256) **par le chef** avant le premier run de mesure.
- R8 : on ne mesure que ce qui déborde du script ; vérifier qu'aucune **identité du modèle** ne décide le critère ;
  vérifier que l'instrument voit (valeurs connues) avant de lire un chiffre.
- Certification = SHA-256 (pas de ZK). Pas de « 100 % », pas d'API qui n'existe pas. Environnement réel : Python + numpy, 2 cœurs.
- Les échecs se publient comme les succès.

## Ce qu'on te demande (choisis ce que tu fais le mieux, réponds point par point)
1. **Revue de code** de `simmat_v3_opt.py` : bugs, biais statistiques, ce qui pourrait fausser Rd ou Pgl
   (temps de corrélation, nombre de graines, demi-série de mesure, pas de temps dt = 0,01 avec ω = 5).
2. **Le plancher de Pgl** : sans drive, Pgl ≈ 0,07 et ne vaut pas 0 à cause de la durée finie et de la corrélation temporelle.
   Propose une estimation **calculable** de ce plancher (formule ou témoin numérique), pour savoir ce qui est vraiment au-dessus.
3. **Une référence analytique** : pour Kuramoto forcé et bruité (champ moyen, par exemple réduction d'Ott-Antonsen ou
   approche de Fokker-Planck), quelle valeur de Rd attendre ? Une comparaison théorie/numérique serait un **étalon** du moteur.
4. **Une question à sceller** : propose une question falsifiable, avec témoins à ressources égales et un seuil chiffré
   (ex. : « l'effet du couplage sur Rd dépasse-t-il la somme des effets séparés de 5 σ sur 10 graines ? »
   ou « l'effet sur Pgl survit-il à N=8 ? »), et dis ce qui tuerait l'hypothèse. Le chef scellera.
5. **Vitesse** (optionnel) : une optimisation numpy pure qui garde les résultats **bit à bit** identiques, ou qui explique pourquoi ils changeraient.

## Format de réponse
Constat → preuve (code numpy court ou calcul) → proposition. Pas de chiffre sans calcul.
Ton énergie et tes emojis sont bienvenus, c'est la culture du labo 🛰️🧮🫡
