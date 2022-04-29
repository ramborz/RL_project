import numpy as np
import cystal_util



filename = "./struct.cif"
cur_file = filename
cur_struct=cystal_util.readstruct(cur_file)
a = cystal_util.engcheck(cur_struct)

print(a )

'''
pick = np.random.randint(0, 99)
print(pick)
if (pick<30): #Ag
    action = pick/5
elif (pick<60):#H
    action = pick/5
elif(pick<90):#N
    action = pick/5
else:#cell
    action = np.random.randint(18, 23)

print (int(action))

act = int(action/2)
act2 = int(action%2)
print(act,act2)

shape =(8,8,6)
state_0 = np.random.randint(0, 50, shape, dtype=np.uint16)
state_1 = np.random.randint(100, 150, shape, dtype=np.uint16)
state_2 = np.random.randint(200, 250, shape, dtype=np.uint16)
state_3 = np.random.randint(300, 350, shape, dtype=np.uint16)
states = [state_0, state_1, state_2, state_3]
print(states)
'''
(3,3,3, 3,3,3,  3,3,3,  3,3,3)