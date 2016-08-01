# encoding: utf-8
"""
klangooapi.py
"""
import requests


class KlangooAPI:
    """Class definition for Klangoo API."""

    def __init__(self):
        """Initialize Klangoo API access."""
        self.s = requests.Session()
        f = open('klangoo_api_key.txt', 'r')
        self.key = f.read().strip()
        f.close()
        # The base URL for all endpoints
        self.url_1 = 'http://magnetapi.klangoo.com/Service.svc/AddDocument'
        self.url_2 = 'http://magnetapi.klangoo.com/Service.svc/GetDocument'

    def entities(self, style, data, timestamp):
        """Extract entities from text using Klangoo.

        Unsure if entities can be extracted from a URL or HTML, documentation
        is not available.

        INPUT:
        style -> data output format, 'json' is currently the only option being
        used
        data -> the data to analyze, currently only using text
        timestamp -> datetime stamp, can use time.time()

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        parameters_1 = {'calk': self.key,
                        'format': style,
                        'text': data,
                        'timestamp': timestamp}
        response_1 = self.s.post(self.url_1, data=parameters_1)

        parameters_2 = {'calk': self.key,
                        'format': style,
                        'docID': response_1.json()['docID']}
        response_2 = self.s.post(self.url_2, data=parameters_2)

        return response_2.json()['document']['entities']

    def key_topics(self, style, data, timestamp):
        """Extract key topics from text using Klangoo.

        Unsure if entities can be extracted from a URL or HTML, documentation
        is not available.

        INPUT:
        style -> data output format, 'json' is currently the only option being
        used
        data -> the data to analyze, currently only using text
        timestamp -> datetime stamp, can use time.time()

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        parameters_1 = {'calk': self.key,
                        'format': style,
                        'text': data,
                        'timestamp': timestamp}
        response_1 = self.s.post(self.url_1, data=parameters_1)

        parameters_2 = {'calk': self.key,
                        'format': style,
                        'docID': response_1.json()['docID']}
        response_2 = self.s.post(self.url_2, data=parameters_2)

        return response_2.json()['document']['keyTopics']
