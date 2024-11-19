import pytest
from pages.calculator_page import CalculatorPage
from tests.conftest import log

"""
Acceptance Tests For Google Calculator
"""


def perform_operation(calculator, numbers, operations, click_equal=True):
    """
    Helper function to enter multiple numbers and perform the specified sequence of operations.

    :param calculator: The calculator object
    :param numbers: A list of numbers
    :param operations: A list of operations (e.g., ['+', '-', '×'])
    :param click_equal: Boolean to determine whether to click the equal button or not
    """

    # Handle the first number separately (no operation before the first number)
    num1 = numbers[0]

    # Handle negative numbers for the first number
    if num1.startswith('-'):
        calculator.subtract()
        num1 = num1[1:]

    calculator.enter_number(num1)

    # Iterate over remaining numbers and operations
    for i in range(1, len(numbers)):
        operation = operations[i - 1]
        num = numbers[i]

        # Perform the operation based on the symbol
        if operation == '+':
            calculator.add()
        elif operation == '-':
            calculator.subtract()
        elif operation == '×':
            calculator.multiply()
        elif operation == '÷':
            calculator.divide()

        # Handle negative numbers
        if num.startswith('-'):
            calculator.subtract()
            num = num[1:]

        calculator.enter_number(num)

    # Only click equal if the click_equal flag is True for the test
    if click_equal:
        calculator.click_equal()


# Helper function to assert results and expressions
def assert_results(calculator, expected_result, expected_expression):
    """
    Helper function to verify that the result and expression are as expected.
    """

    calculator_page = CalculatorPage(page=calculator.page)
    calculator_page.is_visible(selector=calculator_page.expression_field_selector)

    # Verify that the operation is visible for the user on the input calculator field
    actual_expression = calculator.get_expression_text().replace('−', '-')
    assert actual_expression == expected_expression, f"Expected expression '{expected_expression}'," \
                                                     f" but got '{actual_expression}'"

    # Verify the result of calculation
    calculator.assert_calculation_result(expected_result)


