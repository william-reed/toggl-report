import argparse
import os
import requests
import shutil
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description="Generate toggl report for the past two weeks ending at EOD yesterday")
parser.add_argument("--rate", "-r", type=float, help="hourly rate", required=True)
parser.add_argument("--additional", "-a", type=float, help="additional fees per pay period", required=False)
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

hours = report["total_grand"] / 3_600_000  # convert ms to hours

print("Report for {} UTC to {} UTC".format(start, end))
print("Hours:\t{:.2f}".format(hours))
print("Rate:\t${:.2f}/hr".format(RATE))
if ADDITIONAL_FEES is not None:
    print("Other:\t${:.2f}".format(ADDITIONAL_FEES))
else:
    ADDITIONAL_FEES = 0
print("Pay:\t${:.2f}".format(hours * RATE + ADDITIONAL_FEES))
