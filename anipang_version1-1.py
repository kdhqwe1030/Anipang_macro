import pyautogui as pag


def sameValueDel(tmp_list):
    tmp_center_list=[]
    for key in tmp_list:
        tmp_center_list.append([pag.center(key)[0],pag.center(key)[1]])

    tmp_center_list.sort() 
    i,j=0,1
    while True:

        while True:
            if len(tmp_center_list)<=i+j:
                break
            if abs(tmp_center_list[i][0]-tmp_center_list[i+j][0])<16 and abs(tmp_center_list[i][1]-tmp_center_list[i+j][1])<16:
                del tmp_center_list[i+j]
            else:
                j+=1
        j=1
        i+=1
        if len(tmp_center_list)<=i+j:
            break
    return tmp_center_list

def findWhatKind(who):
    if who in animal_bear:
        return "bear"
    elif who in animal_cat:
        return "cat"
    elif who in animal_chick:
        return "chick"
    elif who in animal_monkey:
        return "monkey"
    elif who in animal_pig:
        return "pig"
    elif who in animal_rabbit:
        return "rabbit"
    else:
        return "rat"

def completeMakeField(animal_list):
    test_list=[]
    for j in range(7):
        
        for k in range(7):
            test_list.append(animal_list[k+j*7])
        test_list.sort(key=lambda x:x[1])
        #print(test_list)
        for i in range(7):
            field[i][j]=[findWhatKind(test_list[i]),test_list[i]]
        
        test_list.clear()


def shiftAnimal(start_x,start_y,end_x,end_y):
    pag.moveTo(start_x,start_y)
    pag.dragTo(end_x,end_y,0.3,button='left')#end_y뒤에,4하면 4초동안 옮김

def cellDivision_x(tmp_list3):
    min_number=tmp_list3[0][0]
    result_list=[]
    result_sum_list=[[]]
    list1,list2,list3,list4,list5,list6,list7=[],[],[],[],[],[],[]
    for_list=[min_number+65+65+65*i for i in range(5)]    
    for i in range(len(tmp_list3)):
        if tmp_list3[i][0]<=min_number+65:
            list1.append(tmp_list3[i][0])    
        for j,letter in enumerate(for_list,start=2):
            if letter-75<=tmp_list3[i][0] and tmp_list3[i][0]<=letter:
                (globals()['list{}'.format(j)]).append(tmp_list3[i][0])
    result_list=[list1,list2,list3,list4,list5,list6,list7]
    for i,key in enumerate(result_list()):
        if key<7:
            tmp_list3[cellDivision_y(key)].insert(i,0)
    return tmp_list3
    
def cellDivision_y(tmp_list3):
    
    min_number=tmp_list3[0]
    if min_number<tmp_list3[1]-70 and min_number<tmp_list3[2]-140:
        tmp_list3.insert(0,0)
        return tmp_list3
    list1,list2,list3,list4,list5,list6,list7=[],[],[],[],[],[],[]
    for_list=[min_number+65+65+65*i for i in range(5)]    
    for i in range(len(tmp_list3)):
        if tmp_list3[i]<=min_number+50:
            list1.append(tmp_list3[i])    
        for j,letter in enumerate(for_list,start=2):
            if letter-70<=tmp_list3[i] and tmp_list3[i]<=letter:
                globals()['list{}'.format(j)].append(tmp_list3[i])
            else:
                return j-1
      


   
