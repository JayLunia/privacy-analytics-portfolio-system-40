from pathlib import Path

from src.pipeline import run


def test_pipeline_runs():
    run()
    assert any(Path('reports').iterdir())
