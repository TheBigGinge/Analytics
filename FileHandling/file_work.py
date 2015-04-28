import csv
import zipfile
import os
import time


class FileHandler:
    """
        General file work that you do over and over... blindly... madly... insanely... all work and no play...
    """

    def __init__(self):
        self.header = None
        self.all_files_directory = []

    def open_tsv(self, target_file, header=True):

        with open(target_file, 'rb') as R:
            reader = csv.reader(R, delimiter='\t')

            if header is True:
                self.header = reader.next()

            for row in reader:
                yield row

    def open_csv(self, target_file, header=True):

        with open(target_file, 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            if header is True:
                self.header = reader.next()

            for row in reader:
                yield row

    @staticmethod
    def zip_file_open(zip_file, file_path):

        assert os.path.isdir(file_path) is True, '%s is not a directory' % str(file_path)

        full_zip_file = zipfile.ZipFile(file_path + zip_file)
        file_list = full_zip_file.namelist()

        [full_zip_file.extract(file_name, file_path) for file_name in file_list]

    def find_all_files(self, directory):

        assert os.path.isdir(directory) is True, '%s is not a directory' % str(directory)

        [self.all_files_directory.append(files) for files in os.listdir(directory)]

    def find_all_files_exclusion(self, directory, exclusion_string):

        assert type(exclusion_string) == type(str()), '%s is not as string' % str(exclusion_string)
        assert os.path.isdir(directory) is True, '%s is not a directory' % str(directory)

        [self.all_files_directory.append(files) for files in os.listdir(directory) if exclusion_string not in files]

    def find_all_files_inclusion(self, directory, inclusion_string):

        assert type(inclusion_string) == type(str()), '%s is not as string' % str(inclusion_string)
        assert os.path.isdir(directory) is True, '%s is not a directory' % str(directory)

        [self.all_files_directory.append(files) for files in os.listdir(directory) if inclusion_string in files]


def find_most_recently_created_file(file_directory):
    time_dict = {}

    for files in os.listdir(file_directory):

        recent_time = time.ctime(os.path.getmtime(file_directory + files))
        time_dict[recent_time] = files

    max_time = max(time_dict.keys())

    return time_dict[max_time]