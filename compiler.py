import math
import re
from datetime import datetime
import sys
import time

class DirectExecVM():
    def __init__(self,parent=['unknown'],verbose=False):
        self.db = [0,0,0,0,0,0,0]
        self.tmp = [0]*100
        self.pointer = 0
        self.prog = []
        self.lg = [0,0] # in non-vm, lg has 4 items which 2 and 3 are reversed for system use
        self.reserved = [0]*16
        self.lgstate = 0
        if verbose: print(f"{self.get_formatted_time()} L [from {str(parent)}] -> __init__: Loaded successfully.")
    def increase_pointer(self,verbose=False,parent=['unknown']):
        if verbose: print(f"{self.get_formatted_time()} L [from {str(parent)}] -> increase_pointer: Set self.pointer to {self.pointer+1}")
        self.pointer += 1
    def get_formatted_time(parent=['unknown']):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    def remove_comments(self,code,verbose=False,parent=['unknown']):
        if verbose: print(f"{self.get_formatted_time()} L [from {str(parent)}] -> remove_comments: Removing comments.")
        return re.sub(r'/\*.*?\*/','',code,flags=re.DOTALL)
    def preprocess(self,code,verbose=False,parent=['unknown']):
        if verbose: print(f"{self.get_formatted_time()} L [from {str(parent)}] -> preprocess: Preparing...")
        clean = self.remove_comments(code,verbose,parent=parent)
        clean = clean.replace('\x20','')
        return clean
    def loadprog(self,bytecode,verbose=False,parent=['unknown']):
        # self.prog = bytecode.split()
        self.prog = list(str(bytecode))
        if verbose: print(f"{self.get_formatted_time()} L [from {str(parent)}] -> loadprog: Loaded program to self.prog")
    def execute(self,verbose=False,parent=['unknown']):
        increase_pointer = self.increase_pointer
        if verbose: print(f"{self.get_formatted_time()} L [from {str(parent)}] -> execute:","Set pointer to 0")
        self.pointer = 0
        self.state = 0
        increase_pointer = self.increase_pointer
        while True:
            # time.sleep(0.01)
            # input("")
            self.lgstate -= 1
            if self.pointer >= len(self.prog):
                if verbose: print(f"\033[93m{self.get_formatted_time()} W [from {str(parent)}] -> execute: Reached end of program without exit opcode, exiting\033[0m")
                break
            if verbose:
                # i want to use gray color for this "verbose" type log
                if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: pointer={hex(self.pointer)} state={hex(self.state)} opcode={hex(ord(self.prog[self.pointer]))}\033[0m")
            if self.state == 0:
                if self.prog[self.pointer] == '\x20': # separator (;)
                    self.state = 0
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '1': # init
                    self.state = 0
                    if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: reset db\033[0m")
                    self.db = [0,0,0,0,0,0,0]
                    if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: reset tmp\033[0m")
                    self.tmp = [0]*100
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '2': # clmem
                    if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: reset db\033[0m")
                    self.db = [0,0,0,0,0,0,0]
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '3': # mov
                    self.state = 1
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '4': # section/lbl
                    for i in range(3): increase_pointer()
                    continue
                elif self.prog[self.pointer] == '5': # inc/add
                    self.state = 3
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '6': # turbo mode which doesn't support in py
                    if self.pointer+3 < len(self.prog):
                        if verbose: print(f"{self.get_formatted_time()} W [from {str(parent)}] -> execute: 0x36 (turbo) supports TurboWarp's DirectRunVM only, ignoring.")
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '8': # cltmp - clear temp registers
                    self.tmp = [0]*100
                    if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: reset tmp\033[0m")
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '9': # lgc - clear logic registers
                    self.lg = [0,0]
                    if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: reset lg\033[0m")
                    increase_pointer()
                    continue     
                elif self.prog[self.pointer] == 'm': # memory store (m)
                    self.state = 7
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == 'S': # exit
                    if verbose: print(f"\033[92m{self.get_formatted_time()} L [from {str(parent)}] -> execute: safe exit\033[0m")
                    break
                elif self.prog[self.pointer] == 'c': # start of variable operation(s)
                    self.state = 5
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '7': # goto
                    self.state = 8
                    self.pointer += 1
                    continue
                elif self.prog[self.pointer] == 'q': # \x71, i guess q is right
                    self.state = 4
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == 'n':  # copy temp to variable
                    self.state = 9
                    self.pointer += 1
                    continue
                elif self.prog[self.pointer] == 'f': # lg
                    self.state = 10
                    self.pointer += 1
                    continue
                elif self.prog[self.pointer] == 'g':
                    try: self.lg[0] = float(self.lg[0])
                    except: pass
                    try: self.lg[1] = float(self.lg[1])
                    except: pass
                    try: self.lg[0] = str(self.lg[0])
                    except: pass
                    try: self.lg[1] = str(self.lg[1])
                    except: pass
                    lgpass = (self.lg[0] == self.lg[1])
                    print(f'\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: lg equ "{self.lg[0]}" "{self.lg[1]}" is {lgpass}')
                    if lgpass:
                        self.state = 8
                        increase_pointer()
                    else:
                        self.lgstate = 1
                    continue
                elif self.prog[self.pointer] == '+':
                    # its short, no state needed
                    self.tmp[2] = self.tmp[0]+self.tmp[1]
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == '-':
                    self.tmp[2] = self.tmp[0]-self.tmp[1]
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == "*":
                    self.tmp[2] = self.tmp[0]*self.tmp[1]
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == "/":
                    self.tmp[2] = self.tmp[0]/self.tmp[1]
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == "^":
                    self.tmp[2] = self.tmp[0]**self.tmp[1]
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == 'C': # C: tempXRoot (custom root)
                    self.tmp[2] = self.tmp[0]**(1/self.tmp[1])
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == 'A': # sqrt
                    self.tmp[2] = math.sqrt(self.tmp[0])
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == 'B': # cbrt
                    self.tmp[2] = math.cbrt(self.tmp[0])
                    increase_pointer()
                    continue
                elif self.prog[self.pointer] == 'D': # log
                    self.tmp[2] = math.log(self.tmp[0])
                elif self.prog[self.pointer] == 'h': # lgelse
                    if self.lgstate >= 0:
                        self.state = 8 # just call goto. i hope this works.

                elif verbose:
                    print(f"\033[93m{self.get_formatted_time()} W [from {str(parent)}] -> execute: Unknown opcode {hex(ord(self.prog[self.pointer]))} at {hex(self.pointer)}\033[0m")
                    increase_pointer()
                    continue
            elif self.state == 1:
                if self.prog[self.pointer] != 'c': sys.exit(2)
                self.state = 2
                increase_pointer()
                continue
            elif self.state == 2:
                # WE DETECTED 3, WENT TO STATE 1, SAW 'c', NOW WE'RE IN STATE 2!
                # MUST BE c1-c7! IF NOT, GO HOME AND EAT ERRORS!!!!!!!
                if not self.prog[self.pointer].isdigit():
                    sys.exit(3)  # GO HOME AND EAT ERRORS!
                
                var_index = int(self.prog[self.pointer]) - 1
                self.pointer += 1
                
                # MUST BE 1-7! IF NOT, GO HOME AND EAT ERRORS!!!!!!!
                if var_index < 0 or var_index >= len(self.db):
                    sys.exit(3)  # GO HOME AND EAT ERRORS!
                
                # NOW a OR d MUST BE NEXT! IF NOT, GO HOME AND EAT ERRORS!!!!!!!
                if self.pointer >= len(self.prog):
                    sys.exit(3)  # GO HOME AND EAT ERRORS!
                
                if self.prog[self.pointer] == 'a':
                    # -> I SAW "a" - STRING ASSIGNMENT
                    self.pointer += 1
                    string_buffer = []
                    
                    # LET'S FIND b, BEFORE REACHING FILE END! 
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'b':
                        if self.prog[self.pointer] == '\\':
                            self.pointer += 1
                            if self.pointer < len(self.prog):
                                # handle escape sequences
                                escape_chars = {'a': 'a', 'b': 'b', 'd': 'd', 'e': 'e', '\\': '\\'}
                                char = self.prog[self.pointer]
                                string_buffer.append(escape_chars.get(char, char))
                                self.pointer += 1
                        else:
                            string_buffer.append(self.prog[self.pointer])
                            self.pointer += 1
                    
                    # IF WE REACH FILE END, THROW ERROR ON HIS FACE
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'b':
                        sys.exit(4)  # THROW ERROR ON HIS FACE
                    
                    self.pointer += 1  # Skip 'b'
                    
                    # FOUND b! ASSIGN TO REGISTER cX
                    try:
                        num_str = ''.join(string_buffer)
                        # normalize to float and remove negative-zero sign
                        self.db[var_index] = float(num_str)
                        if isinstance(self.db[var_index], float) and self.db[var_index] == 0.0:
                            self.db[var_index] = 0.0
                        if verbose:
                            print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: mov c{var_index + 1} = {self.db[var_index]} (string)\033[0m")
                    except ValueError:
                        sys.exit(9)
                    
                    self.state = 0
                    continue
                    
                elif self.prog[self.pointer] == 'd':
                    # -> I SAW "d" - NUMBER ASSIGNMENT  
                    increase_pointer()
                    num_buffer = ''
                    
                    # LET'S FIND e, BEFORE REACHING FILE END!
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                        num_buffer += self.prog[self.pointer]
                        self.pointer += 1
                    
                    # AND IF WE DO REACH THE END, GO TO HOME AND EAT ERRORS
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                        sys.exit(8)  # GO HOME AND EAT ERRORS
                    
                    increase_pointer()  # Skip 'e'
                    
                    # FOUND e! ASSIGN TO REGISTER cX
                    try:
                        self.db[var_index] = float(num_buffer)
                        if isinstance(self.db[var_index], float) and self.db[var_index] == 0.0:
                            self.db[var_index] = 0.0
                        if verbose:
                            print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: mov c{var_index + 1} = {self.db[var_index]} (number)\033[0m")
                    except ValueError:
                        sys.exit(9)
                    
                    self.state = 0
                    continue
                    
                else:
                    # -> I SAW OTHER THINGS
                    sys.exit(3)  # GO HOME AND EAT ERROR LA!!!!         
            elif self.state == 3:
                # format: 5{!c}{!p}{!d}{float}{!e}
                # expect variable c1,c2,etc.
                if self.prog[self.pointer] != 'c':
                    sys.exit(5)
                increase_pointer()
                # get variable index
                if self.pointer >= len(self.prog) or not self.prog[self.pointer].isdigit():
                    sys.exit(6)
                self.reserved[0] = int(self.prog[self.pointer])-1
                increase_pointer()
                # skip separator
                if self.pointer < len(self.prog):
                    increase_pointer() # skip separator
                # expect 'd' for float literal
                if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'd':
                    sys.exit(7)
                increase_pointer()
                # parse float between d and e
                self.reserved[1] = ''
                while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                    self.reserved[1] += self.prog[self.pointer]
                    increase_pointer()
                if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                    sys.exit(8)
                increase_pointer()
                try:
                    self.reserved[2] = float(self.reserved[1])
                    newv = float(self.db[self.reserved[0]]) + self.reserved[2]
                    # normalize negative zero
                    if isinstance(newv, float) and newv == 0.0:
                        newv = 0.0
                    self.db[self.reserved[0]] = newv
                except ValueError:
                    sys.exit(9)
                self.state = 0
                continue
            elif self.state == 4:  # q - output
                if verbose:
                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: Processing output instruction\033[0m")
                
                # Check what type of output we have
                if self.pointer >= len(self.prog):
                    if verbose:
                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Unexpected end of program in output\033[0m")
                    self.state = 0
                    continue
                
                if self.prog[self.pointer] == 'a':
                    # STRING OUTPUT: qa...b
                    self.pointer += 1
                    string_buffer = []
                    
                    # Parse string between 'a' and 'b'
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'b':
                        if self.prog[self.pointer] == '\\':
                            # Handle escape sequences
                            self.pointer += 1
                            if self.pointer < len(self.prog):
                                escape_chars = {
                                    'a': 'a', 
                                    'b': 'b', 
                                    'd': 'd', 
                                    'e': 'e', 
                                    '\\': '\\',
                                    'n': '\n',
                                    't': '\t',
                                    'r': '\r'
                                }
                                char = self.prog[self.pointer]
                                string_buffer.append(escape_chars.get(char, char))
                                self.pointer += 1
                            else:
                                # Backslash at end of program
                                string_buffer.append('\\')
                        else:
                            string_buffer.append(self.prog[self.pointer])
                            self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'b':
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Unterminated string in output\033[0m")
                        self.state = 0
                        continue
                    
                    self.pointer += 1  # Skip 'b'
                    output_str = ''.join(string_buffer)
                    print(output_str, end='')  # Use end='' to handle \n properly
                    if verbose:
                        print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: Output string: \"{output_str}\"\033[0m")
                
                elif self.prog[self.pointer] == 'd':
                    # FLOAT OUTPUT: qd...e
                    self.pointer += 1
                    num_buffer = ''
                    
                    # Parse number between 'd' and 'e'
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                        num_buffer += self.prog[self.pointer]
                        self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Unterminated float in output\033[0m")
                        self.state = 0
                        continue
                    
                    self.pointer += 1  # Skip 'e'
                    
                    try:
                        float_value = float(num_buffer)
                        print(float_value)
                        if verbose:
                            print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: Output float: {float_value}\033[0m")
                    except ValueError:
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid float format: {num_buffer}\033[0m")
                
                elif self.prog[self.pointer] == 'c':
                    # VARIABLE OUTPUT: qc{1-7}
                    self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or not self.prog[self.pointer].isdigit():
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Expected variable number after 'c' in output\033[0m")
                        self.state = 0
                        continue
                    
                    var_index = int(self.prog[self.pointer]) - 1
                    self.pointer += 1
                    
                    if 0 <= var_index < len(self.db):
                        value = self.db[var_index]
                        print(value)
                        if verbose:
                            print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: Output c{var_index + 1} = {value}\033[0m")
                    else:
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid variable index c{var_index + 1}\033[0m")
                
                else:
                    if verbose:
                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid output type '{self.prog[self.pointer]}' (expected 'a', 'd', or 'c')\033[0m")
                    # Skip to next valid instruction
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != '\x20':
                        self.pointer += 1
                
                self.state = 0
                continue
            elif self.state == 5:
                if self.prog[self.pointer].isdigit():
                    self.reserved[0] = int(self.prog[self.pointer]) - 1
                    increase_pointer()
                    if self.pointer < len(self.prog) and self.prog[self.pointer] == '?':
                        self.reserved[1] = float(input(f"Value for c{self.reserved[0]+1} \033[90m(Default: {self.db[self.reserved[0]]})\033[0m: "))
                        self.db[self.reserved[0]] = self.reserved[1]
                        if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: assign input \"\033[1;90m{self.reserved[1]}\033[0;90m\" to register db {hex(self.reserved[0])}")
                        increase_pointer()
                    else:
                        # its part of another operation, variable index alreay in reserved[0]
                        # dont reset state yet- let next opcoe hanle it.
                        pass
                    self.state = 0
                    continue
                else:
                    sys.exit(11)
            elif self.state == 6:
                if verbose: print(f"\033[92m{self.get_formatted_time()} W [from {str(parent)}] -> execute: deprecated state 6\033[0m")
                # and what do we do now? should we increase pointer and continue? idk
                self.state = 0
                increase_pointer()
                continue
            elif self.state == 7:
                if verbose: print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: process memory operation\033[0m")
                
                if self.prog[self.pointer] == 'c':
                    # mc... patterns - VARIABLE OPERATIONS
                    self.pointer += 1
                    if self.pointer < len(self.prog) and self.prog[self.pointer].isdigit():
                        var_index = int(self.prog[self.pointer])-1 # var index
                        # the bug: t0+t1 -> t2 in binary, i guess it become [:-1] and [0] to [1]
                        self.pointer += 1
                        if self.pointer < len(self.prog) and self.prog[self.pointer] == 'p':
                            # m - copy var to tmp register
                            self.pointer += 1
                            if self.pointer+1 < len(self.prog) and self.prog[self.pointer].isdigit() and self.prog[self.pointer+1].isdigit():
                                # get tmp reg id
                                tmp_index = int(self.prog[self.pointer]+self.prog[self.pointer+1])
                                self.pointer += 2
                                # tmp_index in bytecode is 1-based and must not be 00
                                if tmp_index == 0:
                                    if verbose:
                                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid tmp id 00 in mcp c{var_index+1}\033[0m")
                                    sys.exit(12)
                                # Convert 1-based tmp index from bytecode to 0-based internal index
                                tmp_index = tmp_index - 1
                                if 0 <= var_index < len(self.db) and 0 <= tmp_index < len(self.tmp):
                                    if verbose:
                                        print(f"{self.get_formatted_time()} D [from {str(parent)}] -> mcp PRE tmp[0:8]={self.tmp[0:8]} db[0:8]={self.db[0:8]}")
                                    # normalize value copied from db to tmp (remove negative zero)
                                    v = float(self.db[var_index])
                                    if v == 0.0:
                                        v = 0.0
                                    self.tmp[tmp_index] = v
                                    if verbose:
                                        print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: mcp c{var_index+1} -> t{tmp_index} = {v}\033[0m")
                                        print(f"{self.get_formatted_time()} D [from {str(parent)}] -> mcp POST tmp[0:8]={self.tmp[0:8]} db[0:8]={self.db[0:8]}")
                                else:
                                    if verbose:
                                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: invalid reg indices c{var_index+1} or tmp[{tmp_index}]\033[0m")
                                    sys.exit(12)
                            self.state = 0
                            continue
                        elif self.pointer < len(self.prog) and self.prog[self.pointer] == 'a':
                            # m - copy autotype (str/float) to var
                            self.pointer += 1
                            string_buffer = []
                            # parse string between a and b
                            while self.pointer < len(self.prog) and self.prog[self.pointer] != 'b':
                                if self.prog[self.pointer] == '\\':
                                    self.pointer += 1
                                    if self.pointer < len(self.prog):
                                        escape_chars = {'a': 'a', 'b': 'b', 'd': 'd', 'e': 'e', '\\': '\\'}
                                        char = self.prog[self.pointer]
                                        string_buffer.append(escape_chars.get(char, char))
                                        self.pointer += 1
                                else:
                                    string_buffer.append(self.prog[self.pointer])
                                    self.pointer += 1
                            if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'b':
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: unterminated string literal in mca\033[0m")
                                sys.exit(4)
                            self.pointer += 1
                            try:
                                num_str = ''.join(string_buffer)
                                v = float(num_str)
                                if v == 0.0:
                                    v = 0.0
                                self.db[var_index] = v
                                if verbose:
                                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: mca c{var_index + 1} = {self.db[var_index]}\033[0m")
                            except ValueError:
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid number format: {''.join(string_buffer)}\033[0m")
                            self.state = 0
                            continue
                        elif self.pointer < len(self.prog) and self.prog[self.pointer] == 'd':
                            # n (cp tmpX varX) - copy float literal to variable
                            self.pointer += 1
                            num_buffer = ''  # Number buffer
                            
                            # Parse number between 'd' and 'e'
                            while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                                num_buffer += self.prog[self.pointer]
                                self.pointer += 1
                            
                            if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Unterminated number in mcd operation\033[0m")
                                sys.exit(8)
                            
                            self.pointer += 1  # Skip 'e'
                            
                            # Convert to float and store
                            try:
                                v = float(num_buffer)
                                if v == 0.0:
                                    v = 0.0
                                self.db[var_index] = v
                                if verbose:
                                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: mcd c{var_index + 1} = {self.db[var_index]}\033[0m")
                            except ValueError:
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid number: {num_buffer}\033[0m")
                            
                            self.state = 0
                            continue
                            
                        else:
                            if verbose:
                                print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Unknown memory operation after c{var_index + 1}\033[0m")
                            sys.exit(3)
                    else:
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Expected variable number after 'c'\033[0m")
                        sys.exit(3)
                    
                elif self.prog[self.pointer] == 'd':
                    # md... patterns - DIRECT FLOAT LITERAL TO TEMP REGISTER
                    self.pointer += 1
                    
                    # Parse float between 'd' and 'e'
                    num_buffer = ''
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                        num_buffer += self.prog[self.pointer]
                        self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Unterminated float literal in md operation\033[0m")
                        sys.exit(8)
                    
                    self.pointer += 1  # Skip 'e'
                    
                    # Now expect 'p' and destination
                    if self.pointer < len(self.prog) and self.prog[self.pointer] == 'p':
                        self.pointer += 1
                        if self.pointer + 1 < len(self.prog) and self.prog[self.pointer].isdigit() and self.prog[self.pointer + 1].isdigit():
                            dest_index = int(self.prog[self.pointer] + self.prog[self.pointer + 1])
                            self.pointer += 2
                            # dest_index must not be 00
                            if dest_index == 0:
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid tmp id 00 in md operation\033[0m")
                                sys.exit(12)
                            # convert 1-based dest index to 0-based
                            dest_index = dest_index - 1
                            try:
                                value = float(num_buffer)
                                # normalize negative zero
                                if value == 0.0:
                                    value = 0.0
                                if 0 <= dest_index < len(self.tmp):
                                    if verbose:
                                        print(f"{self.get_formatted_time()} D [from {str(parent)}] -> md PRE tmp[0:8]={self.tmp[0:8]} db[0:8]={self.db[0:8]}")
                                    self.tmp[dest_index] = value
                                    if verbose:
                                        print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: md{num_buffer}ep{dest_index+1:02d} -> tmp[{dest_index}] = {value}\033[0m")
                                        print(f"{self.get_formatted_time()} D [from {str(parent)}] -> md POST tmp[0:8]={self.tmp[0:8]} db[0:8]={self.db[0:8]}")
                                else:
                                    if verbose:
                                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid tmp index {dest_index+1}\033[0m")
                            except ValueError:
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid float: {num_buffer}\033[0m")
                    
                    self.state = 0
                    continue
                    
                else:
                    if verbose:
                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Expected 'c' or 'd' for memory operation\033[0m")
                    sys.exit(3)
            elif self.state == 8:  # goto (g)
                if verbose: 
                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: find and goto point\033[0m")
                
                # Format: g{label_id}
                if self.pointer + 1 < len(self.prog) and self.prog[self.pointer].isdigit() and self.prog[self.pointer + 1].isdigit():
                    # Get 2-digit label ID (01-99)
                    label_id = int(self.prog[self.pointer] + self.prog[self.pointer + 1])
                    self.pointer += 2
                    
                    if verbose:
                        print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: goto label {label_id:02d}\033[0m")
                    
                    # Search for the label in the program - LABELS ARE 4{xx} FORMAT!
                    label_found = False
                    search_pointer = 0
                    
                    while search_pointer < len(self.prog):
                        # Look for label format: 4{label_id}
                        if (search_pointer + 2 < len(self.prog) and 
                            self.prog[search_pointer] == '4' and
                            self.prog[search_pointer + 1].isdigit() and 
                            self.prog[search_pointer + 2].isdigit() and
                            int(self.prog[search_pointer + 1] + self.prog[search_pointer + 2]) == label_id):
                            
                            # Found the label! Jump to this position
                            self.pointer = search_pointer
                            label_found = True
                            if verbose:
                                print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: jumped to label {label_id:02d} at position {hex(search_pointer)}\033[0m")
                            break
                        
                        search_pointer += 1
                    
                    if not label_found:
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Label {label_id:02d} not found!\033[0m")
                        sys.exit(14)
                
                else:
                    if verbose:
                        print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid goto format\033[0m")
                    sys.exit(3)
                
                self.state = 0
                continue
            elif self.state == 9:  # n - copy temp to variable
                if verbose: 
                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: copy temp to variable\033[0m")
                
                # Format: n{tmp_id}p{c{var_id}}
                if self.pointer + 1 < len(self.prog) and self.prog[self.pointer].isdigit() and self.prog[self.pointer + 1].isdigit():

                    tmp_index = int(self.prog[self.pointer] + self.prog[self.pointer + 1])
                    self.pointer += 2
                    # tmp_index must not be 00
                    if tmp_index == 0:
                        if verbose:
                            print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid tmp id 00 in n operation\033[0m")
                        sys.exit(12)
                    # convert 1-based tmp index to 0-based
                    tmp_index = tmp_index - 1

                    if self.pointer < len(self.prog) and self.prog[self.pointer] == 'p':
                        self.pointer += 1
                        if self.pointer + 1 < len(self.prog) and self.prog[self.pointer] == 'c' and self.prog[self.pointer + 1].isdigit():
                            var_index = int(self.prog[self.pointer + 1]) - 1
                            self.pointer += 2

                            if 0 <= tmp_index < len(self.tmp) and 0 <= var_index < len(self.db):
                                if verbose:
                                    print(f"{self.get_formatted_time()} D [from {str(parent)}] -> n PRE tmp[0:8]={self.tmp[0:8]} db[0:8]={self.db[0:8]}")
                                v = float(self.tmp[tmp_index])
                                if v == 0.0:
                                    v = 0.0
                                self.db[var_index] = v
                                if verbose:
                                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: n{tmp_index+1:02d}pc{var_index + 1} -> c{var_index + 1} = {self.tmp[tmp_index]}\033[0m")
                                    print(f"{self.get_formatted_time()} D [from {str(parent)}] -> n POST tmp[0:8]={self.tmp[0:8]} db[0:8]={self.db[0:8]}")
                            else:
                                if verbose:
                                    print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: Invalid register indices\033[0m")
                self.state = 0
                continue
            elif self.state == 10:
                #        #    elif self.state == 10:  # lgStore_V2 operation
                if verbose: 
                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: Processing lgStore_V2\033[0m")
                
                # PARSE FIRST VALUE ($1)
                value1 = 0
                if self.pointer < len(self.prog) and self.prog[self.pointer] == 'a':
                    # !a…!b FORMAT
                    self.pointer += 1
                    value_buffer = []
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'b':
                        if self.prog[self.pointer] == '\\':
                            self.pointer += 1
                            if self.pointer < len(self.prog):
                                escape_chars = {'a': 'a', 'b': 'b', 'd': 'd', 'e': 'e', '\\': '\\'}
                                char = self.prog[self.pointer]
                                value_buffer.append(escape_chars.get(char, char))
                                self.pointer += 1
                        else:
                            value_buffer.append(self.prog[self.pointer])
                            self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'b':
                        sys.exit(4)
                    
                    self.pointer += 1
                    value1 = float(''.join(value_buffer))
                
                elif self.pointer < len(self.prog) and self.prog[self.pointer] == 'd':
                    # !d…!e FORMAT
                    self.pointer += 1
                    value_buffer = ''
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                        value_buffer += self.prog[self.pointer]
                        self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                        sys.exit(4)
                    
                    self.pointer += 1
                    value1 = float(value_buffer)
                    
                elif self.pointer < len(self.prog) and self.prog[self.pointer] == 'c':
                    # c* FORMAT (VARIABLE)
                    self.pointer += 1
                    if self.pointer < len(self.prog) and self.prog[self.pointer].isdigit():
                        var_index = int(self.prog[self.pointer]) - 1
                        self.pointer += 1
                        if 0 <= var_index < len(self.db):
                            value1 = self.db[var_index]
                        else:
                            sys.exit(3)
                    else:
                        sys.exit(3)
                else:
                    sys.exit(3)
                
                # EXPECT 'p' SEPARATOR
                if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'p':
                    sys.exit(3)
                
                self.pointer += 1  # Skip 'p'
                
                # PARSE SECOND VALUE ($2) - SAME LOGIC AS ABOVE
                value2 = 0
                if self.pointer < len(self.prog) and self.prog[self.pointer] == 'a':
                    # !a…!b FORMAT
                    self.pointer += 1
                    value_buffer = []
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'b':
                        if self.prog[self.pointer] == '\\':
                            self.pointer += 1
                            if self.pointer < len(self.prog):
                                escape_chars = {'a': 'a', 'b': 'b', 'd': 'd', 'e': 'e', '\\': '\\'}
                                char = self.prog[self.pointer]
                                value_buffer.append(escape_chars.get(char, char))
                                self.pointer += 1
                        else:
                            value_buffer.append(self.prog[self.pointer])
                            self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'b':
                        sys.exit(4)
                    
                    self.pointer += 1
                    value2 = float(''.join(value_buffer))
                    
                elif self.pointer < len(self.prog) and self.prog[self.pointer] == 'd':
                    # !d…!e FORMAT
                    self.pointer += 1
                    value_buffer = ''
                    while self.pointer < len(self.prog) and self.prog[self.pointer] != 'e':
                        value_buffer += self.prog[self.pointer]
                        self.pointer += 1
                    
                    if self.pointer >= len(self.prog) or self.prog[self.pointer] != 'e':
                        sys.exit(4)
                    
                    self.pointer += 1
                    value2 = float(value_buffer)
                    
                elif self.pointer < len(self.prog) and self.prog[self.pointer] == 'c':
                    # c* FORMAT (VARIABLE)
                    self.pointer += 1
                    if self.pointer < len(self.prog) and self.prog[self.pointer].isdigit():
                        var_index = int(self.prog[self.pointer]) - 1
                        self.pointer += 1
                        if 0 <= var_index < len(self.db):
                            value2 = self.db[var_index]
                        else:
                            sys.exit(3)
                    else:
                        sys.exit(3)
                else:
                    sys.exit(3)
                
                # STORE BOTH VALUES IN lg[0] AND lg[1]
                self.lg[0] = value1
                self.lg[1] = value2
                
                if verbose:
                    print(f"\033[90m{self.get_formatted_time()} V [from {str(parent)}] -> execute: lgStore_V2 -> lg[0] = {self.lg[0]}, lg[1] = {self.lg[1]}\033[0m")
                
                self.state = 0
                continue
            elif self.state == 11:
                pass
            elif verbose:
                print(f"\033[91m{self.get_formatted_time()} E [from {str(parent)}] -> execute: CRITICAL: Invalid state {hex(self.state)}\033[0m")
                sys.exit(10)
                continue