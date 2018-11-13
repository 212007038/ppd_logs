# region Import region
import os
import sys
import subprocess
import argparse  # command line parser
import fnmatch

# endregion

###############################################################################
# region Variables region
###############################################################################
__version__ = '1.1'  # version of script

COMMAND_7Z = "C:\\Program Files\\7-Zip\\7z.exe"

# endregion

###############################################################################
# region Main region
def main(arg_list=None):
    ###############################################################################
    # Setup command line argument parsing...
    parser = argparse.ArgumentParser(description="Process an exported LeCroy CSV file (from spreadsheet view)")
    parser.add_argument('-d', dest='log_dir',
                        help='optional directory containing 7Z CARESCAPE ONE log files to inspect, defaults to '
                             'current directory', required=True)
    parser.add_argument('-p', dest='log_password', action='store_true', default="helix",
                        help='password for log file', required=False)
    parser.add_argument('-v', dest='verbose', default=False, action='store_true',
                        help='verbose output flag', required=False)
    parser.add_argument('--version', action='version', help='Print version.',
                        version='%(prog)s Version {version}'.format(version=__version__))

    # Parse the command line arguments
    args = parser.parse_args(arg_list)

    ###############################################################################
    # Did the user spec a log file directory?
    if args.log_dir is not None:
        # Test for existence of optional graphics directory.
        if os.path.isdir(args.log_dir) is False:
            print('ERROR, ' + args.log_dir + ' is not a directory')
            print('\n\n')
            parser.print_help()
            return -1
    else:
        args.log_dir = os.getcwd()  # use the current directory if none specified


    ###############################################################################
    # Collect a list of log files to inspect...
    log_files_dict = {}
    for file in os.listdir(args.log_dir):
        if fnmatch.fnmatch(file, '* logs.7z'):
            print(file)
            full_dir = os.path.splitext(file)[0].replace(" ", "_")  # get basename
            #full_dir = full_dir.replace(" ", "_")  # replace any spaces with underscore
            log_files_dict[file] = args.log_dir+"\\"+full_dir



    ###############################################################################
    # Create directories for each 7z...
    for log_file, log_dir in log_files_dict.items():
        try:
            os.mkdir(log_dir)
        except FileExistsError:
            print("Directory exists already")
        except:
            # Unexpected exception.
            print("Unexpected error with mkdir call:", sys.exc_info()[0])
            return 1

    ###############################################################################
    # Unzip to matching directory.
    for log_file, log_dir in log_files_dict.items():
        the_command = 'x "' + args.log_dir + '\\' + log_file + '"'
        print(the_command)
        l = [COMMAND_7Z, the_command, '-p' + args.log_password, '-o' + "'" + log_dir + "'"]
        print(l)
        try:
            command_output = subprocess.check_output(l)
        except subprocess.CalledProcessError as e:
            print('*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(e.output.decode('utf-8'))
            print('ERROR during command execution, return value from command: ' + str(e.returncode))
            print('*** ABORTING ***')
            print('*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            exit(e.returncode)
        except OSError as e:
            print('Error, executing command')
            print('Error string: ' + e.strerror + ', error number: ' + e.errno)
            print('*** ABORTING ***')
            exit(-1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print('*** ABORTING ***')
            exit(-2)

    print(log_files_dict)
    return 0

# endregion

###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
