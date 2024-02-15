
# 문자열에 관한 이벤트를 관리함
class Event:
    def __init__(self):
        self.number = ""
        self.limit = 5

    def one(self):
        if(len(self.number)<self.limit):
            self.number += "1"

    def two(self):
        if(len(self.number)<self.limit):
            self.number += "2"

    def three(self):
        if(len(self.number)<self.limit):
            self.number += "3"

    def four(self):
        if(len(self.number)<self.limit):
            self.number += "4"

    def five(self):
        if(len(self.number)<self.limit):
            self.number += "5"

    def six(self):
        if(len(self.number)<self.limit):
            self.number += "6"

    def seven(self):
        if(len(self.number)<self.limit):
            self.number += "7"

    def eight(self):
        if(len(self.number)<self.limit):
            self.number += "8"

    def nine(self):
        if(len(self.number)<self.limit):
            self.number += "9"

    def delete(self):
        self.number = self.number[:-1]

    def zero(self):
        if(len(self.number)<self.limit):
            self.number += "0"

