import time
import flet as ft
class DialogWindow(ft.UserControl):
    def __init__(self,
                 width=400,
                 mode_theme = ft.ThemeMode.DARK,
                 actions=[],
                 actions_alignment = ft.MainAxisAlignment.CENTER,
                 content=None,
                 content_padding = 10,
                 content_alignment = ft.alignment.center,
                 title='Dialog',
                 title_alignment=ft.alignment.top_left,
                 title_padding = 20,
                 title_size = 25,
                 bgcolor_dialog_dark = 'black,0.2',
                 bgcolor_dialog_light = 'white,0.8',
                 blur_size = [5,5]
                 ):
        super().__init__()
        self.dialog_width = width
        self.actions = actions
        self.actions_alignment = actions_alignment
        self.content = content
        self.content_alignment = content_alignment
        self.content_padding = content_padding
        self.title_text = title
        self.title_alignment = title_alignment
        self.title_padding = title_padding
        self.title_size = title_size
        self.bgcolor_dialog_dark = bgcolor_dialog_dark
        self.bgcolor_dialog_light = bgcolor_dialog_light
        self.content_height_ = None
        self.blur_size = blur_size
        self.mode_theme = mode_theme

    
    def close_alert_window(self,e,action=None):
        def close_alert(e):
            self.page.dialog = None
            self.page.update()
        if action!=None:
            action('f')
        try:
            self.dialog_window.top = self.page.window_height/3
            self.dialog_window.opacity = 0
            self.dialog_window.update()
            self.dialog_area.opacity = 0
            self.dialog_area.on_animation_end = close_alert
            self.dialog_area.update()
            close_alert('')
        except:
            pass

        

    def show(self):
        time.sleep(0.05)
        self.dialog_area.opacity = 1
        self.dialog_area.update()
        self.dialog_window.top = (self.page.window_height/3.5)
        self.dialog_window.opacity = 1
        self.dialog_window.update()
        

    def create_alert_window(self):

        def content_for_dialog():
            return self.content

        def title_and_actions():
            title = ft.Container(ft.Text(self.title_text,size=self.title_size),padding=self.title_padding,alignment=self.title_alignment)
            actions = ft.TextButton(text='OK',width=200,height=50,on_click=self.close_alert_window)
            temporal_action = []
            if self.actions:
                for action in self.actions:
                    temporal_action.append(action.on_click)
                for i,action in enumerate(self.actions):
                    action.on_click = lambda e, i=i: self.close_alert_window(action=temporal_action[i],e=e) 
                actions = ft.Row(self.actions)
            
            
            container = ft.Container(actions,alignment=ft.alignment.bottom_center,height=50)
            row = ft.Column(
                [
                    title,
                    
                    ft.Container(expand=False,content=content_for_dialog(),alignment=self.content_alignment,padding=self.content_padding), #whole content
                    
                    ft.Container(
                                    padding=20,content=ft.Row(
                                    [container],alignment=self.actions_alignment)
                                )
                 ])

            content = row
            return content

        self.dialog_window = ft.Container(width=self.dialog_width,
                                    border_radius=20,
                                    content=title_and_actions(),
                                    bgcolor=self.bgcolor_dialog_dark if self.mode_theme==ft.ThemeMode.DARK else self.bgcolor_dialog_light,
                                    border=ft.border.all(1,'white,0.1'),
                                    top=self.page.window_height/2,
                                    expand=False,
                                    opacity=0,
                                    animate_position=ft.animation.Animation(400,curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT),
                                    animate_opacity=ft.animation.Animation(400,curve=ft.AnimationCurve.EASE_IN_OUT),
                                    )

        self.dialog_window_stack = ft.Stack([self.dialog_window],width=self.dialog_width)
                              

        self.dialog_area = ft.Container(
            width=self.page.window_width,height=self.page.window_height,bgcolor='black,0.5',expand=False,opacity=0,
                                    blur=ft.Blur(self.blur_size[0], self.blur_size[1], ft.BlurTileMode.REPEATED),
                                    content=self.dialog_window_stack,
                                    alignment=ft.alignment.center,
            animate_opacity=ft.animation.Animation(200,curve=ft.AnimationCurve.EASE_IN_OUT),
            )


    def build(self):
        self.create_alert_window()
        return self.dialog_area