"""Validate shared skill metadata, invocation policies, and local references."""

import argparse
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--skills-dir", type=Path, help="Validate installed copies instead of this source tree.")
parser.add_argument("skills", nargs="*", help="Selected skill names; defaults to all skills in the directory.")
args = parser.parse_args()
skill_root = args.skills_dir or ROOT / "skills"
skills = [skill_root / name for name in args.skills] if args.skills else sorted(skill_root.iterdir())

for skill in skills:
    entrypoint = skill / "SKILL.md"
    match = re.match(r"^---\n(.*?)\n---\n", entrypoint.read_text(), re.S)
    assert match, f"Missing frontmatter: {entrypoint}"
    metadata = yaml.safe_load(match[1])
    assert metadata["name"] == skill.name, f"Mismatched name: {entrypoint}"
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name), skill.name
    assert isinstance(metadata["description"], str) and metadata["description"], entrypoint
    manual = metadata.get("disable-model-invocation", False)
    assert isinstance(manual, bool), f"Manual policy must be boolean: {entrypoint}"
    sidecar = skill / "agents/openai.yaml"
    config = yaml.safe_load(sidecar.read_text())
    implicit = config.get("policy", {}).get("allow_implicit_invocation", True)
    assert implicit is (not manual), f"Conflicting invocation policies: {skill}"

links = 0
documents = [document for skill in skills for document in sorted(skill.rglob("*.md"))]
if args.skills_dir is None and not args.skills:
    documents = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md")), *documents]
for document in documents:
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
        if target.startswith(("https://", "http://", "#")):
            continue
        target = target.split("#", 1)[0]
        assert (document.parent / target).exists(), f"Broken link in {document}: {target}"
        links += 1

print(f"PASS: {len(skills)} skill schemas and invocation policies; {links} local links.")
