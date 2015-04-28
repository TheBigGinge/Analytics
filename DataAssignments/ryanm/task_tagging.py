# -*- coding: utf-8 -*-
import nltk
import RyanBot.DataDashboard.data_dashboard as dd
import RyanBot.DataDashboard.dashboard_support as ds
import collections as coll
import csv
import numpy as np


roll_dict = dd.DataDashboard().create_all_rollup_dictionary()
all_rolls = set(roll_dict.values())

task_dict = dd.DataDashboard().find_tasks_for_rollups()

rollup_task_dict = ds.DashboardSupport().create_full_task_dictionary()
print "Removing non answer values..."
for job in rollup_task_dict.keys():
    if job not in all_rolls:
        rollup_task_dict.pop(job)

'''Overall counts for all words'''
all_word_counts = None
'''How many documents a word is in'''
word_documents = {}
'''Counts for each word in a document (job description)'''
job_documents = {}

print "Creating massive task dictionary...."
firs_iteration = True
for job in rollup_task_dict:

    if firs_iteration is True:
        first = rollup_task_dict[job]
        raw = first.encode('utf-8').decode('ascii', 'replace')
        raw = raw.strip()
        text = nltk.word_tokenize(raw)
        tagged_text = nltk.pos_tag(text)
        word_dict = coll.Counter(tagged_text)
        job_documents[job] = dict(word_dict)
        for words in list(set(tagged_text)):

            word_documents[words] = 1
        all_word_counts = word_dict
        firs_iteration = False
    else:

        first = rollup_task_dict[job]
        raw = first.encode('utf-8').decode('ascii', 'replace')
        raw = raw.strip()
        text = nltk.word_tokenize(raw)
        tagged_text = nltk.pos_tag(text)
        word_dict = coll.Counter(tagged_text)
        job_documents[job] = dict(word_dict)
        for words in list(set(tagged_text)):

            try:
                word_documents[words] += 1
            except KeyError:
                word_documents[words] = 1
        all_word_counts = all_word_counts + word_dict


all_word_counts = dict(all_word_counts)
'''Total number of documents (N)'''
documents = len(rollup_task_dict.keys())

print "Writing to file..."
with open("C:\\users\\ryanm\\desktop\\SingularTasksAlt.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')
    header = ['Rollup', 'Top Word', 'Second Word']
    writer.writerow(header)
    print "Finding the highest tf-idf words..."
    job_count = 0
    for jobs in job_documents:
        job_count += 1
        if job_count % 100 == 0:
            print "%s jobs processed..." % job_count
        word_score = []
        for words in job_documents[jobs]:
            if ',' in words or '.' in words:
                continue
            if words[1] not in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'NNS', 'NN', 'NNP']:
                continue
            else:
                doc_count = job_documents[jobs][words]
                total_docs = word_documents[words]
                total_counts = all_word_counts[words]

                tf_idf = float(doc_count) * np.log((float(documents) / float(total_docs)))
                final = tf_idf, words[0]

                word_score.append(final)

        word_score = sorted(word_score)
        length = len(word_score)
        final = jobs, word_score[length - 1][1], word_score[length - 2][1]
        writer.writerow(final)