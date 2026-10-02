"""Sceau SHA-256 du dépôt. python3 MANIFESTE.py (écrit) | --verifier (vérifie)."""
import hashlib, json, pathlib, sys
R = pathlib.Path(__file__).parent; M = R / "MANIFESTE.json"
fs = sorted(p for p in R.rglob("*") if p.is_file() and ".git" not in p.parts and p.name != "MANIFESTE.json" and "__pycache__" not in p.parts)
h = {str(p.relative_to(R)): hashlib.sha256(p.read_bytes()).hexdigest() for p in fs}
if "--verifier" in sys.argv:
    old = json.loads(M.read_text())["fichiers"]; bad = [k for k in old if h.get(k) != old[k]]
    print(f"{len(old)-len(bad)} conformes, {len(bad)} problème(s)", *bad, sep="\n"); sys.exit(1 if bad else 0)
M.write_text(json.dumps({"depot": "RATISS-SIMULTANEITE", "algorithme": "sha256", "fichiers": h}, indent=1, ensure_ascii=False)); print(len(h), "fichiers scellés")
