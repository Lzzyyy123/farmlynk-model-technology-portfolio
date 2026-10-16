"""Validate the public portfolio without inspecting private source locations."""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
EXPECTED_DOCS = [f"{n:02d}-{name}.md" for n, name in [
    (1, "executive-review"), (2, "repository-landscape"), (3, "asset-portfolio"),
    (4, "product-integration"), (5, "remote-sensing"), (6, "land-assessment"),
    (7, "agent-and-knowledge"), (8, "recognition"), (9, "research-results"),
    (10, "intellectual-property"), (11, "topics-and-roadmap"),
    (12, "data-and-evaluation"), (13, "figure-atlas"), (14, "evidence-register"),
    (15, "maintenance"),
]]
VISUALS = [
    "01-platform-landscape.png", "02-remote-sensing.png", "03-agent.png",
    "04-recognition.png", "05-land-assessment.png", "06-research-to-product.png",
    "07-ip-and-roadmap.png",
]
SVG_VISUALS = [name.replace(".png", ".svg") for name in VISUALS]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> None:
    errors: list[str] = []
    for path in [BASE / "README.md", *[BASE / "docs" / n for n in EXPECTED_DOCS]]:
        if not path.exists():
            fail(f"missing:{path.relative_to(BASE)}", errors)
    for name in VISUALS:
        if not (BASE / "assets" / "visuals" / name).exists():
            fail(f"missing:assets/visuals/{name}", errors)
    for name in SVG_VISUALS:
        if not (BASE / "assets" / "visuals" / name).exists():
            fail(f"missing:assets/visuals/{name}", errors)
    for name in ["fieldbcq-metrics.csv", "fieldbcq-dataset-split.csv"]:
        if not (BASE / "data" / name).exists():
            fail(f"missing:data/{name}", errors)
    for name in ["技术资产与研发路线 V2.0.md", "技术资产与研发路线 V2.0.docx", "技术资产与研发路线 V2.0.pdf"]:
        if not (BASE / "deliverables" / name).exists():
            fail(f"missing:deliverables/{name}", errors)

    def load(name):
        try:
            return json.loads((BASE / "data" / name).read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"invalid:data/{name}:{exc}", errors)
            return []

    areas = load("technology-areas.json")
    topics = load("topics.json")
    ip = load("intellectual-property.json")
    inventory = load("model-inventory.json")
    sources = load("external-sources.json")
    figures = load("figures.json")
    if len(areas) != 10: fail(f"technology-areas-count:{len(areas)}", errors)
    if len(topics) != 17: fail(f"topics-count:{len(topics)}", errors)
    if len(ip) != 11: fail(f"ip-count:{len(ip)}", errors)
    if len(inventory) != 15: fail(f"model-inventory-count:{len(inventory)}", errors)
    if len(sources) != 3: fail(f"sources-count:{len(sources)}", errors)
    if len(figures) != 7: fail(f"figures-count:{len(figures)}", errors)

    forbidden_fragments = [
        "~" + "/work", "/" + "Users" + "/", "gitlab." + "lpkhbj.com", "origin/" + "master",
        "models/" + "rice", "j" + "ing_men", "荆" + "门", "RICE" + "-",
        "Open" + "CropModel", "crop" + " " + "model", "code-" + "sources",
        "repositories." + "json", "source-documents." + "json", "api/" + "ocm",
    ]
    scan_roots = [BASE / "README.md", BASE / "docs", BASE / "data", BASE / "deliverables"]
    for root in scan_roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix.lower() in {".png", ".pdf", ".docx"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for fragment in forbidden_fragments:
                if fragment.lower() in text.lower():
                    fail(f"forbidden:{fragment}:{path.relative_to(BASE)}", errors)
    for path in [BASE / "README.md", *[BASE / "docs" / n for n in EXPECTED_DOCS]]:
        if not path.exists():
            continue
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                fail(f"broken-link:{path.relative_to(BASE)}:{target}", errors)
    report = {
        "passed": not errors,
        "scope": "public portfolio consistency check",
        "counts": {"technology_areas": len(areas), "topics": len(topics), "ip": len(ip), "model_inventory": len(inventory), "sources": len(sources), "visuals": len(figures)},
        "errors": errors,
    }
    (BASE / "data" / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
