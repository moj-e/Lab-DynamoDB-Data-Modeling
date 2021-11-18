import user_order_ops as ops
from decimal import Decimal

if __name__ == '__main__':
    
    orders = ops.query_pending_orders()

    for order in orders:
        order_id = order['sk'][7:]
        user_id = order['pk'][6:]
        print()
        print('Status:', order['status'])
        print('Order:', order_id, 'for', user_id, 'to', order['address'], 'address')
        print('Items:')
        items = ops.query_order_items(order_id)
        for item in items:
            print(item['product_name'], 'x', item['quantity'])