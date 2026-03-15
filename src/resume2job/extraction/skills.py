import re

from spacy.language import Language


def extract_skills(text: str, nlp: Language) -> list[str]:
    doc = nlp(text.lower())
    skills = sorted({ent.text for ent in doc.ents if ent.label_ == "SKILL"})
    return skills


def classify_jd_skills(text: str, nlp: Language) -> tuple[list[str], list[str]]:
    # Split at preferred/nice-to-have section markers
    split_pattern = re.compile(
        r"\n\s*(?:nice\s+to\s+have|preferred|bonus|desired|plus|"
        r"nice-to-have|good\s+to\s+have|preferred\s+qualifications|"
        r"preferred\s+skills|bonus\s+skills|desired\s+skills|"
        r"additional\s+skills|optional|ideally)\s*[:|\n]",
        re.IGNORECASE,
    )

    match = split_pattern.search(text)
    if match:
        required_text = text[: match.start()]
        preferred_text = text[match.start() :]
    else:
        required_text = text
        preferred_text = ""

    required_skills = extract_skills(required_text, nlp)
    preferred_skills = extract_skills(preferred_text, nlp) if preferred_text else []

    # Deduplicate: remove from preferred any that are already in required
    required_set = set(required_skills)
    preferred_skills = [s for s in preferred_skills if s not in required_set]

    return required_skills, preferred_skills
