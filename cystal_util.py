import numpy as np
from pymatgen.core.structure import Structure
from maml.apps.bowsr.model.megnet import MEGNet
import pymatgen.core.periodic_table as ELE

DFT_calcuated_structure =  Structure.from_file("./dft/24-AgHN-62-1967.cif")
inital_filename = "./inital/24-AgHN-62-1967.cif"
element_matrix=np.zeros((len(DFT_calcuated_structure.distance_matrix), len(DFT_calcuated_structure.distance_matrix)))
#print(element_matrix)
sites = DFT_calcuated_structure.sites
for i in range(len(DFT_calcuated_structure.distance_matrix)):
    target = ELE.Element(DFT_calcuated_structure[i].species_string)
    for j in range(len(DFT_calcuated_structure.distance_matrix)):
        if i==j: # same atom
            element_matrix[i,j] = 0 
            continue
        temp = ELE.Element(sites[j].species_string)
        #print(temp.atomic_radius_calculated)
        min_dist = target.atomic_radius_calculated+temp.atomic_radius_calculated
        element_matrix[i,j] = min_dist

def readstruct ( filename ):
    #print(filename)
    try:   
        struct_pymatgen = Structure.from_file(filename)
    except:
        print("error reading filename: ", filename)
        return
    return struct_pymatgen
    
        
def radcheck (target):
   
    #print("maxradius  " + np.max(element_matrix))
    radicheck= abs(target.distance_matrix-element_matrix)
    radicheck= -radicheck

    radicheck= target.distance_matrix-element_matrix # test 3

    radicheck= np.min(radicheck)
    return radicheck

model = MEGNet()

def engcheck(target):

    predicted_energy =0
    try:
        predicted_energy = model.predict_energy(target)
    except:
        print("energy error")
        inital_energy ="error"
    return predicted_energy

def mutation(action,struct_str):
    #input struct is a string read from file 
    #pymatgen break the symmetric

    file = open(struct_str, 'r')
    count = 0
    content_list = []
    for line in file:
        count += 1
        if count < 15 :
            content = line  .strip().split("   ")
        else:
            content = line  .strip().split("  ")
        #print (content)
        content_list.append(content)
        #print("Line{}: {}".format(count, line.strip()))
    file.close()
    #print(content_list)

    #amount of muation for cell dim
    gamma = round(abs(float(content_list[12][1])/1000),3)
    #print(gamma)

    #action start
    #atom coordnates are faction of cell dim which is 0-1 so adding 0.01 is ok
    #cell dim will be mutating 1% of cell vol
    if action < 0 or action >23:
        print("illegal action index")
        return struct_str
    if action < 6: #ag
        if action < 2:#x
            if action <1: # x +
                content_list[-3][3] = str(float(content_list[-3][3])+0.01) 
            else: #x - 
                content_list[-3][3] = str(float(content_list[-3][3])-0.01) 
        elif action < 4: # y
            action = action -2 
            if action <1: # y +
                content_list[-3][4] = str(float(content_list[-3][4])+0.01) 
            else: #y - 
                content_list[-3][4] = str(float(content_list[-3][4])-0.01) 
        else: # z
            action = action -4
            if action <1: # z +
                content_list[-3][5] = str(float(content_list[-3][5])+0.01) 
            else: #z - 
                content_list[-3][5] = str(float(content_list[-3][5])-0.01) 


    elif action < 12: #H
        action = action -6
        if action < 2:#x
            if action <1: # x +
                content_list[-2][3] = str(float(content_list[-2][3])+0.01) 
            else: #x - 
                content_list[-2][3] = str(float(content_list[-2][3])-0.01) 
        elif action < 4: # y
            action = action -2 
            if action <1: # y +
                content_list[-2][4] = str(float(content_list[-2][4])+0.01) 
            else: #y - 
                content_list[-2][4] = str(float(content_list[-2][4])-0.01) 
        else: # z
            action = action -4
            if action <1: # z +
                content_list[-2][5] = str(float(content_list[-2][5])+0.01) 
            else: #z - 
                content_list[-2][5] = str(float(content_list[-2][5])-0.01) 

    elif action < 18:#N
        action = action -12
        if action < 2:#x
            if action <1: # x +
                content_list[-1][3] = str(float(content_list[-1][3])+0.01) 
            else: #x - 
                content_list[-1][3] = str(float(content_list[-1][3])-0.01) 
        elif action < 4: # y
            action = action -2 
            if action <1: # y +
                content_list[-1][4] = str(float(content_list[-1][4])+0.01) 
            else: #y - 
                content_list[-1][4] = str(float(content_list[-1][4])-0.01) 
        else: # z
            action = action -4
            if action <1: # z +
                content_list[-1][5] = str(float(content_list[-1][5])+0.01) 
            else: #z - 
                content_list[-1][5] = str(float(content_list[-1][5])-0.01) 
        
    else:#cell
        action = action -18
        if action < 2:#x
            if action <1: # x +
                content_list[3][1] = str(float(content_list[3][1])+gamma) 
            else: #x - 
                content_list[3][1] = str(float(content_list[3][1])-gamma) 
        elif action < 4: # y
            action = action -2 
            if action <1: # y +
                content_list[4][1] = str(float(content_list[4][1])+gamma) 
            else: #y - 
                content_list[4][1] = str(float(content_list[4][1])-gamma) 
        else: # z
            action = action -4
            if action <1: # z +
                content_list[5][1] = str(float(content_list[5][1])+gamma) 
            else: #z - 
                #print("z-")
                content_list[5][1] = str(float(content_list[5][1])-gamma) 
    #print(content_list)

    #save mutation
    with open(struct_str, 'w') as f:
        count = 0
        for line in content_list:
            if count < 15 :
                stringtmp = "   ".join(line)
            else:
                stringtmp = "  ".join(line)
            f.write(stringtmp)
            f.write('\n')
            count += 1
    f.close()

