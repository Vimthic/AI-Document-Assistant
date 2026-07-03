def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

print(add(10, 20))
print(add(30, 25))
print(subtract(50, 15))
print(multiply(5, 6))

#String Handling Example:
# Raw, messy data collected from a website form
raw_user_data = [
    "   john DOe , jOhn.doe@EMAIL.com , 25 ",
    "ALICE smith , alice_smith@gmail.org , 31",
    "   bOb  , bob123@yahoo.com , 19   "
]

print("--- STARTING DATA CLEANING --- \n")

for entry in raw_user_data:
    
    parts = entry.split(",")

    # Stripping: Remove unwanted trailing and leading whitespace from each part
    raw_name = parts[0].strip()
    raw_email = parts[1].strip()
    raw_age = parts[2].strip()
    
    # Capitalizing names properly 
    name_words = raw_name.split()
    clean_name = " ".join([word.capitalize() for word in name_words])
    
    # Convert emails to strictly lowercase
    clean_email = raw_email.lower()
    
    # Type Checking & Replacing the age
    if raw_age.isdigit():
        age = int(raw_age)
    else:
        age = "Unknown"
        
    # Updates all ".org" emails to ".com"
    if clean_email.endswith(".org"):
        clean_email = clean_email.replace(".org", ".com")
        
    # Print out the final cleaned profile 
    print(f"Name: {clean_name:<15} | Email: {clean_email:<25} | Age: {age}")

print("\n--- DATA CLEANING COMPLETE ---")


# Python Collection Example
# E-Commerce Order Management and Analytics System
PRODUCT_CATALOG = (
    ("P101", "Laptop", 899.99),
    ("P102", "Smartphone", 499.99),
    ("P103", "Headphones", 89.99),
    ("P104", "Smartwatch", 199.99),
)

incoming_orders = [
    {"order_id": 1, "items": ["P101", "P103"], "customer": "Alice"},
    {"order_id": 2, "items": ["P102", "P102", "P104"], "customer": "Bob"},  
    {"order_id": 3, "items": ["P103", "P101"], "customer": "Alice"},       
    {"order_id": 4, "items": ["P105"], "customer": "Charlie"}              
]

unique_customers = set()
product_sales_count = {}
revenue_by_customer = {}

print("--- STARTING ORDER PROCESSING ---")

while len(incoming_orders) > 0:
    # Remove and get the first order in line 
    current_order = incoming_orders.pop(0)
    customer_name = current_order["customer"]
    
    print(f"\nProcessing Order #{current_order['order_id']} for {customer_name}...")
    
    # Track unique customers automatically using the set
    unique_customers.add(customer_name)
    
    # Initialize the customer's financial record in dictionary if they are new
    if customer_name not in revenue_by_customer:
        revenue_by_customer[customer_name] = 0.0

    for item_id in current_order["items"]:
        
        product_found = False
        
        # FOR LOOP: Iterates through catalog tuples to find matching product details
        for prod_id, prod_name, price in PRODUCT_CATALOG:
            if item_id == prod_id:
                # Update total customer spending in the dictionary
                revenue_by_customer[customer_name] += price
                
                # Update item popularity metrics in the sales dictionary
                product_sales_count[prod_name] = product_sales_count.get(prod_name, 0) + 1
                
                product_found = True
                print(f" - Added {prod_name} (${price})")
                break  
                
        if not product_found:
            print(f" - WARNING: Product ID '{item_id}' not found in catalog. Skipping item.")

print("\n--- DAILY BUSINESS SUMMARY ---")

print(f"Total Unique Customers Served: {len(unique_customers)} {list(unique_customers)}")

print("\nRevenue generated per customer:")
for customer, total_spent in revenue_by_customer.items():
    print(f" * {customer}: ${total_spent:.2f}")

print("\nItems Sold Inventory:")
for product, count in product_sales_count.items():
    print(f" * {product}: {count} units")
