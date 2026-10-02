# 🧮 RETOUR GLM — revue RATISS-SIMULTANEITE v3_opt (5 points)

De : GLM (Super Z) · À : Jonathan (chef), Arena, RATISS, Qwen Coder, Dola · 02/10/2026
Contexte : clone neuf de `RATISS-SIMULTANEITE`, manifeste 16/16 conforme, replay complet avant toute analyse.
Machine : numpy 2.1.3. Tous les chiffres ci-dessous sont calculés, scripts fournis. Format : constat → preuve → proposition.

---

## 0. R4 d'abord — replay clone neuf

**Constat :** la promesse R4 tient.
**Preuve :** `python3 simmat_v3_opt.py` sur clone neuf → **24/24 lignes de `resultats_v3_opt.json` bit-à-bit identiques** au fichier publié (floats exacts, pas de tolérance). Config identique.
**Proposition :** consigner ce PASS dans JOURNAL.md (clone neuf ≠ machine d'origine, même résultat bit à bit — c'est le test qui compte).

---

## 1. Revue de code `simmat_v3_opt.py`

### Ce qui est solide (à garder tels quels)
- **Nombres aléatoires communs entre cellules** : om (`10_000+s`), φ₀ (`20_000+s`), bruit (`30_000+s`) ne dépendent ni de J, ni de A, ni du nombre de pas → à N fixé, les runs (J, A) sont **appariés bit à bit par construction**. C'est une force majeure : tout test apparié est gratuit.
- **L'identité de Kuramoto est active dans les données mêmes** : à A=0, Pgl est identique pour J=0/0,3/1/3 à ~1e−11 près (N=4 : 0,07350712751…) dans le JSON publié. Le couplage ne fuite pas dans Σφ — témoin intégré gratuit.
- Contrôle d'instrument sur valeurs connues ✓ · Euler-Maruyama correct (sx·√dt) ✓ · pas de wrap des phases : à 200 ut, φ ~ 1000 rad → erreur d'argument ~1e−13 rad, négligeable (prévoir un wrap si T×100).

### Points à traiter (par importance)

**① Pgl n'est PAS stationnaire sur la fenêtre de mesure — le plancher « ≈ 0,07 » est un transitoire.**
- Preuve (moitiés appariées de la fenêtre, graines 0–9, A=0,5) : ΔPgl = **−0,060±0,036** (N=8, J=0) · **−0,067±0,030** (N=8, J=1) · **−0,057±0,030** (N=8, J=3) · −0,021±0,019 (N=16, J=3) — même signe partout. En doublant transitoire+fenêtre (T=40000 pas) : Pgl 0,0820→**0,0505** (N=8, J=0) et 0,1042→**0,0712** (N=8, J=1). Rd, lui, est stationnaire (Δ ≤ +0,005±0,010).
- Proposition : toute mesure scellée de Pgl → T doublé + les deux moitiés rapportées ; écart A/B > 2σ = mesure non mûre, on ne lit pas.

**② Le comparateur « plancher » A=0, J=0 est le mauvais témoin pour J>0.**
- Preuve : à A=0, Pgl est identique pour tout J (identité) → ne peut rien témoigner pour J>0. Et à A=0, J=3, N=16 : Rd = 0,720±0,068 — ce n'est pas un plancher, c'est de l'**auto-synchronisation de l'anneau** (physique réelle, pas un artefact).
- Proposition : le témoin propre est le run **apparié A=0 vs A=0,5 au même J** (seule différence : le terme de drive, bit à bit).

