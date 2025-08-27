# CRM Celery Report Task

## Setup
1. Install Redis:
   ```bash
   sudo apt update && sudo apt install redis-server
   sudo systemctl enable redis-server
crm/README.md
# CRM Celery Report Task

## Setup
1. Install Redis:
   ```bash
   sudo apt update && sudo apt install redis-server
   sudo systemctl enable redis-server


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Start Celery worker:

celery -A crm worker -l info


Start Celery Beat:

celery -A crm beat -l info


Verify logs:

tail -f /tmp/crm_report_log.txt


Every Monday at 6:00 AM, a new report is logged.


---

✅ With this, your **weekly CRM reports** will be generated automatically and logged.  

Would you like me to also **integrate this task into the GraphQL schema**, so you can trigger `generate_crm_report` manually from GraphQL (not just via Beat)?
