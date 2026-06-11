import random
import tkinter as tk
from tkinter import messagebox,ttk
#board kamelan khali ba sefr
lst = [[0]*4 for _ in range(4)]
#zakhire kardan emtiaz lahze 
high_score = 0  
def update_score():
    global high_score  
    current_max = max(max(row) for row in lst)  
    #taghir bishtarin emtiaz dar sorat lazem
    if current_max > high_score:
        high_score = current_max  
    return high_score
#tabe shoro bazi
def start_game():
    rand()
    rand()
    update_ui()
#tabe ezafe kardan adad tasadofi 2 ya 4
def rand():
    global lst
    has_zero = False 
    for t in lst:
        if 0 in t:
            has_zero = True
            break
    # agar 0 mojod bod adad tasadafi bezare
    if has_zero:
        while True:
            x = random.randint(0,3)
            y = random.randint(0,3)
            #darsorat fazaye khali ba adad tasadofi por konad (x,y)haman i,j dar matris ast
            if lst[x][y]==0:
                lst[x][y]=random.choices([2,4], weights=[9,1])[0]
                break

#-----------
def chap():
    global lst
    lst_n = []
    for i in lst:
        new = []
        #hazf kardan 0
        cop = i.copy()
        for _ in range(i.count(0)):
            cop.remove(0)
        o = 0
        #ejra ta ghabl as bishtar shodan index
        while o<len(cop):
            #shart barabari va vojod badi
            if o+1<len(cop) and cop[o]==cop[o+1]:
                new.append(cop[o]*2)
                o +=2
            else:
                new.append(cop[o])
                o+=1
        #por kardan faz az rast
        while len(new)<4:
            new.append(0)
        lst_n.append(new)
    # shart baraye inke taghir peyda karde ya na
    if lst!=lst_n:
        lst = lst_n
        return True
    return False
#---------
def rast():
    #baray hame function ha az function chap estefade mikonim
    #baraye rast daghighan baraks chap hast 
    global lst
    lst = [p[::-1] for p in lst]
    changed = chap()   
    lst = [p[::-1] for p in lst]
    return changed
#-------
def bala():
    #baraye function bala bayad ebteda satr soton ro avaz konim va bad az on dobare bargardonim
    global lst
    lst_f = [[lst[i][j] for i in range(4)] for j in range(4)]
    lst = lst_f
    changed = chap()   
    lst_f = [[lst[i][j] for i in range(4)] for j in range(4)]
    lst = lst_f
    return changed
#-------
def paeen():
    #baraye function chap daghighan khalaf bala ast vali bayad aval satr haro bar aks kard
    global lst
    lst = lst[::-1]                                   
    lst = [[lst[j][i] for j in range(4)] for i in range(4)]  
    changed = chap()                                 
    lst = [[lst[j][i] for j in range(4)] for i in range(4)]  
    lst = lst[::-1]                                 
    return changed

def gameover():
    global lst
    #agar sefri mojod bod hanoz bazi tamom nashode
    for i in lst:
        if 0 in i:
            return False
    #check kardan dar satr ha
    for i in range(4):
        for j in range(3):
            if lst[i][j]==lst[i][j+1]:
                return False
    #check kardan dar soton ha
    for i in range(3):
        for j in range(4):
            if lst[i][j]==lst[i+1][j]:
                return False
    #agar harkodam shart dorost nabod baz tamam mishavad
    return True


#----------------------------  gui ----------------------------
#dorost kardan fazaye khali
cells = [[None]*4 for _ in range(4)]
root = tk.Tk()
root.title("2048")
#karbar natone taghir bede size bazi ro
root.resizable(False, False)

#neshon dadan bishtarin emtiaz
score_label = tk.Label(root, text="", font=("Arial", 16, "bold"), 
                       fg="#4F4E4E")
score_label.pack()
#frame ya board makhsos 4x4
frame = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10)
#tabe baraye dokme retry baraye reset bazi
def retry():
    global lst
    #baraye etminan tamam label haye ghabli ro pak mikonim
    for widget in frame.winfo_children():
        widget.destroy()
    #riset kardan list va board toye mantegh bazi
    lst = [[0]*4 for _ in range(4)]
    make_first_board()
    start_game()
#dokme riset
butt = ttk.Button(root,text='retry',command=retry).pack()
frame.pack()
#sakhtan fazaye khali dar frame
def make_first_board():
    for i in range(4):
        for j in range(4):
            lbl = tk.Label(
                frame,
                text="",
                width=4,
                height=2,
                font=("Arial", 24, "bold"),
                bg="#cdc1b4"
            )
            lbl.grid(row=i, column=j, padx=5, pady=5)
            cells[i][j] = lbl
#seda zadan tabe
make_first_board()
#rang ha baraye har adad makhsos baraye zibayi
colors = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"}
def update_ui():
    #taghir dadn lable avalie dar sorat taghir bishtarin emtiaz
    score_label.config(text=f'bishtarin emtiaz:{str(update_score())}')
    for i in range(4):
        for j in range(4):
            v = lst[i][j]
            #rabet beyn gui va mantegh bazi agar deraye 0 bod text khali va deraye adad bod adad mored nazar
            if v == 0:
                cells[i][j].config(text="",bg="#cdc1b4")
            #rang har adad ra dar dictionery peyda karda va hardafe adad taghir kard rang niz taghir mikonad
            else:
                cells[i][j].config(text=str(v),bg=colors[v])
def key_handler(event):
    #dokme click karde ra be string ke lower shode taghir midim
    key = event.keysym.lower()
    moved = False
    if key == 'w':
        moved = bala()
    elif key == 's':
        moved = paeen()
    elif key == 'a':
        moved = chap()
    elif key == 'd':
        moved = rast()
    #agar harekat taghiri dar board anjam dad boar ro update karde va adad tasadofi ro miazarim
    if moved:
        rand()
        update_ui()
        #neshon dadan bord ya bakht bazi
        if update_score()==2048:
            messagebox.showinfo('2048','shoma bordid!')
            retry()
        elif gameover():
            messagebox.showinfo("2048", "shoma bakhtid!")

#click kardan keyboard
root.bind("<Key>", key_handler)
#shoro bazi
start_game()
#shoro halghe
root.mainloop()