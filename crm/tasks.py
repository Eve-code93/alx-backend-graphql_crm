from celery import shared_task
from datetime import datetime
import requests

GRAPHQL_URL = "http://localhost:8000/graphql/"

@shared_task
def generate_crm_report():
    query = """
    {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
            totalAmount
        }
    }
    """

    try:
        response = requests.post(GRAPHQL_URL, json={"query": query})
        data = response.json().get("data", {})

        total_customers = data.get("allCustomers", {}).get("totalCount", 0)
        total_orders = data.get("allOrders", {}).get("totalCount", 0)
        total_revenue = data.get("allOrders", {}).get("totalAmount", 0)

        report_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(report_line)

    except Exception as e:
        error_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error generating report: {e}\n"
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(error_line)
