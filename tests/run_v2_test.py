"""Test indépendant de la v2 de RATISS : dynamique reprise à l'identique (−γL, injection nœud 0, inertie α, bruit local)."""
import numpy as np
N,T,k=16,200000,4; a,g,sg,sl,Ad,w=0.3,0.4,0.5,1.0,2.0,0.01
A=np.zeros((N,N))
for i in range(N): A[i,(i+1)%N]=A[(i+1)%N,i]=1
L=np.diag(A.sum(1))-A
U=Ad*np.sin(w*np.arange(T))+sg*np.random.RandomState(12345).randn(T)
Xi=sl*np.random.RandomState(54321).randn(T,N)
S=np.zeros((T,N))
for t in range(1,T):
    inj=np.zeros(N); inj[0]=U[t]
    S[t]=(1-a)*S[t-1]+a*(inj-g*(L@S[t-1])+Xi[t])
def mes(sA,sB,seed):  # mesure de RATISS : angle uniforme indépendant par tir
    th=np.random.RandomState(seed).uniform(0,2*np.pi,(2,T))
    return np.corrcoef(np.sign(np.cos(sA-th[0])),np.sign(np.cos(sB-th[1])))[0,1]
xa=sl*np.random.RandomState(1).randn(T); xb=sl*np.random.RandomState(2).randn(T)
PA,PB=U+xa,U+xb
# T-PARTAGE + même filtre passe-bas α (même inertie, sans topologie)
def lp(x):
    y=np.zeros_like(x)
    for t in range(1,T): y[t]=(1-a)*y[t-1]+a*x[t]
    return y
FA,FB=lp(PA),lp(PB)
print("── mesure de RATISS (θ uniforme indépendant) : ρ(X_A,X_B)")
for s in [77777,1,2]: print(f"  graine {s}: SimMat {mes(S[:,0],S[:,k],s):+.4f} | PARTAGE {mes(PA,PB,s):+.4f}")
print("── corrélation des états eux-mêmes (ce que la mesure devrait voir)")
c=lambda x,y: np.corrcoef(x,y)[0,1]
print(f"  SimMat ρ(S0,S{k}) = {c(S[:,0],S[:,k]):.4f}  ρ(S0,S1) = {c(S[:,0],S[:,1]):.4f}")
print(f"  T-PARTAGE brut     = {c(PA,PB):.4f}")
print(f"  T-PARTAGE + filtre α (même inertie, pas de topologie) = {c(FA,FB):.4f}")
