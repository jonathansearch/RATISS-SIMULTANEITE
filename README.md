# 🛰️ RATISS-SIMULTANEITE — la matrice de simultanéité

**RATISS Labs** (labo indépendant de Jonathan Evina) · étiquette **🧮 calcul pur — aucune mesure QPU** · MIT
Équipe : Jonathan (chef) · RATISS (hypothèses) · Arena (exécution, juge) · avec Qwen Coder, GLM, Dola.

## La question
Peut-on construire une « matrice de simultanéité » : des portes coordonnées par le bruit de notre univers,
nos portes et nos micro-ondes, qui produise des corrélations utiles, sans imiter un simulateur quantique en 2ⁿ ?

## Ce qui est établi ici
1. **Le juge CHSH** (`chsh_juge.py`, < 1 s) : singulet exact **2,826** · bruit partagé avec choix indépendants **2,001** ·
   choix dérivés de la même graine (triche) **4,000**. Un modèle classique sans canal entre A et B ne dépasse pas 2 (Bell, 1964).
   Ce qui est conservé : **toute matrice est jugée avec des choix de mesure indépendants de sa graine.**
2. **Trois versions d'hypothèse testées, trois pièges trouvés** (détail dans `JOURNAL.md`, code dans `tests/`) :
   - v1 : signe de diffusion inversé (explosion) et témoin sans bruit partagé ;
   - v2 : mesure aveugle par construction (angle aléatoire indépendant → corrélation 0) et témoin sans le même filtre temporel ;
   - v3 : parité indépendante du couplage par identité de Kuramoto, drive additif sans effet.
3. **v3 optimisée** (`simmat_v3_opt.py`, 10 graines en parallèle, ~35 s) — **scan exploratoire, non scellé** :
   - le couplage en anneau **aide les portes à se verrouiller sur un drive commun** malgré le bruit local
     (N=16 : Rd 0,42 avec drive seul, 0,48 avec couplage seul, **0,81** avec les deux) ;
   - la « parité » GHZ-like (cohérence de la phase totale) : effet du drive à N=4, J=3 = 6,9 σ en test apparié (revue GLM) ;
     l'effet n'est pas significatif à N=8 et N=16 (au niveau du plancher ≈ 0,07).

## Ce qui n'est PAS établi
- Aucune intrication : tout est classique. Aucun S > 2.
- Aucune accélération quantique, aucun lien avec la cryptographie.
- Le verrouillage par couplage est une physique connue (Kuramoto forcé) : c'est un outil, pas une découverte.
- Aucun résultat scellé pour l'instant : les critères seront scellés (SHA-256) par le chef avant le premier run de mesure.

## Rejouer
```bash
pip install numpy
python3 chsh_juge.py
python3 simmat_v3_opt.py        # → resultats_v3_opt.json
python3 tests/run_v3_test.py    # le piège de l'identité de Kuramoto
python3 MANIFESTE.py --verifier
```

## Règles appliquées
R4 aucun chiffre non calculé · R5 critères scellés avant mesure · R6 témoins, append-only · R7 rejouable en une commande ·
**R8 on ne mesure que ce qui déborde du script** · plus, née ici : **vérifier qu'aucune identité du modèle ne décide déjà le critère**,
et **vérifier que l'instrument voit (valeurs connues) avant de lire le chiffre**. Certification : SHA-256.
