import user_order_ops as ops
from decimal import Decimal

if __name__ == '__main__':
    ops.create_user("aarchamb", "Adam Archambault", "aarchambault0@wikipedia.org")
    aarchamb_home   = {
        "street": "1716 Fulton Lane",
        "state": "Csongrád",
        "country": "Hungary"
    } 
    aarchamb_office = {
        "street": "6 Manitowish Place",
        "state": "Csongrád",
        "country": "Hungary"
    }
    ops.add_address("aarchamb", "home", aarchamb_home)
    ops.add_address("aarchamb", "office",aarchamb_office)
    
    ops.create_user("tgrimes1", "Trent Grimes", "tgrimes1@hostgator.com")
    tgrimes1_home   = {
        "street": "98905 Declaration Parkway",
        "country": "Honduras"
    } 
    ops.add_address("tgrimes1", "home", aarchamb_home)
    
    shopping_cart1 = [
        {
            'product_name' : 'New Apple MacBook Pro',
            'price'        : Decimal('2018.42'),
            'quantity'     : 1
        },
        {
            'product_name' : 'Nintendo Switch',
            'price'        : Decimal('368.95'),
            'quantity'     : 1
        },
        {
            'product_name' : 'Seagate Portable 2TB External',
            'price'        : Decimal('59.95'),
            'quantity'     : 1
        }
        ]
    
    shopping_cart2 = [
        {
            'product_name' : 'New Apple MacBook Pro',
            'price'        : Decimal('2018.42'),
            'quantity'     : 1
        },
        {
            'product_name' : 'Charmin Ultra Soft Cushiony Touch Toilet Paper',
            'price'        : Decimal('0.49'),
            'quantity'     : 10
        },
        {
            'product_name' : 'The Legend of Zelda: Breath of the Wild',
            'price'        : Decimal('74.94'),
            'quantity'     : 1
        }
        ]
        
    shopping_cart3 = [
        {
            'product_name' : 'HyperX Fury 16GB',
            'price'        : Decimal('39.99'),
            'quantity'     : 2
        },
        {
            'product_name' : 'Jenga Classic Game',
            'price'        : Decimal('19.99'),
            'quantity'     : 1
        },
        {
            'product_name' : 'Tasha\'s Cauldron of Everything',
            'price'        : Decimal('49.95'),
            'quantity'     : 3
        }
        ]
        
    ops.checkout("aarchamb", "home", shopping_cart1)
    ops.checkout("tgrimes1", "home", shopping_cart2)
    ops.checkout("tgrimes1", "home", shopping_cart3)