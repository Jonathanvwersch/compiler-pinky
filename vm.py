import codecs
from interpreter import TYPE_NUMBER
from utils import stringify, vm_error


class VM:
    def __init__(self):
        self.stack = []
        self.pc = 0  # program counter
        self.sp = 0  # stack pointer

    def run(self, instructions):
        self.pc = 0
        self.sp - 0
        self.is_running = True

        while self.is_running:
            opcode, *args = instructions[self.pc]
            self.pc = self.pc + 1
            getattr(self, opcode)(*args)

    def HALT(self):
        self.is_running = False

    def PUSH(self, val):
        self.stack.append(val)
        self.sp += 1

    def POP(self):
        self.sp -= 1
        return self.stack.pop()

    def ADD(self):
        right_type, right_val = self.POP()
        left_type, left_val = self.POP()
        self.sp -= 2
        if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
            self.stack.append((TYPE_NUMBER, right_val + left_val))
        else:
            vm_error(f"Error on ADD between {left_type} and {right_type}", self.pc)

    def SUB(self):
        right_type, right_val = self.POP()
        left_type, left_val = self.POP()
        self.sp -= 2
        if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
            self.stack.append((TYPE_NUMBER, left_val - right_val))
        else:
            vm_error(f"Error on SUB between {left_type} and {right_type}", self.pc)

    def MUL(self):
        right_type, right_val = self.POP()
        left_type, left_val = self.POP()
        self.sp -= 2
        if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
            self.stack.append((TYPE_NUMBER, left_val * right_val))
        else:
            vm_error(f"Error on MUL between {left_type} and {right_type}", self.pc)

    def DIV(self):
        right_type, right_val = self.POP()
        left_type, left_val = self.POP()
        self.sp -= 2
        if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
            self.stack.append((TYPE_NUMBER, right_val / left_val))
        else:
            vm_error(f"Error on DIV between {left_type} and {right_type}", self.pc)

    def PRINTLN(self):
        _, val = self.POP()
        print(
            codecs.escape_decode(bytes(stringify(val), "utf-8"))[0].decode("utf-8"),
            end="\n",
        )

    def PRINT(self):
        _, val = self.POP()
        print(
            codecs.escape_decode(bytes(stringify(val), "utf-8"))[0].decode("utf-8"),
            end="",
        )

    def LABEL(self, name):
        pass
