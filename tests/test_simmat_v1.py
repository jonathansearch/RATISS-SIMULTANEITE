"""Test du montage proposé par RATISS (v1), code repris tel quel pour la dynamique."""
import numpy as np, time
def ring(N): A=np.zeros((N,N)); [A.__setitem__((i,(i+1)%N),1) or A.__setitem__(((i+1)%N,i),1) for i in range(N)]; return A
def run(N,T,alpha,gamma,sigma=1.0,D=3,sign=+1):
    A=ring(N); L=np.diag(A.sum(1))-A
    U=np.random.RandomState(1).randn(T,N,D)*sigma; S=np.zeros((T,N,D)); S[0]=np.random.RandomState(2).randn(N,D)
    t0=time.perf_counter()
    for t in range(1,T): S[t]=(1-alpha)*S[t-1]+alpha*(U[t]+sign*gamma*(L@S[t-1]))
    return S, time.perf_counter()-t0
# 1) stabilité du signe +γL (le code proposé) vs −γL (diffusion vraie)
for g in [0.1,0.3,1.0]:
    S,_=run(8,2000,0.5,g); S2,_=run(8,2000,0.5,g,sign=-1)
    print(f"γ={g}: +γL max|S|={np.abs(S).max():.3g} | −γL max|S|={np.abs(S2).max():.3g}")
# 2) T-VCL tel que défini (γ=0, α=1) : U indépendant par porte -> corrélation A-B ?
S,_=run(2,100000,1.0,0.0); print("T-VCL corr(S_A,S_B) =",round(np.corrcoef(S[:,0,0],S[:,1,0])[0,1],4))
S,_=run(2,100000,0.5,-0.2,sign=+1); print("SimMat (diffusion vraie) corr =",round(np.corrcoef(S[:,0,0],S[:,1,0])[0,1],4))
# 3) coût : ratio N=16/N=8
for N in [2,8,16,64,256]:
    _,t=run(N,20000,0.5,0.1,sign=-1); print(f"N={N:4d} temps={t:.3f}s")
