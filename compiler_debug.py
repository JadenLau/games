from compiler import DirectExecVM
from os import system
vm = DirectExecVM(verbose=True,parent='debugger')
total = ''
class config():
    def __init__(self):
        self.prefix = '.'
        self.verbose = True
        self.ping = 100 # ms
        self.rmcomment = True
class op():
    def runprog(verbose=True,adjust_total=False,total_in=''):
        vm.loadprog(vm.preprocess(total_in,rm_comment=config.rmcomment,parent='debugger',verbose=verbose),verbose=verbose,parent='debugger')
        if adjust_total:
            global total
            total += total_in
        try:
            vm.execute(parent='debugger',verbose=verbose)
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
config = config()
while True:
    x = input(f'debugger> ')
    # === MULTI CHAR CMDS ===
    if x[0:5] == config.prefix+'set ':
        try: exec('config.'+x[5:])
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
        continue
    # === SINGLE CHAR CMDS ===
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
    elif x[0:2] == config.prefix+'l':
        print(f'\033[94m*lg =',str(vm.lg),'\033[0m')
    elif x[0:2] == config.prefix+'w':
        if len(x) < 5:
            print(f'\033[94mdebuggeer cmd wd invalid length\033[0m')
            continue
        elif x[2:3] == 'd':
            try:
                p=int(x[3:4])-1
                if not (0 <= p <= 6): raise Exception()
            except:
                print(f'\033[94mdebugger cmd wd missing/invalid pm(s)\033[0m') # pm: parameters
                continue
            val = x[5:]
            try:
                vm.db[p] = float(val)
                print(f'\033[94mmov db[{p}] (c{p+1})<- float {float(val)}\033[0m')
            except:
                vm.db[p] = val
                print(f'\033[94mmov db[{p}] (c{p+1})<- str/auto {val}\033[0m')
            continue
        elif x[2:3] == 't':
            try:
                p=int(x[3:5])-1
                if not (0 <= p <= 98): raise Exception()
            except:
                print(f'\033[94mebugger cmd wt missing/invalid pm(s)\033[0m')
                continue
            val = x[6:]
            try:
                vm.tmp[p] = float(val)
                print(f'\033[94mmov tmp[{p}] (t{p+1})<- float {float(val)}\033[0m')
            except:
                vm.tmp[p] = val
                print(f'\033[94mmov tmp[{p}] (t{p+1})<- str/auto {val}\033[0m')
            continue
        elif x[2:3] == 'l':
            print(f'\033[94mdebugger cmd wl incompleted lg feature\033[0m')
            continue
    elif x[0:2] == config.prefix+'r':
        op.runprog(verbose=config.verbose)
    elif x[0:2] == config.prefix+'c':
        total = ""
        print(f'\033[94mclear history\033[0m')
    elif x[0:2] == config.prefix+'q':
        break
    elif x[0:1] == "%":
        try: exec(x[1:len(x)])
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
    elif x[0:1] == '!':
        try: print(eval(x[1:len(x)]))
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
    elif x[0:1] == '$':
        try: system(x[1:len(x)])
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
    elif x[0:1] == config.prefix:
        print(f'\033[94minvalid debugger cmd\033[0m')
        continue
    elif x[0:1] == '':
        continue
    else:
        op.runprog(verbose=config.verbose,adjust_total=True,total_in=x)