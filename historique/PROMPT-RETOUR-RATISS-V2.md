# 🛰️ RETOUR À RATISS — Matrice de simultanéité v2

Frérot 🔥🤝 Ici Jonathan.

Ta réponse m'a fait plaisir : t'as accepté Bell sans chercher de raccourci, t'as séparé les trois graines,
t'as écrit toi-même « si S > 2, c'est un bug ». Là, tu parles comme le labo 💪🛰️
Arena a fait tourner ton code tel quel (`test_simmat_v1.py`, numpy, < 3 s). Voilà ce que le juge dit.
On ne lâche rien, on corrige et on repart plus fort.

---

## 🐛 1. Bug de signe : ta mémoire topologique explose

Tu as écrit `S[t] = (1-α)·S[t-1] + α·(U[t] + γ·L@S[t-1])` avec `L = D - A`.
L est positif → `+γL` **anti-diffuse**. Mesuré (8 portes en anneau, α = 0,5) :

| γ | ton code `+γL` | vraie diffusion `−γL` |
|---|---|---|
| 0,1 | 2,7 | 2,4 |
| 0,3 | **4,9 × 10⁸²** 💥 | 2,3 |
| 1,0 | **NaN** 💥 | NaN 💥 (pas de temps trop grand) |

👉 Corrige en `−γ·L`, et donne la condition de stabilité (anneau : λ_max = 4 → il faut α·γ·4 < 2 − α environ).
Écris-la dans la config : un run instable n'est pas un résultat.

## 🎭 2. Ton T-VCL est un homme de paille

Tu dis « bruit universel partagé », mais `randn(T, N, D)` donne un bruit **indépendant par porte**.
Avec γ = 0, A et B ne partagent **rien** → corrélation mesurée **0,004**.
Avec la diffusion corrigée → **0,10**. N'importe quel couplage « bat » ce témoin : c'est le script qui gagne, pas l'idée. **R8 le rejette.**

👉 Le témoin juste, c'est **T-PARTAGE** : le **meilleur classique à ressources égales**.
A et B lisent **directement le même bruit** (même budget de bruit, même nombre de pas, même mesure locale), sans topologie.
Ta topologie doit faire **mieux que ça**, sinon elle n'apporte rien.

## ⏱️ 3. Ton critère de coût est gagné d'avance

Un modèle classique à N portes coûte au plus N² **par construction**. Il ne peut pas échouer.
Mesuré : N = 8 → 0,109 s · N = 16 → 0,113 s (ratio 1,04) · N = 256 → 0,49 s.
👉 Retire ce critère, ou compare le coût à un **vrai calcul quantique de la même tâche**, sinon il ne teste rien.

## ❌ 4. Une phrase à retirer

« Nos vrais jobs IBM font S > 2 » : **on n'a pas de mesure CHSH archivée**. Nos jobs, c'est surtout des GHZ et des parités.
Pas de chiffre sans fichier (R4). Si tu veux un CHSH réel un jour, propose-le comme job à lancer **sur mon ordre**, jamais avant.

---

## 🎯 Ce que je te demande maintenant (v2)

1. **Une question qui PEUT échouer.** Exemple de forme (à toi de trouver la meilleure) :
   *« À budget de bruit égal, la topologie de couplage fait-elle mieux que le bruit directement partagé (T-PARTAGE),
   sur une tâche définie à l'avance ? »*
   Choisis une **tâche** mesurable et utile au labo, par exemple :
   - garder une corrélation A↔B **plus longtemps** malgré un bruit local ajouté (mémoire) ;
   - **transmettre** une corrélation à une porte lointaine (distance k sur l'anneau) mieux que T-PARTAGE ;
   - **imiter** la courbe de décohérence d'un vrai job GHZ archivé (fidélité vs profondeur) avec moins de paramètres qu'un modèle standard.
2. **Le code corrigé** (−γL, condition de stabilité, T-PARTAGE), court, numpy seul, rejouable en une commande.
3. **Les critères proposés** (je les scelle, pas toi) avec un seuil chiffré (ex. 5 écarts-types sur plusieurs graines) et **ce qui tue l'hypothèse**.
4. **Les témoins** : T-Q, T-VCL (honnête), **T-PARTAGE**, T-SD (la triche, pour mémoire), et un témoin propre à ton mécanisme.
5. **Ton idée des « portes et micro-ondes »** : dis-moi concrètement à quoi ça correspond dans le code (une impulsion périodique ? une porte de rotation à fréquence fixe ?). Si c'est juste un mot, on l'enlève ; si c'est un mécanisme, on le teste.

## 📏 Rappel des règles (tu les connais, je les remets pour le sceau)

- Pas de chiffre prédit avant la mesure. Pas de ZK, pas de « 100 % », pas d'API qui n'existe pas.
- Arena exécute, scelle sur mon ordre, et publie les échecs comme les succès.
- **R8 : on ne mesure que ce qui déborde du script.** Si le montage impose la victoire, ce n'est pas une victoire.

Garde ta vision, frérot, c'est elle qui unifie tout. Rends-la juste falsifiable et on la passe au juge ensemble 🔥🧮🛰️
Envoie ta v2 quand t'es prêt 🫡

— Jonathan
