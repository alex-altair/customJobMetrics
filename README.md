# customJobMetrics
Let PBS Professional collect and report custom job metrics

This hook is a template for collecting arbitrary stat information about jobs. The intention is to use it for network, file system and device stats.

Users will be able to see such usage information in qstat -f output like

```
$ qstat -xfw 1200
    <snip>
    resources_used.if0_rx_bytes = 96587
    resources_used.if0_tx_bytes = 39480
    <snip>
```

In addition these resources used values will also be available in the accounting log files like

```
# tracejob 1200
<snip>
05/20/2022 12:36:45  A    user=pbstest01 group=pbstest01 project=_pbs_project_default jobname=STDIN queue=workq ctime=1653042943 qtime=1653042943 etime=1653042943 start=1653042943
                          exec_host=dexpbstest5/0 exec_vnode=(dexpbstest5:ncpus=1) Resource_List.ncpus=1 Resource_List.nodect=1 Resource_List.place=pack Resource_List.select=1:ncpus=1
                          session=9992 end=1653043005 Exit_status=0 resources_used.cpupercent=0 resources_used.cput=00:00:00 resources_used.if0_rx_bytes=0
                          resources_used.if0_tx_bytes=0 resources_used.mem=5472kb resources_used.ncpus=1 resources_used.vmem=171376kb resources_used.walltime=00:01:00
                          eligible_time=00:00:00 run_count=1
```

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
qmgr -c "set hook customJobMetrics event = 'execjob_begin,execjob_epilogue,execjob_end'"
qmgr -c "import hook customJobMetrics application/x-python default customJobMetrics.py"
qmgr -c "import hook customJobMetrics application/x-config default customJobMetrics.json"
```

Create required resources for tracking and reporting stats

```
qmgr -c "create resource if0_rx_bytes type=string"
qmgr -c "create resource if0_tx_bytes type=string"
```

