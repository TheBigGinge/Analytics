import FileHandling.file_work as fw
import csv
import nltk


def jaccard_index(string_1, string_2):

    bigram1 = list(nltk.bigrams(string_1.lower()))
    bigram2 = list(nltk.bigrams(string_2.lower()))

    union = bigram1 + bigram2

    intersect = 0

    for Set in union:
        if Set in bigram1 and Set in bigram2:
            intersect += 1
        else:
            continue

    jaccard = float(intersect) / float(len(union))

    return jaccard

print "Gathering probabilities..."
combo_probs = {}
with open("C:\\users\\ryanm\\desktop\\ProbabilityCache.csv", 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    header = reader.next()

    for row in reader:
        combo = row[0].lower(), row[1].lower()
        combo_probs[combo] = row[2]

write_header = True
handler = fw.FileHandler()
row_count = 0
with open("C:\\users\\ryanm\\desktop\\truth_data_with_basesalary_comparisons_and_prob.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    for line in handler.open_csv("C:\\users\\ryanm\\desktop\\truth_data_with_basesalary_comparisons.csv"):
        row_count += 1

        if row_count % 1000 == 0:
            print "Processed %s rows..." % row_count

        if write_header is True:
            handler.header.append("Probability")
            writer.writerow(handler.header)
            write_header = False

        internal = line[handler.header.index("InternalTitle")]
        rollup = line[handler.header.index("MatchedRollup")]
        combo = rollup.lower(), internal.lower()

        try:
            probability = combo_probs[combo]
        except KeyError:
            probability = 0
            for keys in combo_probs:
                if keys[0] == rollup.lower():
                    jaccard = jaccard_index(internal, keys[1])
                    if jaccard > .94:
                        combo = rollup.lower(), keys[1].lower()
                        probability = combo_probs[combo]
                        break

        line.append(probability)

        writer.writerow(line)