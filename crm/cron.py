import datetime

def log_crm_heartbeat():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{now} CRM is alive\n")

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """Runs GraphQL mutation to restock products with low stock."""
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
        updateLowStockProducts {
            success
            updatedProducts
        }
    }
    """)

    result = client.execute(mutation)
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"{now} - {result['updateLowStockProducts']}\n")
