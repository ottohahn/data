import time
import re
from docx2txt import process
from alchemyapi import AlchemyAPI
from klangooapi import KlangooAPI


alchemyapi = AlchemyAPI()
klangooapi = KlangooAPI()

files = ['data/CABLE SPLCELEC.docx',
         'data/CONSTR MGMT INSPCTR II.docx',
         'data/CONSTR MGMT INSPCTR III.docx',
         'data/DIR WORKFORCE HEALTH & SAFETY.docx',
         'data/DISTRIBUTION LINE DESIGN SUPVR.docx',
         'data/ENV HLTH&SFTY SPCLST II.docx',
         'data/HAZ WASTE FRMN WN, LT.docx',
         'data/MAINT PLANNER SUBS.docx',
         'data/MGR,ACCOUNT MGMT & SALES.docx',
         'data/MGR,SUBSTN MAINT.docx',
         'data/PRIN TELECOMM ENGR.docx',
         'data/PRIN TRNSMSN PLNG ENGR.docx',
         'data/SR SURV ENGRG TECH-COP.docx',
         'data/SR SURV ENGRG TECH-OFF.docx'
         ]
job_titles = ['CABLE SPLCELEC',
              'CONSTR MGMT INSPCTR II',
              'CONSTR MGMT INSPCTR III',
              'DIR WORKFORCE HEALTH & SAFETY',
              'DISTRIBUTION LINE DESIGN SUPVR',
              'ENV HLTH&SFTY SPCLST II',
              'HAZ WASTE FRMN WN, LT',
              'MAINT PLANNER SUBS',
              'MGR,ACCOUNT MGMT & SALES',
              'MGR,SUBSTN MAINT',
              'PRIN TELECOMM ENGR',
              'PRIN TRNSMSN PLNG ENGR',
              'SR SURV ENGRG TECH-COP',
              'SR SURV ENGRG TECH-OFF'
              ]


def kl_conv(score):
    """Convert Klangoo ranks to scores.

    This is taken directly from current Ruby/Rails code:
    "https://github.com/atipica/analytics/blob/master/lib/klangoo/magnet_client.rb"
    """
    if score == 'VR':
        return '0.85'
    if score == 'R':
        return '0.6'
    if score == 'SR':
        return '0.45'
    if score == 'NR':
        return '0.26'

if __name__ == '__main__':
    text_data = []
    for file in files:
        data = ' '.join(process(file).split())
        data = re.sub(u"(\u2018|\u2019)", "'", data)
        text_data.append(data)
    for position in zip(text_data, job_titles):
        al_response = alchemyapi.entities('text', position[0],
                                          options={'sentiment': 1})
        kl_response = klangooapi.entities('json', position[0], time.time())
        lst = []
        lst.append(position[1] + '\n')
        lst.append('Alchemy API\n')
        if al_response['entities']:
            for word in al_response['entities']:
                lst.append(word['text'] + ', ' + word['relevance'] +
                           ', ' + word['type'] + '\n')
        lst.append('Klangoo API\n')
        if kl_response:
            for word in kl_response:
                lst.append(word['token'] + ', ' + kl_conv(word['rank']) +
                           ', ' + word['type'] + '\n')
        text_file = open('data/' + position[1] + '.txt', 'w')
        text_file.writelines(lst)
        text_file.close()
