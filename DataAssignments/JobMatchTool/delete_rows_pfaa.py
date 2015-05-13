import SqlTools.postgres_heroku as ph

conn_string = "host=ec2-23-23-199-181.compute-1.amazonaws.com dbname=d9g290r40m5d9p port=5432 " + \
              "user=pgfffwsqctjvtd password=hjTE-HRs9fzpnyAGq-YgJohQ2a"

postgres = ph.PostgresHeroku()
postgres.set_conn_string_from_string(conn_string)
postgres.authenticate()

query = "DELETE FROM pfaa WHERE job_title = 'accounting assistant' AND payscale_title = 'accounting assistant'" \
        "AND lm_industry = 'professional, scientific, and technical services'"

postgres.sql_command(query)

postgres.commit_and_close()