"""Juge CHSH — 3 témoins, numpy seul, déterministe (graine 42). MIT.
T-Q   : état singulet calculé exactement (mécanique quantique)       -> attendu 2√2
T-VCL : variables cachées locales + choix INDÉPENDANTS de λ            -> attendu ≤ 2
T-SD  : même VCL, mais choix de mesure tirés de la MÊME graine que λ   -> le « superdéterminisme algorithmique »"""
import numpy as np
N = 200_000
A = [0.0, np.pi/2]; B = [np.pi/4, -np.pi/4]          # réglages optimaux (en angle de spin)

def S_from(Eab): return Eab[0][0] + Eab[0][1] + Eab[1][0] - Eab[1][1]

# T-Q : singulet exact, E(a,b) = -cos(a-b) ; on échantillonne vraiment les issues
def tq(rng):
    E = [[0,0],[0,0]]
    for i,a in enumerate(A):
        for j,b in enumerate(B):
            p_eq = (1 - np.cos(a-b))/2                 # proba que les deux issues soient égales
            eq = rng.random(N) < p_eq
            E[i][j] = (2*eq.mean() - 1)
    return -S_from(E)                                   # convention signe singulet

# T-VCL : λ = angle caché partagé ; A=sign(cos(λ-a)), B=-sign(cos(λ-b)) ; choix indépendants
def tvcl(rng):
    lam = rng.uniform(0, 2*np.pi, N); ia = rng.integers(0,2,N); ib = rng.integers(0,2,N)
    a = np.array(A)[ia]; b = np.array(B)[ib]
    x = np.sign(np.cos(lam-a)); y = -np.sign(np.cos(lam-b))
    E = [[(x*y)[(ia==i)&(ib==j)].mean() for j in (0,1)] for i in (0,1)]
    return -S_from(E)

# T-SD : les choix (ia, ib) sont CALCULÉS à partir de λ (cause commune = la graine)
def tsd(rng):
    lam = rng.uniform(0, 2*np.pi, N)
    x0 = np.sign(np.cos(lam)); 
    # pour chaque λ, le script « choisit » les réglages qui donnent la corrélation voulue
    ia = rng.integers(0,2,N); ib = rng.integers(0,2,N)
    target = np.where((ia==1)&(ib==1), 1, -1)          # ce qu'il faut pour maximiser -S
    x = x0; y = target * x                               # B est fabriqué pour coller au « bon » signe
    E = [[(x*y)[(ia==i)&(ib==j)].mean() for j in (0,1)] for i in (0,1)]
    return -S_from(E)

rng = np.random.default_rng(42)
r = {'T-Q singulet exact': tq(rng), 'T-VCL choix indépendants': tvcl(rng), 'T-SD choix liés à la graine': tsd(rng)}
for k,v in r.items(): print(f"{k:30s} S = {v:.4f}")
