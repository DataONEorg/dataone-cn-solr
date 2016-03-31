#!/usr/bin/python

##########################################################################
# This script will accumulate some running time statistics from 
# indexing performance log files.
#
# Input:
#   logFileLocation (optional. will default to '.' if not provided)
#
# It checks files named: 
#   cn-indexing-performance.log*
#   cn-indexing-tool-performance.log*
# 
##########################################################################

import os
import re
import sys
import collections
import operator

def main():

    if len(sys.argv) > 2 :
        print 'Usage: ' + str(sys.argv[0]) + ' [logFileLocation]'
        return

    logFileLocation = "."
    if len(sys.argv) > 1 :
        logFileLocation = str(sys.argv[1])

    
    formatRegex = '.+processing time for format:(.+),\s*(\d+)'
    formatToTotalTime = {}
    formatToNumParsed = {}
    totalTimeInFormats = 0

    processingTimeRegex = '.+total processing time for id.+,\s*(\d+)'
    totalTimeInProcessing = 0
    totalItemsProcessed = 0

    solrAddRegex = '.+adding docs into Solr index,\s*(\d+)'
    totalTimeInSolrAdd = 0
    totalItemsAdded = 0

    solrBatchAddRegex = '.+batch adding \((\d+)\) docs into Solr index,\s*(\d+)'
    totalTimeInSolrBatchAdd = 0
    totalItemsBatchAdded = 0

    anyIdRegex = '\s*(.+)\s*,\s*(\d+)'
    allIDsToTime = {}
    allIDsToOccurences = {}


    # collect times by regex match:
    for filename in os.listdir(logFileLocation) :
        if (not filename.startswith("cn-indexing-performance.log")) and (not filename.startswith("cn-indexing-tool-performance.log")) :
            continue
        print 'checking file: ' + filename

        for line in open(logFileLocation + filename).xreadlines() :

            # processing time log statements
            processingTimeMatch = re.match(processingTimeRegex, line)
            if processingTimeMatch :
                time = int(processingTimeMatch.group(1))
                totalTimeInProcessing += time
                totalItemsProcessed = totalItemsProcessed + 1

            # solr add log statements
            solrAddMatch = re.match(solrAddRegex, line)
            if solrAddMatch :
                time = int(solrAddMatch.group(1))
                totalTimeInSolrAdd += time
                totalItemsAdded = totalItemsAdded + 1

            # solr batch add log statements
            solrBatchAddMatch = re.match(solrBatchAddRegex, line)
            if solrBatchAddMatch :
                numAdded = int(solrBatchAddMatch.group(1))
                time = int(solrBatchAddMatch.group(2))
                totalTimeInSolrBatchAdd += time
                totalItemsBatchAdded = totalItemsBatchAdded + numAdded

            # format log statements
            formatMatch = re.match(formatRegex, line)    
            if formatMatch :
                formatName = formatMatch.group(1)
                parseTime = int(formatMatch.group(2))
                numParsed = 0
                totalTimeInFormats = totalTimeInFormats + parseTime

                if formatName in formatToTotalTime :
                    parseTime = formatToTotalTime[formatName] + parseTime
                if formatName in formatToNumParsed :
                    numParsed = formatToNumParsed[formatName] + 1

                formatToTotalTime[formatName] = parseTime
                formatToNumParsed[formatName] = numParsed

            # all log statements
            anyLogMatch = re.match(anyIdRegex, line)
            if anyLogMatch :
                logId = anyLogMatch.group(1)
                time = int(anyLogMatch.group(2))
                totalTime = 0
                occurences = 0
                
                if logId in allIDsToTime :
                    totalTime = allIDsToTime[logId] + time
                if logId in allIDsToOccurences :
                    occurences = allIDsToOccurences[logId] + 1

                allIDsToTime[logId] = totalTime
                allIDsToOccurences[logId] = occurences


    # printing out statistics...

    print '--------------------------------------------------------------------------------------'
    # print out total & avg times for processing / adding to solr
    print 'total time spent processing:           ' + str(totalTimeInProcessing)
    print 'avg time processing per object:        ' + str(totalTimeInProcessing / totalItemsProcessed)
    print 'total time spent adding to solr:       ' + str(totalTimeInSolrAdd)
    if totalItemsAdded != 0 :
        print 'avg time spent adding an object:       ' + str(totalTimeInSolrAdd / totalItemsAdded)
    print 'total time spent batch adding to solr: ' + str(totalTimeInSolrBatchAdd)
    if totalItemsBatchAdded != 0 :
        print 'avg time spent batch adding an object: ' + str(totalTimeInSolrBatchAdd / totalItemsBatchAdded)

    print '--------------------------------------------------------------------------------------'
    # print out avg time:
    formatToAvgTime = {}
    for key, val in formatToTotalTime.iteritems() :
        numParsed = formatToNumParsed[key]
        avgTime = float (val) / numParsed
        formatToAvgTime[key] = avgTime

    sortedFormatToAvgTime = collections.OrderedDict(sorted(formatToAvgTime.items(), key = operator.itemgetter(1), reverse=True))
    for key, val in sortedFormatToAvgTime.iteritems() :
        print 'format: {0:50} avg time: {1:.2f} ms'.format(key, val)

    print '--------------------------------------------------------------------------------------'
    # print num docs:
    sortedNumParsed = collections.OrderedDict(sorted(formatToNumParsed.items(), key = operator.itemgetter(1), reverse=True))
    for key, val in sortedNumParsed.iteritems() :
        numParsed = formatToNumParsed[key]
        print 'items of format {0:50} : {1}'.format(key, str(numParsed))

    print '--------------------------------------------------------------------------------------'

    # print format by % of total time
    sortedByTimeList = sorted(formatToTotalTime.items(), key = operator.itemgetter(1), reverse=True)
    for entry in sortedByTimeList :
        key = entry[0]
        val = entry[1]
        print '{0:.2f}% of time   in   format: {1}'.format((float(val)/totalTimeInFormats * 100.0), key)

    print '--------------------------------------------------------------------------------------'

if __name__ == "__main__":
  main()
