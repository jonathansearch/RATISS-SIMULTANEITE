#!/usr/bin/env python3
"""Run de mesure v1 — exécute PROTOCOLE-SCELLE-v1.md à la lettre. MIT.
Usage : python3 mesure_v1.py  → mesure_v1.json (par graine + verdict)"""
import numpy as np, json, time, sys
sys.path.insert(0, __import__('pathlib').Path(__file__).parent.as_posix())
from simmat_v3_opt import Rd_of, check_instrument
SEEDS = list(range(100, 120)); T, DT, W0, WD, SX, SO = 40000, 0.01, 5.0, 5.0, 0.8, 0.5

def sim(N, J, A):
    S = len(SEEDS)
    om = np.stack([W0 + SO*np.random.default_rng(10_000+s).standard_normal(N) for s in SEEDS])
    phi = np.stack([np.random.default_rng(20_000+s).uniform(-np.pi, np.pi, N) for s in SEEDS])
    nz = np.stack([np.random.default_rng(30_000+s).standard_normal((T, N)) for s in SEEDS])
    m = T//2; h = (T-m)//2; Rd = np.zeros(S); Z1 = np.zeros(S, complex); Z2 = np.zeros(S, complex)
    for t in range(T):
        tt = t*DT
        cpl = np.sin(np.roll(phi, 1, 1)-phi) + np.sin(np.roll(phi, -1, 1)-phi)
        phi = phi + (om + A*np.sin(WD*tt-phi) + J*cpl)*DT + SX*np.sqrt(DT)*nz[:, t, :]
        if t >= m:
            rel = phi - WD*(tt+DT); Rd += Rd_of(rel); z = np.exp(1j*rel.sum(1))
            if t < m+h: Z1 += z
            else: Z2 += z
    n = T-m
    return dict(Rd=(Rd/n).tolist(), Pgl=np.abs((Z1+Z2)/n).tolist(), PglA=np.abs(Z1/h).tolist(), PglB=np.abs(Z2/(n-h)).tolist())

def sig(x):
    x = np.asarray(x); se = x.std(ddof=1)/np.sqrt(len(x)); return float(x.mean()), float(se), float(x.mean()/se) if se > 0 else float('inf')

if __name__ == "__main__":
    print("instrument:", check_instrument()); t0 = time.time()
    out = {"protocole": "PROTOCOLE-SCELLE-v1.md", "numpy": np.__version__, "graines": SEEDS, "T": T, "dt": DT, "cellules": {}, "verdict": {}}
    plancher = 3*np.sqrt(np.pi/(4*(T//2)))
    for N in (8, 16):
        C = {(J, A): sim(N, J, A) for J in (0.0, 1.0) for A in (0.0, 0.5)}
        for k, v in C.items(): out["cellules"][f"N{N}_J{k[0]}_A{k[1]}"] = v
        P = lambda J, A, q='Pgl': np.array(C[J, A][q])
        c = P(1.0, .5) - P(0.0, .5)
        mat = P(1.0, .5, 'PglB') - P(1.0, .5, 'PglA')
        R = lambda J, A: np.array(C[J, A]['Rd'])
        syn = (R(1.0, .5)-R(1.0, 0)) - (R(0.0, .5)-R(0.0, 0))
        ident = float(np.max(np.abs(P(1.0, 0) - P(0.0, 0))))
        cm, cse, cz = sig(c); mm, mse, mz = sig(mat); sm, sse, sz = sig(syn)
        g = float(P(1.0, .5).mean())
        mur = abs(mz) <= 2
        v = {"identite_A0_ecart_max": ident, "effet_couplage_Pgl": [cm, cse, cz], "Pgl_A05_J1": g, "garde_plancher": float(plancher),
             "maturite_B_moins_A": [mm, mse, mz], "mesure_mure": bool(mur), "synergie_Rd": [sm, sse, sz],
             "C_principal": ("non lu (mesure non mûre)" if not mur else ("PASSE" if (cz > 5 and g > plancher) else "ÉCHOUE")),
             "C_secondaire": "PASSE" if sz > 5 else "ÉCHOUE"}
        out["verdict"][f"N{N}"] = v
        print(f"N={N}: couplage→Pgl {cm:+.4f}±{cse:.4f} ({cz:.1f}σ) | Pgl={g:.4f} (garde {plancher:.4f}) | maturité {mz:+.1f}σ | synergie Rd {sm:+.4f} ({sz:.1f}σ) | identité {ident:.1e} → {v['C_principal']} / {v['C_secondaire']}", flush=True)
    out["secondes"] = round(time.time()-t0, 1)
    json.dump(out, open("mesure_v1.json", "w"), indent=1); print("durée", out["secondes"], "s")
