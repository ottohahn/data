#!/usr/bin/env python
# encoding: utf-8
"""
alchemy_query.py

This script runs the Alchemy API on various urls, returning their entity
outputs.
"""
from alchemyapi import AlchemyAPI

if __name__ == '__main__':
    alchemyapi = AlchemyAPI()

    urls = ['https://boards.greenhouse.io/thumbtack/jobs/734#.V22y2pMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/732#.V23KA5MrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/212875#.V23KJZMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/101523#.V23KNpMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/714#.V23KSJMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/204909#.V23KWJMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/733#.V23KbJMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/44411#.V23KgJMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/729#.V23KkJMrKYU',
            'https://boards.greenhouse.io/thumbtack/jobs/723#.V23Ko5MrKYU']
    job_titles = ['Android Engineer',
                  'Data Scientist',
                  'Director of IT',
                  'Engineering Director',
                  'Front End Engineer',
                  'Head of Data Science',
                  'iOS Engineer',
                  'Security Engineer',
                  'Site Reliability Engineer',
                  'Software Engineer']

    for position in zip(urls, job_titles):
        response = alchemyapi.entities('url', position[0],
                                       options={'sentiment': 1})
        lst = []
        lst.append(position[1] + '\n')
        for word in response['entities']:
            lst.append(word['text'] + ', ' + word['relevance'] +
                       ', ' + word['type'] + '\n')
        text_file = open('data/' + position[1] + '.txt', 'w')
        text_file.writelines(lst)
        text_file.close()
