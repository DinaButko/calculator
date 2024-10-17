import logging
import colorlog
import pytest
from playwright.sync_api import sync_playwright
from pages.calculator_page import CalculatorPage


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


# Playwright fixtures
@pytest.fixture(scope="session")
def playwright():
    """Set up Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright):
    """Launch the browser instance for each test function."""
    browser = playwright.chromium.launch(headless=True)

    # Use browser.new_context to create a context
    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 640, "height": 480}
    )

    # Start tracing in the context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Stop tracing and export it into a zip archive.
    context.tracing.stop(path="trace.zip")

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
def setup_calculator(page, base_calculator_url):
    """Fixture to initialize CalculatorPage, visit the URL, and clean up afterward."""
    log.info("Setting up the calculator page.")
    calculator = CalculatorPage(page)
    calculator.navigate(base_calculator_url)

    yield calculator

    # Perform cleanup after test
    log.info("Tearing down and cleaning the calculator page.")
    try:
        calculator.clear_all()
    except Exception as e:
        log.error(f"Failed to clear calculator during teardown: {e}")
