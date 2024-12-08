from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["crochet_creations"]
products_collection = db["products"]

def insert_product(name, price, description, image_path, category, color, size, material, stock_quantity, dimensions, featured):
    product = {
        "name": name,
        "price": price,
        "description": description,
        "image": image_path,
        "category": category,
        "color": color,
        "size": size,
        "material": material,
        "stock_quantity": stock_quantity,
        "dimensions": dimensions,
        "featured":featured
    }
    
    # Insert product into MongoDB
    products_collection.insert_one(product)
    print(f"Product '{name}' inserted successfully!")

# Example: Insert a product
if __name__ == "__main__":
    # You can modify these details or prompt the user for input
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    description = input("Enter product description: ")
    image_path = input("Enter product image name: ")
    category = input("Enter product category: ")
    color = input("Enter product color: ")
    size = input("Enter product size: ")
    material = input("Enter product material: ")
    stock_quantity = int(input("Enter product stock quantity: "))
    dimensions = input("Enter product dimensions: ")
    is_featured = input("is this product featured? ")
    
    featured = None
    if is_featured.lower() == "yes":
        featured = True
    elif is_featured.lower() == "no":
        featured = False
    insert_product(name, price, description, image_path, category, color, size, material, stock_quantity, dimensions, featured)