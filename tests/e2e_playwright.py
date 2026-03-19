"""End-to-end Playwright tests for the Next.js frontend.

Requires both servers running:
  - Frontend: http://localhost:3000
  - Backend:  http://localhost:8000

Run with:
  cd /home/bloo/dev/resume2job && python -m pytest tests/e2e_playwright.py -v
"""

import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:3000")
SAMPLES = Path(__file__).resolve().parent.parent / "data" / "samples"
RESUME_TEXT = (SAMPLES / "resumes" / "resume_01_ml_engineer_senior.txt").read_text()
JD_TEXT = (SAMPLES / "job_descriptions" / "jd_01_senior_ml_engineer.txt").read_text()

# Models load slowly on first request; use a generous timeout for API calls.
API_TIMEOUT = 60_000


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=BASE_URL,
        help="Frontend base URL (default: http://localhost:3000)",
    )


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture()
def page(browser, base_url) -> Page:
    """Create a new browser page for each test."""
    ctx = browser.new_context(base_url=base_url)
    pg = ctx.new_page()
    yield pg
    pg.close()
    ctx.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fill_inputs(page: Page) -> None:
    """Fill both resume and JD textareas with sample data."""
    page.get_by_placeholder("Or paste resume text...").fill(RESUME_TEXT[:500])
    page.get_by_placeholder("Paste job description text...").fill(JD_TEXT[:500])


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_navigation_links(page: Page):
    """Verify all 4 nav links exist and navigate to the correct pages."""
    page.goto("/match")

    for label, path in [
        ("Match", "/match"),
        ("Compare", "/compare"),
        ("Entities", "/entities"),
        ("Evaluation", "/evaluation"),
    ]:
        link = page.get_by_role("link", name=label, exact=True)
        expect(link).to_be_visible()
        link.click()
        page.wait_for_url(f"**{path}")


def test_api_health_indicator(page: Page):
    """Verify the green health dot appears when the backend is running."""
    page.goto("/match")
    # The health indicator is a green dot (bg-green-500) next to "API" text.
    api_label = page.get_by_text("API", exact=True)
    expect(api_label).to_be_visible()
    # The green dot is a sibling div with bg-green-500.
    health_dot = page.locator(".bg-green-500")
    expect(health_dot).to_be_visible(timeout=10_000)


def test_match_page_submit(page: Page):
    """Fill resume + JD, click Analyze Match, verify score and breakdown appear."""
    page.goto("/match")
    _fill_inputs(page)

    page.get_by_role("button", name="Analyze Match").click()

    # Wait for a score percentage to appear (e.g. "72%").
    score = page.locator("text=/%$/")
    expect(score.first).to_be_visible(timeout=API_TIMEOUT)

    # Verify breakdown cards.
    expect(page.get_by_text("Required Skills").first).to_be_visible()
    expect(page.get_by_text("Semantic Similarity").first).to_be_visible()


def test_compare_page_submit(page: Page):
    """Fill resume + JD, click Compare All Algorithms, verify 3 algorithm columns."""
    page.goto("/compare")
    _fill_inputs(page)

    page.get_by_role("button", name="Compare All Algorithms").click()

    # Each algorithm column has a heading with the algorithm label.
    for algo_label in ["TF-IDF", "Embedding", "Hybrid"]:
        expect(page.get_by_text(algo_label, exact=True).first).to_be_visible(
            timeout=API_TIMEOUT
        )

    # Verify we got at least three score percentages (one per algorithm).
    percentages = page.locator("text=/%$/")
    expect(percentages.first).to_be_visible(timeout=API_TIMEOUT)
    assert percentages.count() >= 3, (
        f"Expected at least 3 score percentages, got {percentages.count()}"
    )


def test_entities_page_submit(page: Page):
    """Fill resume + JD, click Extract Entities, verify entity panels appear."""
    page.goto("/entities")
    _fill_inputs(page)

    page.get_by_role("button", name="Extract Entities").click()

    expect(page.get_by_text("Resume Entities")).to_be_visible(timeout=API_TIMEOUT)
    expect(page.get_by_text("Job Description Entities")).to_be_visible(
        timeout=API_TIMEOUT
    )


def test_evaluation_page_static(page: Page):
    """Navigate to /evaluation, verify heading, test set size, and metric labels."""
    page.goto("/evaluation")

    expect(page.get_by_role("heading", name="Evaluation")).to_be_visible()
    expect(page.get_by_text("Test Set Size")).to_be_visible()

    for metric in ["NDCG@5", "MRR", "P@3"]:
        expect(page.get_by_text(metric, exact=True)).to_be_visible()


def test_match_page_empty_submit_disabled(page: Page):
    """Verify Analyze Match button is disabled when inputs are empty."""
    page.goto("/match")

    button = page.get_by_role("button", name="Analyze Match")
    expect(button).to_be_disabled()

    # Fill only resume -- button should still be disabled.
    page.get_by_placeholder("Or paste resume text...").fill("some text")
    expect(button).to_be_disabled()

    # Clear resume, fill only JD -- still disabled.
    page.get_by_placeholder("Or paste resume text...").fill("")
    page.get_by_placeholder("Paste job description text...").fill("some text")
    expect(button).to_be_disabled()

    # Fill both -- button should become enabled.
    page.get_by_placeholder("Or paste resume text...").fill("some text")
    expect(button).to_be_enabled()
