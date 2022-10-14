# README.md
this tool checks config uploads from ciscos, commits changes and pushes to gitlab repo

from router side should be settings:
~~~
conf t
logging source-interface Loopback0
ip tftp source-interface Loopback0

no ip domain-lookup
clock timezone MSK 3
no clock summer-time
service timestamps debug datetime msec localtime
service timestamps log datetime year localtime show-timezone
service sequence-numbers
logging buffer 256000 debugging
logging host 192.168.66.102 transport udp port 5140
logging trap warnings
logging console warnings
logging facility syslog
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
~~~