def get_state(struct_str):
    file = open(struct_str, 'r')
    count = 0
    content_list = []
    for line in file:
        count += 1
        if count < 15 :
            content = line  .strip().split("   ")
        else:
            content = line  .strip().split("  ")
        #print (content)
        content_list.append(content)
        #print("Line{}: {}".format(count, line.strip()))
    file.close()

    s = [
        

        round(float(content_list[-3][3]),3),
        round(float(content_list[-3][4]),3),
        round(float(content_list[-3][5]),3),

        round(float(content_list[-2][3]),3),
        round(float(content_list[-2][4]),3),
        round(float(content_list[-2][5]),3),

        round(float(content_list[-1][3]),3),
        round(float(content_list[-1][4]),3),
        round(float(content_list[-1][5]),3), 

        round(float(content_list[3][1]),3),
        round(float(content_list[4][1]),3),
        round(float(content_list[5][1]),3)

    ]
    
    return s


def act (state, action ,struct_str):
    #state [cellx,y,z,agx,y,z,...] total 12
    assert(0 <= action <= 23)
    act = int(action/2)
    act2 = int(action%2)
    if act < 9:
        if act2 ==0:
            state[act] = state[act] + 0.01
        else :
            state[act] = state[act]- 0.01
    else :
    
        file = open(struct_str, 'r')
        count = 0
        content_list = []
        for line in file:
            count += 1
            if count < 15 :
                content = line  .strip().split("   ")
            else:
                content = line  .strip().split("  ")
            #print (content)
            content_list.append(content)
            #print("Line{}: {}".format(count, line.strip()))
        file.close()
        #print(content_list)

        #amount of muation for cell dim
        gamma = round(abs(float(content_list[12][1])/1000),3)
        #print(gamma)

        if act2 ==0:
            state[act] = state[act] + gamma
        else :
            state[act] = state[act]- gamma

    return state
'''  
#testing
for i in range(24):
    print(i)
    mutation(i ,"struct.cif")

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
'''