while 100:
    while True:
        animal_name=["bear","cat","chick","monkey","pig","rabbit","rat","bomb"]
        animal_bear,animal_cat,animal_chick,animal_monkey,animal_pig,animal_rabbit,animal_rat="","","","","","",""
        if (pag.locateCenterOnScreen(r"C:\code\anipang\images\bomb.png",confidence=0.89))!=None:
            qwe=(pag.locateCenterOnScreen(r"C:\code\anipang\images\bomb.png",confidence=0.89))
            pag.leftClick(qwe[0],qwe[1])

            
        #pag.locateCenterOnScreen(r"C:\code\anipang\images\bomb.png",confidence=0.89)
        field=[["" for j in range(7)] for i in range(7)] 

        for i in animal_name:
            globals()['animal_{}'.format(i)]=sameValueDel(list(pag.locateAllOnScreen(rf"C:\code\anipang\images\{i}.png",confidence=0.84)))#0.92
            

        #####필드와 리스트통합
        animal=animal_monkey+animal_bear+animal_cat+animal_chick+animal_pig+animal_rabbit+animal_rat#+animal_bomb
        if len(animal)==49:
            break
        else:
            for i in animal_name:
                if sameValueDel(list(pag.locateAllOnScreen(rf"C:\code\anipang\images\comb\{i}_comb.png",confidence=0.84)))!=None:
                    globals()['animal_{}'.format(i)].append(sameValueDel(list(pag.locateAllOnScreen(rf"C:\code\anipang\images\comb\{i}_comb.png",confidence=0.84))))#0.92
                    if len(animal)!=49:
                        animal.sort()
                        animal=cellDivision_x(animal)
            break

    #####필드에 무슨동물 어디인지 확실하게 정하기
    completeMakeField(animal)






    end=0
    for y in range(7):
        for x in range(4):
            if field[y][x][0]==field[y][x+1][0]:
                if field[y][x][0]==field[y][x+3][0]:
                    shiftAnimal(field[y][x+3][1][0],field[y][x+3][1][1],field[y][x+2][1][0],field[y][x+2][1][1])
                    end=1
    if end==1:
        continue
    for y in range(6):
        for x in range(5):
            if field[y][x][0]==field[y][x+1][0]:
                if field[y][x][0]==field[y+1][x+2][0]:
                    shiftAnimal(field[y+1][x+2][1][0],field[y+1][x+2][1][1],field[y][x+2][1][0],field[y][x+2][1][1])
                    end=1
    if end==1:
        continue
    for y in range(1,7):
        for x in range(5):   
            if field[y][x][0]==field[y][x+1][0]:
                if field[y][x][0]==field[y-1][x+2][0]:
                    shiftAnimal(field[y-1][x+2][1][0],field[y-1][x+2][1][1],field[y][x+2][1][0],field[y][x+2][1][1])
                    end=1
    if end==1:
        continue
    
    for y in range(7):
        for x in range(6,2,-1):
            if field[y][x][0]==field[y][x-1][0]:
                if field[y][x][0]==field[y][x-3][0]:
                    shiftAnimal(field[y][x-3][1][0],field[y][x-3][1][1],field[y][x-2][1][0],field[y][x-2][1][1])
                    end=1    
    if end==1:
        continue
    for y in range(6):
        for x in range(6,3,-1):
            if field[y][x][0]==field[y][x-1][0]:
                if field[y][x][0]==field[y+1][x-2][0]:
                    shiftAnimal(field[y+1][x-2][1][0],field[y+1][x-2][1][1],field[y][x-2][1][0],field[y][x-2][1][1])
                    end=1    
    if end==1:
        continue
    for y in range(1,7):
        for x in range(6,3,-1):
            if field[y][x][0]==field[y][x-1][0]:                               
                if field[y][x][0]==field[y-1][x-2][0]:
                    shiftAnimal(field[y-1][x-2][1][0],field[y-1][x-2][1][1],field[y][x-2][1][0],field[y][x-2][1][1])
                    end=1    
    if end==1:
        continue
    #2
    for x in range(7):
        for y in range(4):
            if field[y][x][0]==field[y+1][x][0]:
                if field[y][x][0]==field[y+3][x][0]:
                    shiftAnimal(field[y+3][x][1][0],field[y+3][x][1][1],field[y+2][x][1][0],field[y+2][x][1][1])
                    end=1
    if end==1:
        continue
    for x in range(1,6):
        for y in range(5):
            if field[y][x][0]==field[y+1][x][0]:
                if field[y][x][0]==field[y+2][x+1][0]:
                    shiftAnimal(field[y+2][x+1][1][0],field[y+2][x+1][1][1],field[y+2][x][1][0],field[y+2][x][1][1])
                if field[y][x][0]==field[y+2][x-1][0]:
                    shiftAnimal(field[y+2][x-1][1][0],field[y+2][x-1][1][1],field[y+2][x][1][0],field[y+2][x][1][1])
                    end=1    
    if end==1:
        continue
    for x in range(7):
        for y in range(6,3,-1):
            if field[y][x][0]==field[y-1][x][0]:
                if field[y][x][0]==field[y-3][x][0]:
                    shiftAnimal(field[y-3][x][1][0],field[y-3][x][1][1],field[y-2][x][1][0],field[y-2][x][1][1])
                    end=1
    if end==1:
        continue
    for x in range(6):        
        for y in range(6,1,-1):
            if field[y][x][0]==field[y-1][x][0]:
                if field[y][x][0]==field[y-2][x+1][0]:
                    shiftAnimal(field[y-2][x+1][1][0],field[y-2][x+1][1][1],field[y-2][x][1][0],field[y-2][x][1][1])
                    end=1    
    if end==1:
        continue
    for x in range(1,7):        
        for y in range(6,1,-1):
            if field[y][x][0]==field[y-1][x][0]:
                if field[y][x][0]==field[y-2][x-1][0]:
                    shiftAnimal(field[y-2][x-1][1][0],field[y-2][x-1][1][1],field[y-2][x][1][0],field[y-2][x][1][1])
                    end=1    
    if end==1:
        continue

    for y in range(6):
        for x in range(5):           
            if (field[y][x][0]==field[y][x+2][0]) and (field[y][x][0]==field[y+1][x+1][0]):
                shiftAnimal(field[y+1][x+1][1][0],field[y+1][x+1][1][1],field[y][x+1][1][0],field[y][x+1][1][1])
                end=1    
    if end==1:
        continue
    for y in range(1,7):
        for x in range(5):
            if (field[y][x][0]==field[y][x+2][0]) and (field[y][x][0]==field[y-1][x+1][0]):
                shiftAnimal(field[y-1][x+1][1][0],field[y-1][x+1][1][1],field[y][x+1][1][0],field[y][x+1][1][1])
                end=1    
    if end==1:
        continue
    for x in range(6):
        for y in range(5):
            if (field[y][x][0]==field[y+2][x][0]) and (field[y][x][0]==field[y+1][x+1][0]):
                shiftAnimal(field[y+1][x+1][1][0],field[y+1][x+1][1][1],field[y+1][x][1][0],field[y+1][x][1][1])
                end=1    
    if end==1:
        continue
    for x in range(1,7):
        for y in range(5):
                if (field[y][x][0]==field[y+2][x][0]) and (field[y][x][0]==field[y+1][x-1][0]):
                    shiftAnimal(field[y+1][x-1][1][0],field[y+1][x-1][1][1],field[y+1][x][1][0],field[y+1][x][1][1])


    field.clear()

