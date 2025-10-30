import random

def verif(box):
    for box_y in range(9):
        for box_x in range(9):
            # v: [box[0][x],box[1][x],...,box[8][x]]
            v = [box[i][box_x] for i in range(9)]
            # h: [box[y][0],box[y][1],...,box[y][8]]
            h = [box[box_y][i] for i in range(9)]
            # b: its different and difficult
            # 9x9 table is cutted into 9 pieces
            # from (0-2)(0-2) to (6-8)(6-8
            # each piece has 3 rows and 3 columns
            # we have x and y
            # detect which piece it belongs to
            # then, get the 3x3 piece
            # example, x=1 y=2 -> [box[0][0],box[0][1],box[0][2],box[1][0],...,box[2][2]]
            pieceX = box_x // 3
            pieceY = box_y // 3
            b = [box[pieceY*3 + i][pieceX*3 + j] for i in range(3) for j in range(3)]
            # detect duplicates in v h b
            for l in [v,h,b]:
                s = set()
                for n in l:
                    if n == 0:
                        continue
                    if n in s:
                        return False
                    s.add(n)
            # detect is numbers in v,h,b valid (should be int 1-9)
            for l in [v,h,b]:
                for n in l:
                    if n < 1 or n > 9:
                        return False
    return True

def generate_box():
    # need to confirm that is a valid sudoku
    # and return all answers, dont delete
    # randomise numbersrn
    # and verify is it VAILD with verif()
    # first, start with from x=0 y=0 to x=0 y=8
    num = [1,2,3,4,5,6,7,8,9]
    num.sort(key=lambda x: random.random())
    b = [num,[],[],[],[],[],[],[],[]]
    # first row (x=0) ok
    # now, calculate piece 0 (0,0)
    # --- calculate (1,0)
    # * remove exist numbers (box)
    n = [b[0][i] for i in range(3)] # (0,0),(0,1),(0,2)
    num = [1,2,3,4,5,6,7,8,9]
    for v in n:
        if v in num:
            num.remove(v)
    # * remove exist numbers (v)
    # since only 1 numbers in row x=0, we don't need to check h one
    # get all numbers in column y=0
    n = [b[i][0] for i in range(1)]
    for v in n:
        if v in num:
            num.remove(v)
    # * remove exist numbers (h)
    # just get (0,0)
    if b[0][0] in num: num.remove(b[0][0])
    # now we get all possible numbers for (1,0)
    n = num[random.randint(0,len(num)-1)]
    # then assign the value to the box
    b[0][1] = n
    # calculated:
    # (0,0)-(0,8) and (1,0)
    # now, we calculate each box ONE BY ONE like this:
    # 1. List of numbers [1,2,3,4,5,6,7,8,9]
    # 2. Check same row, same column, same piece, remove same numbers
    # 3. 
def solve(box):
    # solve sudoku box, return maximum of 100 possibilities
    pb = []
    def backtrack(pos): 
        if len(pb) >= 100:
            return
        if pos == 81:
            # found a solution
            solution = [row[:] for row in box]
            pb.append(solution)
            return
        x = pos % 9
        y = pos // 9
        if box[y][x] != 0:
            backtrack(pos + 1)
            return
        for n in range(1, 10):
            box[y][x] = n
            if verif(box):
                backtrack(pos + 1)
            box[y][x] = 0
    

def main():
    box = [[0]*9 for _ in range(9)]
    

if __name__ == '__main__':
    main()