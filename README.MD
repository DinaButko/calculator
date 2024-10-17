
---

# Calculator Test Automation Suite

This project demonstrates a **test automation framework** for testing a calculator web application using **Python**, **PyTest**, **Playwright**, and follows the **Page Object Model (POM)** design pattern. The suite is designed to validate both basic and advanced functionalities of a calculator app, ensuring robustness, accuracy, and edge-case handling.

## Project Structure

```plaintext
calculator/
│
├── .github/                   # GitHub Actions for running acceptance tests
├── pages/                     # Page Object Model classes for the calculator app
│   ├── __init__.py            # Init file for package
│   ├── base_page.py           # Base class for all Page Object classes
│   └── calculator_page.py     # Specific page class for the calculator functionality
│
├── tests/                     # Test scripts folder
│   ├── __init__.py            # Init file for tests package
│   ├── conftest.py            # Conftest file for setting up fixtures (e.g., browser, context, and page)
│   ├── test_calculator.py     # Test cases for calculator functionality
│   ├── screenshots/           # Folder to store screenshots (if enabled in test scenarios)
│   └── videos/                # Folder to store videos of test runs (if enabled)
│
├── README.MD                  # Project documentation 
├── requirements.txt           # Python dependencies for the project
└── trace.zip                  # Trace file for Playwright (e.g., for debugging failures) (if enabled)
```

## Key Features

This automation framework is designed using best practices such as:

- **Python + PyTest**: PyTest is used as the primary testing framework for writing and organizing test cases. It provides fixtures, test discovery, and detailed reports.
  
- **Playwright**: Playwright is used for browser automation, enabling cross-browser testing (Chromium, Firefox, and WebKit) with fast and reliable browser interaction.

- **Page Object Model (POM)**: This design pattern abstracts the web elements and interactions into page classes (`base_page.py` and `calculator_page.py`) to keep test logic separate from implementation details, promoting reusability and maintainability.

- **Conftest and Fixtures**: The `conftest.py` file sets up Playwright browser instances, context management, ensuring a clean, reproducible environment for each test run.

- **Continuous Integration**: The project is structured in a way that it can be easily integrated into a CI pipeline (e.g., GitHub Actions) for running tests.

## Allure Reporting

The framework integrates **Allure** for generating test results reports. Allure helps visualize test results with features like:

- Visual representation of the test case history, outcomes, and trends.
- Detailed test execution steps, logs embedded in the report.
- Easy navigation through failed tests, passed tests, and skipped ones.
- Reports are automatically generated and accessible through **GitHub Pages** after every CI run.

## Technologies Used

- **Python**: The main programming language for writing test scripts.
- **PyTest**: For managing and running the tests, with a wide range of powerful features like fixtures and parameterization.
- **Playwright**: A modern browser automation library that supports headless browsing and cross-browser compatibility.
- **Page Object Model (POM)**: A design pattern that enhances test maintainability and readability by abstracting page interactions.
- **Conftest**: PyTest’s `conftest.py` is used to define fixtures for setting up browser contexts, pages, and other reusable components.
- **Video and Trace**: Playwright allows the recording of video traces for every test, aiding in debugging and understanding test failures.

## Test Cases Overview

