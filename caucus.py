#!/usr/bin/env python
################################################################################
# Copyright (c) 2016 Layton Nelson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################
import json
from datetime import datetime

import requests
from dateutil import parser
from tabulate import tabulate

# api found at:
# http://www.desmoinesregister.com/pages/interactives/elections-results-primaries-2016/
api_url = "http://api.gannett-cdn.com/v1/2016-primary/results/p/ia/summary"

data = requests.get(api_url)
races = data.json()["races"]
numRaces = len(races)

def printRaceInfo(int):
	race = races[int]

	# get update time
	lastUpdated_raw = parser.parse(race["reportingUnits"][0]["lastUpdated"])
	lastUpdated = lastUpdated_raw.strftime("%Y-%m-%d %H:%M:%S %Z")

	precinctsReporting = race["reportingUnits"][0]["precinctsReporting"]
	precinctsTotal = race["reportingUnits"][0]["precinctsTotal"]
	# precinctsReportingPct_raw = (float(precinctsReporting) / float(precinctsTotal))*100

	precinctsReportingPct = race["reportingUnits"][0]["precinctsReportingPct"]
	candidates = race["reportingUnits"][0]["candidates"]

	# get race information
	stateName = race["reportingUnits"][0]["stateName"]
	electionDate = race["electionDate"]
	party = race["party"]
	officeName = race["officeName"]
	raceType = race["raceType"]

	############################################################################
	# Print the data!
	############################################################################
	# sepLine = "+---------+----------------------+--------+--------+"
	# print("----------------------------------------------------")

	# HEADER ---------------------------------
	print("%s %s %s %s %s") % (electionDate, stateName, party, officeName, raceType)
	print("Last Updated: " + lastUpdated)
	print("%5.2f%% Reported (%d/%d)") % (precinctsReportingPct, precinctsReporting, precinctsTotal)

	# print(sepLine)
	# print("| %-6s | %-20s | %-6s | %-6s |") % ("VotePct", "Candidate", "Delgts", "Votes")
	# print(sepLine)

	# TABLE ---------------------------------
	candidateTable = list()
	tableHeaders = ["VotePct", "Candidate", "Delgts", "Votes", "Status"]

	for candidate in candidates:
		if candidate["ballotOrder"] != 100:  # exclude the generalized "other" canidate(s)
			first = candidate["first"]
			last = candidate["last"]
			name = "%s %s" % (first, last)
			votePct = candidate["votePct"]
			delegateCount = candidate["delegateCount"]
			voteCount = candidate["voteCount"]

			try:
				if candidate["winner"] == True:
					winner = "Winner"
			except KeyError:
				winner = ""

			# print("| %6.2f%% | %-20s | %-6d | %-6d |") % (votePct, name, delegateCount, voteCount)
			candidateTable.append([votePct, name, delegateCount, voteCount, winner])

	# print(sepLine)
	# print(candidateTable)

	print tabulate(candidateTable, headers=tableHeaders, tablefmt="psql")

if __name__ == '__main__':
	for i in xrange(0, numRaces):
		printRaceInfo(i)

		if i < numRaces - 1:
			print("")
