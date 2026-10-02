#!/usr/bin/env python3
"""RATISS Labs — Matrice de simultanéité v3 optimisée (idée : RATISS ; implémentation : Arena). MIT.

Vision gardée : drive micro-onde GLOBAL (bus commun) + bruit LOCAL par porte + couplage en ANNEAU
→ le couplage protège-t-il la cohérence collective contre le bruit local ?

Corrections par rapport à la v3 d'origine :
  1. drive qui ENTRAÎNE chaque porte : A·sin(ω_d t − φ_i)   (avant : additif commun, sans effet)
  2. observables qui dépendent du couplage, mesurées dans le repère du drive :
       Rd   = |⟨e^{i(φ_i − ω_d t)}⟩_i|        verrouillage collectif sur le bus (instantané, moyenné en temps)
       Pgl  = |⟨e^{iΣ_i(φ_i − ω_d t)}⟩_t|     « parité » GHZ-like : cohérence de la phase TOTALE dans le temps
  3. contrôle d'instrument sur valeurs CONNUES d'avance (pas le code comparé à lui-même)
  4. vectorisé : toutes les graines en parallèle, couplage anneau en O(N) par np.roll
Usage : python3 simmat_v3_opt.py            (scan complet, ~1 min)
"""
import numpy as np, json, hashlib, time

# ── 0. Contrôle d'instrument : valeurs connues ────────────────────────────────
def Rd_of(phi_rel):                     # phi_rel : (..., N)
    return np.abs(np.exp(1j * phi_rel).mean(-1))
def check_instrument():
    N = 16
    assert abs(Rd_of(np.zeros(N)) - 1) < 1e-12                       # phases identiques → 1
    k = np.arange(N); assert Rd_of(2*np.pi*k/N) < 1e-12              # phases étalées régulièrement → 0
    tot = np.zeros(1000)                                              # phase totale figée → Pgl = 1
    assert abs(abs(np.exp(1j*tot).mean()) - 1) < 1e-12
    tot = np.random.default_rng(0).uniform(-np.pi, np.pi, 100000)     # phase totale aléatoire → Pgl ≈ 0
    assert abs(np.exp(1j*tot).mean()) < 0.01
    # identité Kuramoto : le couplage seul ne change pas Σφ
    phi = np.random.default_rng(1).uniform(-np.pi, np.pi, N)
    c = np.sin(np.roll(phi, 1) - phi) + np.sin(np.roll(phi, -1) - phi)
    assert abs(c.sum()) < 1e-12
    return "OK"

# ── 1. Moteur vectorisé ───────────────────────────────────────────────────────
def simulate(N, J, A, sx, so, seeds, T=20000, dt=0.01, w0=5.0, wd=5.0):
    S = len(seeds)
    om = np.stack([w0 + so*np.random.default_rng(10_000+s).standard_normal(N) for s in seeds])   # désordre figé
    phi = np.stack([np.random.default_rng(20_000+s).uniform(-np.pi, np.pi, N) for s in seeds])   # état initial
    rn = [np.random.default_rng(30_000+s) for s in seeds]                                         # bruit local
    m = T // 2; Rd = np.zeros(S); Z = np.zeros(S, complex)
    for t in range(T):
        tt = t*dt
        cpl = np.sin(np.roll(phi, 1, 1) - phi) + np.sin(np.roll(phi, -1, 1) - phi)   # anneau, O(N)
        drv = A*np.sin(wd*tt - phi)                                                   # entraînement par le bus
        noise = np.stack([r.standard_normal(N) for r in rn])
        phi = phi + (om + drv + J*cpl)*dt + sx*np.sqrt(dt)*noise
        if t >= m:
            rel = phi - wd*(tt+dt)
            Rd += Rd_of(rel); Z += np.exp(1j*rel.sum(1))
    n = T - m
    return Rd/n, np.abs(Z/n)            # par graine

def stats(x): return float(np.mean(x)), float(np.std(x, ddof=1)/np.sqrt(len(x)))

if __name__ == "__main__":
    print("Contrôle d'instrument :", check_instrument())
    cfg = dict(T=20000, dt=0.01, w0=5.0, wd=5.0, A=0.5, sx=0.8, so=0.5, seeds=list(range(10)))
    print("config :", cfg, "| sha256 =", hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:16])
    out = {"config": cfg, "scan": []}
    t0 = time.time()
    for N in (4, 8, 16):
        for J in (0.0, 0.3, 1.0, 3.0):
            for A in (0.0, cfg["A"]):
                rd, pg = simulate(N, J, A, cfg["sx"], cfg["so"], cfg["seeds"], cfg["T"], cfg["dt"], cfg["w0"], cfg["wd"])
                (rm, re), (pm, pe) = stats(rd), stats(pg)
                out["scan"].append(dict(N=N, J=J, A=A, Rd=rm, Rd_err=re, Pgl=pm, Pgl_err=pe))
                print(f"N={N:2d} J={J:3.1f} drive={A:3.1f} | Rd={rm:.3f}±{re:.3f} | Pgl={pm:.3f}±{pe:.3f}", flush=True)
    out["secondes"] = round(time.time()-t0, 1)
    json.dump(out, open("resultats_v3_opt.json", "w"), indent=1)
    print("durée", out["secondes"], "s → resultats_v3_opt.json")
