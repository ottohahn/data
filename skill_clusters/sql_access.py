#!/usr/bin/env python
# encoding: utf-8
"""
sql_access.py
"""
import datetime
import psycopg2
import pandas as pd

if __name__ == '__main__':

    # Load private PostGRES DB credentials
    f = open('postgres.txt', 'r')
    dct = {}
    keys = ['database', 'user', 'password', 'host', 'port']
    for key, line in zip(keys, f.readlines()):
        dct[key] = line.strip()

    # Connect to postgres DB and run query
    conn = psycopg2.connect(database=dct['database'], user=dct['user'],
                            password=dct['password'], host=dct['host'],
                            port=dct['port'])

    # This query is specific to Thumbtack
    query = """
    SELECT
        a.id,
        a.roles,
        at.trend_id,
        t.name,
        t.kind
    FROM applicants a
    INNER JOIN applicant_trends at
    ON a.id = at.applicant_id
    INNER JOIN trends t
    ON at.trend_id = t.id
    WHERE t.kind IN (
        'Agencies',
        'Animal',
        'Awards',
        'Brands',
        'Character',
        'Communication',
        'Custom',
        'FieldTerminology',
        'JobTitle',
        'OperatingSystem',
        'Organization',
        'Organizations',
        'ProfessionalDegree',
        'Skill Cluster',
        'Software systems',
        'Technology')
    AND a.company_id = 8
    AND ARRAY['engineer', 'engineering'] @> a.roles
    ;
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv(path_or_buf='data/thumbtack_skill_cluster_df_' +
              str(datetime.date.today()) + '.csv')
