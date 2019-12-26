# exit when any command fails
set -e

export TOGGL_TOKEN=""
NAME="Joe Shmoe"
CC_EMAIL="joe@gmail.com"
DEST_EMAIL="boss@gmail.com"
RATE=100.0

# go into script dir to write files there
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

source env/bin/activate
python3 main.py --rate $RATE > report.html

cat report.html | mutt -e "set content_type=text/html" -s "Two week report for $NAME" -a report.pdf -c $CC_EMAIL -- $DEST_EMAIL

rm report.pdf
rm report.html
