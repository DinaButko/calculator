from pages.base_page import BasePage


class CalculatorPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators for calculator buttons
        self.equal_button = "[jsname='Pt8tGc']"
        self.add_button = "[jsname='XSr6wc']"
        self.subtract_button = "[jsname='pPHzQc']"
        self.multiply_button = "[jsname='YovRWb']"
        self.divide_button = "[jsname='WxTTNd']"
        self.clear_all_button = "[jsname='SLn8gc']"  # AC button
        self.clear_entry_button = "[aria-label='clear entry']"  # CE button
        self.result_field_selector = "[jsname='VssY5c']"  # Result of calculation
        self.expression_field_selector = "[jsname='ubtiRe']"

        # Locators for digit buttons
        self.digit_buttons = {
            '0': "[jsname='bkEvMb']",
            '1': "[jsname='N10B9']",
            '2': "[jsname='lVjWed']",
            '3': "[jsname='KN1kY']",
            '4': "[jsname='xAP7E']",
            '5': "[jsname='Ax5wH']",
            '6': "[jsname='abcgof']",
            '7': "[jsname='rk7bOd']",
            '8': "[jsname='T7PMFe']",
            '9': "[jsname='XoxYJ']",
            '.': "[jsname='YrdHyf']",
        }

    def enter_number(self, number: str):
        """Enter a number by pressing the corresponding digit buttons, including negative numbers."""
        # Check if the number is negative
        if number.startswith('-'):
            self.click(self.subtract_button)
            number = number[1:]

        # Enter each digit
        for digit in number:
            if digit in self.digit_buttons:
                self.click(self.digit_buttons[digit])
            else:
                raise ValueError(f"Invalid character '{digit}'. Must be 0-9, '.' or '-' at the start.")

        return self

    def add(self):
        """Click the add (+) button."""
        self.click(self.add_button)
        return self

    def subtract(self):
        """Click the subtract (-) button."""
        self.click(self.subtract_button)
        return self

    def multiply(self):
        """Click the multiply (×) button."""
        self.click(self.multiply_button)
        return self

    def divide(self):
        """Click the divide (÷) button."""
        self.click(self.divide_button)
        return self

    def click_equal(self):
        """Click the equal (=) button."""
        self.click(self.equal_button)
        return self

    def assert_calculation_result(self, expected_result: str):
        """Assert that the result field contains the expected result."""
        self.is_visible(selector=self.result_field_selector)
        self.assert_text(self.result_field_selector, expected_result)
        return self

    def get_expression_text(self) -> str:
        """Get the current expression displayed in the calculator."""
        self.is_visible(selector=self.expression_field_selector)
        return self.get_text(self.expression_field_selector).strip()

    def clear_entry(self):
        """Click the 'Clear Entry' (CE) button."""
        self.page.click(self.clear_entry_button)

    def clear_all(self):
        """Click the clear (AC) button."""
        self.is_all_clear_visible()
        self.click(self.clear_all_button)
        return self

    def is_clear_entry_visible(self):
        """Check if the CE (clear entry) button is visible."""
        return self.page.locator(self.clear_entry_button).is_visible()

    def is_all_clear_visible(self):
        """Check if the AC (all clear) button is visible."""
        return self.page.locator(self.clear_all_button).is_visible()
