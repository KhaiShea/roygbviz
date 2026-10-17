"""Build the docs.

    python docs/_build/build.py                 # render any new or changed figures, then write every page
    python docs/_build/build.py --force         # re-render every figure
    python docs/_build/build.py --only lines/   # only recipes whose slug starts with this
    python docs/_build/build.py --pages         # skip rendering, just rewrite the pages

Pages live in docs/_src/ and use tokens like {{fig:lines/line-plot}}. Each token becomes the light and dark picture
plus a fold-out with the exact code that drew it. Rendering runs that same code, so the two cannot drift apart.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import pkgutil
import re
import sys
import traceback
import warnings
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
HERE = Path(__file__).resolve().parent
DOCS = HERE.parent
ROOT = DOCS.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "src"))

import matplotlib as mpl  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

import recipes  # noqa: E402
from recipes import REGISTRY, Recipe  # noqa: E402

MODES = ("light", "dark", "cream")  # light is white; the pages show light and dark and link the cream version
IMG = DOCS / "img"
CACHE = IMG / ".cache.json"
DPI = 160
TOKEN = re.compile(r"\{\{fig:([A-Za-z0-9_/\-]+)((?:\|[a-z]+(?:=[0-9]+)?)*)\}\}")


def load_recipes() -> None:
    pkg = importlib.import_module("recipes")
    for m in pkgutil.iter_modules(pkg.__path__):
        if m.name.startswith("r_"):
            importlib.import_module(f"recipes.{m.name}")


def source_hash() -> str:
    h = hashlib.sha1()
    for p in sorted((ROOT / "src" / "roygbviz").glob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def img_path(slug: str, mode: str, kind: str) -> Path:
    return IMG / f"{slug}_{mode}.{'gif' if kind == 'anim' else 'png'}"


def render(r: Recipe, mode: str) -> Path:
    import roygbviz as rv  # imported late so src/ is on the path

    mpl.rcdefaults()
    plt.close("all")
    code = r.runnable.replace('rv.use("light")', f'rv.use("{mode}")')
    ns: dict = {"__name__": "__docs__"}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exec(compile(code, f"<{r.slug}>", "exec"), ns)
        obj = ns[r.var] if r.var in ns else eval(r.var, ns)
        out = img_path(r.slug, mode, r.kind)
        out.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(obj, "savefig"):
            obj.savefig(out, dpi=DPI)
        elif r.kind == "gg":
            obj.save(out, dpi=DPI, verbose=False)
        elif r.kind == "anim":
            obj.save(out, writer="pillow", fps=20, dpi=80)
        else:
            obj.savefig(out, dpi=DPI)
    plt.close("all")
    return out


def render_all(only: str | None, force: bool) -> list[str]:
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    sh = source_hash()
    failed: list[str] = []
    todo = [r for r in REGISTRY.values() if (not only or r.slug.startswith(only))]
    for n, r in enumerate(todo, 1):
        for mode in MODES if r.dark else ("light",):
            key = f"{r.slug}|{mode}"
            digest = hashlib.sha1((r.runnable + sh + str(DPI)).encode()).hexdigest()
            if not force and cache.get(key) == digest and img_path(r.slug, mode, r.kind).exists():
                continue
            try:
                render(r, mode)
                cache[key] = digest
                print(f"[{n}/{len(todo)}] {r.slug} {mode}")
            except Exception:  # noqa: BLE001
                failed.append(f"{r.slug} ({mode})")
                print(f"FAILED {r.slug} {mode}\n{traceback.format_exc(limit=3)}")
    IMG.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=0, sort_keys=True))
    return failed


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def block(r: Recipe, opts: str, page: Path) -> str:
    rel = lambda mode: os.path.relpath(img_path(r.slug, mode, r.kind), page.parent).replace(os.sep, "/")
    width = 640
    for o in opts.split("|"):
        if o.startswith("width="):
            width = int(o.split("=")[1])
    if r.kind == "anim" or not r.dark:
        pic = f'<img src="{rel("light")}" alt="{esc(r.caption)}" width="{width}">'
    else:
        # GitHub-only fragments follow GitHub's own theme (a <picture> follows the browser or OS instead).
        # docs/stylesheets/extra.css makes the same two images switch with the MkDocs theme toggle.
        pic = (f'<img src="{rel("light")}#gh-light-mode-only" alt="{esc(r.caption)}" width="{width}">\n'
               f'<img src="{rel("dark")}#gh-dark-mode-only" alt="{esc(r.caption)}" width="{width}">')
    out = f'<p align="center">\n{pic}\n</p>\n'
    if r.kind != "anim" and r.dark:
        out += f'\n<p align="center"><sub>Also in <a href="{rel("cream")}">cream</a></sub></p>\n'
    if "nocode" not in opts.split("|"):
        out += (f'\n<details markdown="1">\n<summary>Show the code</summary>\n\n```python\n{r.shown}\n```\n\n</details>\n')
    return out


def build_pages() -> list[str]:
    problems: list[str] = []
    src = DOCS / "_src"
    for md in sorted(src.rglob("*.md")):
        target = DOCS / md.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        text = md.read_text()

        def sub(m: re.Match) -> str:
            slug = m.group(1)
            if slug not in REGISTRY:
                problems.append(f"{md.relative_to(src)}: unknown figure {slug}")
                return f"**MISSING FIGURE {slug}**"
            return block(REGISTRY[slug], m.group(2), target)

        target.write_text(TOKEN.sub(sub, text))
    used = set()
    for md in src.rglob("*.md"):
        used |= {m.group(1) for m in TOKEN.finditer(md.read_text())}
    unused = sorted(set(REGISTRY) - used)
    if unused:
        problems.append(f"{len(unused)} recipes not used in any page yet" + (": " + ", ".join(unused) if len(unused) < 8 else ""))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pages", action="store_true", help="skip rendering")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    load_recipes()
    if a.list:
        for s in sorted(REGISTRY):
            print(s)
        return 0
    failed = [] if a.pages else render_all(a.only, a.force)
    problems = build_pages()
    print(f"\n{len(REGISTRY)} recipes, {len(failed)} failed")
    for f in failed:
        print("  failed:", f)
    for p in problems:
        print("  note:", p)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
