"""Vendor Scrawl's skill at a pinned commit; update only when its content changes."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "skills/scrawl"
REPOSITORY = "https://github.com/kitlangton/scrawl.git"
BRANCH = "main"
SOURCE_PATH = "skills/scrawl"


def git(checkout, *args):
    return subprocess.check_output(["git", "-C", str(checkout), *args])


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}


def main():
    with tempfile.TemporaryDirectory(prefix="scrawl-upstream-") as temporary:
        checkout = Path(temporary)
        git(checkout, "init", "--quiet")
        git(checkout, "remote", "add", "origin", REPOSITORY)
        git(checkout, "fetch", "--quiet", "--depth=1", "--filter=blob:none", "origin", BRANCH)
        revision = git(checkout, "rev-parse", "FETCH_HEAD").decode().strip()
        files = {}
        entries = git(checkout, "ls-tree", "-rz", revision, "--", SOURCE_PATH)
        for entry in entries.split(b"\0"):
            if not entry:
                continue
            info, path = entry.split(b"\t", 1)
            mode, kind, object_id = info.split()
            if kind != b"blob" or mode != b"100644":
                raise ValueError(f"Unexpected upstream file type: {path!r}")
            name = path.decode().removeprefix(SOURCE_PATH + "/")
            files[name] = git(checkout, "cat-file", "blob", object_id.decode())
        files["LICENSE"] = git(checkout, "show", f"{revision}:LICENSE")
        upstream_hashes = hashes(files)
        receipt_path = DESTINATION / ".upstream.json"
        previous = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
        if previous:
            actual = {
                str(path.relative_to(DESTINATION)): path.read_bytes()
                for path in DESTINATION.rglob("*")
                if path.is_file() and path != receipt_path
            }
            if hashes(actual) != previous["installed_hashes"]:
                raise ValueError("Scrawl has local edits; reconcile them before updating.")
            if previous["upstream_hashes"] == upstream_hashes:
                print(f"Scrawl is current at {previous['commit']}.")
                return

        text = files["SKILL.md"].decode()
        frontmatter, body = text.removeprefix("---\n").split("\n---\n", 1)
        metadata = yaml.safe_load(frontmatter)
        assert metadata["name"] == "scrawl", "Upstream skill was renamed"
        metadata["license"] = "MIT"
        metadata.setdefault("metadata", {}).update({
            "source": f"https://github.com/kitlangton/scrawl/tree/{revision}/{SOURCE_PATH}",
            "source_commit": revision,
        })
        files["SKILL.md"] = (
            "---\n" + yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True, width=10000)
            + "---\n" + body
        ).encode()
        if "agents/openai.yaml" not in files:
            sidecar = {"interface": {"display_name": "Scrawl", "short_description": "Read and inspect Scrawl screen captures"}}
            if metadata.get("disable-model-invocation", False):
                sidecar["policy"] = {"allow_implicit_invocation": False}
            files["agents/openai.yaml"] = yaml.safe_dump(sidecar, sort_keys=False).encode()

        receipt = {
            "repository": REPOSITORY, "branch": BRANCH, "path": SOURCE_PATH,
            "commit": revision, "upstream_hashes": upstream_hashes,
            "installed_hashes": hashes(files),
        }
        staged = checkout / "staged"
        for name, data in files.items():
            target = staged / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (staged / ".upstream.json").write_text(json.dumps(receipt, indent=2) + "\n")
        if DESTINATION.exists():
            shutil.rmtree(DESTINATION)
        shutil.copytree(staged, DESTINATION)
        print(f"Updated Scrawl to {revision}.")


if __name__ == "__main__":
    main()
