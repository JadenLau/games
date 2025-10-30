#from sympy import Q
from compiler import DirectExecVM
from os import system
from datetime import datetime
import time
vm = DirectExecVM(verbose=True,parent='debugger')
class config():
    def __init__(self):
        self.total = ''
        self.prefix = '.'
        self.verbose = True
        self.command = 'debugger'
        self.inputprefix = '>'
        self.ping = 10 # ms
        self.rmcomment = True
        self.debug = False
class op():
    class editor():
        def __init__(self,**args):
            self.os = __import__('os')
            self._logpath = 'editor.log'
            self.__dict__.update(args)
        def verbose(parent='debugger',name='self',outputfile='',msg=''):
            if outputfile != '':
                f = open(outputfile,'a')
                f.write(f"\033[90m[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] V [from {str(parent)}] -> {name}: {msg}\033[0m\n")
                f.close()
            else:
                print(f"\033[90m{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} V [from {str(parent)}] -> {name}: {msg}\033[0m")
        def launch(self,**args):
            # we are making our OWN PROGRAM EDITOR!!!
            # 0. log launch
            self.verbose(name='launch',outputfile=self._logpath,msg='Begin launch sequence.')
            # 1. get terminal size
            tx = self.os.get_terminal_size().columns
            ty = self.os.get_terminal_size().lines
            self.verbose(name='launch',outputfile=self._logpath,msg=f'terminal size: {tx}x{ty}')
            # 2. screen clear
            self.os.system('clear# & cls') # smart enough for both unix and windows
            self.verbose(name='launch',outputfile=self._logpath,msg='clear screen')
            # 3. time for the UI
    def verbose(parent='debugger',name='self',outputfile='',msg=''):
        if outputfile != '':
            f = open(outputfile,'a')
            f.write(f"\033[90m[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] V [from {str(parent)}] -> {name}: {msg}\033[0m\n")
            f.close()
        else:
            print(f"\033[90m{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} V [from {str(parent)}] -> {name}: {msg}\033[0m")
    def debug(parent='debugger',name='self',outputfile='',msg=''):
        if outputfile != '':
            f = open(outputfile,'a')
            f.write(f"\033[95m[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] D [from {str(parent)}] -> {name}: {msg}\033[0m\n")
            f.close()
        else:
            print(f"\033[95m{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} D [from {str(parent)}] -> {name}: {msg}\033[0m")
    def runprog(verbose=True,adjust_total=True,total_in='',cmd=''):
        begin = time.time()
        # Use total_in if provided, otherwise use the passed cmd or config.lastcmd
        code_to_run = total_in if total_in else (cmd if cmd else config.lastcmd)
        
        vm.loadprog(bytecode=vm.preprocess(code_to_run,rm_comment=config.rmcomment,parent='debugger',verbose=verbose),verbose=verbose,parent='debugger')
        print(f'loaded program ({time.time()-begin:.3f}s)')
        begin = time.time()
        if adjust_total and not total_in:  # Only add to history if not running from file/total
            config.total += code_to_run + ' '  # Add space separator
        try:
            exitcode = vm.execute(parent='debugger',verbose=verbose,force_ping=config.ping)
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        finally:
            print(f'\033[92m\nOperation completed with exit code {exitcode} ({time.time()-begin:.3f}s)\033[0m')
