import json
from pathlib import Path

from pydantic import BaseModel

from resume2job.config import PROJECT_ROOT


class LabeledPair(BaseModel):
    jd_file: str
    resume_file: str
    relevance: int


class TestSet(BaseModel):
    pairs: list[LabeledPair]


def load_test_set(test_set_path: Path | None = None) -> TestSet:
    if test_set_path is None:
        test_set_path = PROJECT_ROOT / "data" / "test_set" / "labels.json"
    data = json.loads(test_set_path.read_text())
    return TestSet(**data)


def load_texts(pair: LabeledPair, samples_dir: Path | None = None) -> tuple[str, str]:
    if samples_dir is None:
        samples_dir = PROJECT_ROOT / "data" / "samples"
    resume_text = (samples_dir / pair.resume_file).read_text()
    jd_text = (samples_dir / pair.jd_file).read_text()
    return resume_text, jd_text
