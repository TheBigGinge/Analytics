import RyanBot.DataDashboard.data_dashboard as dd
import random

job_dict = dd.DataDashboard().create_all_rollup_dictionary()

test_list = job_dict.keys()

index = random.sample(xrange(len(test_list)), 1)[0]

print test_list[index]