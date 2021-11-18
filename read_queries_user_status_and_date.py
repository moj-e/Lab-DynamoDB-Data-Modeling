import user_order_ops as ops
from datetime import date

if __name__ == '__main__':
    
    today = date.today()
    sample_date = today.strftime("%b-%d-%Y")
    
    orders = ops.query_user_orders_by_status_and_date("tgrimes1", "Pending", sample_date)

    for order in orders:
        print(order)
        