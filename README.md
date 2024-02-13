# Anipang_Macro


- 프로젝트 개요 : 파이썬을 활용하여 직접 클릭하지 않아도 자동으로 애니팡 매크로 구현

- 개발기간 : 2022.12 ~ 2023.01 



## Images



https://github.com/kdhqwe1030/Anipang_macro/assets/115572203/556b4947-d271-49f6-94cc-6712942da012


## Features
- 애니팡 오토 프로젝트 1때 사진을 통한 이미지 인식으로 매크로를 작성했을 때 많은 오류가 있었기 때문에 이미지 인식이 아닌 화면의 rgb 값을 추출하여 범주 내에 색깔 분류로 작성함.
- 하지만 어떠한 점으로 했을 때 rgb 추출하는 좌표의 미세한 변동 차이로 인해 똑같이 오류의 범주들이 많이 생김. ->이와 같은 오류들을 해결하기 위해 애니팡 한 칸 안의 rgb 값을 평균을 내서 오차를 줄임.
- 애니팡 오토 프로젝트 1때 무수하게 많은 for문을 통해 맞추는 로직을 완성했다면, 2에서는 case를 통해 코드의 간결화와 가독성을 높였다.

- 활성화된 윈도우 창을 인식하여 필요한 필드 부분을 캡쳐

  
```
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
```

  
- 7*7 필드 배열에 각각 동물의 마우스 좌표와 한 칸 안의 rgb값 평균을 이용하여 rgb값 분류를 입력

```
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
```


- 같은 종류의 동물 3개가 한 직선상에 놓인 경우를 구별하는 로직

```
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
```

    
- 조건을 만족했을 때 매크로를 이용하여 동물을 이동하여 점수 획득
```
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
```



## library


- ctypes 
- PIL 
- win32gui
- win32api
- win32con
- pyautogui
- time
- numpy


## learn more


- 더 많은 라이브러리 사용과 다른 로직의 사용으로 이미 한번 시도해보았던 프로젝트의 단점들을 보완하고 목적 수준의 완성도에 도달한 것이 많은 성취감을 주었고 앞으로도 더 많은 프로젝트 들을 시도할 수 있는 발판이 되었다.

  
- 사용하지 않은 라이브러리들을 거치게 되고 잦은 오류에 검색하며 배울 점이 많았다.


- 코드를 작성하기 전 구상 부분의 중요성을 더욱더 느낄 수 있게 되었다. 예상되는 오류를 구상하는 과정에서보다 더 많은 오류가 생기면서 프로젝트를 만드는 시간이 길어지고 집중도가 떨어지는 경우에서  느낄 수 있었다.
  
