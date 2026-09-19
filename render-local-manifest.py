#!/usr/bin/env python3
"""Render the pinned public template for a local file:// checkout."""

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def head(path: Path, bare: bool) -> str:
    command = ["git", f"--git-dir={path}"] if bare else ["git", "-C", str(path)]
    return subprocess.check_output(command + ["rev-parse", "HEAD"], text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("local_repos", type=Path, help="directory containing the two local Git repositories")
    args = parser.parse_args()
    repos = args.local_repos.resolve(strict=True)
    tree = ET.parse(Path(__file__).parent / "local_manifests/so01k-p451-public.xml")
    root = tree.getroot()
    remote = root.find("remote[@name='so01k-public']")
    assert remote is not None
    remote.set("fetch", repos.as_uri() + "/")
    for project in root.findall("project[@remote='so01k-public']"):
        name = project.attrib["name"]
        local_path = repos / (name + ".git")
        if not local_path.exists():
            parser.error(f"missing local repository: {local_path}")
        expected = project.attrib["revision"]
        actual = head(local_path, name == "android_device_sony_poplar_docomo-twrp")
        if actual != expected:
            parser.error(f"unexpected HEAD for {name}: {actual}")
        project.set("name", name + ".git")
    ET.indent(tree, space="    ")
    tree.write(sys.stdout.buffer, encoding="utf-8", xml_declaration=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
