"""Catch time"""

import datetime
import os


class TimeCatcher:
    """Catch time and write to file"""

    def __init__(self, file_name: str = None):
        if file_name is None:
            self.file_name = self.__get_file_name()
        else:
            self.file_name = file_name

    def direct_catch(self, message: str) -> None:
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

    def __file_exists(self) -> bool:
        return os.path.isfile(self.file_name)

    def __get_date(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")

    def __get_time(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")

    def count_time(self) -> str:
        """Count time between entries"""

        if not self.__file_exists():
            return ()

        time_counter = TimeCounter()
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                time_counter.add_entry(line[:-1])

        time_counter.add_entry(f"{self.__get_time()} End")
        time_counter.count_time()
        return (time_counter.get_time_entries(), time_counter.get_total_time())

    def get_entries(self) -> list:
        """Get entries from file"""

        if not self.__file_exists():
            return []

        result = []
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                result.append(line[:-1])
        return result

    def get_last_entry(self) -> list:
        """Get last entry from file"""

        if not self.__file_exists():
            return []

        time_counter = TimeCounter()

        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            time_counter.add_entry(lines[-1][:-1])

        time_counter.add_entry(f"{self.__get_time()} End")
        time_counter.count_time()
        return time_counter.get_time_entries()[-1]


class TimeCounter:
    """Count time between entries"""

    def __init__(self):
        self.previous_entry = None
        self.entries = []
        self.time_entries = []
        self.total_time = 0

    def add_entry(self, entry: str) -> None:
        """Add entry to counter"""

        self.entries.append(entry)

    def count_time(self) -> None:
        """Count time between entries"""

        if len(self.entries) == 0:
            return

        self.time_entries = []
        self.total_time = 0
        for entry in self.entries:
            if self.previous_entry is None:
                self.previous_entry = entry
                continue
            time = self.get_time(entry) - self.get_time(self.previous_entry)
            if time == 0:
                continue
            entry_message = " ".join(self.previous_entry.split(" ")[1:])
            self.time_entries.append((time, entry_message))
            self.total_time += time
            self.previous_entry = entry

    def get_time_entries(self) -> list:
        """Returns list of time entries"""
        return self.time_entries

    def get_total_time(self) -> int:
        """Returns total time in minutes"""
        return self.total_time

    def get_time(self, entry) -> int:
        """Get time from entry"""

        time = entry.split(" ")[0]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        return hour * 60 + minute
