import flet as ft
import random,time,DialogWindow
class MyButton(ft.Container):
    def __init__(self, mine:bool, num:str|int, pox:tuple, vis:bool, flagged:bool):
        super().__init__()
        self.res=ft.Ref[ft.Container]()
        if flagged:
            self.content=ft.Card(
                content=ft.Container(
                    ref=self.res,
                    content=ft.Icon(ft.icons.FLAG_ROUNDED),
                    on_click=self.check,
                    on_long_press=self.check,
                    ink=True,
                    border_radius=10,
                    alignment=ft.alignment.center
                ),
            )
        else:
            self.content=ft.Card(
                content=ft.Container(
                    ref=self.res,
                    content=ft.Icon(ft.icons.QUESTION_MARK_ROUNDED),
                    on_click=self.check,
                    on_long_press=self.check,
                    ink=True,
                    border_radius=10,
                    alignment=ft.alignment.center
                ),
            )
        self.flagged=flagged
        self.pos=pox
        self.num=num
        self.bomb=mine
        self.width=10
        self.height=10
        if vis:
            self.res.current.on_click=None
            self.res.current.on_long_press=None
            self.res.current.content=ft.Text('' if self.num==0 else self.num, text_align=ft.TextAlign.CENTER, color=self.num_to_col(self.num), scale=1.3)
            open_land[self.pos[0]][self.pos[1]]=1
        
    def num_to_col(self,num):
        match num:
            case 1:
                return ft.colors.LIGHT_BLUE
            case 2:
                return ft.colors.LIGHT_GREEN
            case 3:
                return ft.colors.RED_ACCENT
            case 4:
                return ft.colors.BLUE
            case 5:
                return ft.colors.GREEN
            case 6:
                return ft.colors.RED
            case 7:
                return ft.colors.PURPLE
            case 8:
                return ft.colors.DEEP_PURPLE
            
    def check(self,e):
        global loose
        if (time.time()-time_s):
            if toggel.value:
                if self.flagged:
                    open_land[self.pos[0]][self.pos[1]]=0
                else: open_land[self.pos[0]][self.pos[1]]=2
                minesweeper_grid.controls=update_land()
                minesweeper_grid.update()
            elif not self.flagged:
                if self.bomb:
                    self.res.current.on_click=None
                    self.res.current.on_long_press=None
                    self.res.current.content=ft.Image(
                                                src=f"/bomb.svg",
                                                scale=0.5,
                                                color=ft.colors.RED)
                    self.update()
                    loose()
                else:
                    self.res.current.on_click=None
                    self.res.current.on_long_press=None
                    self.res.current.content=ft.Container(ft.Text('' if self.num==0 else self.num, style=ft.TextStyle()),alignment=ft.alignment.center)
                    open_land[self.pos[0]][self.pos[1]]=1
                    minesweeper_grid.controls=update_land()
                    minesweeper_grid.update()

class togg(ft.Container): #Inspired by ToggleSwitch from fletmint
    def __init__(self):
        super().__init__(
            width=133,
            height=45,
            bgcolor="#1b1d22",
            padding=ft.padding.all(5),
            border=ft.border.all(1, "#494D5F"),
            border_radius=10,
        )
        self.value = 0
        self.content = ft.Row(
            controls=[self.cont(ft.icons.ADS_CLICK_ROUNDED, self.value == 0), self.cont(ft.icons.FLAG_ROUNDED, self.value == 1)],
        )

    def cont(self, a, b):
        return ft.Container(
            content=ft.Icon(
                a,
                size=20,
                color="#c3c3c8" if b else "#494D5F",
            ),
            width=55,
            bgcolor="#333742" if b else "",
            border_radius=5,
            alignment=ft.alignment.center,
            on_click=self.toggle,
        )

    def toggle(self, e):
        self.value = 0 if self.value == 1 else 1
        self.content.controls[0] = self.cont(ft.icons.ADS_CLICK_ROUNDED, self.value == 0)
        self.content.controls[1] = self.cont(ft.icons.FLAG_ROUNDED, self.value == 1)
        self.update()

def add_list(list:list,x,y,xy):
    if x>=0 and y>=0:
        try:
            if list[y][x]!=-1:
                list[y][x]+=1
        except:
            return None
    
def add_open_list(list:list,x,y,xy):
    if x>=0 and y>=0:
        global land
        try:
            if land[y][x]==0 and list[y][x]==0:
                list[y][x]=1
                add_open_list(list, x-1, y, (x,y))
                add_open_list(list, x+1, y, (x,y))
                add_open_list(list, x+1, y+1, (x,y))
                add_open_list(list, x-1, y+1, (x,y))
                add_open_list(list, x, y+1, (x,y))
                add_open_list(list, x+1, y-1, (x,y))
                add_open_list(list, x-1, y-1, (x,y))
                add_open_list(list, x, y-1, (x,y))
            else:
                list[y][x]=1
        except:
            return None

