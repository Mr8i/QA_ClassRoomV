import os.path

# Initialise empty lists to store company data
companies = []
sales = []


# Check if the file exists
if os.path.exists("carSale.csv"):
    with open("carSale.csv", "r") as file:
        lines = file.readlines()

        # Process the file line by line
        for i in range(0, len(lines), 2):
            companies.append(lines[i].strip())

            data = lines[i + 1].strip().split(',')
            sales.append(list(map(int, data)))

else:
    print("Error: The file 'carSale.csv' does not exist.")
    exit()


# Calculate the sum of cars sold in each month in a column
monthly_sales = [sum(month) for month in zip(*sales)]

# "" "" total yearly sales by each manufacturer in a row
yearly_sales = [sum(company_sales) for company_sales in sales]

# "" "" the grand total of all car.py sales
grand_total = sum(yearly_sales)


# Display the results
print("\nMonthly sales totals:")
for total in monthly_sales:
    print(total)

print("\nYearly sales totals by manufacturer:")
for company, total in zip(companies, yearly_sales):
    print(f"{company}: {total}")

print("\nGrand total of all car.py sales:", grand_total)


# Save the results into an output file
with open("car_sales_summary.txt", "w") as output_file:
    output_file.write("Monthly sales totals:\n")
    for total in monthly_sales:
        output_file.write(str(total) + "\n")

    output_file.write("\nYearly sales totals by manufacturer:\n")
    for company, total in zip(companies, yearly_sales):
        output_file.write(f"{company}: {total}\n")

    output_file.write("\nGrand total of all car.py sales: " + str(grand_total))

print("\nResults have been saved to 'car_sales_summary.txt'")
