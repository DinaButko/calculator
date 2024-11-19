import logging
import os

import colorlog
import pytest
from pages.calculator_page import CalculatorPage
from playwright.sync_api import sync_playwright


# Set up the logger with color support
def setup_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


# Initialize the logger globally
log = setup_logger()

"""Playwright Fixtures"""


@pytest.fixture(scope="session")
def playwright():
    """Set up Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


def pytest_addoption(parser):
    """Parser function to help to run tests in different browsers"""
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to run tests on: chromium, firefox, or webkit"
    )


@pytest.fixture(scope="function")
def browser(playwright, browser_name, request):
    """Launch the specified browser instance for each test function with unique tracing."""
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=True)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Use browser.new_context to create a context
    context = browser.new_context(
        record_video_dir="../reports/videos",
        record_video_size={"width": 640, "height": 480}
    )

    # Start tracing in the context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Generate a unique trace path using test name and test parameters
    test_name = request.node.name
    param_values = "_".join(str(value) for value in request.node.callspec.params.values()) \
        if hasattr(request.node, "callspec") else ""
    trace_path = f"../reports/traces/{test_name}_{param_values[:0]}_trace.zip"
    print(f"Trace path for test: {trace_path}")  # Debug line
    os.makedirs(os.path.dirname(trace_path), exist_ok=True)

    # Stop tracing and export it into a unique zip archive per test
    context.tracing.stop(path=trace_path)

    # Close context before closing the browser
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Create a new page for each test within the existing context."""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def base_calculator_url():
    """Fixture for the calculator URL."""
    return "https://www.google.com/search?q=calculator"


@pytest.fixture(scope="function")
def setup_calculator(request, page, base_calculator_url):
    """Fixture to initialize CalculatorPage, visit the URL, and conditionally clean up afterward."""
    log.info("Setting up the calculator page.")
    calculator = CalculatorPage(page)
    calculator.navigate(base_calculator_url)

    # Flag to the request object to control teardown
    request.node.skip_teardown = False

    yield calculator

    # Perform cleanup after test unless skip_teardown is True
    if not request.node.skip_teardown:
        log.info("Tearing down and cleaning the calculator page.")
        try:
            calculator.clear_all()
        except Exception as e:
            log.error(f"Failed to clear calculator during teardown: {e}")
