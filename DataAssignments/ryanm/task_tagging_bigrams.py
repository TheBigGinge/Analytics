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

verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
nouns = ['NNS', 'NN', 'NNP']
adverb = ['RB', 'RBR', 'RBS']
adjective = ['JJ', 'JJR', 'JJS']

'''Overall counts for all word combos'''
all_word_counts = None
'''How many documents a word combo is in'''
word_documents = {}
'''Counts for each word combo in a document (job description)'''
job_documents = {}

print "Creating massive task dictionary...."
firs_iteration = True
for job in rollup_task_dict:

    if firs_iteration is True:
        raw = rollup_task_dict[job]
        text = nltk.word_tokenize(raw)
        check = nltk.pos_tag(text)
        word_bigram = list(nltk.bigrams(check))
        word_dict = coll.Counter(word_bigram)
        job_documents[job] = dict(word_dict)
        for words in list(set(word_bigram)):
            word_documents[words] = 1
        all_word_counts = word_dict
        firs_iteration = False
    else:
        try:
            raw = rollup_task_dict[job]
            text = nltk.word_tokenize(raw)
            check = nltk.pos_tag(text)
            word_bigram = list(nltk.bigrams(check))
            word_dict = coll.Counter(word_bigram)
            job_documents[job] = dict(word_dict)
            for words in list(set(word_bigram)):
                try:
                    word_documents[words] += 1
                except KeyError:
                    word_documents[words] = 1
            all_word_counts = all_word_counts + word_dict
        except UnicodeDecodeError:
            print job
            print raw

        except UnicodeEncodeError:
            print "Encode"
            print job
            print text

all_word_counts = dict(all_word_counts)
'''Total number of documents (N)'''
documents = len(rollup_task_dict.keys())

print "Writing to file..."
with open("C:\\users\\ryanm\\desktop\\BigramTasksAlt.csv", 'wb') as W:
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
            if ',' in words[0] or '.' in words[1]:
                continue
            if words[0][1] in nouns and words[1][1] in verbs:
                doc_count = job_documents[jobs][words]
                total_docs = word_documents[words]
                total_counts = all_word_counts[words]

                tf_idf = float(doc_count) * np.log((float(documents) / float(total_docs)))
                final = tf_idf, words

                word_score.append(final)

            elif words[0][1] in adverb and words[1][1] in verbs:
                doc_count = job_documents[jobs][words]
                total_docs = word_documents[words]
                total_counts = all_word_counts[words]

                tf_idf = float(doc_count) * np.log((float(documents) / float(total_docs)))
                final = tf_idf, words

                word_score.append(final)

            elif words[0][1] in adjective and words[1][1] in nouns:
                doc_count = job_documents[jobs][words]
                total_docs = word_documents[words]
                total_counts = all_word_counts[words]

                tf_idf = float(doc_count) * np.log((float(documents) / float(total_docs)))
                final = tf_idf, words

                word_score.append(final)

            elif words[0][1] in verbs and words[1][1] in nouns:
                doc_count = job_documents[jobs][words]
                total_docs = word_documents[words]
                total_counts = all_word_counts[words]

                tf_idf = float(doc_count) * np.log((float(documents) / float(total_docs)))
                final = tf_idf, words

                word_score.append(final)

            else:
                continue
        try:
            word_score = sorted(word_score)
            length = len(word_score)
            final = jobs, word_score[length - 1][1][0][0], word_score[length - 1][1][1][0]
            writer.writerow(final)
        except IndexError:
            final = jobs, 'N/A', 'N/A'
            writer.writerow(final)
