name: Check Rule ID Conflicts

on:
  pull_request:
    branches:
      - main

jobs:
  check-rule-ids:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout PR branch
        uses: actions/checkout@v3

      - name: Clone main branch to temp folder
        run: |
          git clone --depth=1 --branch=main https://github.com/${{ github.repository }} main_branch

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run rule ID conflict checker
        run: python check_rule_ids.py
