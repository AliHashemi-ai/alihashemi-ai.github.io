# Knowledge graph (public)

A generated, queryable cross-reference over everything on this site and in the
CV: people, roles, organizations, projects, papers, skills, achievements, and
the artifacts (website pages, CV source, CV PDF, LinkedIn draft) that
describe them. It exists so future edits to the website/CV/LinkedIn draft can
look up facts here instead of re-deriving them from scratch, and so
inconsistencies between sources get caught.

## Provenance note

This reuses the convention of this repo's own `data/*.yaml` files (flat,
readable, one concept per file) rather than a different schema, because the
other Claude Code session that was asked about ("research_verso pipeline
main") could not be reached from this session — cross-session delivery was
refused with an authentication-boundary error, not a transient failure. If
that session's actual knowledge-graph schema becomes available (e.g. Ali
pastes or uploads it), this graph should be migrated to match it instead.

## Files

- **`entities.json`** — generated. Every node: `{id, type, name, properties, source}`.
  `source` names the `data/*.yaml` file (or repo path) it was derived from.
- **`relations.json`** — generated. Every edge: `{id, type, source, target, properties}`,
  `source`/`target` referencing entity `id`s.
- **`constraints.json`** — hand-authored. Style/content decisions ("(Distinction)" not
  "summa cum laude", no RLHF/DPO/GRPO claims, no uncleared numbers, LinkedIn needs
  approval, where private data lives) and known **conflicts** between sources
  (e.g. 200+ vs 400+ course participants), each with a `status` of `open`,
  `unverified`, or `resolved-by-decision`.
- **`../../scripts/build_knowledge_graph.py`** — the generator. Re-run it after
  editing any `data/*.yaml` file so `entities.json`/`relations.json` stay in sync:

  ```
  python3 scripts/build_knowledge_graph.py
  ```

  It never touches `constraints.json` — edit that by hand.

## Entity types

`Person`, `Organization`, `Role`, `Achievement`, `Education`, `Award`, `Talk`,
`Project`, `Paper`, `Skill`, `SkillCategory`, `Artifact`.

## Relation types

`held_role`, `at_org`, `achieved`, `demonstrates_skill`, `earned`, `received`,
`gave_talk`, `created`, `authored`, `relates_to_paper`, `in_category`,
`represents`.

## Querying it

No graph database is wired up — these are plain JSON files, queryable with
`jq`, Python, or any script. Examples:

```bash
# Every paper that demonstrates the "Distillation" skill
jq -r '.[] | select(.type=="demonstrates_skill") | .source' data/knowledge-graph/relations.json \
  | grep '^paper:' | sort -u

# All achievements for the Multiverse Senior LLM Researcher role
python3 - <<'EOF'
import json
entities = {e["id"]: e for e in json.load(open("data/knowledge-graph/entities.json"))}
relations = json.load(open("data/knowledge-graph/relations.json"))
role = "role:multiverse-computing-llm-research-staff-senior-llm-researcher-tech-lead-model-evaluation"
for r in relations:
    if r["type"] == "achieved" and r["source"] == role:
        print("-", entities[r["target"]]["properties"]["full_text"])
EOF

# Open conflicts that still need Ali's input
jq '.conflicts[] | select(.status=="open")' data/knowledge-graph/constraints.json
```

## What's deliberately NOT here

Recruiter/opportunity data, draft outbound replies, and anything from the
private CV package marked "not cleared for public use" are **not** in this
graph or this repo. See the private store's own notes for where that lives
(not committed; a path outside this repository, shared with Ali directly).
