from dotenv import load_dotenv
load_dotenv(verbose=True)
# From here on, env var available as 
# os.getenv("VAR_NAME")
# For more options, see: https://pypi.org/project/python-dotenv

import doctor_subsystem
import user_subsystem
import getopt
import sys

def main():
    # great software goes here!
    try:
        options, _ = getopt.getopt(
            sys.argv[1:], 'uadp', ['user', 'patient', 'doctor', 'admin'])
    except getopt.GetoptError as e:
        print(e)
        sys.exit()

#    email_service.init_smtp()

    if options[0][0] == '-p' or options[0][0] == '--patient':
        user_subsystem.initialize()
    elif options[0][0] == '-d' or options[0][0] == '--doctor':
        doctor_subsystem.initialize()

if __name__ == "__main__":
    main()
