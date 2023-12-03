import xml.etree.ElementTree as ET
import time
from datetime import datetime



class Order:
    def __init__(self, id, op, price, vol):
        self.id = id
        self.op = op
        self.price = price
        self.vol = vol

class OrderBook:
    def __init__(self):
        self.b_orders = []
        self.s_orders = []

def initiate(file_path):
    order_books = {}
    start = time.time()

    start_datetime = datetime.fromtimestamp(start)
    print(f"Processing started at: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    


    temp = ET.parse(file_path)
    temp_root = temp.getroot()

    for element in temp_root:
        if element.tag == "AddOrder":
            book_name = element.attrib["book"]
            id = int(element.attrib["orderId"])
            op = element.attrib["operation"]
            price = float(element.attrib["price"])
            vol = int(element.attrib["volume"])

            if book_name not in order_books:
                order_books[book_name] = OrderBook()

            order_book = order_books[book_name]
            new_order = Order(id, op, price, vol)

            if op == "BUY":
                e_rem_s_orders(order_book, new_order)
                if new_order.vol > 0:
                    insert(order_book.b_orders, new_order)
            else:
                e_rem_b_orders(order_book, new_order)
                if new_order.vol > 0:
                    insert(order_book.s_orders, new_order)

    for book_name, order_book in order_books.items():
        print(f"book: {book_name}")
        print(" Buy -- Sell")
        print("==================================")
        for buy_order, sell_order in zip(order_book.b_orders, order_book.s_orders):
            print(f" {buy_order.vol}@{buy_order.price:.2f} -- {sell_order.vol}@{sell_order.price:.2f}")
        if len(order_book.b_orders) > len(order_book.s_orders):
            for buy_order in order_book.b_orders[len(order_book.s_orders):]:
                print(f" {buy_order.vol}@{buy_order.price:.2f} --")
        elif len(order_book.s_orders) > len(order_book.b_orders):
            for sell_order in order_book.s_orders[len(order_book.b_orders):]:
                print(f" -- {sell_order.vol}@{sell_order.price:.2f}")

    end_time = time.time()
    end_datetime = datetime.fromtimestamp(end_time)
    
    print(f"Processing completed at: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Processing Duration: {:.3f} seconds".format(end_time - start))


def e_rem_s_orders(order_book, new_order):
    s_orders = order_book.s_orders
    i = 0
    while i < len(s_orders):
        sell_order = s_orders[i]
        if new_order.price >= sell_order.price:
            execution_volume = min(new_order.vol, sell_order.vol)
            new_order.vol -= execution_volume
            sell_order.vol -= execution_volume
            if sell_order.vol == 0:
                s_orders.pop(i)
            if new_order.vol == 0:
                break
        else:
            break

def e_rem_b_orders(order_book, new_order):
    b_orders = order_book.b_orders
    i = 0
    while i < len(b_orders):
        buy_order = b_orders[i]
        if new_order.price <= buy_order.price:
            execution_volume = min(new_order.vol, buy_order.vol)
            new_order.vol -= execution_volume
            buy_order.vol -= execution_volume
            if buy_order.vol == 0:
                b_orders.pop(i)
            if new_order.vol == 0:
                break
        else:
            break

def insert(orders, new_order):
    for i, order in enumerate(orders):
        if new_order.op == "BUY" and new_order.price > order.price:
            break
        if new_order.op == "SELL" and new_order.price < order.price:
            break
    else:
        i = len(orders)
    orders.insert(i, new_order)

if __name__ == "__main__":
    initiate("orders 1.xml")
