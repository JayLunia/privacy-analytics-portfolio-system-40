
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yaml


def load_config(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def share(value: int, parties: int, rng: np.random.Generator) -> list[int]:
    pieces = rng.integers(-100, 100, size=parties - 1)
    return [int(x) for x in pieces] + [int(value - pieces.sum())]


def run(config_path: str = "configs/default.yaml") -> None:
    cfg = load_config(config_path)
    rng = np.random.default_rng(cfg.get("seed", 42))
    values = [120, 95, 140, 80]
    shares = [share(value, cfg.get("parties", 3), rng) for value in values]
    aggregate = int(np.array(shares).sum())
    report = Path("reports")
    report.mkdir(exist_ok=True)
    (report / "summary.json").write_text(
        json.dumps({"private_record_count": len(values), "approved_aggregate": aggregate}, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    run(parser.parse_args().config)
