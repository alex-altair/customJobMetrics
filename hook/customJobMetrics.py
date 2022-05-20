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

pbs.event().accept()
