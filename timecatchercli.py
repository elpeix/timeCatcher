import argparse
import sys
from src.timecatcher import TimeCatcher


class TimeCatcherCli:

    time_catcher: TimeCatcher

    def __init__(self, file_name=None):
        self.time_catcher = TimeCatcher(file_name)

    def catch(self, message:str = None) -> None:
        if not message:
            message = input("Message: ")
        self.time_catcher.catch(message)

    def manual_catch(self, line:str = None) -> bool:
        if not line:
            line = input("Line (HH:MM message): ")
        return self.time_catcher.manual_catch(line)

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

    def sanitize(self) -> None:
        self.time_catcher.sanitize()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Catch time")
    parser.add_argument("-c", "--catch", help="Catch time", action="store_true")
    parser.add_argument("-a", "--add", help="Add manual line to log", action="store_true")
    parser.add_argument("-m", "--message", help="Message to log")
    parser.add_argument("-t", "--total", help="Count total time", action="store_true")
    parser.add_argument("-p", "--print", help="Print last entry", action="store_true")
    parser.add_argument("-l", "--log", help="Print log", action="store_true")
    parser.add_argument("-f", "--file", help="File name")
    parser.add_argument("-s", "--sanitize", help="Sanitize log", action="store_true")
    args = parser.parse_args()

    items = ['catch', 'add', 'total', 'print', 'log', 'file', 'sanitize']
    if not any(getattr(args, item) for item in items):
        parser.print_help()
        sys.exit()

    if args.file and args.catch:
        print("Can't use file name with catch")
        sys.exit()

    if args.file:
        time_catcher = TimeCatcherCli(args.file)
    else:
        time_catcher = TimeCatcherCli()

    if args.catch:
        time_catcher.catch(args.message)

    if args.add:
        time_catcher.manual_catch(args.message)

    if args.sanitize:
        time_catcher.sanitize()
        print("Sanitized")

    if args.print:
        print(time_catcher.get_last_entry())

    if args.total:
        print(time_catcher.count_time())

    if args.log:
        print(time_catcher.get_log())
