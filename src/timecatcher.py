import datetime
import os

from src.line_validator import LineValidator


class TimeCatcher:

    def __init__(self, file_name: str = None):
        if file_name is None:
            self.file_name = f"timeLog_{DateTimeGetter.get_date()}.log"
        else:
            self.file_name = file_name

    def catch(self, message: str) -> None:
        if message is None or message == "":
            return
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"{DateTimeGetter.get_time()} {message}\n")

    def manual_catch(self, line:str) -> bool:
        if not self.__line_is_entry(line):
            return False
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"{line}\n")
        self.sanitize()
        return True

    def __file_exists(self) -> bool:
        return os.path.isfile(self.file_name)

    def count_time(self) -> tuple:
        entries = self.get_entries()
        if len(entries) == 0:
            return ()

        time_counter = TimeCounter()
        for entry in entries:
            time_counter.add_entry(entry)

        time_counter.count_time()
        return (
            time_counter.get_time_entries(),
            time_counter.get_total_time()
        )

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

    def get_last_entry(self) -> tuple:
        entries = self.get_entries()
        if len(entries) == 0:
            return ()

        time_counter = TimeCounter()
        time_counter.add_entry(entries[-1])
        time_counter.count_time()
        time_entries = time_counter.get_time_entries()
        if len(time_entries) == 0:
            return ()
        return time_entries[-1]

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
        self.entries = []
        self.time_entries = []
        self.total_time = 0

    def add_entry(self, entry: str) -> None:
        self.entries.append(entry)

    def count_time(self) -> None:
        if len(self.entries) == 0:
            return

        entries_copy = self.entries.copy()
        entries_copy.sort()

        if self.__is_valuable_entry(entries_copy[-1]):
            entries_copy.append(f"{DateTimeGetter.get_time()} *End")

        self.time_entries = []
        self.total_time = 0
        previous_entry = None
        for entry in entries_copy:
            if previous_entry is None:
                if self.__is_valuable_entry(entry):
                    previous_entry = entry
                continue
            
            time = self.get_time(entry) - self.get_time(previous_entry)
            if time == 0:
                continue
            message = self.__get_message(previous_entry)
            self.time_entries.append((
                time, 
                self.__get_message(previous_entry)
            ))
            self.total_time += time
            previous_entry = entry if self.__is_valuable_entry(entry) else None

    def get_time_entries(self) -> list:
        return self.time_entries

    def get_total_time(self) -> int:
        return self.total_time

    def get_time(self, entry) -> int:
        time = entry.split(" ")[0]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        return hour * 60 + minute

    def __get_message(self, entry: str) -> str:
        return " ".join(entry.split(" ")[1:])
    
    def __is_valuable_entry(self, entry: str) -> bool:
        return self.__get_message(entry)[0] != "*"


class DateTimeGetter:

    @staticmethod
    def get_date() -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")

    @staticmethod
    def get_time() -> str:
        now = datetime.datetime.now()
        return now.strftime("%H:%M")
