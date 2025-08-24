import pandas as pd

df = pd.read_excel("/home/dcsadmin/Documents/PersonalisedGreeting/Database/EmployeePreference.xlsx", engine='openpyxl')

# Function to generate a birthday greeting card based on NGS
def generate_birthday_card(ngs):
    if ngs not in df['NGS'].values:\
        return "NGS not found in the database. Please enter a valid NGS."

    employee_data = df[df['NGS'] == ngs].iloc[0]

    greeting_card = (
        f"Create a heartwarming and visually appealing image that captures the essence of "
        f"{employee_data['RITU']} in {employee_data['TRAVEL']} incorporating {employee_data['COLOUR']} as the background color. "
        f"The image should radiate positivity and excitement."
    )

    return greeting_card

# Get NGS from the user
user_ngs = int(input("Enter the NGS of the employee: "))

# Store the name of the user-entered NGS in a variable named 'Text'
Text = df[df['NGS'] == user_ngs]['NAME'].values[0]
print("Name: ", Text)

# Generate birthday greeting card and store it in the 'prompt' variable
prompt = generate_birthday_card(user_ngs)

# Print the generated string or error message
print("\n",prompt)