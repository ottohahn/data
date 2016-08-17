#!/usr/bin/env python
# -*- coding=utf-8 -*-
import datetime
import re
import os
import numpy as np
from dateutil import parser
from natsort import natsorted
from collections import OrderedDict

dates_zero=re.compile(ur'[0-9]{4}\s?-\s?[0-9]{4}|[0-9]{2}/[0-9]{2,4}|Jan|Feb|Mar|March|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec [0-9]{4} -|[0-9]{4}')

dates_one = re.compile(ur'[A-Z]+\s[0-9]{2,4}(\t|\s)*(-|~|to|through)(\t|\s)*(Present|Current|[A-Z]+\s[0-9]{2,4})|[0-9]{4}(\t|\s)*(-|~|to|through)(\t|\s)*(Present|Current|[0-9]{4})|[0-9]{,2}(\.|/)[0-9]{2,4}(\t|\s)*(-|~|to|through)(\t|\s)*(Present|Current|[0-9]{,2}(\.|/)[0-9]{2,4})|[A-Z]+(\t|\s)*[0-9]{4}(\t|\s)*[A-Z]+(\t|\s)*[0-9]{4}', re.IGNORECASE)

headerstrt = re.compile(ur'Experience\n|Experience\s\t\n|EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL BACKGROUND|PROFESSIONAL EXPERIENCE|JOBS') #Need to deal with orthographic errors

headerstop = re.compile(ur'EDUCATION|Education\n|Education\s\t\n|Skills|SKILLS|SUMMARY|Volunteer|VOLUNTEER|PROJECTS|QUALIFICATIONS')

def print_exp(resume):
    fileinp = open(resume, 'rU')
    lines = fileinp.readlines()
    fileinp.close()
    i = 0
    signal = True
    while i < len(lines):
        line = re.sub(u"\xe2\x80\x93", "-", lines[i])
        if re.search(headerstrt, line):
            signal = True
            finddate = re.search(dates, line)
            if finddate:
                print resume+'\t'+ \
                    finddate.string[finddate.span()[0]:finddate.span()[1]]
            if re.search(headerstop, line):
                signal = False
            i += 1
        elif re.search(headerstop, line):
            signal = False
            i += 1
        else:
            if signal:
                finddate = re.search(dates, line)
                if finddate:
                    print resume+'\t'+ \
                        finddate.string[finddate.span()[0]:finddate.span()[1]]
                i += 1
            else:
                i += 1

def get_exp_zero(resume):
    fileinp = open(resume, 'rU')
    lines = fileinp.readlines()
    fileinp.close()
    i = 0
    signal = True
    date_list = []
    while i < len(lines):
        line = re.sub(u"\xe2\x80\x93", "-", lines[i])
        if re.search(headerstrt, line):
            signal = True
            finddate = re.search(dates_zero, line)
            if finddate:
                date_list.append(line)
            if re.search(headerstop, line):
                signal = False
            i += 1
        elif re.search(headerstop, line):
            signal = False
            i += 1
        else:
            if signal:
                finddate = re.search(dates_zero, line)
                if finddate:
                    date_list.append(line)
                i += 1
            else:
                i += 1
    return date_list

# def get_exp(resume):
#     fileinp = open(resume, 'rU')
#     lines = fileinp.readlines()
#     fileinp.close()
#     i = 0
#     signal = True
#     date_list = []
#     while i < len(lines):
#         line = re.sub(u"\xe2\x80\x93", "-", lines[i])
#         if re.search(headerstrt, line):
#             signal = True
#             finddate = re.search(dates, line)
#             if finddate:
#                 date_list.append(finddate.string[finddate.span()[0]:finddate.span()[1]])
#             if re.search(headerstop, line):
#                 signal = False
#             i += 1
#         elif re.search(headerstop, line):
#             signal = False
#             i += 1
#         else:
#             if signal:
#                 finddate = re.search(dates, line)
#                 if finddate:
#                     date_list.append(finddate.string[finddate.span()[0]:finddate.span()[1]])
#                 i += 1
#             else:
#                 i += 1
#     return date_list

def get_exp_one(lst):
    date_list = []
    for line in lst:
        finddate = re.search(dates_one, line)
        if finddate:
            date_list.append(finddate.string[finddate.span()[0]:finddate.span()[1]])
    return date_list

def convert_dates(date_list, cur_date=None):
    if not date_list:
        return None
    else:
        if cur_date:
            cur_date = parser.parse(cur_date)
        else:
            cur_date = datetime.datetime.today()
        new_list = []
        for group in date_list:
            group = re.sub(r"(\t|\n|\.)", " ", group)
            lst = re.split(ur"(-|~|\s\s|\s(-|~|to|through)\s)", group)
            beg = parser.parse(lst[0])
            if lst[-1].lower() in ['present', 'current']:
                end = cur_date
            else:
                end = parser.parse(lst[-1])
            new_list.append((beg, end))
        return sorted(new_list, reverse=True)

def remove_overlap(converted_dates):
    if not converted_dates:
        return None
    else:
        for i, x in enumerate(converted_dates):
            if i == 0:
                i += 1
            else:
                if x[1] > converted_dates[i-1][0]:
                    line = list(converted_dates[i-1])
                    line[0] = x[1]
                    converted_dates[i-1] = tuple(line)
                i += 1

def get_yrs(no_ov_dates):
    if not no_ov_dates:
        return 0
    else:
        new_list = []
        for group in no_ov_dates:
            new_list.append((group[1]-group[0]).days)
        return float(np.sum(new_list))/365

# def chain_exp()
