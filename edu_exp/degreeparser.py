import re
import os
from collections import OrderedDict
from natsort import natsorted

"""
Sample code to extract degree based on regular expressions from our gold standard sample of resumes from the database:
One for bachelors' one for masters' and one for doctorate.
This takes into account associate (2 yr degrees)
August/09: Creation
August/10: Add Vineet's comments
August/15: Created parser for sections
August/17: Refined script for increased coverage
"""


bachelor = re.compile(ur'B\.Math|B\.A\.|BTech\.|BTech|B\.Stat\.|BFA|BVA|BCA|Bachelor\'s|Bachelor|B\.A\.|B\. A\.|B\.A|B\. A|BA|B\.S\.|B\. S\.|BS|BEIT|B\.Tech|B\.E\.|BE|BIS\.|BASc|AB|B.com|B-Tech|B\.Sc\.|B Tech')
masters = re.compile(ur'Master|Masters|M\.A\.|M\.S\.|M\. S\.|M\. Sc\.|MBA|EMBA|MSE|M.Tech|MTech|M\.Sc\.|Masterof|MSc|MS|M\.Stat\.|MEng|M\.Eng|MFA|M\.F\.A\.|MDiv\.')
doctor = re.compile(ur'Doctor|DOCTOR|doctor|Ph\.D\.|Ph\. D\.|PhD|JD|J\.D\.|\s+JD\s*|\s+MD\s+|M\.D\.|Phd')
associate = re.compile(ur'Associate Degree|Associates Degree|Associate of Arts|Associate in Arts|A\.A\.|Associate of Science|Associate in Science|Associates in Science|A\.S\.|Associate of Applied Science|Associate in Applied Science|Associates of Applied Science|Associate in Applied Science|A\.A\.S\.|Associate of Arts and Science|Associates Degree| Associate of|Associate\'s degree')
headerstrt = re.compile(ur'Education|EDUCATION|education|SCHOLASTIC  RECORD') #Need to deal with ortographic errors?
headerstop = re.compile(ur'Experience|EXPERIENCE|SUMMARY|Volunteer|VOLUNTEER|REFERENCES|References|Skills|SKILLS|recommended')
files = os.listdir('.')
ordered_files = natsorted(files)
results = OrderedDict()
for fn in ordered_files:
    if os.path.isfile(fn):
        if fn.endswith('.txt'):
            results[fn] = set()
            fileinp = open(fn, 'r')
            lines = fileinp.readlines()
            i = 0
            signal = False
            while i < len(lines):
                head = re.search(headerstrt, lines[i])
                stop = re.search(headerstop, lines[i])
                if head:
                    signal = True
                if stop:
                    signal = False
                if signal == True:
                    matchba = re.search(bachelor, lines[i])
                    matchma = re.search(masters, lines[i])
                    matchdr = re.search(doctor, lines[i])
                    matchas = re.search(associate, lines[i])
                    if matchba:
                        results[fn].add('Bachelor')
                    if matchma:
                        results[fn].add('Masters')
                    if matchdr:
                        results[fn].add('Doctorate')
                    if matchas:
                        results[fn].add('Associate')
                i += 1
            results[fn] = list(results[fn])
            print fn+','+', '.join(results[fn])
