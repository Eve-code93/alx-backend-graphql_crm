from celery import shared_task
from django.utils import timezone
from crm.models import Customer, Order

@shared_task
def generate_crm_report():
    customers = Customer.objects.count()
    orders = Order.objects.count()
    revenue = Order.objects.aggregate(total=models.Sum("totalamount"))["total"] or 0

    report = (
        f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Report: {customers} customers, {orders} orders, {revenue} revenue\n"
    )

    log_path = "/tmp/crm_report_log.txt"
    with open(log_path, "a") as f:
        f.write(report)

    return report
