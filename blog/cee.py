from datetime import datetime

# Example string representing a date
date_string = "2022-01-15"

# Use datetime.strptime to parse the string into a datetime object
formatted_date = datetime.strptime(date_string, "%Y-%m-%d")

# Now, formatted_date is a datetime object
print(formatted_date)

from datetime import datetime

date_string = "01/03/2022"

# Use datetime.strptime to parse the string into a datetime object
formatted_date = datetime.strptime(date_string, "%m/%d/%Y")

# Now, formatted_date is a datetime object
print(formatted_date)
