# 🛰️ RETOUR À RATISS — Matrice de simultanéité v4

Frérot 🔥 Ici Jonathan.

T'as signé l'échec de la v2 sans te cacher, t'as pivoté vers une vraie physique (Kuramoto, synchronisation, parité GHZ),
t'as même ajouté un contrôle d'instrument au démarrage. C'est exactement l'esprit du labo 💪
Arena a refait tourner ta dynamique v3 à l'identique (`run_v3_test.py`, ta config, ~10 s). Essai à blanc, rien n'est scellé.
Le juge a trouvé **un piège mathématique** qui tue C1 avant même le premier run. Écoute bien, c'est une belle leçon.

---

## 🧮 1. Ta parité ne dépend pas de J, par construction

Le couplage de Kuramoto est **antisymétrique** : sin(φ_j − φ_i) = −sin(φ_i − φ_j).
Quand tu sommes sur toutes les portes, il s'annule exactement :
d(Σφ)/dt = Σω_i + N·Ω_d(t) + Σ bruits. **J n'apparaît plus.**
Donc cos(Σφ) est **identique pour tout J**. Mesuré (mêmes graines) :

| J | R (synchronisation) | parité moyenne cos(Σφ) | \|⟨e^{iΣφ}⟩\| dans le repère tournant |
|---|---|---|---|
| 0,0 | 0,208 | +0,0017 | 0,0171 |
| 0,3 | 0,299 | +0,0017 | 0,0171 |
| 1,0 | 0,505 | +0,0017 | 0,0171 |
| 3,0 | 0,862 | +0,0017 | 0,0171 |

→ **C1 et C3 ne peuvent jamais passer**, quelle que soit la config. Ce n'est pas un échec de la nature, c'est une identité du modèle.
Et la parité moyenne ≈ 0 de toute façon : la phase totale tourne (ω₀ = 5) et le bruit de N portes s'y additionne.

## 🔌 2. Ta micro-onde ne fait rien

Ton drive est **additif et identique** pour toutes les portes : `+ A_d·sin(ω_d t)`.
C'est un décalage de phase commun : il ne change aucune différence de phase, donc ni R ni la synchronisation.
Mesuré à J = 0,3 : R = **0,2993 avec drive**, **0,2993 sans drive**.
👉 Un drive qui **entraîne** les portes s'écrit `A_d·sin(ω_d t − φ_i)` (Kuramoto forcé / verrouillage par injection) :
là, il dépend de l'état de chaque porte et peut vraiment agir.

## 🔍 3. Ton contrôle d'instrument a été écrit pour passer

Le commentaire dit « phases identiques → parité = 1 », mais le test vérifie `cos(Σφ) == cos(4,0)` = **−0,654**.
Le test compare le code à lui-même, il ne vérifie pas la propriété annoncée.
👉 Un contrôle d'instrument doit tester une **valeur connue d'avance** (ici : φ_i = 0 pour tout i → parité = 1 ; puis la même chose dans le repère tournant).

## 📈 4. C2 (synchronisation) va passer, mais elle ne prouve rien de neuf

R monte bien avec J (0,21 → 0,86) : c'est la transition de Kuramoto, connue depuis 1975.
C'est un très bon **étalon** (le modèle se comporte comme la théorie), pas une découverte.

## ❌ 5. Trois phrases à retirer (R4)

- « Durée de vie GHZ > durée de vie single-qubit × N dans les jobs IBM » : **aucun fichier**, et en général la fidélité
  GHZ décroît **plus vite** quand N augmente.
- « Géométrie réelle des puces IBM = bus central all-to-all » : les puces IBM récentes sont en **heavy-hex**,
  couplage entre **plus proches voisins**. À vérifier avant de l'écrire, jamais l'inverse.
- T-SD « noise_seed = drive_seed » : ton drive n'a aucun aléa, donc ce témoin ne triche sur rien. Il ne mesure rien.

---

## 🎯 Ce que je te demande (v4)

1. **Réponds point par point**, franchement, comme pour la v2.
2. Si tu gardes Kuramoto, trouve une **observable qui dépend vraiment du couplage**
   (par exemple R, une corrélation de phase φ_0 ↔ φ_k, un temps de cohérence d'une **différence** de phase…)
   et explique pourquoi elle aurait un sens « GHZ-like ». Prouve d'abord qu'elle n'est pas **imposée** par le modèle (R8).
3. Si tu veux une micro-onde qui agit, écris-la sous forme d'**entraînement** (sin(ω_d t − φ_i)) et donne le témoin sans couplage avec **le même** drive.
4. **Ou pivote vers nos données réelles** : on a des jobs GHZ archivés. Une question falsifiable et utile pourrait être :
   *« un modèle de phases à N paramètres (ou moins) reproduit-il la décroissance mesurée de nos parités GHZ mieux qu'un
   modèle de décohérence indépendante standard ? »* Ça connecte ta vision à du matériel où l'intrication est réelle.
   Tu proposes, je décide, Arena exécute sur les fichiers existants (rien sur QPU sans mon ordre).
5. Même format : hypothèse en une phrase, mécanisme calculable, code numpy court, **contrôle d'instrument sur valeur connue**,
   témoins à ressources égales, critères (que je scelle), ce qui tue l'hypothèse, limites.

## 📏 La règle du jour, ajoutée au labo grâce à toi

**Avant de sceller un critère, vérifier qu'il n'est pas décidé par une identité du modèle.**
Si une quantité ne dépend pas du paramètre testé, aucun run ne peut trancher : c'est R8 dans sa forme mathématique.

Trois versions, trois pièges trouvés : l'instrument aveugle, le témoin sans filtre, et maintenant l'identité cachée.
C'est comme ça qu'un labo devient solide, frérot. Reviens avec la v4 🔥🧮🛰️🫡

— Jonathan
