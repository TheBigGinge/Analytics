import SqlTools.postgres_heroku as ph

postgres = ph.PostgresHeroku()
conn_string = "host=ec2-23-23-199-181.compute-1.amazonaws.com dbname=d9g290r40m5d9p port=5432 " + \
              "user=pgfffwsqctjvtd password=hjTE-HRs9fzpnyAGq-YgJohQ2a"

postgres.set_conn_string_from_string(conn_string)
postgres.authenticate()

postgres.sql_command('''DROP TABLE answers''')
postgres.sql_command('''CREATE TABLE answers (Job_Code text, Job_Title text, PayScale_Title text, Match_Code text,
                     Score text, Start_Time text, End_Time text, Verifier text, Accepted text)''')

postgres.commit_and_close()