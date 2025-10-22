prog = [
    "1 2 8 9 c1? c2? c3? mc1p11 mc2p12 mc3p13 9 3c5d1e fc1pd0e g01 md-1ep01 mc1p02 * n03pc1 md-1ep01 mc2p02 * n03pc2 md-1ep01 mc3p02 * n03pc3 3c5d1e 401 mc2p01 mc2p02 * n03pc4 mc1p01 mc3p02 * n03pc6 mc6p01 md4ep02 * n03pc6 mc4p01 mc6p02 - n03pc3 mc3p01 A n03pc3 mc2p01 md-1ep02 * n03pc2 mc2p01 mc3p02 - n03pc2 mc2p01 md-1ep02 * n03pc2 mc1p01 md2ep02 * n03pc1 mc2p01 mc2p02 * n03pc1 mc5p01 mc1p02 * n03pc6 n11pc1 n12pc2 n13pc3 9 3c5d1e fc1pd0e g02 md-1ep01 mc1p02 * n03pc1 md-1ep01 mc2p02 * n03pc2 md-1ep01 mc3p02 * n03pc3 3c5d1e 402 mc2p01 mc2p02 * n03pc4 mc1p01 mc3p02 * n03pc6 mc6p01 md4ep02 * n03pc6 mc4p01 mc6p02 - n03pc3 mc3p01 A n03pc3 mc2p01 md-1ep02 * n03pc2 mc2p01 mc3p02 + n03pc2 mc2p01 md-1ep02 * n03pc2 mc1p01 md2ep02 * n03pc1 mc2p01 mc2p02 * n03pc1 mc5p01 mc1p02 * n03pc7 qc6 qc7 S",
    "1 2 8 9 c1? c2? mc1p01 mc2p02 + n03pc1 qc1 S"
    "qaEmptybS",
    "qaEmptybS"
]
sel = input("Select program ID: ") # i will select 0
core = prog[int(sel)]
from compiler import DirectExecVM; vm=DirectExecVM(verbose=True); vm.loadprog(bytecode=vm.preprocess(verbose=True,code=core),verbose=True)
vm.execute(verbose=True)

# (x+2)(x+3)
# = (x2+5x+6)
# 2 5 6