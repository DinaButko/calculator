#!/bin/bash

# Run for Chromium
echo "Running tests on Chromium..."
pytest --reruns 2 --reruns-delay 5 --html=reports/results/chromium_report.html --self-contained-html --browser chromium

# Run for Firefox
echo "Running tests on Firefox..."
pytest --reruns 2 --reruns-delay 5 --html=reports/results/firefox_report.html --self-contained-html --browser firefox

# Run for WebKit
echo "Running tests on WebKit..."
pytest --reruns 2 --reruns-delay 5 --html=reports/results/webkit_report.html --self-contained-html --browser webkit

echo "All browser tests completed."

# In order to run tests
# Make executable
#chmod +x run_all_browsers.sh

#./run_all_browsers.sh