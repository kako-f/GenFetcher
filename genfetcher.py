import sys
import platform
import datetime

from common.argumentParser import ArgumentParser as Ap
from common.commonFunc import CommonFunctions as Cf
from downloader import Downloader as Dl

program_name = 'GenFetcher'
program_ver = '1.0.0'
system = platform.system()


def main_module(args):
    arguments = Ap(prog_version=program_ver, argv=args, program_name=program_name)
    if arguments.return_arguments().download is not None and arguments.return_arguments().download is not False:
        print("Please enter your email for identification purpose. Necessary to download data from NCBI.")
        email = Cf.check_input()
        downloader = Dl(email=email, database='nuccore', type_of_return='text')
        start_time = datetime.datetime.now()
        downloader.start()
        end_time = datetime.datetime.now()
        print('Ended at: ', end_time)
        print('Total execution time: ', end_time - start_time)
        exit()
    else:
        pass


if __name__ == '__main__':
    intro = '\n############################################\n' \
            '# {p} {v}                          #\n' \
            '# Download genomic data from NCBI    #\n' \
            '############################################'.format(v=program_ver, p=program_name)
    system_info = '\n########################\n' \
                  '# Platform : {plat}   #\n' \
                  '########################\n'.format(plat=system)

    print(intro)
    print(system_info)
    main_module(sys.argv[1:])
