#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import configparser


class TimeCatcher:

    def __init__(self, file_name: str = None):
        self.__init_config()
        if file_name is None:
            self.file_name = f"timeLog_{DateTimeGetter.get_date()}.log"
        else:
            self.file_name = file_name
        self.file_name = f"{self.log_path}/{self.file_name}"

    def __init_config(self) -> None:
        home_path = os.path.expanduser("~")
        config_path = f"{home_path}/.config/timeCatcher"
        config_file = f"{config_path}/config.ini"

        config = configparser.ConfigParser()
        config.read(config_file, encoding="utf-8")
        if 'App' in config and 'time_log_path' in config['App']:
            log_path = config['App']['time_log_path']
            log_path = self.__parse_log_path(log_path)
            if log_path:
                self.log_path = log_path
                return

        log_path = f"{home_path}/.timeCatcher"
        os.makedirs(log_path, exist_ok=True)

        os.makedirs(config_path, exist_ok=True)
        config['App'] = {'time_log_path': log_path}

        with open(config_file, 'w', encoding="utf-8") as configfile:
            config.write(configfile)

        self.log_path = log_path

    def __parse_log_path(self, log_path: str) -> str:
        home_path = os.path.expanduser("~")
        if log_path[-1] == "/":
            log_path = log_path[:-1]
        if log_path[0] == "~":
            log_path = f"{home_path}{log_path[1:]}"
        if os.path.isdir(log_path):
            return log_path
        return None

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


class LineValidator:

    def __init__(self, line):
        self.line = line

    def is_valid(self) -> bool:
        if not self.__is_valid_line():
            return False
        split_line = self.line.split(" ")
        if len(split_line) < 2 or not self.__has_valid_time(split_line[0]):
            return False
        message = " ".join(split_line[1:]).strip()
        return len(message) > 0

    def __is_valid_line(self) -> bool:
        if not self.line or not isinstance(self.line, str):
            return False
        return True

    def __has_valid_time(self, time_entry:str) -> bool:
        if not time_entry or not isinstance(time_entry, str):
            return False
        if len(time_entry) != 5 or not time_entry.replace(":", "").isdigit():
            return False
        hour, minute = time_entry.split(":")
        if int(hour) < 0 or int(hour) > 23:
            return False
        if int(minute) < 0 or int(minute) > 59:
            return False
        return True
