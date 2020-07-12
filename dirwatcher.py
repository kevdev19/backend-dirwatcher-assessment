"""
DEV PLAN
1) Command line args to monitor given directory for text files created within monitored directory
    a) Create versatile command line argument parser that can handle these options:
       X An argument that controls the "polling interval" (instead of hard-coding it)
       X An argument that specifics the "magic_string" to search for
       X An argument that filters what kind of "file extension" to search within (i.e., .txt, .log)
       X An argument to specify the "directory to watch" (this directory may not yet exist!)

2) Continually search within all files in directory for "magic_string" as command line argument
    a) Implement using a timed polling loop (HINT: "if" statement):
        if "magic_string" in "file":
            -log msg indicating - file and line where magic_text found
    b) Once magic_string is logged, it should not be logged again unless it appears in subsequent entry later
    c) Files in monitored dir may be added, deleted, or appended at anytime by other processes
    Program should log a msg when new files appear OR other previously-watched files disappear
        -Anything previously written to a file will not change
        -Only new content will be added to the end of the file. You WON'T have to continually re-check sections fo a file
    -Program should terminate itself when catching SIGTERM and SIGINT signals (OS Signals)
        -OS will send signal event to process it wants to terminate from outside
        -Program will only act on those signals if it is listening for them
        -Be sure to log a termination msg
        -Handling OS signals and polling directory being watched will be two separate functions
        -You won't be getting an OS signal when files are created or deleted
3) Model contents of directory within your program using a dictionary(DICTIONARY MODEL):
    a) Keys: file names, values: last line number read during previous polling iteration
    b) Keep track of last line read
    c) When opening and reading file, skip over all the lines you've previously examined
    d) Synchronize DICTIONARY MODEL:
        1) for "every file" in "directory":
                add it to your "dictionary" if not already there
                exclude files without proper file extensions
                Report new files added to dictionary
        2) for "every entry" in "dictionary":
                find out if still exists in dictionary
                if not, remove it from dictionary
                then report as "deleted"
        3) Once dictionary is synchronized, iterate through all of its files to find "magic_string"
            starting from line number where you left off last ime



    -SUCCESS CRITERIA
     - Have a demonstrable OS signal handler
     - Log messages for files containing "magic_string"
     - Handle and log different exceptions - "file not found", "dir does not exist"
     - Handle and report top-level unknown exceptions so program stays alive
     - Include startup and shutdown banner in your logs:
        - Shutdown banner - total runtime(uptime)
        -
"""

import signal
import time
import logging
import argparse
import os
import sys


author = "Kevin Blount"

exit_flag = False
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """

    # log the associated signal name
    logger.warning('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True

# relative path
# root

# absolute path
# /Users/kevin/kenzie-assessments/Q3/sprint5A/backend-dirwatcher-assessment/root


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    # An argument to specify the "directory to watch" (this directory may not yet exist!)
    parser.add_argument('-dir', default='/', action='store',
                        help='directory to watch')
    # An argument that filters what kind of "file extension" to search within (i.e., .txt, .log)
    parser.add_argument(
        '-ext', action='store', help='filters file extension to search within')
    # An argument that controls the "polling interval" (instead of hard-coding it)
    parser.add_argument('-int', default=1.0, action='store', type=float,
                        help='controls the polling interval')
    # An argument that specifics the "magic_string" to search for
    parser.add_argument(
        'magic', action='store', help='specifies the magic str to search for')

    return parser


def watch_directory(dir):
    try:
        with os.scandir(dir) as d:
            pass
    except FileNotFoundError:
        logger.error(f'No directory found {dir}')


start_time = time.time()


def main():
    parser = create_parser()
    args = parser.parse_args()
    # You can access args using dot notation like so:
    print(f"Directory to watch: {args.dir}")
    print(f"File extension to search within is: {args.ext}")
    print(f"Polling interval given is: {args.int}")
    print(f"Magic string is: {args.magic}")

    start_banner = f"""
    -------------------------------------------------------------------
    Starting {__file__}
    on:  {time.ctime(start_time)}
    -------------------------------------------------------------------
    """
    logger.info(start_banner)

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        watch_directory(args.dir)

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(args.int)

    # final exit point happens here

    stop_banner = f"""
    -------------------------------------------------------------------
    Stopped {__file__}
    Uptime was {time.time() - start_time}
    -------------------------------------------------------------------
    """

    logger.info(stop_banner)

    # Include the overall uptime since program start


if __name__ == "__main__":
    main()
