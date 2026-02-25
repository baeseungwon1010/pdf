const f = document.getElementById("file");
const o = document.getElementById("out");
const btn = document.getElementById("btn");
const flagBtn = document.getElementById("flagBtn");

const show = (x) =>
  (o.textContent = typeof x === "string" ? x : JSON.stringify(x, null, 2));

btn.onclick = async () => {
  if (!f.files[0]) return show("Select a PDF first.");
  const fd = new FormData();
  fd.append("file", f.files[0]);

  const r = await fetch("/upload", { method: "POST", body: fd });
  const j = await r.json().catch(() => ({}));
  show(j);

  if (j.saved_as) {
    const p = await fetch(`/process/${j.saved_as}`, { method: "POST" });
    show((o.textContent || "") + "\n\n" + (await p.text()));
  }
};

flagBtn.onclick = async () => {
  const r = await fetch("/flag");
  const j = await r.json().catch(() => ({}));
  show(j);
};
