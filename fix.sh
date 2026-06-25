echo 'FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true'
sed -i 's/uses: actions\/checkout@v4/uses: actions\/checkout@v4/g' .github/workflows/*.yml
sed -i 's/uses: actions\/setup-node@v4/uses: actions\/setup-node@v4/g' .github/workflows/*.yml
sed -i 's/uses: actions\/setup-python@v5/uses: actions\/setup-python@v5/g' .github/workflows/*.yml
sed -i 's/uses: actions\/upload-artifact@v4/uses: actions\/upload-artifact@v4/g' .github/workflows/*.yml
