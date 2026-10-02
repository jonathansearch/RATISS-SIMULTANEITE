# 🛰️ RETOUR À RATISS — Matrice de simultanéité v3

Frérot 🔥 Ici Jonathan.

Ta v2, c'est du sérieux : −γL corrigé, condition de stabilité, T-PARTAGE, micro-onde = drive cohérent au nœud 0,
graines séparées, et surtout **une question qui peut échouer**. Respect 💪
Arena a refait tourner ta dynamique à l'identique (`run_v2_test.py`, ta config, < 3 s). Le juge a parlé, et il est dur.
⚠️ Transparence R5 : c'est un **essai à blanc avant sceau**, pour ne pas sceller une config déjà perdante. Rien n'est scellé.

---

## 💀 1. Ta mesure est morte par construction

`X = sign(cos(S − θ))` avec θ **uniforme et indépendant à chaque tir**, pour A et pour B.
Moyenné sur θ_A et θ_B indépendants, E[X_A·X_B] = E[X_A]·E[X_B] = 0, **quel que soit l'état**.
Mesuré :

| graine de choix | ρ SimMat | ρ PARTAGE |
|---|---|---|
| 77777 | +0,0025 | −0,0017 |
| 1 | −0,0004 | −0,0020 |
| 2 | −0,0006 | +0,0007 |

→ Tout vaut zéro, même quand les états sont corrélés à 69 %. Ce n'est pas un résultat, c'est l'instrument qui est aveugle.
C'est la leçon NAVIER : **vérifier l'instrument avant de croire le chiffre.**
👉 Pour CHSH, il faut **deux réglages discrets** par côté (a, a′ et b, b′), choisis au hasard, et des corrélations
calculées **par paire de réglages**. Pour C1/C2, mesure directement la corrélation des **états** (ou des signes de l'état), pas à travers un angle aléatoire.

## 📉 2. Sur les états eux-mêmes, C1 et C2 tombent

| quantité | valeur |
|---|---|
| SimMat ρ(porte 0, porte 1) | 0,514 |
| **SimMat ρ(porte 0, porte 4)** | **0,0098** |
| T-PARTAGE brut | 0,694 |
| T-PARTAGE + même filtre α | **0,921** |

- **C1** : 0,0098 contre 0,694 → la topologie perd d'un facteur 70.
- **C2** : ρ(k=4)/ρ(k=1) = 0,02, alors que tu demandais > 0,5 → le guide d'ondes n'a pas de portée à distance 4.

## 🎭 3. Et même si ça avait gagné, la victoire n'aurait pas été à la topologie

Ton drive est lent (ω = 0,01, période ≈ 628 pas) et le bruit local est blanc. L'inertie α est un **filtre passe-bas** :
elle garde le drive et tue le bruit. Ce gain vient du **temps**, pas de l'anneau.
La preuve : T-PARTAGE avec le **même filtre α**, sans aucune topologie, monte à **0,921**.
👉 **R8** : le témoin juste est **T-PARTAGE-FILTRÉ** (accès direct + même inertie). C'est lui que la topologie doit battre.

---

## 🎯 Ce que je te demande (v3)

1. **Réponds à ces 3 points franchement.** Si l'hypothèse « topologie = mémoire utile » est morte sous cette forme, écris-le :
   on publie l'échec, c'est la signature du labo.
2. **Si tu vois encore une porte**, une seule question falsifiable, avec :
   - une mesure **vivante** (vérifie-la toi-même sur un cas où la réponse est connue : deux états identiques doivent donner ρ ≈ 1, deux bruits indépendants ρ ≈ 0) ;
   - un témoin **à ressources égales**, y compris le même filtrage temporel (T-PARTAGE-FILTRÉ) ;
   - une raison physique pour laquelle un réseau **pourrait** battre un accès direct (par exemple : moyenne spatiale de bruits locaux indépendants sur plusieurs portes, redondance, vote, correction d'erreur…) ;
   - des critères que **je** scelle, et ce qui tue l'hypothèse.
3. **Ou bien une autre direction**, si tu la trouves plus forte, mais toujours en lien avec ce qu'on veut :
   des corrélations coordonnées par le bruit, nos portes, nos micro-ondes, et un lien possible avec nos vrais jobs GHZ archivés.
4. Garde le format : hypothèse en une phrase, mécanisme calculable, code numpy court, témoins, critères, limites.

## 📏 Toujours les mêmes règles

Pas de chiffre prédit avant la mesure. Pas de ZK, pas de « 100 % », pas d'API inexistante.
**R8 : on ne mesure que ce qui déborde du script.** Et maintenant aussi : **on vérifie que l'instrument voit avant de lire le chiffre.**

T'es pas tombé, frérot : t'as trouvé deux pièges de plus pour le labo. Garde ta vision et reviens avec la v3 🔥🧮🛰️🫡

— Jonathan
