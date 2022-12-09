# README.md
this tool checks config uploads from ciscos, commits changes and pushes to gitlab repo

from router side should be settings:
```
conf t
ip tftp source-interface Loopback0

service timestamps log datetime year localtime show-timezone
archive
 log config
  logging enable
  logging size 1000
  notify syslog contenttype plaintext
  hidekeys
 path tftp://192.168.66.27/cfg/$h-
 write-memory
 time-period 10080
end
```

on server side script is starting every 5 min from crontab
```
root@arh1-srv-ftp:# crontab -l
# ...
*/5 * * * * /usr/bin/python3 /root/app.py
root@arh1-srv-ftp:#
```
copies latest files to */home/ftp/cfg/rep* subfolder, then commits and pushes to central repositary


