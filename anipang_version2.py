from ctypes import windll, wintypes, byref, sizeof
from PIL import ImageGrab
import win32gui
import win32api
import win32con
import pyautogui as pag
import time
import numpy as np 
BLACK,BLUE,WHITE,GRAY,BROWN,PINK,YELLOW,GREEN=['black','blue','white','gray','brown','pink','yellow','green']


def _get_background_image():
    time.sleep(2)
    global img
    global X0,Y0,X1,Y1
    global pix
    def _get_window_rect(hwnd):
        f = windll.dwmapi.DwmGetWindowAttribute
        rect = wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(wintypes.HWND(hwnd),
        wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        byref(rect),
        sizeof(rect)
        )
        return rect.left, rect.top, rect.right, rect.bottom
        
    handle = win32gui.GetForegroundWindow()
    x0,y0,x1,y1=_get_window_rect(handle)
    X0,Y0,X1,Y1=x0,y0+(y1-y0)/4+20,x1-35,y1-(y1-y0)/5+10+0.4
    X0,Y0,X1,Y1=int(X0),int(Y0),int(X1),int(Y1)
    img = ImageGrab.grab((X0,Y0,X1,Y1))
    img.save("save.png")
    pix=np.array(img)
    #print(img.size)

def make_martrix():
    color_martrix=[[0 for i in range(7)]for j in range(7)]
    for i in range(32,480,64):
        for j in range(32,480,64):
         I,J=i//64,j//64    
         color_martrix[I][J]=[X0+i,Y0+j]  #밑에줄에넣기
         color_martrix[I][J]=[color_martrix[I][J],sum(I*64,J*64)]
    return color_martrix
    
def sum(a,b):
    sum_r=0
    sum_b=0
    sum_g=0
    for i in range(a,a+64):
        for j in range(b,b+64):
            sum_r+=pix[i][j][0]
            sum_b+=pix[i][j][1]
            sum_g+=pix[i][j][2]
    average=[sum_r//4096,sum_b//4096,sum_g//4096]
    return get_color_name(average)
def get_color_name(rgb):
    r,g,b=rgb
    # if (r<100) and (g<70) and (b<50):
    #     return BLACK
    if (10<r<30) and (80<b<120) and (90<b<120):
        return BLUE
    if (100<r<130) and (100<g<130) and (100<b<130):
        return WHITE
    if (60<r<90) and (70<g<100) and (80<b<110):
        return GRAY
    if (100<r<120) and (60<g<90) and (40<b<70):
        return BROWN
    if (130<r<150) and (65<g<95) and (70<b<100):
        return PINK
    if (120<r<140) and (80<g<110) and (20<b<55):
        return YELLOW
    if (60<r<90) and (90<g<130) and (b<60):
        return GREEN
    
    return None
    

    
    
def get_move_info(color_matrix,i,j):
    result=None
    cases=[
        [ (i+0, j+0),(i+0, j+2),(i+0, j+3),1,"down"]
        ,[ (i+0, j+0),(i+0, j+1),(i+0, j+3),3,"up"]
        ,[ (i+0, j+0),(i+1, j+1),(i+1, j+2),1,"right"]
        ,[ (i+0, j+0),(i-1, j+1),(i-1, j+2),1,"left"]
        ,[ (i+0, j+0),(i+1, j-1),(i+1, j+1),1,"right"]
        ,[ (i+0, j+0),(i+1, j+1),(i+0, j+2),2,"left"]
        ,[ (i+0, j+0),(i+1, j-2),(i+1, j-1),1,"right"]
        ,[ (i+0, j+0),(i+0, j+1),(i+1, j+2),3,"left"]

        ,[ (i+0, j+0),(i+2, j+0),(i+3, j+0),1,"right"]
        ,[ (i+0, j+0),(i+1, j+0),(i+3, j+0),3,"left"]
        ,[ (i+0, j+0),(i+1, j+1),(i+2, j+1),1,"down"]
        ,[ (i+0, j+0),(i+1, j-1),(i+2, j-1),1,"up"]
        ,[ (i+0, j+0),(i+1, j-1),(i+2, j+0),2,"down"]
        ,[ (i+0, j+0),(i+1, j+1),(i+2, j+0),2,"up"]
        ,[ (i+0, j+0),(i+1, j+0),(i+2, j-1),3,"down"]
        ,[ (i+0, j+0),(i+1, j+0),(i+2, j+1),3,"up"]
    ]

    for case in cases:
        try:
            result=None
            pos1,pos2,pos3,sel_pos,direction=case
            ani1= color_matrix[pos1[1]][pos1[0]][1]
            ani2= color_matrix[pos2[1]][pos2[0]][1]
            ani3= color_matrix[pos3[1]][pos3[0]][1]
            if (ani1 == ani2) and (ani2  == ani3) and ani1!=None:
                if pos1[1]>-1 and pos1[0]>-1 and pos2[0]>-1 and pos2[1]>-1 and pos3[0]>-1 and pos3[1]>-1:
                    result=case
                    print(ani1,ani2,ani3)
                    break
                    
        except:
            continue
    if result!=None:
        print(result,i,j)
    return result   


def mouse_click(case,color_martrix):
    # print(case)
    # print(case[case[3]-1])
    i,j=case[case[3]-1]
    if i>6 or j>6:
        return 
    x,y=color_martrix[i][j][0]
    x,y=int(x),int(y)
    pag.moveTo(x,y)
    if case[4]=='right':
        x2,y2=x+64,y
    elif case[4]=='up':
        x2,y2=x,y-64
    elif case[4]=='down':
        x2,y2=x,y+64
    elif case[4]=='left':
        x2,y2=x-64,y
    pag.dragTo(x2,y2,0.2,button='left')

def make_candy(color_martrix):
    move_cands=[]
    move_info=None
    for i in range(7):
        for j in range(7):
            move_info=get_move_info(color_martrix,i,j)
            if move_info!=None:
                print(move_info)
            if move_info:
                move_cands.append(move_info)
    
    return move_cands


def main():
    while True:
        print("#########################################")
        if pag.locateOnScreen(r"anipang2\end.png")!=None:
            break
        _get_background_image()
        
        color_martrix=make_martrix()
        end=0
        for i in range(7):
            for j in range(7):
                if color_martrix[i][j][0]=='black':
                    pag.leftClick(color_martrix[i][j][0][0],color_martrix[i][j][0][1])
                    end=1
                    break
        if end==1:
            continue
            

            
        List=make_candy(color_martrix)

        
        for List_info in List:
            try:
                if pag.locateOnScreen(r"anipang2\end.png")!=None:
                     break               
                mouse_click(List_info,color_martrix)
            except:
                continue
    
    print("종료")

                

main()