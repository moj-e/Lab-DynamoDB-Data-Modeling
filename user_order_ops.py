import boto3
from boto3.dynamodb.conditions import Key
import hashlib
import random
from datetime import date
from decimal import Decimal

def create_user(username, fullname, email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    user = {
        'pk'      : '#USER#{0}'.format(username), 
        'sk'      : 'PROFILE',
        'email'   : email,
        'address' : {}
    }
    table.put_item(Item=user)
    print("User {0} created".format(username))
    
def add_address(username, address_label, address):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    try:
        # Update item in table for the given username key.
        resp = table.update_item(
            Key={'pk' : '#USER#{0}'.format(username),
                 'sk' : 'PROFILE'
            },
            UpdateExpression='SET address.#address = :address',
            ExpressionAttributeNames={'#address' : address_label},
            ExpressionAttributeValues={':address': address},
            ConditionExpression = "attribute_not_exists(address.#address)"
            )
        print("Address added")
    except Exception as err:
        print("Error message {0}".format(err))
     
def query_user_profile(username):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sk').eq('PROFILE')
    )
    return response['Items']

def add_item(order_id, product_name, quantity, price): 
    
    item_id = hashlib.sha256(product_name.encode()).hexdigest()[:8]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    item = {
        'pk'           : '#ITEM#{0}'.format(item_id), 
        'sk'           : '#ORDER#{0}'.format(order_id),
        'product_name' : product_name,
        'quantity'     : quantity,
        'price'        : price,
        'status'       : "Pending",
    }
    table.put_item(Item=item)
    print("Added {0} to order {1}".format(product_name, order_id))
    
def checkout(username, address, items): 
    # Generate order ID. In real life, there are better
    # ways of doing this
    order_id = hashlib.sha256(str(random.random()).encode()).hexdigest()[:random.randrange(1, 20)]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    today = date.today()
    order_date = today.strftime("%b-%d-%Y")
    
    item = {
        'pk'      : '#USER#{0}'.format(username), 
        'sk'      : '#ORDER#{0}'.format(order_id),
        'date'    : order_date,
        'address' : address,
        'status'  : "Pending",
        'sd'      : '#Pending#{0}'.format(order_date)
    }
    table.put_item(Item=item)
    
    for item in items:
        add_item(order_id, 
                 item['product_name'], 
                 item['quantity'], 
                 item['price']
                 )

def query_order_items(order_id):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        IndexName='inverted-index',
        KeyConditionExpression=Key('sk').eq('#ORDER#{0}'.format(order_id)) & 
                               Key('pk').begins_with('#ITEM#')
    )
    return response['Items']

def query_user_orders_by_status(username, status):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        IndexName='sd_lsi',
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sd').begins_with('#{0}#'.format(status))
    )
    return response['Items']

def query_user_orders_by_status_and_date(username, status, date):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        IndexName='sd_lsi',
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sd').eq('#{0}#{1}'.format(status, date))
    )
    return response['Items']
    
def query_pending_orders():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        IndexName='status_gsi',
        KeyConditionExpression=Key('status').eq("Pending") & 
                               Key('pk').begins_with('#USER#')
    )
    return response['Items']