# PROTOCOLE SCELLÉ v1 — scellé sur ordre du chef le 02/10/2026, AVANT le run de mesure

Exécution : `python3 mesure_v1.py` (scellé avec ce fichier, voir `SCEAU-v1.sha256`). Verdict par N (8 et 16).

Base : revue GLM (`historique/RETOUR-GLM-SIMULTANEITE-v1.md`), chiffres clés reproduits par Arena le 02/10.

**Question** : à ressources égales, l'effet du **couplage** sur la parité Pgl survit-il à N=8 et N=16 ?

- Cellules : N ∈ {8, 16} × J ∈ {0 ; 1,0} × A ∈ {0 ; 0,5}, appariées par graine (mêmes om, φ₀, bruit, bit à bit).
- Graines fraîches 100–119 (jamais utilisées), T = 40 000 pas, dt = 0,01, mesure sur la 2ᵉ moitié, numpy version écrite dans le JSON.
- **Critère principal (correction Arena)** : effet du couplage sous drive, apparié :
  c_s = Pgl_s(A=0,5 ; J=1) − Pgl_s(A=0,5 ; J=0) > 5·SEM(c).
  (La proposition GLM, Pgl(A=0,5 ; J=1) − Pgl(A=0 ; J=1), mesure l'effet du **drive** à J fixé, pas celui du couplage.)
- Garde : Pgl(A=0,5 ; J=1) > 3 × plancher blanc √(π/4n), n = 20 000 → 3 × 0,0063 = 0,019.
- Maturité : moitiés A/B de la fenêtre ; |B − A| > 2σ → mesure non mûre, non lue.
- **Critère secondaire** : synergie Rd s_s = [Rd(A,J)−Rd(0,J)] − [Rd(A,0)−Rd(0,0)] > 5σ (graines fraîches).
- Témoins : identité (A=0 : Pgl indépendant de J), contrôle d'instrument, étalon Fokker-Planck J=0 (GLM).
- Ce qui tue : c < 5σ à N=8 → « l'effet parité du couplage ne survit pas à N=8 », publié tel quel.
  Borne GLM : sans couplage, cohérence de parité vraie ≤ 0,474^N (N=16 : 6,5×10⁻⁶).
