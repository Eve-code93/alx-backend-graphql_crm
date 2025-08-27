#!/usr/bin/env python3
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def main():
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        orders(lastWeek: true) {
            id
            customer {
                email
            }
        }
    }
    """)

    result = client.execute(query)
    orders = result.get("orders", [])

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/order_reminders_log.txt", "a") as f:
        for order in orders:
            f.write(f"{timestamp} - Order ID: {order['id']} - Email: {order['customer']['email']}\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
