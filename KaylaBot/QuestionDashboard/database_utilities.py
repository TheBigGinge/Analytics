import csv

main_file_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\"


def get_all_the_questions():

    all_questions = []

    with open(main_file_path + 'All_Questions.csv', 'rb') as R:
        reader = csv.reader(R, delimiter=',')

        [all_questions.append(row[0]) for row in reader if row[0] != 'All Questions']

    return all_questions