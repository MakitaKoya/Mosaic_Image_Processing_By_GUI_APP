import tkinter as tk
import customtkinter
import os
from PIL import Image
import cv2

from lib import RGB_mean as RGB
from lib import triangle_mask_mean as TMM
from lib import rect_mask_mean as RMM
from lib import hex_mask_mean as HMM
from lib import super_pixel as SP

FONT_TYPE = "meiryo"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.fonts = (FONT_TYPE, 15)
        self.img_filepath = None

        self.setup_form()
    
    def setup_form(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.geometry("1000x600")
        self.title("MOSAIC IMAGE PROCESSING")
        self.minsize(400,300)

        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.read_file_frame = ReadFileFrame(master=self,header_name="ファイル読み込み")
        self.read_file_frame.grid(row=0,column=0,padx=20,pady=20,sticky="ew")

        self.image_proc_main = ImageProcFrame(master=self,header_name="画像処理")
        self.image_proc_main.grid(row=1,column=0,padx=20,pady=20,sticky='news')

class ReadFileFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="ReadFileFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE,15)
        self.header_name = header_name

        self.setup_form()

    def setup_form(self):
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.label = customtkinter.CTkLabel(self,
                                            text=self.header_name,
                                            font=(FONT_TYPE,11))
        self.label.grid(row=0,column=0,padx=20,sticky="w")

        self.textbox = customtkinter.CTkEntry(master=self,
                                              placeholder_text="画像ファイルを読み込む",
                                              width=120,
                                              font=self.fonts)
        self.textbox.grid(row=1,column=0,padx=10,pady=(0,10),sticky="ew")

        self.button_select = customtkinter.CTkButton(master=self,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     text_color=("gray10","#DCE4EE"),
                                                     command=self.button_select_callback,
                                                     text="ファイル選択",
                                                     font=self.fonts)
        self.button_select.grid(row=1,column=1,padx=10,pady=(0,10))

        self.button_open = customtkinter.CTkButton(master=self,
                                                   command=self.button_open_callback,
                                                   text="開く",
                                                   font=self.fonts)
        self.button_open.grid(row=1,column=2,padx=10,pady=(0,10))

    def button_select_callback(self):
        file_name = ReadFileFrame.file_read()

        if file_name is not None:
            self.textbox.delete(0,tk.END)
            self.textbox.insert(0,file_name)

    def button_open_callback(self):
        file_name = self.textbox.get()
        if (file_name is not None) and (len(file_name) != 0):
            self.master.image_proc_main.input_img(file_name)
        else:
            tk.messagebox.showinfo("確認", f"画像を選択してください。")

    @staticmethod
    def file_read():
        current_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = tk.filedialog.askopenfilename(filetypes=[("動画像ファイル","*.png;*.jpg;*.jpeg;*.mp4")],initialdir=current_dir)

        if len(file_path) != 0:
            return file_path
        else:
            return None
        
class ImageProcFrame(customtkinter.CTkFrame):
    def __init__(self,*args,header_name="ImageProcFrame",**kwargs):
        super().__init__(*args,**kwargs)

        self.fonts = (FONT_TYPE,15)
        self.header_name = header_name

        self.setup_form()
    
    def setup_form(self):
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.setting = SettingFrame(master=self,header_name="画像処理設定")
        self.setting.grid(row=0,column=0,padx=10,pady=20,sticky='ns')

    def show_img(self,frame):
        func = self.setting.func_menu.get()
        if func == 'rgb_mean':
            R_value = self.setting.R_value.get()
            G_value = self.setting.G_value.get()
            B_value = self.setting.B_value.get()
            proc_img = RGB.main(frame,R_value,G_value,B_value)

        else:
            value = self.setting.sliderValue
            if func == 'triangle_mask_mean':
                proc_img = TMM.main(frame,value*10)
            elif func == 'rect_mask_mean':
                proc_img = RMM.main(frame,value*10)
            elif func == 'hex_mask_mean':
                proc_img = HMM.main(frame,value*10)
            elif func == 'super_pixel':
                proc_img = SP.main(frame,value*100)

        img = cv2.cvtColor(proc_img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.proc_image = customtkinter.CTkImage(img,size=(640,480))
        self.proc_img_show = customtkinter.CTkLabel(self,image=self.proc_image,text="")
        self.proc_img_show.grid(row=0,column=1,padx=10,pady=20,sticky="ns")

    def input_img(self,file_path=None):
        file_path = self.master.read_file_frame.textbox.get()
        if hasattr(self, 'capture'):
            self.capture.release()
            self.after_cancel(self.update_id) 
        self.capture = cv2.VideoCapture(file_path)
        if not self.capture.isOpened():
            raise IOError("can't open capture!")
        self.update()
    
    def update(self):
        ret,frame = self.capture.read()
        if ret:
            self.show_img(frame)
            self.old_frame = frame
            self.update_id = self.after(50, self.update)
        else:
            self.capture.release()
        
    

class SettingFrame(customtkinter.CTkFrame):
    def __init__(self,*args,header_name="SettingFrame",**kwargs):
        super().__init__(*args,**kwargs)

        self.fonts = (FONT_TYPE,15)
        self.header_name = header_name

        self.setup_form()
    
    def setup_form(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0,weight=1)

        self.label = customtkinter.CTkLabel(self,text=self.header_name,font=(FONT_TYPE,11))
        self.label.grid(row=0,column=0,padx=20,sticky='nw')

        # 機能の選択
        self.menu_label = customtkinter.CTkLabel(self,text="画像処理関数の選択",font=(FONT_TYPE,13))
        self.menu_label.grid(row=1,column=0,padx=20,pady=(20,0),sticky='ew')

        self.func_menu = customtkinter.CTkOptionMenu(master=self,
                                                     values=['rgb_mean','triangle_mask_mean','rect_mask_mean','hex_mask_mean','super_pixel'],
                                                     command=self.change_fanction)
        self.func_menu.grid(row=2,column=0,padx=20,pady=(0,20),sticky='ew')

        # 模様の細かさの設定用スライドバー
        self.slider_label = customtkinter.CTkLabel(self,text="模様の細かさ:5",font=(FONT_TYPE,13))
        self.slider_label.grid(row=3,column=0,padx=20,pady=(20,0),sticky='ew')

        self.mask_slider = customtkinter.CTkSlider(master=self,
                                                   from_=1,
                                                   to=10,
                                                   number_of_steps=9,
                                                   hover=False,
                                                   width=150,
                                                   command=self.slider_event)
        self.mask_slider.grid(row=4,column=0,padx=20,pady=(0,20),sticky='ew')

        self.sliderValue = 30

        # 初期状態ではスライダーは非表示にしておく
        self.slider_label.grid_remove()
        self.mask_slider.grid_remove()

        # RGB各色平均の選択用チェックボックス
        self.R_value = tk.BooleanVar()
        self.G_value = tk.BooleanVar()
        self.B_value = tk.BooleanVar()

        self.RGB_checkbox_label = customtkinter.CTkLabel(self,text="RGB各色平均化",font=(FONT_TYPE,13))
        self.RGB_checkbox_label.grid(row=3,column=0,padx=20,pady=(20,0),sticky='ew')

        self.R_checkbox = customtkinter.CTkCheckBox(master=self,
                                                    text="R 平均化",
                                                    command=self.checkbox_event,
                                                    variable=self.R_value)
        self.R_checkbox.grid(row=4,column=0,padx=20,pady=(10,0),sticky='ew')

        self.G_checkbox = customtkinter.CTkCheckBox(master=self,
                                                    text="G 平均化",
                                                    command=self.checkbox_event,
                                                    variable=self.G_value)
        self.G_checkbox.grid(row=5,column=0,padx=20,pady=10,sticky='ew')
        
        self.B_checkbox = customtkinter.CTkCheckBox(master=self,
                                                    text="B 平均化",
                                                    command=self.checkbox_event,
                                                    variable=self.B_value)
        self.B_checkbox.grid(row=6,column=0,padx=20,pady=(0,20),sticky='ew')

    def change_fanction(self,choice):
        if choice == 'rgb_mean':
            self.slider_label.grid_remove()
            self.mask_slider.grid_remove()

            self.RGB_checkbox_label.grid()
            self.R_checkbox.grid()
            self.G_checkbox.grid()
            self.B_checkbox.grid()
        else:
            self.RGB_checkbox_label.grid_remove()
            self.R_checkbox.grid_remove()
            self.G_checkbox.grid_remove()
            self.B_checkbox.grid_remove()

            self.slider_label.grid()
            self.mask_slider.grid()
        self.master.show_img(self.master.old_frame)
    
    def slider_event(self, value):
        self.sliderValue = int(value)
        old_label = self.slider_label.cget("text")
        new_label = f"模様の細かさ:{self.sliderValue}"
        if old_label != new_label:
            self.slider_label.configure(text=new_label)
            self.master.show_img(self.master.old_frame)

    def checkbox_event(self):
        self.master.show_img(self.master.old_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
