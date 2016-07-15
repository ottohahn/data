import psycopg2
import pandas as pd

if __name__ == '__main__':

    f = open('postgres.txt', 'r')
    dct = {}
    keys = ['database', 'user', 'password', 'host', 'port']
    for key, line in zip(keys, f.readlines()):
        dct[key] = line.strip()

    conn = psycopg2.connect(database=dct['database'], user=dct['user'],
                            password=dct['password'], host=dct['host'],
                            port=dct['port'])
    # c = conn.cursor()
    query = """
    SELECT
        a.id,
        -- a.first_name,
        -- a.last_name,
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
    # c.execute(query)
    # output = c.fetchall()
    df = pd.read_sql_query(query, conn)
    df.to_csv(path_or_buf='data/skill_cluster_df.csv')
