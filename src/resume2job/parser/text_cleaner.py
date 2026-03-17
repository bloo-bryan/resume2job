import re
import unicodedata

_BULLET_CHARS = re.compile(r"[•▪►◦▸●○■◆]")
_SPACES_TABS = re.compile(r"[ \t]+")
_EXCESS_NEWLINES = re.compile(r"\n{3,}")
_PAGE_X_OF_Y = re.compile(r"page\s+\d+\s+of\s+\d+", re.IGNORECASE)


def clean_text(raw_text: str | None) -> str:
    if not raw_text:
        return ""

    text = unicodedata.normalize("NFKD", raw_text)

    text = "".join(
        ch for ch in text if not unicodedata.category(ch).startswith("C") or ch in "\n\t "
    )

    text = _BULLET_CHARS.sub("-", text)

    text = _SPACES_TABS.sub(" ", text)

    text = _EXCESS_NEWLINES.sub("\n\n", text)

    text = _PAGE_X_OF_Y.sub("", text)

    text = "\n".join(line.strip() for line in text.splitlines())

    return text.strip()
