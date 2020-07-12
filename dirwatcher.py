

import signal
import time
import logging
import argparse
import os


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
    This is a handler for SIGTERM and SIGINT. Other signals can be
    mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its
    loop if the signal is trapped.
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
    # argument to specify the "directory to watch" (may not yet exist!)
    parser.add_argument('-dir', default='/', action='store',
                        help='directory to watch')
    # argument that filters kind of "file extension" to search (.txt, .log)
    parser.add_argument(
        '-ext', action='store', help='filters file extension to search within')
    # argument that controls the "polling interval" (instead of hard-coding it)
    parser.add_argument('-int', default=1.0, action='store', type=float,
                        help='controls the polling interval')
    # argument that specifics the "magic_string" to search for
    parser.add_argument(
        'magic', action='store', help='specifies the magic str to search for')

    return parser


def watch_directory(dir):
    try:
        with os.scandir(dir) as d:
            if d:
                logger.info(f'found directory {dir}')
    except FileNotFoundError as e:
        logger.error(f'{e}')


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
    {'-' * 70}
    Starting {__file__}
    on:  {time.ctime(start_time)}
    {'-' * 70}
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
    {'-' * 70}
    Stopped {__file__}
    Uptime was {time.time() - start_time}
    {'-' * 70}
    """

    logger.info(stop_banner)

    # Include the overall uptime since program start


if __name__ == "__main__":
    main()