| **Test Case**                           | **Description**                                                                                                                                                          | **Parameters/Examples**                                                                                                |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Calculator Buttons Presence**         | Verifies that all digit buttons (0-9), operator buttons (+, -, ×, ÷), and special buttons (AC/CE) are present and visible.                                               | N/A                                                                                                                    |
| **Basic Operations**                    | Tests basic calculator operations such as addition, subtraction, multiplication, and division.                                                                           | `5 + 6 = 11` <br> `10 - 3 = 7` <br> `100 × 100 = 10000` <br> `50 ÷ 5 = 10`                                              |
| **Negative Number Operations**          | Tests operations involving negative numbers for addition, subtraction, multiplication, and division.                                                                     | `-5.5 + 2.2 = -3.3` <br> `-10.1 - 3.5 = -13.6` <br> `2.5 × -2 = -5` <br> `-7.5 ÷ -2.5 = 3`                              |
| **Float Operations**                    | Tests calculator operations involving floating-point numbers to check for precision and correctness.                                                                     | `5.5 + 2.2 = 7.7` <br> `10.1 - 3.5 = 6.6` <br> `7.5 ÷ 2.5 = 3`                                                         |
| **Large Number Operations**             | Tests large number operations, ensuring that the calculator handles big numbers and scientific notation correctly.                                                       | `1000000000 + 2000000000 = 3000000000` <br> `999999999999 - 1 = 999999999998` <br> `5000000000 × 2000000000 = 1e+19`    |
| **Operations with Zero**                | Tests operations involving zero, including addition, subtraction, multiplication, and division by zero.                                                                  | `5 ÷ 0 = Infinity` <br> `0 ÷ 5 = 0` <br> `0 ÷ 0 = Error` <br> `0 + 5 = 5` <br> `5 × 0 = 0`                              |
| **Decimal Precision**                   | Tests the precision of decimal results, ensuring that the calculator rounds or truncates results correctly.                                                              | `1 ÷ 3 = 0.3333333333` <br> `10 ÷ 6 = 1.6666666667`                                                                    |
| **Using Result in Next Operation**      | Tests that the result from one operation can be used as input for the next operation.                                                                                    | `5 + 5 = 10` then `× 2 = 20` <br> `8 ÷ 2 = 4` then `+ 3 = 7`                                                            |
| **Successive Equals Presses**           | Tests pressing the equal button multiple times to ensure that the result stays the same (no changes after the first result).                                             | `5 + 2 = 7` (press equal multiple times, result stays `7`) <br> `4 × 3 = 12` (press equal multiple times, stays `12`)   |
| **Clean All (AC) Functionality**        | Tests the functionality of the **Clear All (AC)** button after performing operations, ensuring it resets the display to `0`.                                             | `5 + 9 = 14` (clear display and verify reset) <br> `10 - 3 = 7` (clear display and check memory retains result)          |
| **Step-by-Step Clean Entry (CE)**       | Tests the **Clear Entry (CE)** functionality step-by-step after entering operations but before pressing equal, reducing the expression incrementally until it's cleared. | `5 + 9` (clear in steps: `5 + 9`, `5 +`, `5`, `0`) <br> `100 × 2` (clear in steps: `100 × 2`, `100 ×`, `100`, `0`)      |

## Useful Commands for PyTest and Playwright

### PyTest Commands
- **Run all tests**:
  ```bash
  pytest
  ```

- **Run a specific test**:
  ```bash
  pytest tests/test_calculator.py::test_calculator_basic_operations
  ```

- **Generate HTML report**:
  ```bash
  pytest --html=report.html
  ```

- **Run tests with verbose output**:
  ```bash
  pytest -v
  ```

- **Run tests and show extra logging (useful for debugging)**:
  ```bash
  pytest -s
  ```

- **Run tests in parallel (e.g., 4 workers)**:
  ```bash
  pytest -n 4
  ```

- **Only run tests that failed last time**:
  ```bash
  pytest --lf
  ```

- **Run tests and stop after the first failure**:
  ```bash
  pytest -x
  ```

### Playwright Commands
- **Install Playwright Browsers** (if not already installed):
  ```bash
  playwright install
  ```

- **Run Playwright tests with a specific browser** (e.g., Chromium):
  ```bash
  pytest --browser chromium
  ```

## How to Run the Tests

1. **Install Dependencies**:
   Ensure all required Python packages are installed by running:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Tests**:
   Execute the following command from the root of the project:

   ```bash
   pytest tests/test_calculator.py
   ```

3. **View Test Reports**:
   Allure reports integrated in GitHub Actions flow. 

--- 

