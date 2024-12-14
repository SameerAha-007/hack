import mysql.connector
from mysql.connector import Error

def insert_product_data(product_id, product_name, product_price, merchant):
    """
    Stores product data into the MySQL database.
    :param product_id: str, product ID
    :param product_name: str, product name
    :param product_price: float, product price
    :param merchant: str, merchant name
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',         
            database='your_database', 
            user='your_username',     
            password='your_password'  
        )

        if connection.is_connected():
            cursor = connection.cursor()

            query = '''INSERT INTO products (product_id, product_name, product_price, merchant)
                       VALUES (%s, %s, %s, %s)'''

            values = (product_id, product_name, product_price, merchant)

            cursor.execute(query, values)
            connection.commit()

            print("Product data inserted successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    insert_product_data("P12345", "Laptop", 799.99, "Amazon")
