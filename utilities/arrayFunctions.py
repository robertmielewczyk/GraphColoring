import copy
def hillClimbIncrease(graph, mask):
    #This monster suprisingly works, but refactor it later
    colorLimit = graph.numberOfNodes
    masks = generateInceraseDecreaseMasks(graph)
    increaseSet = []
    for i in masks:
        #create new mask which looks like mask
        newMask = copy.deepcopy(mask)
        for j in range(len(i)):
            #check from mask if you should increase the value
            if(i[j]==1):
                #check if increasing wouldnt hit the limit if yes wrap around value
                if((newMask[j]+1)==colorLimit):
                    newMask[j]=0
                #if value less than limit just increase
                elif(newMask[j]+1<colorLimit):
                    newMask[j]+=1
        # Append newly created mask
        increaseSet.append(newMask)

    return increaseSet


def hillClimbDecrease(graph, mask):
    #This monster suprisingly works, but refactor it later
    colorLimit = graph.numberOfNodes
    masks = generateInceraseDecreaseMasks(graph)
    decreaseSet = []
    for i in masks:
        #create new mask which looks like mask
        newMask = copy.deepcopy(mask)
        for j in range(len(i)):
            #check from mask if you should increase the value
            if(i[j]==1):
                #check if decreasing wouldnt hit the limit if yes wrap around value
                if((newMask[j]-1)<0):
                    newMask[j]=colorLimit
                #if value less than limit just increase
                elif((newMask[j]-1)>=0):
                    newMask[j]-=1
        # Append newly created mask
        decreaseSet.append(newMask)

    return decreaseSet

def generateInceraseDecreaseMasks(graph):
    '''
    generates a binary mask like [0,1,1] where 1 stands for do something, 0 for dont
    '''
    from itertools import product
    colors = [i for i in range(2)]
    masks = []
    for i in product(colors, repeat=graph.numberOfNodes):
        masks.append(i)
    return masks


def generateNeigboursSet(graph, mask):
    '''
    generates a set [(+1, -1),...]
    '''
    neighbourSet = []
    increaseSet = hillClimbIncrease(graph, mask)
    decreaseSet = hillClimbDecrease(graph, mask)
    neighbourSet.extend(decreaseSet)
    neighbourSet.extend(increaseSet)
    return neighbourSet

def baseIncrement(array, base):
        lastElement = len(array)
        pointer = lastElement-1
        for i in range(lastElement):
            if(array[pointer] < base):
                array[pointer]+=1
                break
            elif(array[pointer] == base):
                #if next value exists turn current to 0 and let the loop repeat
                if(pointer-1>0):
                    array[pointer] = 0
                    pointer-=1
                else:
                    #wrap around make it 0000 and break
                    for i in range(len(array)):
                        array[i] = 0
                    break
        return array

#Experimental
def baseDecrement(array, base):
        lastElement = len(array)
        pointer = lastElement-1
        for i in range(lastElement):
            if(array[pointer] > 0):
                array[pointer]-=1
                break
            elif(array[pointer] == 0):
                #if next value exists turn current to 0 and let the loop repeat
                if(pointer-1>0):
                    array[pointer] = base
                    pointer-=1
                else:
                    #wrap around make it 555(base) and break
                    for i in range(len(array)):
                        array[i] = base
                    break
        return array