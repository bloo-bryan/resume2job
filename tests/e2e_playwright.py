"""End-to-end Playwright test for the Streamlit frontend."""

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8501"
SAMPLES = Path(__file__).resolve().parent.parent / "data" / "samples"
RESUME_TEXT = (SAMPLES / "resumes" / "resume_01_ml_engineer_senior.txt").read_text()
JD_TEXT = (SAMPLES / "job_descriptions" / "jd_01_senior_ml_engineer.txt").read_text()


def wait_for_app_load(page):
    page.wait_for_selector("text=Resume2Job", timeout=30000)
    time.sleep(2)


def test_match_tab(page):
    print("--- Testing Match Tab ---")

    # Scope to Match tab panel
    match_tab = page.get_by_role("tab", name="Match")
    match_tab.click()
    time.sleep(1)

    # Use .first to target the first instance (Match tab)
    resume_area = page.locator('textarea[aria-label="Or paste resume text"]').first
    resume_area.fill(RESUME_TEXT[:500])

    jd_area = page.locator('textarea[aria-label="Paste Job Description"]').first
    jd_area.fill(JD_TEXT[:500])

    page.get_by_role("button", name="Analyze Match").click()

    page.wait_for_selector("text=Overall Match Score", timeout=120000)
    print("  Match score displayed!")

    assert page.locator("text=Required Skills").count() > 0, "Missing required skills breakdown"
    assert page.locator("text=Semantic Similarity").count() > 0, "Missing semantic similarity"
    print("  Score breakdown rendered!")


def test_comparison_tab(page):
    print("--- Testing Comparison Tab ---")

    page.get_by_role("tab", name="Comparison").click()
    time.sleep(1)

    # Use nth(1) for Comparison tab's inputs
    resume_area = page.locator('textarea[aria-label="Or paste resume text"]').nth(1)
    resume_area.fill(RESUME_TEXT[:500])

    jd_area = page.locator('textarea[aria-label="Paste Job Description"]').nth(1)
    jd_area.fill(JD_TEXT[:500])

    page.get_by_role("button", name="Compare All Algorithms").click()

    page.wait_for_selector("text=TFIDF", timeout=120000)
    assert page.locator("text=EMBEDDING").count() > 0, "Missing embedding column"
    assert page.locator("text=HYBRID").count() > 0, "Missing hybrid column"
    print("  Three-column comparison displayed!")


def test_entities_tab(page):
    print("--- Testing Entities Tab ---")

    page.get_by_role("tab", name="Entities").click()
    time.sleep(1)

    # Use nth(2) for Entities tab's inputs
    resume_area = page.locator('textarea[aria-label="Or paste resume text"]').nth(2)
    resume_area.fill(RESUME_TEXT[:500])

    jd_area = page.locator('textarea[aria-label="Paste Job Description"]').nth(2)
    jd_area.fill(JD_TEXT[:500])

    page.get_by_role("button", name="Extract Entities").click()

    page.wait_for_selector("text=Resume Entities", timeout=120000)
    assert page.locator("text=Job Description Entities").count() > 0, "Missing JD entities"
    print("  Entity extraction displayed!")


def test_about_tab(page):
    print("--- Testing About Tab ---")

    page.get_by_role("tab", name="About").click()
    time.sleep(1)

    assert page.locator("text=About Resume2Job").count() > 0, "About content missing"
    assert page.locator("text=Three-scorer architecture").count() > 0, "Architecture info missing"
    print("  About tab rendered!")


def test_sidebar_health(page):
    print("--- Testing Sidebar Health ---")

    assert page.locator("text=API: Connected").count() > 0, "Health status not showing"
    print("  Health indicator displayed!")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening {BASE_URL}...")
        page.goto(BASE_URL)
        wait_for_app_load(page)
        print("App loaded!\n")

        page.screenshot(path="/tmp/streamlit_initial.png", full_page=True)
        print("Screenshot saved: /tmp/streamlit_initial.png\n")

        test_sidebar_health(page)
        test_match_tab(page)

        page.screenshot(path="/tmp/streamlit_match.png", full_page=True)
        print("Screenshot saved: /tmp/streamlit_match.png\n")

        test_comparison_tab(page)
        page.screenshot(path="/tmp/streamlit_comparison.png", full_page=True)
        print("Screenshot saved: /tmp/streamlit_comparison.png\n")

        test_entities_tab(page)
        page.screenshot(path="/tmp/streamlit_entities.png", full_page=True)
        print("Screenshot saved: /tmp/streamlit_entities.png\n")

        test_about_tab(page)

        browser.close()
        print("\n=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    main()
