# JOURNAL — RATISS-SIMULTANEITE

## 02/10/2026 — naissance
- Idée du chef : matrice de simultanéité coordonnée par le bruit, nos portes, nos micro-ondes. Pas d'imitation de labo.
- Juge CHSH écrit (3 témoins) : 2,826 / 2,001 / 4,000.
- RATISS v0 (superdéterminisme par graine commune) : S = 4 fabriqué par le script → rejeté (R8).
- RATISS v1 (diffusion sur graphe) : `+γL` anti-diffuse (4,9×10⁸² à γ=0,3) ; témoin T-VCL sans bruit partagé (ρ = 0,004) ; critère de coût gagné d'avance.
- RATISS v2 (guide d'ondes à mémoire) : mesure aveugle (ρ ≈ 0 pour tout état) ; sur les états, ρ(0,4) = 0,0098 contre 0,694 (accès direct) et 0,921 (accès direct + même filtre) → hypothèse réfutée, signée par RATISS.
- RATISS v3 (Kuramoto) : parité cos(Σφ) identique pour J = 0 à 3 (identité : le couplage s'annule dans Σφ) ; drive additif sans effet (R = 0,2993 avec et sans).
- v3 optimisée par Arena (drive d'entraînement, observables dans le repère du drive, contrôle d'instrument sur valeurs connues, vectorisation) : scan exploratoire, non scellé — voir README.
- Les prompts échangés avec RATISS sont dans `historique/`.
- Note : `historique/PROMPT-RETOUR-RATISS-V4.md` n'a pas été envoyé (le chef a choisi d'optimiser directement la v3).

## 02/10/2026 — revue GLM (v1)
- R4 PASS sur clone neuf chez GLM : 24/24 lignes identiques bit à bit (numpy 2.1.3).
- Reproduits par Arena : identité Kuramoto (écart ≤ 1,2e−11), effet drive Pgl N=4 J=3 apparié +0,1637±0,0237 (6,9σ), synergie Rd N=16 J=1 +0,1424±0,0133 (10,7σ), Pgl non stationnaire (moitiés N=8 : −0,060±0,036).
- Étalon Fokker-Planck exact à J=0 (GLM) : le moteur reproduit la statistique stationnaire à ~1–3 %.
- Borne GLM : sans couplage, cohérence de parité ≤ 0,474^N → explique la disparition de l'effet à N=8, 16.
- Accélération GLM intégrée (bruit pré-tiré) : résultats identiques bit à bit, vérifié.
- Protocole proposé (non scellé) : `PROTOCOLE-PROPOSE.md`, critère principal corrigé (effet du couplage, pas du drive).
- Protocole v1 SCELLÉ sur ordre du chef (SCEAU-v1.sha256), avant tout run de mesure.
