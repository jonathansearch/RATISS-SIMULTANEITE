# RÉSULTATS v1 — run de mesure scellé (02/10/2026)

Protocole : `PROTOCOLE-SCELLE-v1.md` · sceau `SCEAU-v1.sha256` (commit `0bfef7f`, public avant le run).
Graines fraîches 100–119, T = 40 000, dt = 0,01, tests appariés par graine. Données : `mesure_v1.json`. Durée : 15,6 s.

| | effet du couplage sur Pgl | Pgl (A=0,5 ; J=1) | maturité (B−A) | synergie Rd | identité A=0 | **Principal** | **Secondaire** |
|---|---|---|---|---|---|---|---|
| N=8 | +0,0072 ± 0,0100 (0,7σ) | 0,0654 | −3,1σ | −0,0112 (−0,4σ) | 1,0e−10 | **non lu** (mesure non mûre) | **ÉCHOUE** |
| N=16 | +0,0091 ± 0,0076 (1,2σ) | 0,0384 | −0,6σ | +0,1287 (8,0σ) | 6,8e−11 | **ÉCHOUE** | **PASSE** |

## Verdict à la lettre
- **L'effet du couplage sur la parité ne survit pas à N=16** (1,2σ < 5σ). À N=8, la mesure n'est pas mûre (Pgl encore en dérive sur la fenêtre doublée) : non lue, comme prévu au protocole.
- **La synergie couplage + drive sur le verrouillage (Rd) est confirmée à N=16 sur graines fraîches : 8,0σ.** Elle n'apparaît pas à N=8 (−0,4σ).
- Les témoins tiennent : identité de Kuramoto à ≤ 1e−10, contrôle d'instrument OK.

## Lecture
- La « parité » GHZ-like ne profite pas du couplage au-delà de petites tailles : cohérent avec la borne 0,474^N (GLM) et la non-stationnarité.
- Le phénomène robuste de ce modèle est le **verrouillage collectif sur un bus commun** à N=16. C'est une physique classique connue (Kuramoto forcé) : un outil, pas une découverte, et pas d'intrication.
- Non prévu : l'absence de synergie à N=8. Hypothèse à tester (pas un résultat) : régime de couplage différent selon N à J fixé.
