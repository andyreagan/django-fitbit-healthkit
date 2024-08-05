# Functional test of the sample app and fitbit lib.
# Idea is to
# - create an account (see empty dashboard)
# - log out (see login page)
# - log in (see empty dashboard)
# - connect to fitbit (go through fitbit oauth)
# - see the dashboard (with fitbit data!)

# Use playwright

from playwright.sync_api import sync_playwright

def test_fitbit_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000")
        page.screenshot(path="screenshots/fitbit_dashboard_1.png")
        assert "Dashboard" in page.title()
        page.click("text=Connect to Fitbit")
        page.screenshot(path="screenshots/fitbit_dashboard_2.png")
        assert "Fitbit" in page.title()
        page.fill('input[name="email"]', "")
