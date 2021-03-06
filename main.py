import argparse
import os
import requests
import shutil
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description="Generate toggl report for the past two weeks ending at EOD yesterday")
parser.add_argument("--rate", "-r", type=float, help="hourly rate", required=True)
parser.add_argument("--additional", "-a", type=float, help="additional fees per pay period", required=False, default=0)
args = parser.parse_args()
RATE = args.rate
ADDITIONAL_FEES = args.additional

REPORTS_URL = "https://toggl.com/reports/api/v2/details"
WORKSPACE_URL = "https://www.toggl.com/api/v8/workspaces"

TOKEN = os.environ["TOGGL_TOKEN"]
USER_AGENT = "report_generator"
AUTH = HTTPBasicAuth(TOKEN, "api_token")

# strip out the time of day to go to UTC 0:00
today = datetime.utcnow().date()
# start is two weeks ago from yesterday
today = datetime(today.year, today.month, today.day)
start = today - timedelta(days=14)
# end is EOD yesterday
end = today - timedelta(days=1)
end = datetime(end.year, end.month, end.day, 23, 59, 59)

workspaces = requests.get(url=WORKSPACE_URL, auth=AUTH).json()
# get first workspace id
workspace_id = workspaces[0]["id"]

PARAMS = {
    "workspace_id": workspace_id,
    "user_agent": USER_AGENT,
    "since": start.isoformat(),
    "until": end.isoformat(),
}

# get json report
report = requests.get(url=REPORTS_URL, params=PARAMS, auth=AUTH).json()
report_pdf = requests.get(url=REPORTS_URL + ".pdf", params=PARAMS, auth=AUTH, stream=True)
# get the PDF
with open("report.pdf", "wb") as f:
    for chunk in report_pdf:
        f.write(chunk)

hours = Decimal(report["total_grand"]) / Decimal(3_600_000)  # convert ms to hours
pay = Decimal(hours) * Decimal(RATE) + Decimal(ADDITIONAL_FEES)
pay = pay.quantize(Decimal("0.01"), ROUND_HALF_UP)

print("<h3>Report for <b>{}</b> UTC to <b>{}</b> UTC</h3>".format(start, end))

headers = ["Category", "Quantity"]
rows = [
    ["Hours", "{:.2f}".format(hours)],
    ["Rate", "${:.2f}".format(RATE)],
    ["Other Fees", "${:.2f}".format(ADDITIONAL_FEES)],
    ["Pay", "${:.2f}".format(pay)]
]

print("<table>")
print("<tr>{}</tr>".format("".join(["<th>{}</th>".format(h) for h in headers])))
for row in rows:
    print("<tr>{}</tr>".format("".join(["<td>{}</td>".format(r) for r in row])))
print("</table>")
