"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 32 # 32 8-bit addresses
        self.reg = [0] * 8 # 8 general-purpose registers

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

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            IR = self.ram_read(self.pc)
            if IR == 0b10000010: #LDI
                self.reg[operand_a] = operand_b
                op_size = 2
            elif IR == 0b01000111: #PRN
                print(self.reg[operand_a])
                op_size = 1
            elif IR == 0b10100010: #MUL
                self.reg[operand_a] *= self.reg[operand_b]
                op_size = 2
            elif IR == 0b00000001: #HLT
                running = self.HLT()

            self.pc += op_size + 1

    def HLT(self):
        return False


cpu1 = CPU()
cpu2 = CPU()

cpu1.load("./ls8/examples/print8.ls8")
cpu1.run()
cpu2.load("./ls8/examples/mult.ls8")
cpu2.run()

