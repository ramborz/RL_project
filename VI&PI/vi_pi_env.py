import numpy as np
import sys
import shutil
#import discrete_env
import cystal_util

# Mapping between action and index number
#Ag H N 
Ag_x_i = 0
Ag_x_d = 1
Ag_y_i = 2
Ag_y_d = 3
Ag_z_i = 4
Ag_z_d = 5

H_x_i = 6
H_x_d = 7
H_y_i = 8
H_y_d = 9
H_z_i = 10
H_z_d = 11

N_x_i = 12
N_x_d = 13
N_y_i = 14
N_y_d = 15
N_z_i = 16
N_z_d = 17

cell_x_i = 18
cell_x_d = 19
cell_y_i = 20
cell_y_d = 21
cell_z_i = 22
cell_z_d = 23

# Maps for the two different environments
#env dime:
# cell xyz + all atom xyz = 4 
# states = n^4
MAPS = {
    "X5": [
        #cell 5-10 discreate 1
        #atom 0-1 discreate 0.2
    ],
    "X100": [ 
        #cell 5-15 discreate 0.05
        #atom 0-1 discreate 0.01
    ],

}
class FrozenLakeEnv(discrete_env.DiscreteEnv):


    def __init__(self, desc=None, map_name="X5"):
       
        self.nrow = 
        self.ncol = 

        nA = 23 # number of actions
        nS = (5*5*5)^4   # number of states
        
        #S_shape = (5,5,5,4)
        #S = np.random.randint(0, 1, S_shape, dtype=np.uint16)
        #print (S)



        P = {s : {a : [] for a in range(nA)} for s in range(nS)}

        def to_s(row, col):
            return row*ncol + col
        def inc(row, col, a):
            if a==0: # left
                col = max(col-1,0)
            elif a==1: # down
                row = min(row+1,nrow-1)
            elif a==2: # right
                col = min(col+1,ncol-1)
            elif a==3: # up
                row = max(row-1,0)
            return (row, col)

        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(24):
                    li = P[s][a]
                    letter = desc[row, col]
                    if letter in b'GH':
                        li.append((1.0, s, 0, True))
                    else:
                        if is_slippery:
                            for b in [(a-1)%4, a, (a+1)%4]:
                                newrow, newcol = inc(row, col, b)
                                newstate = to_s(newrow, newcol)
                                newletter = desc[newrow, newcol]
                                done = bytes(newletter) in b'GH'
                                rew = float(newletter == b'G')
                                li.append((0.8 if b==a else 0.1, newstate, rew, done))
                        else:
                            newrow, newcol = inc(row, col, a)
                            newstate = to_s(newrow, newcol)
                            newletter = desc[newrow, newcol]
                            done = bytes(newletter) in b'GH'
                            rew = float(newletter == b'G')
                            li.append((1.0, newstate, rew, done))

        super(FrozenLakeEnv, self).__init__(nS, nA, P, isd)