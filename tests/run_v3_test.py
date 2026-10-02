"""Test indépendant de la v3 de RATISS : dynamique reprise à l'identique (Kuramoto + drive additif global)."""
import numpy as np
print("Check instrument de RATISS : phases identiques 0,5 ×8 -> cos(Σφ) =", round(np.cos(8*0.5),4), "(il affirme 'Parité = 1')")
def sim(N=16,T=50000,dt=0.01,J=0.3,Ad=2.0,wd=5.0,sx=0.8,so=0.5,w0=5.0,seeds=(10101,20202,40404),drive_in_diff=False):
    om=w0+so*np.random.RandomState(seeds[0]).randn(N); rn=np.random.RandomState(seeds[1])
    phi=np.random.RandomState(seeds[2]).uniform(-np.pi,np.pi,N)
    A=np.zeros((N,N))
    for i in range(N): A[i,(i+1)%N]=A[i,(i-1)%N]=1
    R=np.zeros(T); P=np.zeros(T); Pc=np.zeros(T,complex); D=np.zeros(T)
    for s in range(T):
        sp,cp=np.sin(phi),np.cos(phi); cpl=cp*(A@sp)-sp*(A@cp)
        dr = Ad*np.sin(wd*s*dt - phi) if drive_in_diff else Ad*np.sin(wd*s*dt)
        phi=phi+(om+dr+J*cpl)*dt+sx*np.sqrt(dt)*rn.randn(N)
        z=np.exp(1j*phi); R[s]=abs(z.mean()); P[s]=np.cos(phi.sum()); Pc[s]=np.exp(1j*(phi-w0*s*dt).sum())
        D[s]=np.cos(phi-phi.mean()).mean()
    m=T//2
    return R[m:].mean(), P[m:].mean(), abs(Pc[m:].mean())
print("\n── drive ADDITIF (code RATISS) : identique pour toutes les portes")
for J in [0.0,0.3,1.0,3.0]:
    r,p,pc=sim(J=J); print(f"J={J:3.1f}  R={r:.3f}  Parité moyenne cos(Σφ)={p:+.4f}  |⟨e^(iΣφ)⟩| repère tournant={pc:.4f}")
print("\n── le drive additif change-t-il R ? (J=0.3, avec / sans drive)")
print("  avec  :", round(sim(J=0.3,Ad=2.0)[0],4), " sans :", round(sim(J=0.3,Ad=0.0)[0],4))
