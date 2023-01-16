"""Catch time"""

import argparse
import datetime

class TimeCatcher:
    """Catch time and write to file"""

    def __init__(self, file_name=None):
        if file_name is None:
            self.file_name = self.__get_file_name()
        else:
            self.file_name = file_name

    def direct_catch(self, message) -> None:
        """Catch time with message"""

        self.__write_to_file(message)

    def catch_time(self) -> None:
        """Catch time getting message from input"""

        message = input("Message: ")
        self.__write_to_file(message)

    def __write_to_file(self, message=None) -> None:
        if message is None or message == "":
            return
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"{self.__get_time()} {message}\n")

    def __get_file_name(self) -> str:
        return f"timeLog_{self.__get_date()}.log"

    def __get_date(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")

    def __get_time(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")

    def count_time(self) -> str:
        """Count time between entries"""

        time_counter = TimeCounter()
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                time_counter.add_entry(line[:-1])

        time_counter.add_entry(f"{self.__get_time()} End")
        return time_counter.count_time()

    def get_log(self) -> str:
        """Get log from file"""

        output = ""
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                output += line
        return output


class TimeCounter:
    """Count time between entries"""

    def __init__(self):
        self.previous_entry = None
        self.entries = []

    def add_entry(self, entry) -> None:
        """Add entry to counter"""

        self.entries.append(entry)

    def count_time(self) -> str:
        """Count time between entries"""

        if len(self.entries) == 0:
            return "No entries"

        output = ""
        total_time = 0
        for entry in self.entries:
            if self.previous_entry is None:
                self.previous_entry = entry
                continue
            time = self.get_time(entry) - self.get_time(self.previous_entry)
            if time == 0:
                continue
            hour = time // 60
            minutes = time % 60
            output += f"{hour:2}:{minutes:02d} - {self.previous_entry.split(' ')[1]}\n"
            total_time += time
            self.previous_entry = entry

        hour = total_time // 60
        minutes = total_time % 60
        output += f"\nTotal: {hour}:{minutes}"
        return output

    def get_time(self, entry) -> int:
        """Get time from entry"""

        time = entry.split(" ")[0]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        return hour * 60 + minute


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Catch time")
    parser.add_argument("-c", "--catch", help="Catch time", action="store_true")
    parser.add_argument("-m", "--message", help="Message to log")
    parser.add_argument("-t", "--total", help="Count total time", action="store_true")
    parser.add_argument("-l", "--log", help="Print log", action="store_true")
    parser.add_argument("-f", "--file", help="File name")
    args = parser.parse_args()

    if not args.catch and not args.total and not args.log:
        parser.print_help()
        exit()

    if args.file and args.catch:
        print("Can't use file name with catch")
        exit()

    if args.file:
        timeCatcher = TimeCatcher(args.file)
    else:
        timeCatcher = TimeCatcher()

    if args.catch:
        if args.message:
            timeCatcher.direct_catch(args.message)
        else:
            timeCatcher.catch_time()

    if args.total:
        print(timeCatcher.count_time())

    if args.log:
        print(timeCatcher.get_log())
