#Imports
import os
import re
import collections
import datetime

report = os.path.normpath('report.txt')
with open('report.txt', 'w') as report:  # blank file
    report.write("")

#Regex
domainRegex = re.compile(r'''([0-9a-z-]+\.[a-z-]+\.?[a-z-]+\.?[a-z-]+\.?\s[A-Z]+)''', re.VERBOSE)  # regex domain name
lineRegex = re.compile(r'''(([0-9][0-9][0-9][0-9])-([0-9]?[0-9])-([0-9]?[0-9]) \s   # regex time
                                (0?0|[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9]):([0-9]|[0-5][0-9]).(([0-9][0-9])?[0-9]))''',
                       re.VERBOSE)
t = []
report = os.path.normpath('dnslog.txt')
with open('dnslog.txt', 'r') as in_file:  # input file
    line = in_file.read()  # read file
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
    if diff.seconds >= 60:  # checking for the sites opened within 60-90 seconds
        with open('report.txt', 'a+') as report:
            report.write('\n')
            report.write('{}: {} Time:{}'.format(value[0], key1_len, key[0]) + '\n')  # write main domain names
            for j, each in enumerate(value1, start=1):
                report.write("{}.{}".format(str(j), str(each)) + '\n')  # write sub domain names
        del key[0:key1_len + 1]  # deleting each key and value after writing in file
        del value[0:value1_len + 1]
        del key1[:]
        del value1[:]
    elif diff.seconds < 60:
        key1.append(key[j])
        value1.append(value[j])
    j = j + 1
