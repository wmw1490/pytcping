#!/usr/bin/env python3
"""
TCP Ping Test -- reads tcping.dat file to perform a connection oriented tcp ping to a target host/ip and port.

"""
# Author:  Wally Wilhoite
# 
# Release info:
#
# 1.0 2018-12-12 - initial release, performs pings and reports results to console.
#
#

import sys
import socket
import time
import signal
from timeit import default_timer as timer

maxCount = 3

# Default to 10000 connections max
#maxCount = 10000
count = 0

## Inputs
host = 'ns2.cdc.gov'
port = 53


# Pass/Fail counters
passed = 0
failed = 0


def getResults():
    """ Summarize Results """

    lRate = 0
    if failed != 0:
        lRate = failed / (count) * 100
        lRate = "%.2f" % lRate

    print("\nTCP Ping Results: Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Failed: {:}%)".format((count), passed, failed, str(lRate)))

def signal_handler(signal, frame):
    """ Catch Ctrl-C and Exit """
    getResults()
    sys.exit(0)

# Register SIGINT Handler
signal.signal(signal.SIGINT, signal_handler)

# Loop while less than max count or until Ctrl-C caught
def tcping( lookupBy, host, port, maxCount):
    #
    # Setup variables used during this function
    count = 0
    # Pass/Fail counters
    passed = 0
    failed = 0
    
    while count < maxCount:
        # Increment Counter
        count += 1
        success = False

        # New Socket
        s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

        # 1sec Timeout
        s.settimeout(1)

        # Start a timer
        s_start = timer()

        # Try to Connect
        try:
            s.connect((host, int(port)))
            s.shutdown(socket.SHUT_RD)
            success = True
    
        # Connection Timed Out
        except socket.timeout:
            print("Connection timed out!")
            failed += 1
        except OSError as e:
            print("OS Error:", e)
            failed += 1

        # Stop Timer
        s_stop = timer()
        s_runtime = "%.2f" % (1000 * (s_stop - s_start))

        if success:
            print("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (host, port, (count-1), s_runtime))
            passed += 1

        # Sleep for 1sec
        if count < maxCount:
            time.sleep(.25)

        # need to return runtime min/max/avg

#
# main function will iterate through the file containing the hosts, ips, ports to test
#
def main():
    # 
    # Open file containing hosts to ping
    # read into a list
    # iterate through list
    # write results to dynaodb 
    # send failures to message queue for processing (send alert email)
    #
    tcping('H', '8.8.4.4', 53, 6)
    tcping('H', 'ns1.cdc.gov', 53, 2)
    tcping('H', 'ns2.cdc.gov', 53, 2)
    tcping('H', 'www.suntrust.com', 443, 2)
    tcping('H', 'www.cdcfcu.com', 443, 2)
    tcping('H', 'citgo.cdc.gov', 443, 2)
    tcping('H', 'www.google.com', 443, 2)
    tcping('H', 'www.microsoft.com', 443, 2)
    tcping('H', 'www.hhs.gov', 443, 2)
    tcping('H', 'access.cdc.gov', 443, 2)
    
    
    


if __name__== "__main__":
    main()