def add_bomb_around(land,x,y):
        add_list(land, x-1, y, (x,y))
        add_list(land, x+1, y, (x,y))
        add_list(land, x+1, y+1, (x,y))
        add_list(land, x-1, y+1, (x,y))
        add_list(land, x, y+1, (x,y))
        add_list(land, x+1, y-1, (x,y))
        add_list(land, x-1, y-1, (x,y))
        add_list(land, x, y-1, (x,y))
    
def sm(page,row):
    game_init(page,row)


def main(page: ft.Page):
    global loose,game_init
    page.clean()
    
    def restt(e):
        sm(page,rowss)
    
    def loose():
        page.dialog=DialogWindow.DialogWindow(title="You lose!",title_alignment=ft.alignment.center,actions=[ft.TextButton("Restart",on_click=restt),ft.TextButton("Main menu",on_click=lambda e: main(page))])
        page.update()
        page.dialog.show()

    def game_init(page: ft.Page,rows):
        global rowss,land,open_land
        page.clean()
        rowss=rows
        match rows:
            case 5:
                page.title="Minesweeper 5x5 (5 bomb)"
                page.window_width=460
                page.window_height=544
            case 10:
                page.title="Minesweeper 10x10 (10 bomb)"
                page.window_width=512
                page.window_height=600
            case 15:
                page.title="Minesweeper 15x15 (15 bomb)"
                page.window_width=610
                page.window_height=705
        page.update()
        land=[[0 for _ in range(rowss)] for _ in range(rowss)]
        open_land=[[0 for _ in range(rowss)] for _ in range(rowss)]
        #gen bombs
        p=0
        while p<rowss:
            i=random.randint(0,rowss-1)
            j=random.randint(0,rowss-1)
            if land[i][j]!=-1:
                land[i][j]=-1
                add_bomb_around(land,j,i)
                p+=1                
        def update_open_land():
            global land,open_land
            ll=open_land
            y=0
            for i in ll:
                x=0
                for j in i:
                    if j == 1 and land[y][x]==0:
                        add_open_list(ll, x-1, y, (x,y))
                        add_open_list(ll, x+1, y, (x,y))
                        add_open_list(ll, x+1, y+1, (x,y))
                        add_open_list(ll, x-1, y+1, (x,y))
                        add_open_list(ll, x, y+1, (x,y))
                        add_open_list(ll, x+1, y-1, (x,y))
                        add_open_list(ll, x-1, y-1, (x,y))
                        add_open_list(ll, x, y-1, (x,y))
                    x+=1
                y+=1
            return ll
        def check_win():
            global open_land
            res=0
            for i in open_land:
                for j in i:
                    if j == 0 or j==2:
                        res+=1
            if res<=rowss:
                return True
            return False
        
        def flgandvis(num):
            match num:
                case 0:
                    return False,False
                case 1:
                    return True,False
                case 2: return False,True
            
        #create buttons
        global update_land
        def update_land():
            global open_land,land
            res=[]
            y=0
            open_land=update_open_land()
            if check_win():
                page.dialog=DialogWindow.DialogWindow(title="You win!",title_alignment=ft.alignment.center,content=ft.Container(ft.Text(f"Time spent: {round(time.time()-time_s,2)}s\nMode: {rowss}x{rowss}"),padding=10),actions=[ft.TextButton("Restart",on_click=restt),ft.TextButton("Main menu",on_click=lambda e: main(page))])
                page.update()
                page.dialog.show()
            else:
                for i in land:
                    x=0
                    for j in i:
                        b,h=flgandvis(open_land[y][x])
                        a=MyButton(True if j ==-1 else False,j,(y,x), b, h)
                        res.append(a)
                        x+=1
                    y+=1
                return res
        aa=update_land()
        global minesweeper_grid,toggel
        minesweeper_grid=ft.GridView(controls=aa,
            expand=1,
            runs_count=rowss,
            child_aspect_ratio=1.0,
            spacing=2,
            run_spacing=1,
            padding=5
        )
        toggel=togg()
        page.add(minesweeper_grid,toggel)
        page.update()
        global time_s
        time_s=time.time()
    
    page.window_center()
    page.window_width=500
    page.window_height=500
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.title="Minesweeper"
    page.window_maximizable=False
    page.window_full_screen=False
    page.window_resizable=False
    page.padding=5
    page.dialog=DialogWindow.DialogWindow(title="Minesweeper",title_alignment=ft.alignment.center,actions=[ft.TextButton("5x5",on_click=lambda e:sm(page,5)),ft.TextButton("10x10",on_click=lambda e:sm(page,10)),ft.TextButton("15x15",on_click=lambda e:sm(page,15))])
    page.update()
    page.dialog.show()
    page.update()

ft.app(main,name="Minesweeper",assets_dir="assets")
