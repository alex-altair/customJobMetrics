#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
qmgr -c "create hook customJobMetrics"
qmgr -c "set hook customJobMetrics enabled= True"
qmgr -c "set hook customJobMetrics event = 'execjob_begin,execjob_epilogue,execjob_end,exechost_periodic'"
qmgr -c "import hook customJobMetrics application/x-python default customJobMetrics.py"
qmgr -c "import hook customJobMetrics application/x-config default customJobMetrics.json"
'''

import pbs
import sys
import subprocess
import os
import json

ip_cmd   = '/usr/sbin/ip'
pbs_home = '/var/spool/pbs'

def get_ip_stat(iface):
    # example: ip -s a l ens192

    if0_rx_bytes = 0
    if0_tx_bytes = 0

    cmd = [ip_cmd, '-s', 'a', 'l', iface]
    result = subprocess.run(cmd, stdout=subprocess.PIPE)

    result = result.stdout.decode('utf-8').split('\n')

    found_rx = False
    found_tx = False

    for l in result:
        l = l.strip()

        if found_rx:
            if0_rx_bytes = l.split()[0]
            found_rx = False

        if found_tx:
            if0_tx_bytes = l.split()[0]
            found_tx = False

        if l.startswith('RX'):
            found_rx = True
        if l.startswith('TX'):
            found_tx = True

    return (if0_rx_bytes, if0_tx_bytes)

def caller_name():
    return str(sys._getframe(1).f_code.co_name)

def execjob_begin():
    pbs.logmsg(pbs.LOG_DEBUG, 'In %s' % (caller_name()))

    e = pbs.event()
    j = e.job

    # Check if $PBS_HOME/metrics does exist
    metrics_path = os.path.join(pbs_home, 'metrics')
    if not os.path.isdir(metrics_path):
        os.mkdir(metrics_path)

    # Initialize resource used values
    j.resources_used['if0_rx_bytes'] = '0'
    j.resources_used['if0_tx_bytes'] = '0'

    # Fetch if0_rx_bytes and if0_tx_bytes
    (if0_rx_bytes, if0_tx_bytes) = get_ip_stat('ens192')
    pbs.logmsg(pbs.EVENT_DEBUG, "if0_rx_bytes = %s; if0_tx_bytes = %s" % (if0_rx_bytes, if0_tx_bytes))

    # Write initial usage information to $PBS_HOME/metrics/$PBS_JOBID.m
    
    usage = {}
    usage['if0_rx_bytes'] = if0_rx_bytes
    usage['if0_tx_bytes'] = if0_tx_bytes 

    metrics_file = os.path.join(metrics_path, j.id + '.m')
    
    with open(metrics_file, 'w') as fd_out:
        json.dump(usage, fd_out) 


def execjob_end():
    pbs.logmsg(pbs.LOG_DEBUG, 'In %s' % (caller_name()))

    e = pbs.event()
    j = e.job

    # Read last usage information from $PBS_HOME/metrics/$PBS_JOBID.m
    metrics_path = os.path.join(pbs_home, 'metrics')
    metrics_file = os.path.join(metrics_path, j.id + '.m')

    with open(metrics_file) as fd_in:
        last_usage = json.load(fd_in)

    # Read current usage information
    (if0_rx_bytes, if0_tx_bytes) = get_ip_stat('ens192')


    # Set final resource used values
    j.resources_used['if0_rx_bytes'] = str(int(if0_rx_bytes)-int(last_usage['if0_rx_bytes']))
    j.resources_used['if0_tx_bytes'] = str(int(if0_tx_bytes)-int(last_usage['if0_tx_bytes']))


    # Clean up the usage file
    os.remove(metrics_file)


try:
    pbs.logmsg(pbs.LOG_DEBUG, 'Starting %s' % (pbs.event().hook_name))

    if pbs.event().type == pbs.EXECJOB_BEGIN:
        execjob_begin()

    if pbs.event().type == pbs.EXECJOB_END:
        execjob_end()

    pbs.event().accept()

except SystemExit:
    pass

except:
    import traceback

    log_buffer = traceback.format_exc()
    pbs.logmsg(pbs.LOG_DEBUG, 'Hook exception:')
    for line in log_buffer.split('\n'):
        pbs.logmsg(pbs.LOG_DEBUG, line)
    pbs.event().reject("Exception trapped in %s:\n %s" % (pbs.event().hook_name, log_buffer))

pbs.event().accept()
