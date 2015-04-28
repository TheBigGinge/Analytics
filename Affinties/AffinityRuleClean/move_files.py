import shutil
import os
import collections
from Affinties.AffinityRuleClean import new_directories


class CopyFiles:
    """
    Can classify affinties for production, dev, and test.

    Here's an example of how to use this:
        classify = CopyFiles("C:\\users\\ryanm\\affinities_prod\\",
                             "C:\\users\\ryanm\\desktop\\affinities_moved_prod\\")
        classify.run()
        classify.test_files()

    It classifies then copies all the files. You will then need to delete all the files (EXCEPT HG!!!!)
    from the repo folder and then paste the new files in there.

    Run a hg addremove afterwards to pick up all the changes.

    NOTE: This was written to classify the affinities from the original repo (folders from 0 to 250). This will need
          to be changed to handle the folder "Possible Duplicates" if we want to add more classification handling
          in the future.
    """

    def __init__(self, original_affinity_path, new_affinity_path):
        """
        :param original_affinity_path:
            File path to the repo
        :param new_affinity_path:
            file path to where you want the affinities classified and copied to.
        :return:
            All the affinities reclassified in your specified folder
        """
        self.copy_count = 0
        self.original_affinity_path = original_affinity_path
        self.new_affinity_path = new_affinity_path
        self.classified = set()
        self.original_affinities = collections.OrderedDict()
        self.new_affinities = collections.OrderedDict()
        self.missing_keys = set()
        self.file_found = False
        self.create_directories()

    def create_directories(self):

        if not os.path.exists(self.new_affinity_path):
            os.makedirs(self.new_affinity_path)

        for values in new_directories.new_directories:
            if not os.path.exists(self.new_affinity_path + values + '\\'):
                os.makedirs(self.new_affinity_path + values + '\\')

    def file_cycle(self):

        for directories in os.listdir(self.original_affinity_path):
            if '.hg' not in directories:

                for files in os.listdir(self.original_affinity_path + directories + '\\'):
                    yield directories, files

    def run(self):

        print "Copying files to proper directories"

        file_counter = 0
        for directories, files in self.file_cycle():
            directories += '\\'
            file_counter += 1

            if file_counter % 5000 == 0:
                print "Copied %s files" % file_counter

            if files not in self.classified:
                affinity_id, affinity_name, all_text = \
                    self.get_affinity_information(self.original_affinity_path + directories, files)

                self.naics_parse(files, directories, affinity_name, affinity_id)
                self.onet_parse(files, directories, affinity_name, affinity_id)
                self.ipeds_parse(files, directories, affinity_name, affinity_id)
                self.question_affinity_parse(files, directories, affinity_name, affinity_id)
                self.classify_easy_files(files, directories, affinity_name, affinity_id)
                self.classify_using_text(files, directories, all_text, affinity_id, affinity_name)

                if self.file_found is False:
                    location = new_directories.directory_keys['Unable To Classify']
                    self.copy_to_new_directory(files, directories, location)
                    self.new_affinities[affinity_id] = files

            self.file_found = False

    def copy_to_new_directory(self, files, directories, location=None, keys=None, dictionary=None,
                              affinity_name=None):
        """
        Copies files from the original path to the newly designated one.
        :param files:
            file to copy
        :param directories:
            iterated directory of the original location
        :param location:
            new directory the file is going to
        :param keys:
            dictionary key that references where to place the file
        :param dictionary:
            dictionary from the new_directories.py file
        :return:
            nothing
        """
        if keys is not None:
            location = dictionary[keys]
            shutil.copy(self.original_affinity_path + directories + files, self.new_affinity_path + location
                        + '\\' + files)
            self.classified.add(files)
            self.file_found = True
        else:
            shutil.copy(self.original_affinity_path + directories + files, self.new_affinity_path + location
                        + '\\' + files)
            self.classified.add(files)
            self.file_found = True

    def naics_parse(self, files, directories, affinity_name, affinity_id):

        if self.file_found is False:
            if "NAICS CODE" in affinity_name and "2012" not in affinity_name:
                location = new_directories.directory_keys['NAICS CODE']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "2012 NAICS CODE" in affinity_name:
                location = new_directories.directory_keys['2012 NAICS CODE']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

    def onet_parse(self, files, directories, affinity_name, affinity_id):
        if self.file_found is False:
            if "Unclassified" in affinity_name and "PayScale Code" in affinity_name:
                location = new_directories.directory_keys['Unclassified']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "Generic" in affinity_name and "PayScale Code" in affinity_name:
                location = new_directories.directory_keys['Generic']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "Generic" not in affinity_name and "Unclassified" not in affinity_name \
                    and "PayScale Code" in affinity_name:
                location = new_directories.directory_keys['PayScale Code']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

    def ipeds_parse(self, files, directories, affinity_name, affinity_id):
        if self.file_found is False:
            if "IPEDS ID" in affinity_name and "2013" not in affinity_name:
                location = new_directories.directory_keys['IPEDS ID']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)
                self.new_affinities[affinity_id] = files

            elif "2013 IPEDS ID" in affinity_name:
                location = new_directories.directory_keys['2013 IPEDS ID']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

    def question_affinity_parse(self, files, directories, affinity_name, affinity_id):
        if self.file_found is False:
            if "SEARCH SURVEY" in affinity_name:
                location = new_directories.directory_keys['SEARCH SURVEY']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "SEARCH" in affinity_name and "SURVEY" not in affinity_name:
                location = new_directories.directory_keys['SEARCH']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "People with" in affinity_name and "SEARCH" not in affinity_name:
                location = new_directories.directory_keys['People with']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)
                self.new_affinities[affinity_id] = files

            elif "People Asked" in affinity_name and "SEARCH" not in affinity_name:
                location = new_directories.directory_keys['People Asked']
                self.copy_to_new_directory(files, directories, location)

            elif "People in " in affinity_name and "Region" in affinity_name:
                location = new_directories.directory_keys['Region']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "People who" in affinity_name:
                location = new_directories.directory_keys['People Asked']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

    def classify_using_text(self, files, directories, all_text, affinity_id, affinity_name):

        if self.file_found is False:
            #needed to add this historical first otherwise it would cause copying errors
            if "status\\historical" in all_text:
                location = new_directories.directory_keys['historical']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "PayScale Code" and " {Unclassified" in all_text:
                location = new_directories.directory_keys['Unclassified']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "PayScale Code" and " {Generic" in all_text:
                location = new_directories.directory_keys['Generic']
                self.copy_to_new_directory(files, directories, location)

            elif "PayScale Code" in all_text and " {Generic" not in all_text and " {Unclassified" not in all_text:
                location = new_directories.directory_keys['PayScale Code']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "field\\county" in all_text and "indexas\\county" in all_text:
                location = new_directories.directory_keys['County']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)

            elif "Combined Statistical Area}" in all_text:
                location = new_directories.directory_keys['Combined Statistical Area']
                self.copy_to_new_directory(files, directories, location, affinity_name=affinity_name)
            else:
                [self.copy_to_new_directory(files, directories, keys=keys,
                 dictionary=new_directories.in_line_keys, affinity_name=affinity_name)
                 for keys in new_directories.in_line_keys.keys() if keys in all_text]

    def classify_easy_files(self, files, directories, affinity_name, affinity_id):
        #originally used affinity name but since City, State, and Country have different affinity names
        #than their actual name inside the rule I went back to file name
        if self.file_found is False:
            [self.copy_to_new_directory(files, directories, keys=keys, dictionary=new_directories.easy_classify,
                                        affinity_name=affinity_name)
             for keys in new_directories.easy_classify.keys() if keys in files]

    def test_files(self):
        """
        Making sure nothing crazy went wrong with the copying.
        Checks for matches for all files between original repo and new classification.
        It also counts the original files and compares them to the count of newly classified files.
        :return:
            results of the file matching and the results of the counts comparison
        """
        print "Testing..."

        new_set_count = 0
        old_set_count = 0

        print "Pulling affinity ID's and file location from original affinties..."
        for directories in os.listdir(self.original_affinity_path):
            if '.hg' not in directories:

                for files in os.listdir(self.original_affinity_path + directories + '\\'):
                    affinity_id, affinity_name, all_text = \
                        self.get_affinity_information(self.original_affinity_path + directories + '\\', files)

                    self.original_affinities[affinity_id] = self.original_affinity_path + directories + "\\" + files
                    old_set_count += 1

        print "Pulling affinity ID's and file location for all newly placed affinties...."

        for directories in os.listdir(self.new_affinity_path):
            if '.hg' not in directories:

                for files in os.listdir(self.new_affinity_path + directories + '\\'):
                    affinity_id, affinity_name, all_text = \
                        self.get_affinity_information(self.new_affinity_path + directories + '\\', files)
                    new_set_count += 1
                    self.new_affinities[affinity_id] = files

        original_keys = set(self.original_affinities.keys())
        new_keys = set(self.new_affinities.keys())

        missing_counter = 0

        for id_number in original_keys:

            if id_number not in new_keys:
                missing_counter += 1
                self.missing_keys.add(id_number)
                print str(id_number) + " : Found in original directory but not in new directory. " \
                                       "Probably a case copying error"

        print "Missing %s files" % missing_counter
        print "Original file count: %s, New file count: %s" % (old_set_count, new_set_count)

        print "Adding missing affinties back in via the Possible Duplicates Folder..."
        self.add_missing_affinties()

    @staticmethod
    def get_affinity_information(directory, files):
        """
        A lot of the affinities will not have their full name as the name of the .txt file. Also, many affinities
        have the same name as other affinities. The only way around this is looking at their text inside
        to get their unique ID's, full name, and full text.

        This slows the process down since I have to open all files but it makes sure every affinity is accounted for.
        :param directory:
            original directory (repo)
        :param files:
            file name
        :return:
            The affinity ID, the affinity name, and the full text in a set
        """

        with open(directory + files, 'rb') as open_file:

            for line in open_file:
                all_text = line
                affinity_id = line[:line.find("{")].strip().replace("Rule ", "")

                #parsing affinity for it's full name
                start_int = line.find("{") + 1
                affinity_name = line[start_int:]
                affinity_name = affinity_name[: affinity_name.find("}")].strip()

                return affinity_id, affinity_name, all_text

    def add_missing_affinties(self):

        print "Adding in the missing affinities..."

        for affinity_id in self.missing_keys:
            new_path = self.new_affinity_path + "Possible Duplicates\\" + str(affinity_id) + "\\"

            if not os.path.exists(new_path):
                os.makedirs(new_path)

            start_int = self.original_affinities[affinity_id].rfind("\\") + 1
            final_file_name = self.original_affinities[affinity_id][start_int:].strip()

            shutil.copy(self.original_affinities[affinity_id], new_path + final_file_name)

        #Final Test

        old_count = len(self.original_affinities.keys())
        new_count = 0

        for directories in os.listdir(self.new_affinity_path):

            for files in os.listdir(self.new_affinity_path + directories + "\\"):
                new_count += 1

        print "Newly placed affinity account now: %s, Original Affinity Account: %s" % (new_count, old_count)
        print "Copying now complete"