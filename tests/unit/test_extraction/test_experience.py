from datetime import date

import pytest

from resume2job.extraction.experience import (
    _parse_date,
    _years_between,
    extract_experience,
    extract_min_experience_years,
)


class TestParseDate:
    def test_abbreviated_month_year(self) -> None:
        result = _parse_date("Jan 2020")
        assert result == date(2020, 1, 1)

    def test_full_month_year(self) -> None:
        result = _parse_date("January 2020")
        assert result == date(2020, 1, 1)

    def test_mm_slash_yyyy(self) -> None:
        result = _parse_date("01/2020")
        assert result == date(2020, 1, 1)

    def test_year_only(self) -> None:
        result = _parse_date("2020")
        assert result == date(2020, 1, 1)

    def test_present(self) -> None:
        result = _parse_date("Present")
        assert result == date.today()

    def test_current(self) -> None:
        result = _parse_date("Current")
        assert result == date.today()

    def test_invalid_returns_none(self) -> None:
        result = _parse_date("not a date")
        assert result is None

    def test_sept_abbreviation(self) -> None:
        result = _parse_date("Sept 2021")
        assert result == date(2021, 9, 1)

    def test_strips_whitespace(self) -> None:
        result = _parse_date("  Mar 2019  ")
        assert result == date(2019, 3, 1)


class TestYearsBetween:
    def test_simple_years(self) -> None:
        start = date(2020, 1, 1)
        end = date(2022, 1, 1)
        years = _years_between(start, end)
        assert 1.9 <= years <= 2.1

    def test_zero_duration(self) -> None:
        d = date(2020, 1, 1)
        assert _years_between(d, d) == 0.0

    def test_negative_clamped_to_zero(self) -> None:
        start = date(2022, 1, 1)
        end = date(2020, 1, 1)
        assert _years_between(start, end) == 0.0

    def test_partial_year(self) -> None:
        start = date(2020, 1, 1)
        end = date(2020, 7, 1)
        years = _years_between(start, end)
        assert 0.4 <= years <= 0.6


class TestExtractExperience:
    def test_finds_date_ranges(self) -> None:
        text = (
            "Software Engineer\n"
            "Jan 2018 - Dec 2020\n"
            "- Did stuff\n"
        )
        result = extract_experience(text)
        assert len(result.positions) == 1
        assert result.total_years > 0

    def test_multiple_positions(self) -> None:
        text = (
            "Senior Engineer\n"
            "Jan 2020 - Present\n"
            "- Led team\n"
            "\n"
            "Junior Engineer\n"
            "June 2017 - Dec 2019\n"
            "- Learned stuff\n"
        )
        result = extract_experience(text)
        assert len(result.positions) == 2

    def test_no_dates_returns_empty(self) -> None:
        text = "I have experience in Python and ML."
        result = extract_experience(text)
        assert result.total_years == 0.0
        assert result.positions == []

    def test_title_heuristic(self) -> None:
        text = (
            "Machine Learning Engineer\n"
            "March 2021 - Present\n"
        )
        result = extract_experience(text)
        assert len(result.positions) == 1
        assert "Machine Learning Engineer" in result.positions[0].title

    def test_en_dash_separator(self) -> None:
        text = "Engineer\nJan 2020 \u2013 Dec 2022\n"
        result = extract_experience(text)
        assert len(result.positions) == 1
        assert result.total_years > 0


class TestExtractMinExperienceYears:
    def test_years_of_experience(self) -> None:
        text = "5+ years of experience in machine learning"
        result = extract_min_experience_years(text)
        assert result == 5.0

    def test_minimum_years(self) -> None:
        text = "Minimum 3 years in software engineering"
        result = extract_min_experience_years(text)
        assert result == 3.0

    def test_at_least_years(self) -> None:
        text = "At least 7 years of relevant experience"
        result = extract_min_experience_years(text)
        assert result == 7.0

    def test_no_match_returns_none(self) -> None:
        text = "We are looking for a talented engineer."
        result = extract_min_experience_years(text)
        assert result is None

    def test_yrs_abbreviation(self) -> None:
        text = "5+ yrs experience required"
        result = extract_min_experience_years(text)
        assert result == 5.0
