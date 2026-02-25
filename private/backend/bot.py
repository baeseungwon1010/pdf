import fitz, subprocess, sys, json
from pathlib import Path

pdf = Path(sys.argv[1]).resolve()
out = Path(__file__).parent / "extracted" / pdf.stem
out.mkdir(parents=True, exist_ok=True)

doc = fitz.open(str(pdf))
names = doc.embfile_names()
doc.close()

res = []
for i, n in enumerate(names):
    o = out / f"file_{i}"
    p = subprocess.run(
        [sys.executable, "-m", "pymupdf", "embed-extract",
         str(pdf), "-name", n],
        capture_output=True,
        text=True
    )
    res.append({"name": n, "ok": p.returncode == 0, "out": str(o), "stderr": p.stderr})

print(json.dumps({
    "pdf": str(pdf),
    "count": len(names),
    "names": names,
    "results": res
}, ensure_ascii=False))
