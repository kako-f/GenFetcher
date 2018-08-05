import argparse


class ArgumentParser(object):
    def __init__(self, prog_version, argv, program_name):
        """

        :param prog_version:
        :param argv:
        :param program_name:
        """
        self.program_v = prog_version
        self.arguments = argv
        self.ap = argparse.ArgumentParser(description=program_name + " is a program writen in Python3 to find "
                                                                     "download genomic data from NCBI."
                                                                     "Written by Camilo Fuentes Beals."
                                                                     "\n Program version: " + self.program_v)

        file_group = self.ap.add_mutually_exclusive_group(required=True)
        file_group.add_argument('-d', '--download', action='store_true', help='Download genome data from NCBI.')

    def return_arguments(self):
        """

        :return: Processed arguments.
        """
        return self.ap.parse_args(self.arguments)