config = config()
while True:
    # Show current history and program for clarity (verbose-style)
    #print(f"\033[90mHIST[{len(config.total)}]: {config.total!r}\033[0m")
    #print(f"\033[90mPROG: {vm.prog}\033[0m")
    x = input(f'{config.command}{config.inputprefix} ')
    config.lastcmd = x
    # === MULTI CHAR CMDS ===
    if x[0:5] == config.prefix+'set ':
        try: 
            exec(f'config.{x[5:]}')
            print(f'\033[94mExecuted: config.{x[5:]}\033[0m')
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    elif x[0:8] == config.prefix+'export ':
        try:
            f = open(x[8:],'w')
            f.write(config.total)
            f.close()
            print(f"\033[92mExport cmds -> {x[8:]}\033[0m")
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    elif x[0:8] == config.prefix+'editor ':
        op.editor()
        continue
    elif x[0:9] == config.prefix+'runfile ':
        try: op.runprog(verbose=config.verbose,adjust_total=False,total_in=open(x[9:],'r').read())
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue 
    elif x[0:5] == config.prefix+'cat ':
        # we have to make it colorful
        # light colors:
        x91 = '\033[91m' # red
        x92 = '\033[92m' # green
        x93 = '\033[93m' # yellow
        x94 = '\033[94m' # blue
        x95 = '\033[95m' # purple
        x96 = '\033[96m' # cyan
        x97 = '\033[97m' # white
        x90 = '\033[90m' # gray
        # first of all, read
        try: f = open(x[5:],'r').read()
        except Exception as e:
            print(f"\033[91mException: {type(e).__name__}: {e}\033[0m")
            continue
        # we will color up syntaxs, for characters one by one
        pointer = 0
        state = 0
        out = ''
        while True:
            if pointer >= len(f): break
            if state == 0:
                if f[pointer] == '1': # init everything
                    out += x91+f[pointer]
                    pointer += 1
                    continue
                elif f[pointer] == '2': # clear db
                    out += x91+f[pointer]
                    pointer += 1
                    continue
                elif f[pointer] == '3': # mov
                    out += x91+f[pointer]
                    pointer += 1
                    state = 1
                    continue
                else:
                    out += f[pointer]
                pointer += 1
                continue
            elif state == 1:
                if f[pointer] == 'a': # mov pm 0 type is auto
                    # string color light blue (autotype default is str)
                    out += x94+f[pointer]
                else:
                    out += f[pointer]
                pointer += 1
                state = 0
                continue
        print(out + '\033[0m')  # Reset color at end
        continue
    # === SINGLE CHAR CMDS ===
    elif x[0:2] == config.prefix+'h':
        print(f'\033[94mhistory = {config.total!r}\033[0m')
        continue
    elif x[0:2] == config.prefix+'d':
        try: x=int(x[2:3])
        except:
            print(f'\033[94m*db =',*vm.db,'\033[0m')
            continue
        print(f'\033[94mdb[{x}] (c{x+1}) = "{vm.db[x]}" (type {type(vm.db[x])}),','\033[0m')
        continue
    elif x[0:2] == config.prefix+'t':
        try: x=int(x[2:4])
        except:
            print(f'\033[94m*tmp =',str(vm.tmp),'\033[0m')
            continue
        print(f'\033[94mtmp[{x}] (tmp{x+1}) =',str(vm.tmp[x]),'\033[0m')
        continue
    elif x[0:2] == config.prefix+'l':
        print(f'\033[94m*lg =',str(vm.lg),'\033[0m')
        continue
    elif x[0:2] == config.prefix+'w':
        if len(x) < 5:
            print(f'\033[94mdebuggeer cmd wd invalid length\033[0m')
            continue
        elif x[2:3] == 'd':
            try:
                p=int(x[3:4])
                if not (1 <= p <= 7): raise Exception()
            except:
                print(f'\033[94mdebugger cmd wd missing/invalid pm(s)\033[0m') # pm: parameters
                continue
            val = x[5:]
            try:
                vm.db[p-1] = float(val)
                print(f'\033[94mmov db[{p-1}] (c{p})<- float {float(val)}\033[0m')
            except:
                vm.db[p-1] = val
                print(f'\033[94mmov db[{p-1}] (c{p})<- str/auto {val}\033[0m')
            continue
        elif x[2:3] == 't':
            try:
                p=int(x[3:5])
                if not (1 <= p <= 99): raise Exception()
            except:
                print(f'\033[94mebugger cmd wt missing/invalid pm(s)\033[0m')
                continue
            if x[4] == ',' or x[4] == '\x20': val = x[5:]
            else: val = x[6:]
            try:
                vm.tmp[p-1] = float(val)
                print(f'\033[94mmov tmp[{p-1}] (t{p})<- float {float(val)}\033[0m')
            except:
                vm.tmp[p-1] = val
                print(f'\033[94mmov tmp[{p-1}] (t{p})<- str/auto {val}\033[0m')
            continue
        elif x[2:3] == 'l':
            print(f'\033[94mdebugger cmd wl incompleted lg feature\033[0m')
            continue
        continue
    elif x[0:2] == config.prefix+'r':
        vm.loadprog(
            bytecode=vm.preprocess(
                code=config.total,
                rm_comment=config.rmcomment,
                parent='debugger',
                verbose=config.verbose
            ),
            verbose=config.verbose,
            parent='debugger'
        )
        try:
            vm.execute(parent='debugger',verbose=config.verbose,force_ping=config.ping)
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    elif x[0:2] == config.prefix+'c':
        config.total = ""
        print(f'\033[94mclear history\033[0m')
        continue
    elif x[0:2] == config.prefix+'q':
        break
    elif x[0:1] == "%":
        try: exec(x[1:len(x)])
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    elif x[0:1] == '!':
        try: print(eval(x[1:len(x)]))
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    elif x[0:1] == '$':
        try: system(x[1:len(x)])
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    elif x[0:1] == config.prefix:
        print(f'\033[94minvalid debugger cmd\033[0m')
        continue
    elif x[0:1] == '':
        continue
    else:
        op.runprog(verbose=config.verbose,adjust_total=True,cmd=x)