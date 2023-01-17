import argparse
import sys
from src.timecatcher import TimeCatcher


class TimeCatcherCli:

    time_catcher: TimeCatcher

    def __init__(self, file_name=None):
        self.time_catcher = TimeCatcher(file_name)

    def catch_time(self) -> None:
        self.time_catcher.catch_time()

    def direct_catch(self, message) -> None:
        self.time_catcher.direct_catch(message)

    def count_time(self) -> str:
        time_entries = self.time_catcher.count_time()
        if not time_entries or not time_entries[0]:
            return "No log"

        output = ""
        for entry in time_entries[0]:
            time = self.__time_format(entry[0])
            output += f"{time} - {entry[1]}\n"

        time_total = self.__time_format(time_entries[1])
        output += f"\nTotal: {time_total}"
        return output

    def get_log(self) -> str:
        entries = self.time_catcher.get_entries()
        if not entries:
            return "No log"

        return "\n".join(entries)

    def get_last_entry(self) -> str:
        time_entry = self.time_catcher.get_last_entry()
        if not time_entry:
            return "No log"

        time = self.__time_format(time_entry[0])
        return f"{time} - {time_entry[1]}"

    def __time_format(self, time: int) -> str:
        hour = time // 60
        minutes = time % 60
        return f"{hour:2}:{minutes:02d}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Catch time")
    parser.add_argument("-c", "--catch", help="Catch time", action="store_true")
    parser.add_argument("-m", "--message", help="Message to log")
    parser.add_argument("-t", "--total", help="Count total time", action="store_true")
    parser.add_argument("-p", "--print", help="Print last entry", action="store_true")
    parser.add_argument("-l", "--log", help="Print log", action="store_true")
    parser.add_argument("-f", "--file", help="File name")
    args = parser.parse_args()

    if not args.catch and not args.total and not args.log and not args.print:
        parser.print_help()
        sys.exit()

    if args.file and args.catch:
        print("Can't use file name with catch")
        sys.exit()

    if args.file:
        timeCatcher = TimeCatcherCli(args.file)
    else:
        timeCatcher = TimeCatcherCli()

    if args.catch:
        if args.message:
            timeCatcher.direct_catch(args.message)
        else:
            timeCatcher.catch_time()

    if args.print:
        print(timeCatcher.get_last_entry())

    if args.total:
        print(timeCatcher.count_time())

    if args.log:
        print(timeCatcher.get_log())
