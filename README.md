# toggl report generator
Generates a toggl report for the past two weeks. Send email with text similar to the following with a detailed report pdf attached.

```
Report for 2019-12-01 00:00:00 UTC to 2019-12-14 23:59:59 UTC
Hours:  34.47
Rate:   50.00/hr
Pay:    $1723.50
```

Variables must be edited in `report-gen.sh` to your desired values. Run `setup.sh` for an easy setup.

## cron
Run the script every other Monday to send a report for the previous two weeks (ending at the previous night)

```
0 12 * * 0 [ `expr \`date +\%s\` / 86400 \% 2` -eq 1 ] && <script>
```
