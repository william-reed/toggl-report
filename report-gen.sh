export TOGGL_TOKEN=""
NAME="Joe Shmoe"
CC_EMAIL="joe@gmail.com"
DEST_EMAIL="boss@gmail.com"
RATE=100.0

source env/bin/activate
python3 main.py --rate $RATE > report.txt

cat report.txt | mutt -s "Bi-weekly report for $NAME" -a report.pdf -c $CC_EMAIL -- $DEST_EMAIL
