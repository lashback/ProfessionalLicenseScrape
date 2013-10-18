#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import csv

infile = open('08-13.txt')
outfile = open('08-13.csv', 'w')
writer = csv.writer(outfile)

license = None
name = None
month = None

working_name = None


for line in infile:
	working_name = name
	month_search = re.search('(?:(of|\n)) (January?|February?|March?|April?|August?|September?|October?|November?|December)\w+ (\d{4})\.', line)
	if month_search:
		month = month_search.group(0).strip()
	name_search = re.search('([A-Z][a-z].+) –', line)
	if name_search:
		name = name_search.group(0).strip()
	
	license_search = re.search('([A-Z]{4,})', line)
	if license_search:
		license = line.strip()

	if name != working_name:
		writer.writerow([name, license, month])