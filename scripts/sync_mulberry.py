from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path("/tmp/mb/EN")
DESTINATION = ROOT / "backend" / "assets" / "pictograms" / "mulberry"
DICTIONARY = ROOT / "backend" / "assets" / "pictograms" / "mulberry_es.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--license", type=Path)
    args = parser.parse_args()

    mapping = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    filenames = set(mapping.values())
    invalid = [
        filename
        for filename in filenames
        if Path(filename).name != filename or not filename.endswith(".svg")
    ]
    if invalid:
        raise ValueError(f"Invalid Mulberry filenames: {', '.join(sorted(invalid))}")

    missing = sorted(filename for filename in filenames if not (args.source / filename).is_file())
    if missing:
        raise FileNotFoundError(f"Missing Mulberry SVGs: {', '.join(missing)}")

    license_path = args.license or args.source.parent / "LICENSE.txt"
    if not license_path.is_file():
        raise FileNotFoundError(f"Mulberry license not found: {license_path}")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    for stale in DESTINATION.glob("*.svg"):
        if stale.name not in filenames:
            stale.unlink()
    for filename in sorted(filenames):
        shutil.copyfile(args.source / filename, DESTINATION / filename)
    shutil.copyfile(license_path, DESTINATION / "LICENSE.txt")
    print(
        f"Copied {len(filenames)} Mulberry SVGs for {len(mapping)} Spanish words "
        f"to {DESTINATION}"
    )


if __name__ == "__main__":
    main()
