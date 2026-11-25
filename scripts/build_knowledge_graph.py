#!/usr/bin/env python3
"""Generate the public knowledge graph from data/*.yaml.

The YAML files under data/ remain the single source of truth for the website
and CV. This script derives data/knowledge-graph/entities.json and
relations.json from them, so the graph can never drift from the content it
describes. Re-run it after editing any data/*.yaml file:

    python3 scripts/build_knowledge_graph.py

Hand-authored facts that aren't in data/*.yaml (style decisions, known
conflicts between sources, skill keyword -> paper links) live in
data/knowledge-graph/constraints.json, which this script does not touch.

Schema (see data/knowledge-graph/README.md for the full write-up):
  entity:  {id, type, name, properties: {...}, source}
  relation: {id, type, source, target, properties: {...}}
"""
import json
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "data" / "knowledge-graph"
OUT.mkdir(parents=True, exist_ok=True)

entities = []
relations = []
_rel_i = 0


def slugify(text):
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return re.sub(r"-{2,}", "-", text)


def add_entity(id_, type_, name, properties=None, source=None):
    entities.append({
        "id": id_,
        "type": type_,
        "name": name,
        "properties": properties or {},
        "source": source,
    })
    return id_


def add_relation(type_, source, target, properties=None):
    global _rel_i
    _rel_i += 1
    relations.append({
        "id": f"rel-{_rel_i:04d}",
        "type": type_,
        "source": source,
        "target": target,
        "properties": properties or {},
    })


