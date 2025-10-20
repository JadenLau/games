import builtins

class emulator():
    def __init__(self,a,b,c,d,x,y,m,pointer):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x
        self.y = y
        self.m = m
        self.pi = 3.14159265358979
        self.e = 2.71828182845904
        self.prog = [0]*1024
        self.fmla1 = [] # QuadEquation0
        self.const1 = 1.672621777*(10**-27) # mp
        self.const2 = 1.674927351*(10**-27) # mn
        self.const3 = 9.10938291*(10**-31) # me
        self.const4 = 1.883531475*(10**-28) # mw
        self.const5 = 5.291772109*(10**-11) # a?
        self.const6 = 6.62606957*(10**-34) # h
        self.const7 = 5.05078353*(10**-27) # Mn
        self.const8 = 1.883531475*(10**-28) # Mm
        self.const9 = 1.054571726*(10**-34) # k
        self.const10 = 1.054571726*(10**-34) # a
        self.const11 = 2.817940327*(10**-15) # re
        self.const12 = 2.426310239*(10**-12) # ?c
        self.const13 = 267522200.5 # yp
        self.const14 = 1.321409856*(10**-15) # ycp
        self.const15 = 1.319590907*(10**-15) # ycn
        self.const16 = 10973731.568539 # Rinf
        self.const17 = 1.660538921*(10**-27) # u
        self.const18 = 1.410606743*(10**-26) # Mp
        self.const19 = -9.2847643*(10**-24) # Me
        self.const20 = -9.6623647*(10**-27) # Mn
        self.const21 = -4.49044807*(10**-26) # Mm
        # it should be more here
    class int():
        def __init__(self,val):
            if type(val) is builtins.int: self.value = val
            elif type(val) is builtins.float: self.value = builtins.int(builtins.round(val))
            else: raise TypeError()
        def __str__(self): # im confused is that syntax oke, that int(x) does returns the correct value
            return self.value

    class float():
        def __init__(self,val):
