import re
from datetime import date

from resume2job.models import ExperienceInfo, Position

MONTH_MAP: dict[str, int] = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

# Matches date ranges like:
#   "Jan 2020 - Dec 2022", "January 2020 - December 2022"
#   "01/2020 - 12/2022", "2018 - Present", "2018 - 2022"
#   "Jan 2020 – Present" (en-dash)
DATE_RANGE_PATTERN = re.compile(
    r"(?P<start>"
    r"(?:[A-Za-z]+\.?\s+)?\d{4}"      # "Jan 2020" or "January 2020" or "2020"
    r"|"
    r"\d{1,2}/\d{4}"                   # "01/2020"
    r")"
    r"\s*[-–]\s*"                       # dash or en-dash separator
    r"(?P<end>"
    r"(?:[A-Za-z]+\.?\s+)?\d{4}"
    r"|"
    r"\d{1,2}/\d{4}"
    r"|"
    r"[Pp]resent|[Cc]urrent"
    r")",
)

MIN_EXPERIENCE_PATTERN = re.compile(
    r"(?:"
    r"(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)"
    r"|"
    r"(?:minimum|at\s+least|min\.?)\s+(\d+)\s*\+?\s*(?:years?|yrs?)"
    r"|"
    r"(\d+)\+\s*(?:years?|yrs?)"
    r")",
    re.IGNORECASE,
)


def _parse_date(date_str: str) -> date | None:
    date_str = date_str.strip().rstrip(".")
    if date_str.lower() in ("present", "current"):
        return date.today()

    # Try mm/yyyy
    mm_yyyy = re.match(r"^(\d{1,2})/(\d{4})$", date_str)
    if mm_yyyy:
        month, year = int(mm_yyyy.group(1)), int(mm_yyyy.group(2))
        if 1 <= month <= 12:
            return date(year, month, 1)
        return None

    # Try "Month Year" or "Mon Year"
    month_year = re.match(r"^([A-Za-z]+)\s+(\d{4})$", date_str)
    if month_year:
        month_str = month_year.group(1).lower().rstrip(".")
        year = int(month_year.group(2))
        month = MONTH_MAP.get(month_str)
        if month:
            return date(year, month, 1)
        return None

    # Try year only
    year_only = re.match(r"^(\d{4})$", date_str)
    if year_only:
        return date(int(year_only.group(1)), 1, 1)

    return None


def _years_between(start: date, end: date) -> float:
    diff = (end - start).days / 365.25
    return max(diff, 0.0)


def extract_experience(text: str) -> ExperienceInfo:
    lines = text.split("\n")
    positions: list[Position] = []
    total_years = 0.0

    for i, line in enumerate(lines):
        for match in DATE_RANGE_PATTERN.finditer(line):
            start_date = _parse_date(match.group("start"))
            end_date = _parse_date(match.group("end"))
            years = None
            if start_date and end_date:
                years = round(_years_between(start_date, end_date), 1)
                total_years += years

            # Heuristic: look at the line before the date range for a job title
            title = ""
            if i > 0:
                candidate = lines[i - 1].strip()
                # Use the previous line if it's non-empty and not itself a date range
                if candidate and not DATE_RANGE_PATTERN.search(candidate):
                    title = candidate

            positions.append(
                Position(
                    title=title or "Unknown",
                    start_date=match.group("start").strip(),
                    end_date=match.group("end").strip(),
                    years=years,
                )
            )

    # Sanity check: clamp total years to 0-50
    total_years = max(0.0, min(total_years, 50.0))

    return ExperienceInfo(
        total_years=round(total_years, 1),
        positions=positions,
    )


def extract_min_experience_years(text: str) -> float | None:
    match = MIN_EXPERIENCE_PATTERN.search(text)
    if not match:
        return None
    # Return whichever group matched
    for group in match.groups():
        if group is not None:
            return float(group)
    return None
