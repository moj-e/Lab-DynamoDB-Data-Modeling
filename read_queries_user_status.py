import user_order_ops as ops

if __name__ == '__main__':
    
    orders = ops.query_user_orders_by_status("tgrimes1", "Pending")

    for order in orders:
        print(order)
        