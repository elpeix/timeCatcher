import datetime
import os

from src.line_validator import LineValidator


class TimeCatcher:

    def __init__(self, file_name: str = None):
        if file_name is None:
            now = datetime.datetime.now()
            str_date = now.strftime("%Y-%m-%d")
            self.file_name = f"timeLog_{str_date}.log"
        else:
            self.file_name = file_name

    def catch(self, message: str) -> None:
        if message is None or message == "":
            return
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"{self.__get_time()} {message}\n")

    def manual_catch(self, line:str) -> bool:
        if not self.__line_is_entry(line):
            return False
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"{line}\n")
        self.sanitize()
        return True

    def __file_exists(self) -> bool:
        return os.path.isfile(self.file_name)

    def __get_time(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%H:%M")

    def count_time(self) -> tuple:
        entries = self.get_entries()
        if len(entries) == 0:
            return ()

        entries.sort()
        time_counter = TimeCounter()
        for entry in entries:
            time_counter.add_entry(entry)

        time_counter.add_entry(f"{self.__get_time()} End")
        time_counter.count_time()
        return (time_counter.get_time_entries(), time_counter.get_total_time())

    def get_entries(self) -> list:
        if not self.__file_exists():
            return []

        result = []
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if self.__line_is_entry(line):
                    result.append(line[:-1])
        return result

    def get_last_entry(self) -> list:
        entries = self.get_entries()
        if len(entries) == 0:
            return []

        time_counter = TimeCounter()
        time_counter.add_entry(entries[-1])
        time_counter.add_entry(f"{self.__get_time()} End")
        time_counter.count_time()
        return time_counter.get_time_entries()[-1]

    def __line_is_entry(self, line: str) -> bool:
        line_validator = LineValidator(line)
        return line_validator.is_valid()

    def sanitize(self) -> None:
        entries = self.get_entries()
        if len(entries) == 0:
            return

        entries.sort()
        tmp_file_name = f"{self.file_name}.tmp"
        with open(tmp_file_name, "w", encoding="utf-8") as file:
            for entry in entries:
                file.write(f"{entry}\n")

        os.remove(self.file_name)
        os.rename(tmp_file_name, self.file_name)


class TimeCounter:

    def __init__(self):
        self.previous_entry = None
        self.entries = []
        self.time_entries = []
        self.total_time = 0

    def add_entry(self, entry: str) -> None:
        self.entries.append(entry)

    def count_time(self) -> None:
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
        return self.time_entries

    def get_total_time(self) -> int:
        return self.total_time

    def get_time(self, entry) -> int:
        time = entry.split(" ")[0]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        return hour * 60 + minute
