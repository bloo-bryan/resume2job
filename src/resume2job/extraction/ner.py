import logging
from functools import lru_cache
from pathlib import Path

import spacy
from spacy.language import Language

from resume2job.config import get_settings

logger = logging.getLogger(__name__)


def _load_skill_patterns(skills_path: Path) -> list[dict]:
    """Read CSV and build phrase patterns for EntityRuler."""
    import csv

    patterns = []
    with open(skills_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row["preferred_label"].strip()
            if label:
                patterns.append({"label": "SKILL", "pattern": label.lower()})
            alt_labels = row.get("alt_labels", "")
            if alt_labels:
                for alt in alt_labels.split("|"):
                    alt = alt.strip()
                    if alt:
                        patterns.append({"label": "SKILL", "pattern": alt.lower()})
    return patterns


@lru_cache(maxsize=1)
def build_nlp_pipeline() -> Language:
    settings = get_settings()
    nlp = spacy.load(settings.spacy_model)

    skills_path = settings.skills_csv_path
    if skills_path.exists():
        patterns = _load_skill_patterns(skills_path)
        ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})
        ruler.add_patterns(patterns)
        logger.info("Loaded %d skill patterns from %s", len(patterns), skills_path)
    else:
        logger.warning("Skills CSV not found at %s, running without skill patterns", skills_path)

    return nlp
