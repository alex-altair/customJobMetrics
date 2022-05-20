# customJobMetrics
Let PBS Professional collect and report custom job metrics

# Examples on what to collect and how

## Collect ip stats on single nodes

```
[root@dexpbstest4 ~]# ip -s a l ens192
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:82:41:8d brd ff:ff:ff:ff:ff:ff
    inet 10.246.88.147/22 brd 10.246.91.255 scope global noprefixroute ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::5ac:4da4:9fc2:89b/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
    RX: bytes  packets  errors  dropped overrun mcast
    50740516950 148093578 0       306745  0       20216282
    TX: bytes  packets  errors  dropped carrier collsns
    7190366812 54186370 0       0       0       0
```

# Implementation of collecting and reporting ip stats for single host jobs

## Architecture

# Configuration of the customJobMetrics hook

Create and import the hook and its json config file

```
qmgr -c "create hook customJobMetrics"
qmgr -c "set hook customJobMetrics enabled= True"
qmgr -c "set hook customJobMetrics event = 'execjob_begin,execjob_epilogue,execjob_end,exechost_periodic'"
qmgr -c "import hook customJobMetrics application/x-python default customJobMetrics.py"
qmgr -c "import hook customJobMetrics application/x-config default customJobMetrics.json"
```



