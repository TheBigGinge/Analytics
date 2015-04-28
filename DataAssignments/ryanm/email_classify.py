import FileHandling.file_work as fw
import zipfile
import RyanBot.DataDashboard.data_dashboard as dd
import csv


file_path = '\\\\filer02\\public\\Email\\'
handler = fw.FileHandler()


def unzip_file(zip_file):
    #TODO: Make this method appear in file handling and replace this method and the one in Data Dist

    full_zip_file = zipfile.ZipFile(file_path + zip_file)
    file_list = full_zip_file.namelist()

    [full_zip_file.extract(file_name, file_path) for file_name in file_list]

#unzip_file('members_export_8e23b4cca9.zip')
rollup_dict = dd.DataDashboard().create_all_rollup_dictionary()
mapping = {}

for row in handler.open_csv("C:\\users\\ryanm\\desktop\\mapping_email.csv"):
    mapping[row[0]] = row[1]

supers = []
fires = []
secondary = []
post_second = []
machine = []


def rollup_try(job_title):
    try:
        rollup = rollup_dict[job_title]
    except KeyError:
        rollup = 'N/A'

    return rollup


def classification(job_title, rollup):

    try:
        classify = mapping[job_title]
    except KeyError:
        try:
            classify = mapping[rollup]
        except KeyError:
            classify = 'N/A'

    return classify

header = None
write_header = True
line_count = 1
for row in handler.open_csv(file_path + 'members_export_8e23b4cca9.csv'):
    if line_count % 10000 == 0:
        print "Processed %s rows..." % line_count
    line_count += 1

    if write_header is True:
        header = handler.header
        write_header = False

    if row[handler.header.index("Job Title")] != "":
        rollup = rollup_try(row[3])
        classify = classification(row[3], rollup)

        if classify == 'N/A':
            continue
        else:
            if classify == 'Machinists':
                machine.append(row)
            if classify == 'Post Secondary':
                post_second.append(row)
            if classify == 'Non Secondary':
                secondary.append(row)
            if classify == 'FireFighter':
                fires.append(row)
            if classify == 'Supervisor \ Manager':
                supers.append(row)


def write_to_file(category):

    if category == 'Supervisor \ Manager':
        file_name = 'SupervisorManager.csv'
        list_use = supers
    elif category == 'FireFighter':
        file_name = 'FireFighters.csv'
        list_use = fires
    elif category == 'Non Secondary':
        file_name = 'Secondary.csv'
        list_use = secondary
    elif category == 'Post Secondary':
        file_name = 'PostSecondary.csv'
        list_use = post_second
    else:
        file_name = 'Machinists.csv'
        list_use = machine

    with open(file_path + file_name, 'wb') as W:
        writer = csv.writer(W, lineterminator='\n')

        writer.writerow(header)

        for row in list_use:
            writer.writerow(row)

write_to_file('Machinists')
write_to_file('FireFighter')
write_to_file('Non Secondary')
write_to_file('Post Secondary')
write_to_file('Supervisor \ Manager')