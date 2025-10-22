from compiler import DirectExecVM
from os import system
vm = DirectExecVM(verbose=True,parent='debugger')
total = ''
while True:
    x = input(f'debugger> ')
    if x[0:2] == '\\d':
        try: x=int(x[2:3])
        except:
            print(f'\033[94m*db =',*vm.db,'\033[0m')
            continue
        print(f'\033[94mdb[{x}] (c{x+1}) = "{vm.db[x]}" (type {type(vm.db[x])}),','\033[0m')
        continue
    elif x[0:2] == '\\t':
        try: x=int(x[2:4])
        except:
            print(f'\033[94m*tmp =',str(vm.tmp),'\033[0m')
            continue
        print(f'\033[94mtmp[{x}] (tmp{x+1}) =',str(vm.tmp[x]),'\033[0m')
    elif x[0:2] == '\\l':
        print(f'\033[94m*lg =',str(vm.lg),'\033[0m')
    elif x[0:2] == '\\w':
        if len(x) < 5:
            print(f'\033[94mdebuggeer cmd wd invalid length\033[0m')
            continue
        if x[2:3] == 'd':
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
    elif x[0:2] == '\\r':
        vm.loadprog(vm.preprocess(total,parent='debugger',verbose=True),verbose=True,parent='debugger')
        try:
            vm.execute(parent='debugger',verbose=True)
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")
    elif x[0:2] == '\\c':
        total = ""
        print(f'\033[94mclear history\033[0m')
    elif x[0:2] == '\\q':
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
    else:
        total += x
        vm.loadprog(vm.preprocess(x,parent='debugger',verbose=False),verbose=False,parent='debugger')
        try:
            vm.execute(parent='debugger',verbose=True)
        except SystemExit as e:
            print(f"\033[91mFailure ({e.code})\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {type(e).__name__}: {e}\033[0m")