def load(name):
    with open(DATA / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


PERSON = "person:ali-hashemi"
add_entity(PERSON, "Person", "Ali Hashemi", {
    "role_title": "Senior LLM Researcher · Tech Lead, Model Evaluation",
    "affiliation": "LLM Research Staff, Multiverse Computing",
    "location": "Berlin, Germany",
    "email": "alihashemi.ee@gmail.com",
    "links": {
        "website": "https://alihashemi-ai.github.io/",
        "github": "https://github.com/alihashemi-ai",
        "linkedin": "https://www.linkedin.com/in/alihashemi-ai/",
        "x": "https://x.com/alihashemi_ai",
        "scholar": "https://scholar.google.com/citations?user=rCcFTFgAAAAJ",
        "orcid": "https://orcid.org/0000-0003-4957-4630",
        "huggingface": "https://huggingface.co/ali-hashemi",
    },
}, source="hugo.toml, content/_index.md")

# ---------------- Organizations + Roles (data/experience.yaml) ----------------
_org_ids = {}


def org_id(name):
    if name not in _org_ids:
        oid = f"org:{slugify(name)}"
        add_entity(oid, "Organization", name, source="data/experience.yaml")
        _org_ids[name] = oid
    return _org_ids[name]


for i, exp in enumerate(load("experience")):
    rid = f"role:{slugify(exp['org'])}-{slugify(exp['role'])}"
    add_entity(rid, "Role", exp["role"], {
        "org": exp["org"],
        "location": exp.get("location"),
        "start": exp.get("start"),
        "end": exp.get("end"),
        "current": exp.get("current", False),
    }, source="data/experience.yaml")
    add_relation("held_role", PERSON, rid, {"start": exp.get("start"), "end": exp.get("end")})
    add_relation("at_org", rid, org_id(exp["org"]))

    for j, bullet in enumerate(exp.get("bullets", [])):
        aid = f"achievement:{slugify(exp['org'])}-{slugify(exp['role'])}-{j}"
        add_entity(aid, "Achievement", bullet[:80] + ("…" if len(bullet) > 80 else ""), {
            "full_text": bullet,
        }, source="data/experience.yaml")
        add_relation("achieved", rid, aid)

    for tag in exp.get("tags", []):
        sid = f"skill:{slugify(tag)}"
        if not any(e["id"] == sid for e in entities):
            add_entity(sid, "Skill", tag, source="data/experience.yaml, data/skills.yaml")
        add_relation("demonstrates_skill", rid, sid)

# ---------------- Education ----------------
for edu in load("education"):
    eid = f"education:{slugify(edu['org'])}-{slugify(edu['degree'])}"
    add_entity(eid, "Education", edu["degree"], {
        "org": edu["org"],
        "location": edu.get("location"),
        "start": edu.get("start"),
        "end": edu.get("end"),
        "details": edu.get("details", []),
    }, source="data/education.yaml")
    add_relation("earned", PERSON, eid)
    add_relation("at_org", eid, org_id(edu["org"]))

# ---------------- Awards ----------------
for i, award in enumerate(load("awards")):
    wid = f"award:{award['year']}-{i}"
    add_entity(wid, "Award", award["text"], {"year": award["year"]}, source="data/awards.yaml")
    add_relation("received", PERSON, wid, {"year": award["year"]})

# ---------------- Talks ----------------
for i, talk in enumerate(load("talks")):
    tid = f"talk:{slugify(talk['date'])}-{i}"
    add_entity(tid, "Talk", talk["title"], {
        "date": talk["date"], "venue": talk.get("venue"), "location": talk.get("location"),
    }, source="data/talks.yaml")
    add_relation("gave_talk", PERSON, tid)

# ---------------- Projects ----------------
_project_ids = {}
for proj in load("projects"):
    pid = f"project:{slugify(proj['title'])}"
    _project_ids[proj["title"]] = pid
    add_entity(pid, "Project", proj["title"], {
        "org": proj.get("org"),
        "period": proj.get("period"),
        "metric": proj.get("metric"),
        "description": proj.get("description"),
        "image": proj.get("image"),
        "links": proj.get("links", []),
    }, source="data/projects.yaml")
    add_relation("created", PERSON, pid)
    if proj.get("org"):
        add_relation("at_org", pid, org_id(proj["org"]))
    for tag in proj.get("tags", []):
        sid = f"skill:{slugify(tag)}"
        if not any(e["id"] == sid for e in entities):
            add_entity(sid, "Skill", tag, source="data/projects.yaml")
        add_relation("demonstrates_skill", pid, sid)

# ---------------- Publications ----------------
_paper_url_index = {}
for pub in load("publications"):
    key = pub.get("details") or pub["title"]
    paper_slug = slugify(pub["title"])[:60]
    paid = f"paper:{paper_slug}"
    add_entity(paid, "Paper", pub["title"], {
        "authors": pub.get("authors"),
        "venue": pub.get("venue"),
        "venueShort": pub.get("venueShort"),
        "details": pub.get("details"),
        "year": pub.get("year"),
        "type": pub.get("type"),
        "highlight": pub.get("highlight", False),
        "url": pub.get("url"),
        "image": pub.get("image"),
        "takeaway": pub.get("takeaway"),
        "links": pub.get("links", []),
    }, source="data/publications.yaml")
    add_relation("authored", PERSON, paid, {"year": pub.get("year")})
    if pub.get("url"):
        _paper_url_index[pub["url"]] = paid
    for link in pub.get("links", []):
        if link.get("url"):
            _paper_url_index[link["url"]] = paid

# link projects to papers via shared URLs (e.g. Foundation Model Distillation -> SubDistill paper)
for proj in load("projects"):
    pid = _project_ids[proj["title"]]
    seen_targets = set()
    for link in proj.get("links", []):
        target = _paper_url_index.get(link.get("url"))
        if target and target not in seen_targets:
            seen_targets.add(target)
            add_relation("relates_to_paper", pid, target, {"via_link_label": link.get("label")})

# Hand-mapped paper -> skill links for the recent LLM-focused papers (titles/venues
# alone don't reliably imply a skill keyword, so this is a small explicit table
# rather than a heuristic).
PAPER_SKILL_LINKS = {
    "paper:quantization-aware-healing-a-practical-recipe-for-recov": ["skill:post-training", "skill:distillation"],
    "paper:efficient-knowledge-distillation-for-llms-offline-top-k": ["skill:distillation", "skill:post-training"],
    "paper:llm-compression-by-block-removal-with-constrained-binar": ["skill:llm-compression", "skill:post-training"],
    "paper:distilling-lightweight-domain-experts-from-large-ml-mod": ["skill:distillation"],
}
for paid, skill_ids in PAPER_SKILL_LINKS.items():
    if any(e["id"] == paid for e in entities):
        for sid in skill_ids:
            if any(e["id"] == sid for e in entities):
                add_relation("demonstrates_skill", paid, sid)

# ---------------- Skills taxonomy (data/skills.yaml categories) ----------------
for cat in load("skills"):
    cid = f"skillcategory:{slugify(cat['category'])}"
    add_entity(cid, "SkillCategory", cat["category"], source="data/skills.yaml")
    for item in cat.get("items", []):
        sid = f"skill:{slugify(item)}"
        if not any(e["id"] == sid for e in entities):
            add_entity(sid, "Skill", item, source="data/skills.yaml")
        add_relation("in_category", sid, cid)

# ---------------- Artifacts ----------------
ARTIFACTS = [
    ("artifact:website-home", "content/_index.md + layouts/index.html", "Website home page (bio, selected projects/publications)"),
    ("artifact:website-projects", "layouts/projects/list.html", "Website Projects page"),
    ("artifact:website-publications", "layouts/publications/list.html", "Website Publications page"),
    ("artifact:website-cv-page", "content/cv/_index.md + layouts/cv/list.html", "Website CV page"),
    ("artifact:cv-tex", "cv/1pageCV.tex", "One-page CV LaTeX source"),
    ("artifact:cv-pdf", "static/files/Ali_Hashemi_CV.pdf", "Compiled one-page CV PDF"),
    ("artifact:linkedin-draft", "drafts/linkedin.md", "Draft LinkedIn headline/About/experience text (not posted)"),
]
for aid, path, desc in ARTIFACTS:
    add_entity(aid, "Artifact", desc, {"path": path}, source="repo")
    add_relation("represents", aid, PERSON)

entities_path = OUT / "entities.json"
relations_path = OUT / "relations.json"
entities_path.write_text(json.dumps(entities, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
relations_path.write_text(json.dumps(relations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"Wrote {len(entities)} entities -> {entities_path.relative_to(ROOT)}")
print(f"Wrote {len(relations)} relations -> {relations_path.relative_to(ROOT)}")