# Test case for verifying buttons presence
def test_all_buttons_calculator_present(setup_calculator):
    """Verify that all required buttons (digits and operations) for the calculator are present."""
    log.info("Test 'test_all_buttons_calculator_present' has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Helper function to verify buttons
    def verify_buttons(buttons_dict):
        for button, selector in buttons_dict.items():
            assert calculator.is_visible(selector), f"Button '{button}' is not visible"

    # Verify digit buttons (0-9 and '.')
    verify_buttons(calculator.digit_buttons)

    # Verify operator buttons
    operator_buttons = {
        '+': calculator.add_button,
        '-': calculator.subtract_button,
        '×': calculator.multiply_button,
        '÷': calculator.divide_button,
        '=': calculator.equal_button,
        'AC': calculator.clear_all_button,
    }
    verify_buttons(operator_buttons)

    log.info("Test 'test_all_buttons_calculator_present' successfully completed")


@pytest.mark.parametrize("numbers, operations, expected_result, expected_expression", [
    (['5', '6'], ['+'], '11', '5 + 6 ='),
    (['10', '3'], ['-'], '7', '10 - 3 ='),
    (['100', '100'], ['×'], '10000', '100 × 100 ='),
    (['50', '5'], ['÷'], '10', '50 ÷ 5 ='),
    (['5', '3', '2', '8'], ['+', '-', '+'], '14', '5 + 3 - 2 + 8 =')
])
def test_basic_calculator_operations(setup_calculator, numbers, operations, expected_result, expected_expression):
    """Parametrized test for basic calculator operations with multiple numbers and operations"""
    log.info(f" 'test_basic_calculator_operations' for {numbers} with operations {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, numbers, operations)

    # Assert the final result
    assert_results(calculator, expected_result, expected_expression)

    log.info(f"Test for {numbers} with operations {operations} successfully completed with result {expected_result}")


@pytest.mark.parametrize("numbers, operations, expected_result, expected_expression", [
    (['-5.5', '2.2'], ['+'], '-3.3', '-5.5 + 2.2 ='),
    (['-10.1', '3.5'], ['-'], '-13.6', '-10.1 - 3.5 ='),
    (['2.5', '-2'], ['×'], '-5', '2.5 × -2 ='),
    (['-7.5', '-2.5'], ['÷'], '3', '-7.5 ÷ -2.5 ='),
    (['-0.1', '-0.2'], ['+'], '-0.3', '-0.1 - 0.2 =')
])
def test_calculator_negative_number_operations(setup_calculator, numbers, operations, expected_result,
                                               expected_expression):
    """Parametrized test for calculator operations involving negative numbers"""
    log.info(f" 'test_calculator_negative_number_operations' for {numbers} with operations {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, numbers, operations)

    # Assert the final result
    assert_results(calculator, expected_result, expected_expression)

    log.info(f"Test for {numbers} with operations {operations} successfully completed with result {expected_result}")


@pytest.mark.parametrize("numbers, operations, expected_result, expected_expression", [
    (['5.5', '2.2'], ['+'], '7.7', '5.5 + 2.2 ='),
    (['10.1', '3.5'], ['-'], '6.6', '10.1 - 3.5 ='),
    (['2.5', '2'], ['×'], '5', '2.5 × 2 ='),
    (['7.5', '2.5'], ['÷'], '3', '7.5 ÷ 2.5 ='),
    (['0.1', '0.2'], ['+'], '0.3', '0.1 + 0.2 =')
])
def test_calculator_basic_float_operations(setup_calculator, numbers, operations, expected_result, expected_expression):
    """Parametrized test for basic calculator operations with float numbers"""
    log.info(f" 'test_calculator_basic_float_operations' for {numbers} with operations {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, numbers, operations)

    # Assert the final result
    assert_results(calculator, expected_result, expected_expression)

    log.info(f"Test for {numbers} with operations {operations} successfully completed with result {expected_result}")


@pytest.mark.parametrize("numbers, operations, expected_result, expected_expression", [
    (['1000000000', '2000000000'], ['+'], '3000000000', '1000000000 + 2000000000 ='),
    (['999999999999', '1'], ['-'], '999999999998', '999999999999 - 1 ='),
    (['5000000000', '2000000000'], ['×'], '1e+19', '5000000000 × 2000000000 ='),
    (['1000000000000', '1000000'], ['÷'], '1000000', '1000000000000 ÷ 1000000 =')
])
def test_calculator_large_number_operations(setup_calculator, numbers, operations, expected_result,
                                            expected_expression):
    """Parametrized test for calculator operations involving large numbers"""
    log.info(f" 'test_calculator_large_number_operations' for {numbers} with operations {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, numbers, operations)

    # Assert the final result
    assert_results(calculator, expected_result, expected_expression)

    log.info(f"Test for {numbers} with operations {operations} successfully completed with result {expected_result}")


@pytest.mark.parametrize("numbers, operations, expected_result, expected_expression", [
    (['0', '5'], ['+'], '5', '0 + 5 ='),
    (['5', '0'], ['+'], '5', '5 + 0 ='),
    (['0', '5'], ['-'], '-5', '0 - 5 ='),
    (['5', '0'], ['-'], '5', '5 - 0 ='),
    (['0', '5'], ['×'], '0', '0 × 5 ='),
    (['5', '0'], ['×'], '0', '5 × 0 ='),
    (['5', '0'], ['÷'], 'Infinity', '5 ÷ 0 ='),
    (['0', '5'], ['÷'], '0', '0 ÷ 5 ='),
    (['0', '0'], ['÷'], 'Error', '0 ÷ 0 =')
])
def test_calculator_operations_with_zero(setup_calculator, numbers, operations, expected_result, expected_expression):
    """Parametrized test for calculator operations involving 0"""
    log.info(f" 'test_calculator_operations_with_zero' for {numbers} with operations {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, numbers, operations)

    # Assert the final result
    assert_results(calculator, expected_result, expected_expression)

    log.info(f"Test for {numbers} with operations {operations} successfully completed with result {expected_result}")


@pytest.mark.parametrize("numbers, operations, expected_result", [
    (['1', '3'], ['÷'], '0.33333333333'),
    (['10', '6'], ['÷'], '1.66666666667')
])
def test_calculator_decimal_precision(setup_calculator, numbers, operations, expected_result):
    """Test calculator precision for long decimal results like 1 ÷ 3."""
    log.info(f" 'test_calculator_decimal_precision' for {numbers} with operations {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, numbers, operations)

    # Assert the final result
    calculator.assert_calculation_result(expected_result)

    log.info(f"Test for {numbers} with operations {operations} completed with expected result {expected_result}")


@pytest.mark.parametrize("initial_numbers, initial_operations, next_operation, expected_result", [
    (['5', '5'], ['+'], ('×', '2'), '20'),  # Result from 5 + 5 = 10, then 10 × 2 = 20
    (['8', '2'], ['÷'], ('+', '3'), '7'),  # Result from 8 ÷ 2 = 4, then 4 + 3 = 7
    (['10', '2'], ['×'], ('+', '3'), '23')  # Result from 10 × 2 = 20, then 20 + 3 = 23
])
def test_calculator_use_result_in_next_operation(setup_calculator, initial_numbers, initial_operations, next_operation,
                                                 expected_result):
    """Test using the result of one operation in the next operation."""
    log.info(
        f" 'test_calculator_use_result_in_next_operation' for {initial_numbers} with operations {initial_operations} then {next_operation} has started")

    calculator = setup_calculator

    # Perform initial operation
    perform_operation(calculator, initial_numbers, initial_operations)

    # Perform the next operation using the result of the first operation
    next_operator, next_number = next_operation

    # Perform the next operation based on the operator
    if next_operator == '+':
        calculator.add()
    elif next_operator == '-':
        calculator.subtract()
    elif next_operator == '×':
        calculator.multiply()
    elif next_operator == '÷':
        calculator.divide()

    # Enter the next number and complete the operation
    calculator.enter_number(next_number)
    calculator.click_equal()

    # Assert the final result
    calculator.assert_calculation_result(expected_result)

    log.info(f"Test for {initial_numbers} followed by {next_operation} completed with result {expected_result}")


@pytest.mark.parametrize("initial_numbers, initial_operations, expected_result", [
    (['5', '2'], ['+'], '7'),  # 5 + 2 = 7, pressing equal again should still be 7
    (['4', '3'], ['×'], '12')  # 4 × 3 = 12, pressing equal again should still be 12
])
def test_calculator_successive_equals(setup_calculator, initial_numbers, initial_operations, expected_result):
    """Test that pressing equal repeatedly does not change the result in Google Calculator."""
    log.info(f" 'test_calculator_successive_equals' for {initial_numbers} {initial_operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    # Perform the initial operation
    perform_operation(calculator, initial_numbers, initial_operations)

    # Verify the first result after pressing equal
    calculator.assert_calculation_result(expected_result)

    # Press equals multiple times and verify that the result stays the same
    for _ in range(3):
        calculator.click_equal()
        calculator.assert_calculation_result(expected_result)

    log.info(f"Test for successive equals on {initial_numbers} completed successfully")


@pytest.mark.parametrize("numbers, operations, expected_result, expected_expression", [
    (['5', '9'], ['+'], '14', '5 + 9 ='),
    (['10', '3'], ['-'], '7', '10 - 3 ='),
    (['100', '2'], ['×'], '200', '100 × 2 ='),
    (['50', '5'], ['÷'], '10', '50 ÷ 5 =')
])
def test_calculator_clear_all_functionality(setup_calculator, request, numbers, operations, expected_result,
                                            expected_expression):
    """
    Parametrized test to verify the 'Clear All' (AC) functionality after operations.
    """

    # Set flag to skip teardown in this specific test
    request.node.skip_teardown = True

    log.info(f"'test_calculator_clean_functionality' for {numbers} {operations} has started")

    # Initialize calculator for the test
    calculator = setup_calculator

    calculator_page = CalculatorPage(page=calculator.page)

    # Perform the operation
    perform_operation(calculator, numbers, operations, click_equal=True)

    # Verify the full operation expression and result
    calculator.is_visible(selector=calculator_page.expression_field_selector)
    actual_expression = calculator.get_expression_text().replace('−', '-')
    assert actual_expression == expected_expression, \
        f"Expected expression '{expected_expression}', but got '{actual_expression}'"

    calculator.assert_calculation_result(expected_result)

    # Test Clear All (AC) functionality
    calculator.clear_all()

    # Verify the display is reset to 0 after clearing
    calculator.assert_calculation_result('0')

    # Verify that the memory retains the previous result as "Ans = X"
    actual_memory_display = calculator.get_expression_text().replace('−', '-')
    expected_memory_display = f"Ans = {expected_result}"
    assert actual_memory_display == expected_memory_display, \
        f"Expected memory display '{expected_memory_display}', but got '{actual_memory_display}'"

    log.info(
        f"Test for {numbers} with operations {operations} successfully completed with clean functionality and memory "
        f"retention validated")


@pytest.mark.parametrize("numbers, operations, stepwise_expressions", [
    (['5', '9'], ['+'], ['5 + 9', '5 +', '5', '0']),  # Step-by-step clearing for '5 + 9'
    (['5', '3'], ['-'], ['5 - 3', '5 -', '5', '0']),  # Step-by-step clearing for '5 - 3'
    (['5', '1'], ['×'], ['5 × 1', '5 ×', '5', '0']),  # Step-by-step clearing for '5 × 1'
    (['5', '5'], ['÷'], ['5 ÷ 5', '5 ÷', '5', '0'])  # Step-by-step clearing for '5 ÷ 5'
])
def test_calculator_step_by_step_cleaning(setup_calculator, request, numbers, operations, stepwise_expressions):
    """
    Parametrized test to verify step-by-step clearing of the calculator expression
    after entering the operation and the second number, but without pressing the equal button.
    The expression should reduce step by step until fully cleared.
    """

    log.info(f"'test_calculator_step_by_step_cleaning_without_equal' for {numbers} {operations} has started")

    # Set flag to skip teardown in this specific test
    request.node.skip_teardown = True

    # Initialize calculator for the test
    calculator = setup_calculator

    # Step 1: Enter the full expression without pressing equal using perform_operation but don't click equal
    perform_operation(calculator, numbers, operations, click_equal=False)

    # Step 2: Clear the expression step by step, excluding the result
    for i in range(len(stepwise_expressions)):
        # Verify that the expression/result is reduced step by step
        expected_expression = stepwise_expressions[i]
        calculator.assert_calculation_result(expected_expression)

        # Press the clear button 
        if i < len(stepwise_expressions) - 1:
            if calculator.is_clear_entry_visible():
                calculator.clear_entry()  # Use Clear Entry (CE)
            elif calculator.is_all_clear_visible():
                calculator.all_clear()  # Use All Clear (AC)

    # At the final step, the expression should be empty or show '0'
    calculator.assert_calculation_result('0')

    log.info(f"Test for {numbers} {operations} successfully completed with step-by-step clearing")
