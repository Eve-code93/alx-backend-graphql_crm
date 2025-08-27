#!/bin/bash
# Script to clean up inactive customers (no orders in the last year)

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
DELETED=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

echo "\$TIMESTAMP - Deleted customers: \$DELETED" >> /tmp/customer_cleanup_log.txt
