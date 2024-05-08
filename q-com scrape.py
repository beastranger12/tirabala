import re
import csv

def parse_product_line(line):
    # Detect lines without numbers and assume they are categories
    if not re.search(r'\d', line):
        return None, line.strip()  # Returns the category name

    # Extract discount
    discount_match = re.search(r'(\d+)% Off', line)
    discount = discount_match.group(1) + '%' if discount_match else ''

    # Remove the discount part for easier processing
    clean_line = re.sub(r'\d+% Off', '', line)

    # Remove 'Add to Cart' text
    clean_line = re.sub(r'Add to Cart', '', clean_line)

    # Extract prices and measurement
    prices = re.findall(r'₹(\d+)', clean_line)
    measurement = re.search(r'(\d+\.?\d* [mg]l?)', clean_line)

    title = clean_line.split('₹')[0].strip()
    measurement_value = measurement.group(1) if measurement else ''

    # Handle price fields based on the extracted prices
    if len(prices) == 1:
        mrp = selling_price = prices[0]
    elif len(prices) > 1:
        selling_price, mrp = prices[0], prices[-1]

    return [title, mrp, selling_price, discount if discount else '', measurement_value], None

def process_file(input_file, output_file):
    current_category = ''
    products = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            parsed_data, category = parse_product_line(line)
            if category:
                current_category = category  # Update the current category
            elif parsed_data:
                products.append([current_category] + parsed_data)  # Add product data with category

    # Write data to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['L1', 'Title', 'MRP', 'Selling Price', 'Discount', 'Measurement Value'])
        writer.writerows(products)

# Example usage
process_file('input.txt', 'output.csv')
