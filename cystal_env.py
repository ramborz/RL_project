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

# Trasitsion prob
class ActionSpace(object):
    def __init__(self): # AgNH 24 actions
        self.n = 24

    def sample(self):# Trasition Prob
        pick = np.random.randint(0, 99)
        if (pick<30): #Ag
            action = pick/5
        elif (pick<60):#H
            action = pick/5
        elif(pick<90):#N
            action = pick/5
        else:#cell
            action = np.random.randint(18, 23)
        #print (action)
        return int(action)



class ObservationSpace(object):
    '''
    #states:
    #  cell :
    #       x , y,  z
    max volume ~ 2000
    min volume ~ 100
    xyz max 10
    min 5
    
    atoms max 1
    min 0
    distcrete 100

    distcrete_size = 100 * 12

    shape: (4,3)

    cell (5,5,5) (15,15,15)
    ag 
    h
    n    (0,0,0) (1,1,1)
    4
    (x,y,z)
    (x,y,z)
    (x,y,z)
    (x,y,z)


    R x 12

    '''
    def __init__(self, ):
        #self.qtable = np.random.uniform(low = -5,high = 0, size =([100]*12 + [24]))
        #self.shape =  self.qtable.shape
        shape =(12,)
        self.shape = (12,)
        '''
        self.state_0 = np.random.randint(0, 100, shape, dtype=np.uint16)
        self.state_1 = np.random.randint(0, 100, shape, dtype=np.uint16)
        self.state_2 = np.random.randint(0, 100, shape, dtype=np.uint16)
        self.state_3 = np.random.randint(0, 100, shape, dtype=np.uint16)
    
        self.states = [self.state_0, self.state_1, self.state_2, self.state_3 ]  
        ''' 


    


class EnvTest(object):
    """
    Adapted from Igor Gitman, CMU / Karan Goel
    Modified 
    """
    def __init__(self):
        
        self.initfile = "./inital/24-AgHN-62-1967.cif"
        self.filename = "./struct.cif"
        shutil.copyfile(self.initfile, self.filename)
        #self.rewards = cystal_util.engcheck()
        #self.was_in_second = False
        self.action_space = ActionSpace()
        self.observation_space = ObservationSpace()
        

    def reset(self):
        shutil.copyfile(self.initfile, self.filename)
        filename = "./struct.cif"
        self.cur_file = filename
        self.cur_state = cystal_util.get_state(self.cur_file)
        #print(self.cur_state)
        self.num_iters = 0
        #self.was_in_second = False
        return self.cur_state
        
        

    def step(self, action):
        filename = "./struct.cif"
        assert(0 <= action <= 23)

        self.num_iters += 1
        self.cur_state = cystal_util.act(self.cur_state,action,filename)
        
        self.cur_file = cystal_util.mutation(action,filename)
        #self.cur_state = cystal_util.get_state(self.cur_file)

        self.cur_struct = cystal_util.readstruct(filename)
        
        #reward = cystal_util.engcheck(self.cur_struct)
        reward = cystal_util.radcheck(self.cur_struct)
        #reward = cystal_util.engcheck(self.cur_struct)+cystal_util.radcheck(self.cur_struct)
        return self.cur_state, reward , self.num_iters >= 5,{'ale.lives':0}



      
    def render(self):
        print(self.cur_state)

