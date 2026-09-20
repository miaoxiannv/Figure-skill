#!/usr/bin/env python3
"""Version check and self-update for the nature-figure-pdf skill.

    python scripts/check_update.py --check    # local VERSION vs GitHub main
    python scripts/check_update.py --update   # git pull (clone) or tarball refresh

Zero third-party dependencies. The R library installed by
scripts/install_gseavis.R lives outside the skill folder and is never
touched by an update.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

REPO = "miaoxiannv/Figure-skill"
SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_DIR / "VERSION"
REMOTE_VERSION = f"https://raw.githubusercontent.com/{REPO}/main/VERSION"
REMOTE_TARBALL = f"https://github.com/{REPO}/archive/refs/heads/main.tar.gz"


def local_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "unknown"


def remote_version() -> str:
    with urllib.request.urlopen(REMOTE_VERSION, timeout=30) as r:
        return r.read().decode("utf-8").strip()


def check() -> int:
    loc, rem = local_version(), remote_version()
    if loc == rem:
        print(f"local {loc} | remote {rem} — up to date")
        return 0
    print(f"local {loc} | remote {rem} — update available:")
    print(f"  python scripts/check_update.py --update")
    return 1


def update() -> int:
    if (SKILL_DIR / ".git").exists():
        print("git clone detected — updating via git pull")
        r = subprocess.run(["git", "-C", str(SKILL_DIR), "pull", "--ff-only"],
                           capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode == 0:
            print("updated to", local_version())
            return 0
        print("git pull failed — falling back to tarball refresh", file=sys.stderr)

    print("refreshing from", REMOTE_TARBALL)
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        tb = td / "main.tar.gz"
        urllib.request.urlretrieve(REMOTE_TARBALL, tb)
        with tarfile.open(tb) as tf:
            tf.extractall(td)
        src = td / "main"
        if not src.is_dir():
            print("unexpected archive layout", file=sys.stderr)
            return 1
        n = 0
        for f in src.rglob("*"):
            rel = f.relative_to(src)
            if rel.parts and rel.parts[0] == ".git":
                continue
            dst = SKILL_DIR / rel
            if f.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                n += 1
        print(f"refreshed {n} files -> version {local_version()}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="compare local vs GitHub main")
    g.add_argument("--update", action="store_true", help="git pull or tarball refresh")
    a = ap.parse_args()
    return check() if a.check else update()


if __name__ == "__main__":
    sys.exit(main())
