#Imports
import os
import re
import collections
import datetime

report = os.path.normpath('report.txt')
with open('report.txt', 'w') as report:  # blank file
    report.write("")

#Regex
# ^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$
domainRegex = re.compile(r'''([0-9a-z-]+\.[a-z-]+\.?[a-z-]+\.?[a-z-]+\.?\s[A-Z]+)''', re.VERBOSE)  # regex domain name
lineRegex = re.compile(r'''(([0-9][0-9][0-9][0-9])-([0-9]?[0-9])-([0-9]?[0-9]) \s   
                                (0?0|[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9]):([0-9]|[0-5][0-9]).(([0-9][0-9])?[0-9]))''',
                       re.VERBOSE)	# regex time
t = []
report = os.path.normpath('dnslog1.txt')
with open('dnslog1.txt', 'r') as in_file:  # input file
    line = in_file.read()  # read file
    # line=line.replace('A','') # tried to segregate ipv4 and ipv6
    d = domainRegex.findall(line)
    d = [rm[: -3] for rm in d]
    e = lineRegex.findall(line)
    for ex in e:
        t.append(ex[0])
    t = [rm[11:] for rm in t]
dict = collections.OrderedDict(zip(t, d))  # dictionary
key = list(dict.keys())
value = list(dict.values())
key1 = []
value1 = []
j = 0

while j < len(key):
    start = key[0]
    start_dt = datetime.datetime.strptime(start, '%H:%M:%S.%f')
    end = key[j]
    end_dt = datetime.datetime.strptime(end, '%H:%M:%S.%f')
    diff = (end_dt - start_dt)
    key1_len = len(key1)
    value1_len = len(value1)
    if diff.seconds >= 62:  # checking for the sites opened within 60-90 seconds
        with open('report.txt', 'a+') as report:
            report.write('\n')
            report.write('{}: {} Time:{}'.format(value[0], key1_len, key[0]) + '\n')  # write main domain names
            for j, sub in enumerate(value1, start=1):
                report.write('{}.{}'.format(str(j), str(sub)) + '\n')  # write sub domain names
        del key[0:key1_len + 1]  # deleting each key and value after writing in file
        del value[0:value1_len + 1]
        del key1[:]
        del value1[:]
        j = 0
    elif diff.seconds < 62:
        key1.append(key[j])
        value1.append(value[j])
    j = j + 1

with open('report.txt', 'a+') as report:    #to reiterate the list again and write remaining sites (to eliminate false positives)
    key1_len = len(key1)
    report.write('\n')
    report.write('{}: {} Time:{}'.format(value[0], key1_len, key[0]) + '\n')
    for j, sub in enumerate(value1, start=1):
        report.write('{}.{}'.format(str(j), str(sub)) + '\n')