**③ La force statistique est sous-utilisée : les σ publiés sont non appariés.**
- Preuve (tests appariés par graine, mêmes streams) : effet drive sur Pgl à N=4, J=3 : **+0,1637±0,0237 = 6,9σ** ; synergie Rd à N=16, J=1 : **+0,1424±0,0133 = 10,7σ** (invisible en non apparié) ; effet drive sur Pgl à N=8 : 1,4σ, N=16 : 0,9σ (l'effet parité meurt bien avec N).
- Proposition : tout critère scellé = test apparié par graine. Le « ≈ 4,7σ » du README passe à 6,9σ apparié.

**④ Statistique résumée fragile.** Pgl par graine est lourdement étalé (les graines à petit |ΣΔ| dominent à A=0) → moyenne±SEM sur 10 graines résume mal. Prop : reporter par graine dans le JSON, tester apparié.

**⑤ dt=0,01 : biais Euler-Maruyama non détectable sur Rd** (dt = 0,01/0,005/0,0025 à temps fixe : 0,4692/0,4626/0,4764 — non monotone, bruit > tendance), et l'étalon Fokker-Planck borne le biais système à ≤ ~0,02 (§3). Prop : dt figé au sceau, inutile de raffiner.

**⑥ Signature Euler documentée, bénigne.** Drive évalué au début du pas → rotation globale effective ∓ω_d·dt/2 = ∓0,025 rad. Invariante par |·| donc **sans effet sur Rd ni Pgl** ; mesurée sous le seuil (rotation agrégée : −0,005/+0,028/−0,002 rad). À noter au protocole, rien à corriger.

**⑦ Reproductibilité liée à numpy.** PCG64 est stable mais numpy se réserve de changer les distributions de Generator. Prop : sceller `numpy==2.x` dans PARAMETRES (mon replay : numpy 2.1.3, 24/24 identiques).

---

## 2. Le plancher de Pgl — formule, témoin, et le résultat mécanique

**Formule exacte.** z_t = e^{iΘ_t}, Θ = Σφ_rel. Pour une série (quasi) stationnaire :
**E|z̄|² = (1/n²)[n·C(0) + 2Σ_{k=1}^{n−1}(n−k)·C(k)]**, C(k) = ⟨cos(Θ_{t+k}−Θ_t)⟩.
Le plancher est entièrement déterminé par l'autocorrélation ; sa part irréductible (z blanc) vaut √(π/4n) = **0,0089** à n=10 000 — le reste vient de la corrélation : τ_eff ≈ 0,65 / 0,49 / 0,14 ut (N=4/8/16, A=0,5, calculés).

**Preuve calculée (J=0, graines 0–9)** : mesuré 0,0735 / 0,0723 / 0,0672 (A=0) et 0,0999 / 0,0820 / 0,0499 (A=0,5) — la formule par FFT circulaire restitue chaque valeur (identité — vérification d'implémentation, pas un test physique).

**Le résultat qui compte — la cohérence de parité VRAIE à J=0 est morte d'avance :**
C(∞) = |⟨z⟩|² = cohérence vraie ; à J=0, ⟨e^{iΣψ}⟩ = Πμ(Δ_i) (indépendance), donc **|⟨e^{iΣψ}⟩| ≤ (E|μ(Δ)|)^N = 0,4740^N** :
- N=4 : ≤ 5,0e−2 · N=8 : ≤ 2,5e−3 · **N=16 : ≤ 6,5e−6** (μ(Δ) = solution exacte d'Adler forcé, §3 ; E|μ(Δ)| = 0,4740 par quadrature GH-41).
→ La cohérence de parité vraie décroît **exponentiellement en N** pendant que le plancher ne descend qu'en **1/√n**. C'est la raison mécanique du « pas significatif à N=8, 16 » — désormais calculée, plus seulement observée. Tout effet parité à grand N DOIT donc venir du couplage.

**Témoin numérique pour le protocole :** run apparié A=0 au même J (identité → même trajectoire de Σφ bit à bit) ; différence par graine = signal pur à ressources égales.

---

## 3. Étalon analytique — Fokker-Planck exact du cas J=0 (le moteur est validé)

Ott-Antonsen ne s'applique pas ici (couplage anneau ≠ all-to-all, désordre gaussien ≠ Cauchy, bruit blanc). Mais **à J=0 chaque porte est un oscillateur d'Adler forcé bruité, exactement soluble** :
dψ = (Δ − A·sinψ)dτ + sx·dW, densité stationnaire à flux non nul (Δ≠0) :
**P(ψ) = e^V·(c − κ·I(ψ))**, V = (Δψ + A·cosψ)/D, D = sx²/2, I = ∫e^{−V}, κ = signe(Δ),
**c = κ·e^{V(2π)}·I(2π)/(e^{V(2π)} − e^{V(0)})** (périodicité). μ(Δ) = ⟨e^{iψ}⟩ par quadrature.

**Validation croisée (200 répliques Langevin indépendantes, fenêtre 10 000 pas) :**
- Δ=+0,3 : moyenne des répliques (+0,4346, +0,2896) vs μ_FP (+0,4318, +0,2924) → **z = 0,39** · Δ=+1,5 : **z = 1,46**.
- std(m) = 0,1464 → la dispersion par oscillateur mesurée sur le moteur (RMS |m−μ| = 0,12–0,16) est **exactement** la dispersion finie-temporelle attendue, pas un écart.

**Test collectif exact** (insensible aux temps de corrélation) : ⟨|X̄|²⟩ = |⟨μ(Δ_i)⟩|² + (1 − ⟨|μ|²⟩)/N :
mesuré **0,3369 / 0,2533 / 0,1972** vs prédit **0,3217 / 0,2435 / 0,2094** (N=4/8/16) → écarts +0,015 / +0,010 / −0,012.

**Verdict : l'instrument VOIT (R8).** Le moteur reproduit la statistique stationnaire exacte du modèle à ~1–3 % près là où une solution exacte existe (J=0). Limite honnête : l'étalon ne couvre pas J>0 (pas de solution exacte) — la convergence dt et les moitiés de fenêtre prennent le relais. Bonus : |μ̄| = 0,3790 (limite N→∞ de Rd à J=0, A=0,5) ; mesuré 0,4206 (N=16), l'écart décroissant en N est l'inflation modulaire finie-N attendue de ⟨|X̄|⟩.

*Note de fabrique : ma première solution de flux était fausse (périodicité : j'avais (e^{V(2π)} − 1) au lieu de (e^{V(2π)} − e^{V(0)})) — un Langevin brut indépendant l'a attrapée avant toute conclusion. L'échec publié, comme d'habitude (R6).*

---

## 4. Question à sceller (le chef scelle — aucun run avant)

**« À ressources égales (mêmes graines → mêmes om/φ₀/bruit bit à bit), l'effet du couplage sur la parité Pgl survit-il à N=8 et N=16 une fois le plancher maîtrisé ? »**

- **Protocole** : N ∈ {8, 16} × J ∈ {0 ; 1,0} × A ∈ {0 ; 0,5} (4 cellules appariées par N) · **20 graines fraîches 100–119** (jamais retouchées, append-only) · T=40 000 pas (transitoire 200 ut, cf. §1-①) · dt=0,01 · numpy scellé. Coût : ~25 s.
- **Critère principal (Pgl, apparié)** : d_s = Pgl_s(A=0,5 ; J=1) − Pgl_s(A=0 ; J=1) → retenu si mean(d) > 5·SEM(d) **et** Pgl(A=0,5 ; J=1) > 3× le plancher blanc (0,027).
- **Critère secondaire (Rd, apparié)** : synergie s_s = [Rd_s(A,J) − Rd_s(0,J)] − [Rd_s(A,0) − Rd_s(0,0)] > 5σ — sur graines 0–9 elle vaut déjà **10,7σ** à N=16, J=1 ; le sceau doit porter sur les fraîches.
- **Témins à ressources égales** : (a) cellule A=0 = identité en aveugle (Pgl indépendant de J) ; (b) moitiés A/B de fenêtre ; (c) contrôle d'instrument valeurs connues ; (d) étalon FP J=0 à 0,02 près.
- **Ce qui tue l'hypothèse** : d_s < 5σ à N=8 → « l'effet parité ne survit pas à N=8 », publié tel quel (R6). Passe à N=8, échoue à N=16 → effet transitoire en 1/N, hypothèse affaiblie. Et dans tous les cas, la borne 0,4740^N (§2) encadre : sans couplage, pas de parité collective au-delà de N=4.

---

## 5. Vitesse — optimisation sûre, prouvée bit à bit

**Changement unique : pré-tirage du bruit** `nz = np.stack([rng(30_000+s).standard_normal((T,N)) for s in seeds])` puis `nz[:, t, :]` (le reste de l'expression est inchangé au float près).
- Preuve d'identité de flux : `standard_normal((T,N))` ≡ T× `standard_normal(N)` **bit à bit** (testé graines 30_000+0 et +7).
- Scan complet : **24/24 lignes identiques** au JSON publié · durée **21,8 → 16,1 s (×1,35)** sur cette machine.
- Gain candidat refusé par prudence : sauter `J*cpl` quand J=0 (risque −0,0 vs +0,0 — pas bit-sûr sans preuve). Prêt à coller si Arena l'accepte.

---

## En une phrase

Le moteur est sain (R4 PASS, étalon exact validé, identité active), mais les Pgl du scan sont des transitoires fini-temporels et la moitié de la force statistique dort dans l'appariement — le protocole proposé au §4 récupère les deux pour ~25 s de calcul.

— GLM (Super Z), mode outil. 🛰️🧮🫡
