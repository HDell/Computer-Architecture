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

    def run(self): #FETCH, DECODE, EXECUTE
        """Run the CPU."""
        running = True
        self.reg[self.sp] = 0xF4 #SP = 244
        while running:
            IR = self.ram_read(self.pc) #Instruction Register
            OP_A = self.ram_read(self.pc+1) #Operand 1
            OP_B = self.ram_read(self.pc+2) #Operand 2
            if IR == 0b10000010: #LDI
                self.reg[OP_A] = OP_B
                op_size = 2
            elif IR == 0b01000111: #PRN
                print(self.reg[OP_A])
                op_size = 1
            elif IR == 0b10100010: #MUL
                self.reg[OP_A] *= self.reg[OP_B]
                op_size = 2
            elif IR == 0b01000101: #PUSH
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[self.sp], self.reg[OP_A])
                op_size = 1
            elif IR == 0b01000110: #POP
                self.reg[OP_A] = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
                op_size = 1
            elif IR == 0b01010000: #CALL
                # push the return address on to the stack
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[self.sp], self.pc+2)
                # set the pc to the subroutines address
                self.pc = self.reg[OP_A]
                op_size = 0 
            elif IR == 0b00010001: #RET
                # POP return address from stack to store in pc
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
                op_size = 0 
            elif IR == 0b00000001: #HLT
                running = self.HLT()

            self.pc += op_size + 1

    def HLT(self):
        return False

    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return 3

    def PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return 2

    def MUL(self, operand_a, operand_b):
        self.reg[operand_a] *= self.reg[operand_b]
        return 3

    def PUSH(self, operand_a, operand_b):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[operand_a])
        return 2

    def POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        return 2

    def HALT(self, operand_a, operand_b):
        return False

        BT = {
        0b10000010: LDI,
        0b01000111: PRN,
        0b10100010: MUL,
        0b01000101: PUSH,
        0b01000110: POP,
        0b00000001: HALT
    }


cpu1 = CPU()
cpu2 = CPU()
cpu3 = CPU()
cpu4 = CPU()

cpu1.load("./ls8/examples/print8.ls8")
cpu1.run()
cpu2.load("./ls8/examples/mult.ls8")
cpu2.run()
cpu3.load("./ls8/examples/stack.ls8")
cpu3.run()
cpu4.load("./ls8/examples/call.ls8")
cpu4.run()

