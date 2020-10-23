import sys

import companies

print(f"ARGV: {sys.argv}")

homedir = '/home/'
companies.process_all_company_files()

# order_file = os.path.join(homedir, userdir, '.market/orders.csv')
# if os.path.isfile(order_file):
# if user doesn't exist, create user and company
# if orders valid, insert into db
# if orders invalid, report error

# Load all market order files
# Check validity of each file
# Report invalid files
# Create new companies
# For each company, gather and resolve orders
# Report results to each player
# Update public market data
# Wait for next market period
