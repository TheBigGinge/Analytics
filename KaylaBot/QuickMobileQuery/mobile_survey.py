import LogFileTools.log_iterator as li
import mobile_questions as ques
import FileHandling.file_work as fw
import datetime
import SqlTools.payscale_replicated as pr
import csv
import os
import getpass

"""
This is a quick script thrown together to get activation rates for specific questions
The basic numbers such as saw 20, bail 20, etc come form the surveyprofiledata logs.
The activation counts come from psdb14
You need to be logged into the firewall and currently have SQL Server installed
"""
mobile_type = ['iPhone', 'Android', 'BlackBerry']
mobile_count = {}
overall_count = {}

final_active_mobile = {}
final_active_regular = {}
guid_dict = {}

temp_in = '\\\\filer01\\public\\Data_Analytics\\AnonReports\\TempIn\\MobileKayla\\'
temp_out = '\\\\filer01\\public\\Data_Analytics\\AnonReports\\TempOut\\MobileKayla\\'
start_date = datetime.datetime(2014, 10, 1)
end_date = datetime.datetime(2014, 10, 1)


is_active = set()
mobile_question_guid = {}
non_question_guid = {}
profile_class = {}


'''Log File Denominator pull'''
mobile_survey = li.CSVLogIterator(start_date, end_date)
mobile_survey.find_all_logs_survey()
local_path = os.path.expanduser("~" + getpass.getuser()) + "\\desktop\\"


def dict_insert(value, dictionary, key, question):
    if value == "True":
        try:
            dictionary[question][key] += 1
        except KeyError:
            try:
                dictionary[question][key] = 1
            except KeyError:
                dictionary[question] = {}
                dictionary[question][key] = 1


def get_profiles():

    print "Finding profile ids..."
    #Find profile_ids
    query = '''
    select * from BlobStore with (NOLOCK)
    where GUID in ('''

    for i, item in enumerate(current_guids):
        if i == len(current_guids) - 1:
            query += "'" + item + "')"
        else:
            query += "'" + item + "',"

    test = pr.SqlServer('Profiles')
    test.set_query_string(query)
    test.initialize_connection()

    for row in test.return_results():
        guid_dict[str(row.GUID).lower()] = row.ID

    print 'Finding if those profiles are active...'
    query = '''
    select Profile_ID, PROFILE_ACTIVE from Profiles with (NOLOCK)
    where Profile_ID in ('''

    for i, item in enumerate(current_guids):
        if i == len(current_guids) - 1:
            query += "'" + str(guid_dict[item]) + "')"
        else:
            query += "'" + str(guid_dict[item]) + "',"

    test = pr.SqlServer('PayscaleSearch')
    test.set_query_string(query)
    test.initialize_connection()

    for row in test.return_results():
        if str(row.PROFILE_ACTIVE) == '1':
            is_active.add(str(row.Profile_ID))

    #print len(is_active)
    #print len(guid_dict.keys())

    print 'Pulling field group / field answers...'
    query = '''
    select PROFILE_ID, FIELD_ID, FG_ID, STATUS from ProfileAnswers with (NOLOCK)
    where PROFILE_ID in ('''

    for i, item in enumerate(current_guids):
        if i == len(current_guids) - 1:
            query += "'" + str(guid_dict[item]) + "')"
        else:
            query += "'" + str(guid_dict[item]) + "',"

    test = pr.SqlServer('PayscaleSearch')
    test.set_query_string(query)
    test.initialize_connection()

    for row in test.return_results():
        if str(row.FIELD_ID) == '338':

            try:
                profile_class[str(row.PROFILE_ID)].add('Skill/Skill')
            except KeyError:
                profile_class[str(row.PROFILE_ID)] = set()
                profile_class[str(row.PROFILE_ID)].add('Skill/Skill')
        elif str(row.FG_ID) == '771' and str(row.FIELD_ID) == '586':
            try:
                profile_class[str(row.PROFILE_ID)].add('BachelorEducation/Major')
            except KeyError:
                profile_class[str(row.PROFILE_ID)] = set()
                profile_class[str(row.PROFILE_ID)].add('BachelorEducation/Major')
        elif str(row.FIELD_ID) == '344':
            try:
                profile_class[str(row.PROFILE_ID)].add('Certifications/Certifications')
            except KeyError:
                profile_class[str(row.PROFILE_ID)] = set()
                profile_class[str(row.PROFILE_ID)].add('Certifications/Certifications')


