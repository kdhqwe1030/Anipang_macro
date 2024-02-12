import pyautogui as pag
import time

def sameValueDel(tmp_list):
    tmp_center_list=[]
    for key in tmp_list:
        tmp_center_list.append([pag.center(key)[0],pag.center(key)[1]])

    tmp_center_list.sort() ####################
    i,j=0,1
    while True:

        while True:
            if len(tmp_center_list)<=i+j:
                break
            if abs(tmp_center_list[i][0]-tmp_center_list[i+j][0])<17 and abs(tmp_center_list[i][1]-tmp_center_list[i+j][1])<17:
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
    animal_list.sort()
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
    pag.dragTo(end_x,end_y,0.3,button='left')
   
while 100:
    while True:
        
        animal_name=["bear","cat","chick","monkey","pig","rabbit","rat","bomb"]
        animal_bear,animal_cat,animal_chick,animal_monkey,animal_pig,animal_rabbit,animal_rat="","","","","","",""
        if (pag.locateCenterOnScreen(r"C:\code\anipang\images\bomb.png",confidence=0.78))!=None:
            qwe=(pag.locateCenterOnScreen(r"C:\code\anipang\images\bomb.png",confidence=0.78))
            pag.leftClick(qwe[0],qwe[1])

            
        
        field=[["" for j in range(7)] for i in range(7)] 

        for i in animal_name:
            globals()['animal_{}'.format(i)]=sameValueDel(list(pag.locateAllOnScreen(rf"C:\code\anipang\images\{i}.png",confidence=0.82)))#0.92
            

        #####필드와 리스트통합
        animal=animal_monkey+animal_bear+animal_cat+animal_chick+animal_pig+animal_rabbit+animal_rat#+animal_bomb
        if len(animal)==49:
            break
        else:
            for i in animal_name:
                if sameValueDel(list(pag.locateAllOnScreen(rf"C:\code\anipang\images\comb\{i}_comb.png",confidence=0.80)))!=None:
                    globals()['animal_{}'.format(i)].append(sameValueDel(list(pag.locateAllOnScreen(rf"C:\code\anipang\images\comb\{i}_comb.png",confidence=0.80))))
                    if len(animal)!=49:#0.92
                        print("인식오류")

                    else:
                        break
            
    #####필드에 무슨동물 어디인지 확실하게 정하기
    completeMakeField(animal)



    for row in range(7):
        for col in range(7):
            print(field[row][col][1][0],field[row][col][1][1],end=" ")
        print("\n")
    

    
    #1
    for y in range(7):
        for x in range(7):
                try:
                    if field[y][x][0]==field[y][x+1][0]:
                        
                        try:
                            if field[y][x][0]==field[y][x+3][0]:
                                shiftAnimal(field[y][x+3][1][0],field[y][x+3][1][1],field[y][x+2][1][0],field[y][x+2][1][1])
                        except:
                            pass
                        try:
                            if field[y][x][0]==field[y+1][x+2][0]:
                                shiftAnimal(field[y+1][x+2][1][0],field[y+1][x+2][1][1],field[y][x+2][1][0],field[y][x+2][1][1])
                        except:
                            pass
                        try:
                            if field[y][x][0]==field[y-1][x+2][0]:
                                shiftAnimal(field[y-1][x+2][1][0],field[y-1][x+2][1][1],field[y][x+2][1][0],field[y][x+2][1][1])
                        except:
                            pass
                except:
                    pass

        for x in range(7,0,-1):
                try:
                    if field[y][x][0]==field[y][x-1][0]:
                        
                        try:
                            if field[y][x][0]==field[y][x-3][0]:
                                shiftAnimal(field[y][x-3][1][0],field[y][x-3][1][1],field[y][x-2][1][0],field[y][x-2][1][1])
                        except:
                            pass
                        try:
                            if field[y][x][0]==field[y+1][x-2][0]:
                                shiftAnimal(field[y+1][x-2][1][0],field[y+1][x-2][1][1],field[y][x-2][1][0],field[y][x-2][1][1])
                        except:
                            pass
                        try:
                            if field[y][x][0]==field[y-1][x-2][0]:
                                shiftAnimal(field[y-1][x-2][1][0],field[y-1][x-2][1][1],field[y][x-2][1][0],field[y][x-2][1][1])
                        except:
                            pass
                except:
                    pass
    #2
    for x in range(7):
        for y in range(7):
                try:
                    if field[y][x][0]==field[y+1][x][0]:
                        
                        try:
                            if field[y][x][0]==field[y+3][x][0]:
                                shiftAnimal(field[y+3][x][1][0],field[y+3][x][1][1],field[y+2][x][1][0],field[y+2][x][1][1])
                        except:
                            pass
                        try:
                            if field[y][x][0]==field[y+2][x+1][0]:
                                shiftAnimal(field[y+2][x+1][1][0],field[y+2][x+1][1][1],field[y+2][x][1][0],field[y+2][x][1][1])
                        except:
                            pass
                        try:
                            if field[y][x][0]==field[y+2][x-1][0]:
                                shiftAnimal(field[y+2][x-1][1][0],field[y+2][x-1][1][1],field[y+2][x][1][0],field[y+2][x][1][1])
                        except:
                            pass
                except:
                    pass

        for y in range(7,0,-1):
            try:
                if field[y][x][0]==field[y-1][x][0]:
                    
                    try:
                        if field[y][x][0]==field[y-3][x][0]:
                            shiftAnimal(field[y-3][x][1][0],field[y-3][x][1][1],field[y-2][x][1][0],field[y-2][x][1][1])
                    except:
                        pass
                    try:
                        if field[y][x][0]==field[y-2][x+1][0]:
                            shiftAnimal(field[y-2][x+1][1][0],field[y-2][x+1][1][1],field[y-2][x][1][0],field[y-2][x][1][1])
                    except:
                        pass
                    try:
                        if field[y][x][0]==field[y-2][x-1][0]:
                            shiftAnimal(field[y-2][x-1][1][0],field[y-2][x-1][1][1],field[y-2][x][1][0],field[y-2][x][1][1])
                    except:
                        pass
            except:
                pass

    for y in range(7):
        for x in range(7):
            try:
                if (field[y][x][0]==field[y][x+2][0]) and (field[y][x][0]==field[y+1][x+1][0]):
                    shiftAnimal(field[y+1][x+1][1][0],field[y+1][x+1][1][1],field[y][x+1][1][0],field[y][x+1][1][1])
            except:
                pass
            try:
                if (field[y][x][0]==field[y][x+2][0]) and (field[y][x][0]==field[y-1][x+1][0]):
                    shiftAnimal(field[y-1][x+1][1][0],field[y-1][x+1][1][1],field[y][x+1][1][0],field[y][x+1][1][1])
            except:
                pass

    for x in range(7):
        for y in range(7):
            try:
                if (field[y][x][0]==field[y+2][x][0]) and (field[y][x][0]==field[y+1][x+1][0]):
                    shiftAnimal(field[y+1][x+1][1][0],field[y+1][x+1][1][1],field[y+1][x][1][0],field[y+1][x][1][1])
            except:
                pass
            try:
                if (field[y][x][0]==field[y+2][x][0]) and (field[y][x][0]==field[y+1][x-1][0]):
                    shiftAnimal(field[y+1][x-1][1][0],field[y+1][x-1][1][1],field[y+1][x][1][0],field[y+1][x][1][1])
            except:
                pass


    field.clear()
