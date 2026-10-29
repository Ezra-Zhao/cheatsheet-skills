#!/usr/bin/env python3
"""Verify this repo's skills:
- every skills/<name>/SKILL.md frontmatter parses as YAML
- name == directory name, lowercase-hyphen, unique
- body (after frontmatter) SHA-256 matches skills-manifest.json,
  which records the hash of the source CHEATSHEET.md each skill
  was built from — so a skill can never silently drift from its sheet.
Run: python3 scripts/verify_skills.py  (needs PyYAML)"""
import hashlib, json, os, re, sys

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml"); sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

manifest = json.load(open(os.path.join(ROOT, "scripts", "skills-manifest.json")))
fails, seen = [], set()
for name in sorted(os.listdir(SKILLS)):
    p = os.path.join(SKILLS, name, "SKILL.md")
    raw = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n\n(.*)$", raw, re.S)
    if not m:
        fails.append(f"{name}: no frontmatter block"); continue
    fm = yaml.safe_load(m.group(1))
    if fm.get("name") != name: fails.append(f"{name}: name mismatch")
    if not NAME_RE.match(name): fails.append(f"{name}: illegal name")
    if name in seen: fails.append(f"{name}: duplicate")
    seen.add(name)
    h = hashlib.sha256(m.group(2).encode("utf-8")).hexdigest()
    if manifest.get(name) != h:
        fails.append(f"{name}: body hash != manifest (drift from source sheet)")

missing = set(manifest) - seen
if missing: fails.append(f"manifest entries without skill: {sorted(missing)}")
if fails:
    print("FAILED:"); [print(" -", f) for f in fails]; sys.exit(1)
print(f"OK: {len(seen)} skills verified (frontmatter valid, bodies match source-sheet manifest)")
