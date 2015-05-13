import csv
import SqlTools.postgres_heroku as ph

conn_string = "host=ec2-23-23-199-181.compute-1.amazonaws.com dbname=d9g290r40m5d9p port=5432 " + \
              "user=pgfffwsqctjvtd password=hjTE-HRs9fzpnyAGq-YgJohQ2a"

write_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\TempData\\"


postgres = ph.PostgresHeroku()
postgres.set_conn_string_from_string(conn_string)
postgres.authenticate()


query = "SELECT * FROM answers"

postgres.sql_command(query)

rows = postgres.fetchall()

with open(write_path + 'JobMatcherResults.csv', 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    header = ['Job Code', 'Job Title', 'PayScale Title', 'Match Code', 'Score', 'Start Time', 'End Time', 'Verifier',
              'Accepted']
    writer.writerow(header)

    for row in rows:
        writer.writerow(row)

postgres.commit_and_close()