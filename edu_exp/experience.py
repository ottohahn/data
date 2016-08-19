#!/usr/bin/env python
# -*- coding=utf-8 -*-
import datetime
import re
import os
import numpy as np
from dateutil import parser
from natsort import natsorted
from collections import OrderedDict

class GetExp():

    def __init__(self):
        self.dates_zero = re.compile(ur'(([A-Z]+|[0-9]{,2})(\s|\t|\/|\.)*(’|‘)*([0-9]{4}|[0-9]{2})(\t|\s)*(~|—|–|-|to|To|TO|THROUGH|Through|through|\s)(\t|\s)*([A-Z]+|[0-9]{,2})(\s|\t|\/|\.)*(’|‘)*([0-9]{2}|[0-9]{4})*|[0-9]{4}(\t|\s)*(~|—|–|-|to|To|TO|THROUGH|Through|through|\s)(\t|\s)*(Present|Current|[0-9]{4}))', re.IGNORECASE)

        self.dates_one = re.compile(ur'[A-Z]+\s?[0-9]{2,4}(\t|\s)*(~|—|–|-|to|To|TO|THROUGH|Through|through)(\t|\s)*(Present|Current|[A-Z]+\s?[0-9]{2,4})|[0-9]{4}(\t|\s)*(~|—|–|-|to|To|TO|THROUGH|Through|through)(\t|\s)*(Present|Current|[0-9]{4})|[0-9]{,2}(\.|\/)[0-9]{2,4}(\t|\s)*(~|—|–|-|to|To|TO|THROUGH|Through|through)(\t|\s)*(Present|Current|[0-9]{,2}(\.|\/)[0-9]{2,4})|[A-Z]+(\t|\s)*[0-9]{4}(\t|\s)*[A-Z]+(\t|\s)*(Present|Current|[0-9]{4})', re.IGNORECASE)

        self.headerstrt = re.compile(ur'Experience\n|Experience\s\t\n|EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL BACKGROUND|PROFESSIONAL EXPERIENCE|JOBS') #Need to deal with orthographic errors

        self.headerstop = re.compile(ur'EDUCATION|Education\n|Education\s\t\n|Skills|SKILLS|SUMMARY|Volunteer|VOLUNTEER|PROJECTS|QUALIFICATIONS')

    def print_exp(self, resume):
        fileinp = open(resume, 'rU')
        lines = fileinp.readlines()
        fileinp.close()
        i = 0
        signal = True
        while i < len(lines):
            line = re.sub(u"\xe2\x80\x93", "-", lines[i])
            line = re.sub(u"\xe2\x80\x94", "-", line)
            if re.search(self.headerstrt, line):
                signal = True
                finddate = re.search(self.dates_one, line)
                if finddate:
                    print resume+'\t'+ line
                if re.search(self.headerstop, line):
                    signal = False
                i += 1
            elif re.search(self.headerstop, line):
                signal = False
                i += 1
            else:
                if signal:
                    finddate = re.search(self.dates_one, line)
                    if finddate:
                        print resume+'\t'+ line
                    i += 1
                else:
                    i += 1

    def get_exp_zero(self, resume):
        fileinp = open(resume, 'rU')
        lines = fileinp.readlines()
        fileinp.close()
        i = 0
        signal = True
        date_list = []
        while i < len(lines):
            line = re.sub(u"\xe2\x80\x93", "-", lines[i])
            line = re.sub(u"\xe2\x80\x94", "-", line)
            if re.search(self.headerstrt, line):
                signal = True
                finddate = re.search(self.dates_zero, line)
                if finddate:
                    date_list.append(line)
                if re.search(self.headerstop, line):
                    signal = False
                i += 1
            elif re.search(self.headerstop, line):
                signal = False
                i += 1
            else:
                if signal:
                    finddate = re.search(self.dates_zero, line)
                    if finddate:
                        date_list.append(line)
                    i += 1
                else:
                    i += 1
        return date_list

    def get_exp_one(self, lst):
        date_list = []
        for line in lst:
            finddate = re.search(self.dates_one, line)
            if finddate:
                date_list.append(finddate.string[finddate.span()[0]:finddate.span()[1]])
        return date_list

    def convert_dates(self, date_list, cur_date=None):
        today = datetime.datetime.today()
        if not date_list:
            return None
        else:
            if cur_date:
                cur_date = parser.parse(cur_date)
            else:
                cur_date = today
            new_list = []
            for group in date_list:
                group = re.sub(r"(\t|\n|\.)", " ", group)
                lst = re.split(ur"(~|—|–|-|\s\s|(\s\s|\s)(~|—|–|-|to|TO|To|THROUGH|Through|through)(\s\s|\s))", group)
                lst = [x.strip() for x in lst if x is not None]
                if len(lst) > 1:
                    if len(lst[0]) == 4:
                        mon_yr = re.split(r'\/', lst[0])
                        if len(mon_yr) == 2:
                            lst[0] = mon_yr[0]+" "+"20"+mon_yr[1]
                            beg = parser.parse(lst[0])
                        else:
                            try:
                                beg = datetime.datetime.strptime(lst[0], "%Y")
                                if beg > cur_date:
                                    beg = cur_date
                            except ValueError:
                                # return None
                                continue
                    else:
                        try:
                            beg = parser.parse(lst[0])
                            if beg > cur_date:
                                beg = cur_date
                        except ValueError:
                            # return None
                            continue
                    if lst[-1].lower() in ['present', 'current']:
                        end = cur_date
                    else:
                        if len(lst[-1]) == 4:
                            mon_yr = re.split(r'\/', lst[-1])
                            if len(mon_yr) == 2:
                                lst[-1] = mon_yr[0]+" "+"20"+mon_yr[1]
                                end = parser.parse(lst[-1])
                            else:
                                try:
                                    end = datetime.datetime.strptime(lst[-1], "%Y")
                                    if end > cur_date:
                                        end = cur_date
                                except ValueError:
                                    # return None
                                    continue
                        else:
                            try:
                                end = parser.parse(lst[-1])
                                if end > cur_date:
                                    end = cur_date
                            except ValueError:
                                # return None
                                continue
                    if end >= beg:
                        new_list.append((beg, end))
                else:
                    if len(lst[0]) == 4:
                        try:
                            beg = datetime.datetime.strptime(lst[0], "%Y")
                            end = beg + datetime.timedelta(days=365)
                            new_list.append((beg, end))
                        except ValueError:
                            # return None
                            continue
            return sorted(new_list, reverse=True)

    def remove_overlap(self, converted_dates):
        if not converted_dates:
            return None
        else:
            for i, x in enumerate(converted_dates):
                if i == 0:
                    continue
                else:
                    if x[1] > converted_dates[i-1][0]:
                        line = list(converted_dates[i-1])
                        line[0] = x[1]
                        if line[1] < line[0]:
                            line[1] = line[0]
                        converted_dates[i-1] = tuple(line)
        if converted_dates[0][1] < converted_dates[0][0]:
            line_zero = list(converted_dates[0])
            line_zero[1] = converted_dates[0][0]
            converted_dates[0] = tuple(line_zero)
        return converted_dates

    def get_yrs(self, no_ov_dates):
        if not no_ov_dates:
            return 0
        else:
            new_list = []
            for group in no_ov_dates:
                new_list.append((group[1]-group[0]).days)
            yrs = float(np.sum(new_list))/365
            if yrs < 0:
                return 0
            else:
                return yrs

    def chain_exp(self, resume, cur_date=None):
        lst = self.get_exp_zero(resume)
        clean_lst = self.get_exp_one(lst)
        converted_dts = self.convert_dates(clean_lst, cur_date)
        rem_ov_lst = self.remove_overlap(converted_dts)
        yrs = self.get_yrs(rem_ov_lst)
        return yrs

