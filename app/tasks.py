import time
import requests
from bs4 import BeautifulSoup

from app.celery_config import make_celery

celery_app = make_celery()


@celery_app.task(name="async_send_email")
def async_send_email(email, subject, body):
    time.sleep(5)
    print(f"Email sent to {email} - {subject}")
    return {"success": True, "email": email, "subject": subject, "body": body}


@celery_app.task(name="async_parse_exploits")
def async_parse_exploits():
    url = "https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    exploits = []
    table = None

    for tbl in soup.find_all('table'):
        if len(tbl.find_all('tr')) > 100:
            table = tbl
            break

    if not table:
        return {"error": "Exploits table not found"}

    for idx, row in enumerate(table.find_all('tr')):
        if idx > 100:
            break
        try:
            cols = row.find_all('td')
            if len(cols) >= 2:
                exploit_id = cols[0].text.strip()
                cve_id = cols[1].text.strip()
                exploits.append({"exploit_id": exploit_id, "cve_id": cve_id})
        except Exception as err:
            print(f"Skipping row due to error: {err}")

    print(f"Extracted {len(exploits)} exploits")
    return exploits