handler = fw.FileHandler()
for files in mobile_survey.log_files_to_use:
    print "Working on " + files
    current_guids = []
    for row in handler.open_csv(mobile_survey.path_to_use + files):
        saw_payscale = row[handler.header.index("SawMyPayscale")]
        saw_20 = row[handler.header.index("Saw20")]
        bail_20 = row[handler.header.index("Bailed20")]
        saw_30 = row[handler.header.index("Saw30")]
        bail_30 = row[handler.header.index("Bailed30")]
        guid = row[handler.header.index("ProfileGuid")].strip()
        guid_dict[guid] = 0
        current_guids.append(guid)

        if row[handler.header.index("Platform")] not in mobile_type:

            for question in ques.mobiles:
                try:
                    question_test = row[handler.header.index(question)]
                except KeyError:
                    question_test = 'N/A'

                if question_test == 'Field Shown':
                    try:
                        non_question_guid[question].add(guid)
                    except KeyError:
                        non_question_guid[question] = set()
                        non_question_guid[question].add(guid)

                    try:
                        overall_count[question]['Total'] += 1
                    except KeyError:
                        try:
                            overall_count[question]['Total'] = 1
                        except KeyError:
                            overall_count[question] = {}
                            overall_count[question]['Total'] = 1

                    dict_insert(saw_payscale, overall_count, 'SawPayScale', question)
                    dict_insert(saw_20, overall_count, 'Saw20', question)
                    dict_insert(saw_30, overall_count, 'Saw30', question)
                    dict_insert(bail_20, overall_count, 'Bail20', question)
                    dict_insert(bail_30, overall_count, 'Bail30', question)

        elif row[handler.header.index("Platform")] in mobile_type:
            for question in ques.mobiles:
                try:
                    question_test = row[handler.header.index(question)]
                except KeyError:
                    question_test = 'N/A'

                if question_test == 'Field Shown':
                    try:
                        mobile_question_guid[question].add(guid)
                    except KeyError:
                        mobile_question_guid[question] = set()
                        mobile_question_guid[question].add(guid)
                    try:
                        mobile_count[question]['Total'] += 1
                    except KeyError:
                        try:
                            mobile_count[question]['Total'] = 1
                        except KeyError:
                            mobile_count[question] = {}
                            mobile_count[question]['Total'] = 1

                    dict_insert(saw_payscale, mobile_count, 'SawPayScale', question)
                    dict_insert(saw_20, mobile_count, 'Saw20', question)
                    dict_insert(saw_30, mobile_count, 'Saw30', question)
                    dict_insert(bail_20, mobile_count, 'Bail20', question)
                    dict_insert(bail_30, mobile_count, 'Bail30', question)

    get_profiles()


print "Counting active profiles by question..."
for question in non_question_guid:
    for guid in non_question_guid[question]:
        profile = guid_dict[guid.lower()]
        if str(profile) in is_active:
            try:
                question_set = profile_class[str(profile)]
            except KeyError:
                question_set = 'N/A'
            if question == 'Certifications/Certifications' and question in question_set:
                try:
                    final_active_regular[question] += 1
                except KeyError:
                    final_active_regular[question] = 1
            elif question == 'Skill/Skill' and question in question_set:
                try:
                    final_active_regular[question] += 1
                except KeyError:
                    final_active_regular[question] = 1
            elif question == 'BachelorEducation/Major' and question in question_set:
                try:
                    final_active_regular[question] += 1
                except KeyError:
                    final_active_regular[question] = 1

for question in mobile_question_guid:
    for guid in mobile_question_guid[question]:
        profile = guid_dict[guid.lower()]
        if str(profile) in is_active:
            try:
                question_set = profile_class[str(profile)]
            except KeyError:
                question_set = 'N/A'
            if question == 'Certifications/Certifications' and question in question_set:
                try:
                    final_active_mobile[question] += 1
                except KeyError:
                    final_active_mobile[question] = 1
            elif question == 'Skill/Skill' and question in question_set:
                try:
                    final_active_mobile[question] += 1
                except KeyError:
                    final_active_mobile[question] = 1
            elif question == 'BachelorEducation/Major' and question in question_set:
                try:
                    final_active_mobile[question] += 1
                except KeyError:
                    final_active_mobile[question] = 1

print "Writing to file..."
with open(local_path + "Mobile Survey.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')
    header = ['Question', 'Value', 'Non-Mobile', 'Mobile']

    writer.writerow(header)

    for question in overall_count:

        try:
            regular_active = final_active_regular[question]
        except KeyError:
            regular_active = 0

        try:
            mobile_active = final_active_mobile[question]
        except KeyError:
            mobile_active = 0

        final = question, 'Active Profiles', regular_active, mobile_active
        writer.writerow(final)

        for keys in overall_count[question]:
            try:
                overall = overall_count[question][keys]
            except KeyError:
                overall = 0

            try:
                mobile = mobile_count[question][keys]
            except KeyError:
                mobile = 0
            final = question, keys, overall, mobile
            writer.writerow(final)