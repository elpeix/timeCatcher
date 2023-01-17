class LineValidator:

    def __init__(self, line):
        self.line = line

    def is_valid(self) -> bool:
        if not self.__is_valid_line():
            return False

        split_line = self.line.split(" ")
        if len(split_line) < 2:
            return False

        if not self.__has_valid_time(split_line[0]):
            return False
        
        message = " ".join(split_line[1:]).strip()
        if not message:
            return False
        
        return True

    def __is_valid_line(self) -> bool:
        if not self.line:
            return False
        
        if not isinstance(self.line, str):
            return False
        
        return True

    def __has_valid_time(self, time_entry:str) -> bool:
        if not time_entry:
            return False
        
        if not isinstance(time_entry, str):
            return False
        
        if len(time_entry) != 5:
            return False
        
        if not time_entry.replace(":", "").isdigit():
            return False
        
        hour, minute = time_entry.split(":")
        if int(hour) < 0 or int(hour) > 23:
            return False
        
        if int(minute) < 0 or int(minute) > 59:
            return False
        
        return True