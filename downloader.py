from Bio import Entrez
from urllib.error import HTTPError
import time
import os

from common.commonFunc import CommonFunctions as Cf


class Downloader(object):
    def __init__(self, email, database='nuccore', type_of_return='text'):
        """
        Main function for downloading a list of accession codes from NCBI.

        :param email: Required for identification purposes in NCBI servers.
        :param database: Which database are we querying on.
        refer to:
        https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly
        for more information of the accepted databases.
        default: 'nuccore' - (Nucleotide)
        :param type_of_return: the return type of the data donwloaded from NCBI, default 'text'
        refer to:
        https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly
        for more information about the possible return types
        """
        Entrez.email = email
        self.list_of_accession = []

        self.db = database
        self.type_of_return = type_of_return
        self.web_env = ''
        self.query_key = ''
        self.fetch_handles = ''
        self.save_directory = ''
        self.common_functions = Cf()
        self.save_path = ''

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i + n]

    def start(self):
        """
        For downloading the files.
        Choose between typing the accession codes, or passing a file with them.

        FASTA and GB files are first searched in the specified database to later be downloaded, parsed and
        written to a file.
        :return:
        """
        commonfunc = Cf()
        files_e = []
        final_list_acc = []

        print("Module for downloading genomes files from NCBI.")
        file_or_not = commonfunc.query_yes_no("Want to input the accession numbers or pass a file with them?.")
        if file_or_not:
            print("Please input list of accession numbers (comma separated).")
            data = commonfunc.check_input()
            self.list_of_accession = data.split(sep=',')
        else:
            print("Please input the location of the file.")
            file_loc = commonfunc.check_input()
            with open(file_loc) as accession_lines:
                for line in accession_lines:
                    self.list_of_accession.append(line.strip())

        print("Removing possible duplicates.")
        self.list_of_accession = list(set(self.list_of_accession))
        print('Enter a directory to save the files.')
        self.save_directory = commonfunc.check_input()
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        else:
            pass
        print("Do you want to download Fasta or Genbank files?")
        print("1 - Fasta Files")
        print("2 - Genbank Files")
        while True:
            try:
                user_input = self.common_functions.check_input()
                if user_input == '1':
                    print('Fasta files')
                    temp_l = Cf().get_files(file_extensions='*.fasta', directory=self.save_directory)
                    final_files = [file + '.fasta' for file in self.list_of_accession]
                    print(self.save_directory)
                    print('There already ' + str(len(temp_l)) + ' downloaded files.')
                    print(len(final_files))

                    for f in temp_l:
                        files_e.append(os.path.basename(f))
                    filtered = list(set(final_files).difference(files_e))
                    for acc in filtered:
                        final_list_acc.append(os.path.splitext(os.path.basename(acc))[0])

                    if final_list_acc:
                        print('Total of: ' + str(len(final_list_acc)) + ' accession numbers.')
                        for x, chunked_list in enumerate(self.chunks(final_list_acc, 1000), start=1):
                            print('Chunk ' + str(x) + ' of ' + str(len(chunked_list)))
                            self.download(type_of_file='fasta', starts_with='>', list_acc=chunked_list)
                    else:
                        print('Nothing to download. Terminating.')
                        exit()

                elif user_input == '2':
                    print('Genbank Files')
                    temp_l = Cf().get_files(file_extensions='*.gb', directory=self.save_directory)
                    final_files = [file + '.gb' for file in self.list_of_accession]
                    print(self.save_directory)
                    print('There already ' + str(len(temp_l)) + ' downloaded files.')
                    print(len(final_files))

                    for f in temp_l:
                        files_e.append(os.path.basename(f))
                    filtered = list(set(final_files).difference(files_e))

                    for acc in filtered:
                        final_list_acc.append(os.path.splitext(os.path.basename(acc))[0])

                    if final_list_acc:
                        print('Total of: ' + str(len(final_list_acc)) + ' accession numbers.')
                        for x, chunked_list in enumerate(self.chunks(final_list_acc, 1000), start=1):
                            print('Chunk ' + str(x) + ' of ' + str(len(chunked_list)))
                            self.download(type_of_file='gb', starts_with='LOCUS', list_acc=chunked_list)
                    else:
                        print('Nothing to download. Terminating.')
                        exit()
                else:
                    pass
            except ValueError:
                print('Invalid option.\n')
            else:
                break

    def search(self, list_of_acc):
        """
        This function takes the type of file for searching and the accession codes given previously to
        search for them in the specified database of NCBI.
        :return:
        """
        try:
            search_handle = Entrez.epost(db="nuccore", id=",".join(list_of_acc))
            search_results = Entrez.read(search_handle)
            self.web_env = search_results["WebEnv"]
            self.query_key = search_results["QueryKey"]
        except RuntimeError:
            search_handle = Entrez.epost(db="nuccore", id=",".join(list_of_acc))
            search_results = Entrez.read(search_handle)
            self.web_env = search_results["WebEnv"]
            self.query_key = search_results["QueryKey"]

        print(self.web_env)
        print(self.query_key)

    def download(self, type_of_file, starts_with, list_acc):
        """

        This function connects to NCBI through Entrez and manage the download of the files.


        :param type_of_file: what type of file are we downloading.
        :param starts_with: which character is the first of the file to be downloaded.
        '>' for fasta files
        'LOCUS' for gb files.
        :param list_acc
        :return:
        """
        self.search(list_of_acc=list_acc)
        batch_size = 10
        count = len(list_acc)
        for start in range(0, count, batch_size):
            end = min(count, start + batch_size)
            print('Downloading record %i of %i' % (start + 1, end), 'of %i' % count)
            attp = 0
            while attp < 5:
                attp += 1
                try:
                    self.fetch_handles = Entrez.efetch(db=self.db, rettype=type_of_file, retmode=self.type_of_return,
                                                       webenv=self.web_env,
                                                       query_key=self.query_key,
                                                       retstart=start,
                                                       retmax=batch_size)
                    time.sleep(5)
                # except urllib3.exceptions.HTTPError as err:
                except HTTPError as err:
                    if 400 <= err.code <= 599:
                        print("Received error from server %s" % err)
                        print('Attempt %i of 3' % attp)
                        print("Waiting 1 minute")
                        time.sleep(60)
                    else:
                        raise

            self.parser(fetched_files=self.fetch_handles,
                        type_of_file=type_of_file,
                        starts_with=starts_with,
                        file_number=start,
                        list_acc=list_acc)

    def parser(self, fetched_files, type_of_file, starts_with, file_number, list_acc):
        """
        The idea behind this function is to parse the data downloaded from NCBI. A unique file is downloaded if you
        input two or more accession codes to download, so it's necessary to write the data for each file in separated
        files.


        :param fetched_files: Downloaded data from NCBI, comes all in once
        :param type_of_file: what are we downloading
        :param starts_with: first character of the file
        :param file_number: what file are we currently downloading and parsing
        :param list_acc
        :return:
        """
        extension = ''
        file = ''

        if type_of_file == 'fasta':
            extension = 'fasta'
        elif type_of_file == 'gb':
            extension = 'gb'

        for line in fetched_files:
            if line.startswith(starts_with):
                save_path = os.path.normpath(
                    os.path.join(self.save_directory, list_acc[file_number]))
                file = open(save_path + '.' + extension, 'w')
                print('Saving: ' + list_acc[file_number])
                file_number += 1
            file.write(line)
