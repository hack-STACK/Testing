#!/bin/bash

clear

echo "========================================="
echo " Authentication Test Suite"
echo "========================================="
echo ""

echo "Register Test"
pytest tests/authentication/test_register.py -q

echo ""
echo "Login Test"
pytest tests/authentication/test_login.py -q

echo ""
echo "Logout Test"
pytest tests/authentication/test_logout.py -q

echo ""
echo "Delete Account Test"
pytest tests/authentication/test_delete_account.py -q

echo ""
echo "Generating HTML Report..."
pytest tests/authentication \
    --html=reports/authentication_report.html \
    --self-contained-html -q

echo ""
echo "========================================="
echo " Authentication Completed"
echo " HTML Report : reports/authentication_report.html"
echo "========================================="