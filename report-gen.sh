export TOGGL_TOKEN=""
NAME="Joe Shmoe"
CC_EMAIL="joe@gmail.com"
DEST_EMAIL="boss@gmail.com"
RATE=100.0

python3 main.py --rate $RATE > report.txt

cat report.txt | mail -s "Bi-weekly report for $NAME" -a report.pdf -c $CC_EMAIL $DEST_EMAIL
