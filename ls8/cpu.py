"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.sp = 7
        self.ram = [0] * 256 # 256 8-bit addresses
        self.reg = [0] * 8 # 8 general-purpose registers
        self.running = False
        self.BT = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b10100000: self.ADD,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b00000001: self.HALT
        }

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open (filename) as f:
            for instruction in f:
                comment_split = instruction.split("#")
                byte = comment_split[0].strip()
                if byte == '':
                    continue
                decimal = int(byte, 2)
                self.ram[address] = decimal
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def LDI(self, operand_a, operand_b, pc):
        self.reg[operand_a] = operand_b
        return pc + 3

    def PRN(self, operand_a, operand_b, pc):
        print(self.reg[operand_a])
        return pc + 2

    def MUL(self, operand_a, operand_b, pc):
        self.reg[operand_a] *= self.reg[operand_b]
        return pc + 3

    def ADD(self, operand_a, operand_b, pc):
        self.reg[operand_a] += self.reg[operand_b]
        return pc + 3

    def PUSH(self, operand_a, operand_b, pc):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[operand_a])
        return pc + 2

    def POP(self, operand_a, operand_b, pc):
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        return pc + 2
    
    def CALL(self, operand_a, operand_b, pc):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.pc+2)
        self.pc = self.reg[operand_a]
        return self.pc
    
    def RET(self, operand_a, operand_b, pc):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        return self.pc

    def HALT(self, operand_a, operand_b, pc):
        self.running = False
        return -1

    def run(self): #FETCH, DECODE, EXECUTE
        """Run the CPU."""
        self.running = True
        self.reg[self.sp] = 0xF4 #SP = 244
        while self.running:
            IR = self.ram_read(self.pc) #Instruction Register
            OP_A = self.ram_read(self.pc+1) #Operand 1
            OP_B = self.ram_read(self.pc+2) #Operand 2
            if IR in self.BT:
                self.pc = self.BT[IR](OP_A, OP_B, self.pc)
            else:
                print("Invalid")
                


cpu1 = CPU()
cpu2 = CPU()
cpu3 = CPU()
cpu4 = CPU()

print("Print8.ls8")
cpu1.load("./ls8/examples/print8.ls8")
cpu1.run()
print()
print("Mult.ls8")
cpu2.load("./ls8/examples/mult.ls8")
cpu2.run()
print()
print("Stack.ls8")
cpu3.load("./ls8/examples/stack.ls8")
cpu3.run()
print()
print("Call.ls8")
cpu4.load("./ls8/examples/call.ls8")
cpu4.run()

