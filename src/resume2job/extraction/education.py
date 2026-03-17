import re

from spacy.language import Language

from resume2job.models import EducationEntry

DEGREE_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bPh\.?D\.?\b", re.IGNORECASE), "Ph.D."),
    (re.compile(r"\bDoctor(?:ate)?\s+of\b", re.IGNORECASE), "Ph.D."),
    (re.compile(r"\bMBA\b"), "MBA"),
    (re.compile(r"\bM\.?S\.?\b(?:\s+in\b)?", re.IGNORECASE), "M.S."),
    (
        re.compile(
            r"\bMaster(?:'?s)?\s+(?:of\s+)?(?:Science|Arts|Engineering|Business)\b",
            re.IGNORECASE,
        ),
        "M.S.",
    ),
    (re.compile(r"\bMaster(?:'?s)?\s+(?:degree|of)\b", re.IGNORECASE), "M.S."),
    (re.compile(r"\bM\.?A\.?\b(?:\s+in\b)?", re.IGNORECASE), "M.S."),
    (re.compile(r"\bB\.?S\.?\b(?:\s+in\b)?", re.IGNORECASE), "B.S."),
    (re.compile(r"\bBachelor(?:'?s)?\s+(?:of\s+)?Science\b", re.IGNORECASE), "B.S."),
    (re.compile(r"\bB\.?A\.?\b(?:\s+in\b)?", re.IGNORECASE), "B.A."),
    (re.compile(r"\bBachelor(?:'?s)?\s+(?:of\s+)?Arts\b", re.IGNORECASE), "B.A."),
    (re.compile(r"\bBachelor(?:'?s)?\s+(?:degree|of)\b", re.IGNORECASE), "B.S."),
    (re.compile(r"\bAssociate(?:'?s)?\s+(?:degree|of)\b", re.IGNORECASE), "Associate"),
]

DEGREE_RANK: dict[str, int] = {
    "Ph.D.": 4,
    "MBA": 3,
    "M.S.": 3,
    "B.S.": 2,
    "B.A.": 2,
    "Associate": 1,
}

# Pattern to extract field of study after degree mention
FIELD_PATTERN = re.compile(
    r"(?:in|of)\s+([A-Z][A-Za-z\s&/,]+?)(?:\s+(?:from|at|-|–|,|\n|$))",
    re.IGNORECASE,
)


def extract_education(text: str, nlp: Language) -> list[EducationEntry]:
    entries: list[EducationEntry] = []
    seen_degrees: set[str] = set()

    lines = text.split("\n")
    for i, line in enumerate(lines):
        for pattern, degree_label in DEGREE_PATTERNS:
            if pattern.search(line):
                if degree_label in seen_degrees:
                    continue
                seen_degrees.add(degree_label)

                # Extract field of study
                field: str | None = None
                field_match = FIELD_PATTERN.search(line)
                if field_match:
                    field = field_match.group(1).strip().rstrip(",. ")
                    # Cap field length to avoid grabbing too much
                    if len(field) > 60:
                        field = field[:60].rsplit(" ", 1)[0]

                # Find nearest ORG entity for institution
                institution: str | None = None
                # Look at current line and nearby lines for an org
                context = "\n".join(lines[max(0, i - 1) : i + 2])
                context_doc = nlp(context)
                for ent in context_doc.ents:
                    if ent.label_ == "ORG":
                        institution = ent.text
                        break

                entries.append(
                    EducationEntry(
                        degree=degree_label,
                        field=field,
                        institution=institution,
                    )
                )
                break  # Only match first degree pattern per line

    # Sort by rank descending
    entries.sort(key=lambda e: DEGREE_RANK.get(e.degree, 0), reverse=True)
    return entries


def extract_required_education(text: str) -> str | None:
    best_degree: str | None = None
    best_rank: int = 0

    for pattern, degree_label in DEGREE_PATTERNS:
        if pattern.search(text):
            rank = DEGREE_RANK.get(degree_label, 0)
            if rank > best_rank:
                best_rank = rank
                best_degree = degree_label

    return best_degree
