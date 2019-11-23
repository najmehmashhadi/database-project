import tkinter as tk
from PIL import Image,ImageTk,ImageFilter,ImageEnhance
from tkinter import messagebox
#import csv
#import os
from tkinter import filedialog
#import redis
import time
#import json
#import numpy
#redis_host = "localhost"
#redis_port1 = 6379;redis_password1 =""
#redis_port2 = 6379;redis_password2 =""
#redis_port3 = 6379;redis_password3 =""
#redis_port4 = 6379;redis_password4 =""
#redis_port5 = 6379;redis_password5 =""
#dataset_address='D:/Najma_app'

from pysyncobj import SyncObj, SyncObjConf, replicated

def main_app_fun(node):
    num_user=node.get('num_user')
    time.sleep(0.5)
    if num_user is None: 
       node.set('num_user',0)
       time.sleep(0.5)
    main_app = tk.Tk()             
    main_app.title('Parsa')
    main_app.geometry("500x300")
    app=main_login_window(main_app,node)
#    main_frame.mainloop()
    return main_app

class KVStorage(SyncObj):
    def __init__(self, selfAddress, partnerAddrs):
        cfg = SyncObjConf(dynamicMembershipChange = True)
        super(KVStorage, self).__init__(selfAddress, partnerAddrs, cfg)
        self.__data = {}

    @replicated
    def set(self, key, value):
        self.__data[key] = value

    @replicated
    def pop(self, key):
        self.__data.pop(key, None)

    def get(self, key):
        return self.__data.get(key, None)

_g_kvstorage = None

class main_login_window():
    def __init__(self, master,dataset):
        self.dataset = dataset
        self.user_num_ID=' '
        self.master = master
        self.num_user=self.dataset.get('num_user')
        time.sleep(0.5)
        print(self.num_user)
        
        tk.Label(master=self.master, text='User ID').place(x=100, y=50)
        self.user_ID_entry = tk.Entry(self.master) 
        self.user_ID_entry.place(x=200, y=50)
        
        
        tk.Label(master=self.master, text='Password').place(x=100, y=100)
        self.password_entry = tk.Entry(self.master) 
        self.password_entry.place(x=200, y=100)
        
        
        tk.Button(master=self.master, text ="  Login  ", command = self.login_fun).place(x=190, y=150)
        
        tk.Button(master=self.master, text =" New User ", command = self.new_user_fun).place(x=290, y=150)
    

    def login_fun(self):
        user_info_requested=[self.user_ID_entry.get(),self.password_entry.get()]
        st=0
        print(self.num_user)
        for user_idx in range(1,self.num_user+1):
            user_info_list=self.dataset.get('user_'+str(user_idx))
            time.sleep(0.5)
            print(user_info_list)
            if(user_info_list[0]==user_info_requested[0]):
                if(user_info_list[1]==user_info_requested[1]):
                       st=1
                       break
        if(st==1):
           self.user_idx=user_idx
           self.edit_image_fun()
           
        else:
           messagebox.showinfo("Error", "The user ID or password you entered was incorrect.")
              
    def new_user_fun(self):
        self.master.destroy()
        
        userframe = tk.Tk()
        userframe.title('Parsa')
        userframe.geometry("500x500")
        app = user_frame_window(userframe,self.dataset)
    
    def edit_image_fun(self):
        self.master.destroy()
        
        image_edit_frame = tk.Tk()
        image_edit_frame.geometry("700x500")
        app = edit_image_window(image_edit_frame,self.user_idx,self.dataset)

class user_frame_window():
    def __init__(self, master,dataset):
        self.userframe = master
        self.dataset=dataset
        self.num_user=self.dataset.get('num_user')
        time.sleep(0.5)
        print(self.num_user)
        tk.Label(master=self.userframe, text='First Name').place(x=100, y=50)
        self.first_name_entry = tk.Entry(self.userframe) 
        self.first_name_entry.place(x=200, y=50)
        
        
        tk.Label(master=self.userframe, text='Last Name').place(x=100, y=100)
        self.last_name_entry = tk.Entry(self.userframe) 
        self.last_name_entry.place(x=200, y=100)
        
        tk.Label(master=self.userframe, text='Age').place(x=100, y=150)
        self.age_entry = tk.Entry(self.userframe) 
        self.age_entry.place(x=200, y=150)
        
        tk.Label(master=self.userframe, text='Job').place(x=100, y=200)
        self.job_entry = tk.Entry(self.userframe) 
        self.job_entry.place(x=200, y=200)
        
        tk.Label(master=self.userframe, text='User ID').place(x=100, y=250)
        self.user_ID_entry = tk.Entry(self.userframe) 
        self.user_ID_entry.place(x=200, y=250)
        
        tk.Label(master=self.userframe, text='Password').place(x=100, y=300)
        self.password_entry = tk.Entry(self.userframe) 
        self.password_entry.place(x=200, y=300)
    
    
        tk.Button(master=self.userframe, text ="  Create  ", command = self.create_fun).place(x=200, y=350)
        
    def create_fun(self):
        user_info_list = [self.user_ID_entry.get(),self.password_entry.get(),self.first_name_entry.get(), 
                   self.last_name_entry.get(),self.age_entry.get(),self.job_entry.get(),0]
        
#        print(user_info_list)
        self.num_user=self.num_user+1
#        print(self.num_user)
        self.dataset.set('num_user',self.num_user)
        time.sleep(0.5)
        self.dataset.set('user_'+str(self.num_user),user_info_list)
#        print(self.dataset.get('num_user'))
        time.sleep(0.5)
        self.userframe.destroy()
        main_app_fun(self.dataset)   


class edit_image_window():
    def __init__(self, master,user_idx,dataset):
        self.image_edit_frame = master
        self.dataset=dataset
        self.user_idx=user_idx
        self.user_info=self.dataset.get('user_'+str(user_idx))
        time.sleep(0.5)
        self.num_img=self.user_info[-1]
        self.image_edit_frame.title('Parsa -'+ self.user_info[0])
#        tk.Label(master=self.image_edit_frame, text="Hello"+self.ID).place(x=200, y=10)
        tk.Label(master=self.image_edit_frame, text='Image History').place(x=10, y=70)
        sub_frame = tk.Frame(self.image_edit_frame)
        sub_frame.place(x=10, y=100)
        self.mylist = tk.Listbox(sub_frame,width =12)
#        self.mylist.see(2)
        self.mylist.bind("<Double-Button-1>", self.list_image_callback)
#        self.mylist.bind('<<ListboxSelect>>', self.list_image_callback)
        #mylist.place(x=10, y=10)
        self.mylist.grid(row=0, column=1)
        
        scrollbar = tk.Scrollbar(sub_frame, orient="vertical")
        #scrollbar.place(x=200, y=30)
        scrollbar.grid(row=0, column=2, sticky='ns')
        #scrollbar.pack(side="right", fill="y")
        self.mylist.configure(yscrollcommand=scrollbar.set)
        #scrollbar.config(command=mylist.yview)
        #scrollbar.set(20,400)
        self.aupdate_list()
        scrollbar.config( command = self.mylist.yview )  
        tk.Label(master=self.image_edit_frame, text='Image Panel').place(x=180, y=70)
    
        tk.Button(master=self.image_edit_frame, text ="  My Profile  ", command = self.my_profile_fun).place(x=20, y=20)
        tk.Button(master=self.image_edit_frame, text ="  Log out    ", command = self.log_out_fun).place(x=130, y=20)
        
        tk.Button(master=self.image_edit_frame, text ="  Reset          ", command = self.reset_fun).place(x=530, y=50)
        tk.Button(master=self.image_edit_frame, text ="  Gray           ", command = self.gray_fun).place(x=530, y=100)
        tk.Button(master=self.image_edit_frame, text ="  Rotate        ", command = self.rotate_fun).place(x=530, y=150)
        tk.Button(master=self.image_edit_frame, text ="  Blur            ", command = self.blur_fun).place(x=530, y=200)
        tk.Button(master=self.image_edit_frame, text ="  Contrast     ", command = self.contrast_fun).place(x=530, y=250)
        tk.Button(master=self.image_edit_frame, text ="  Brightness  ", command = self.brightness_fun).place(x=530, y=300)
        tk.Button(master=self.image_edit_frame, text ="  Sharpness   ", command = self.sharpness_fun).place(x=530, y=350)
        tk.Button(master=self.image_edit_frame, text ="  Edges          ", command = self.edges_fun).place(x=530, y=400)
        
        tk.Button(master=self.image_edit_frame, text ="  Load  ", command = self.load_fun).place(x=250, y=420)
        tk.Button(master=self.image_edit_frame, text ="  Save  ", command = self.save_fun).place(x=350, y=420)
        
        self.img=Image.open("image5.jpg")
        self.img=self.img.resize((300,300),Image.ANTIALIAS)
        self.img_r=self.img
#        aa=list(self.img.getdata())
#        print(aa[1:5])
        img_size=self.img.size
        img_tk=ImageTk.PhotoImage(self.img)
        
        self.canvas = tk.Canvas(self.image_edit_frame, width = img_size[0], height = img_size[1])
        
        self.canvas.place(x=180, y=100)
        
        self.image_on_canvas=self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
        self.image_edit_frame.mainloop()
    
    def aupdate_list(self):
        self.mylist.delete(0,tk.END)
        
        for img_idx in range(1,self.num_img+1):
           self.mylist.insert(tk.END,'image_'+str(img_idx))
           
        
          
    def my_profile_fun(self):
        user_profile = tk.Tk()
        user_profile.title('Parsa')
        user_profile.geometry("500x500")
        app = my_profile_window(user_profile,self.dataset,self.user_idx)  
    def list_image_callback(self,event):
        list_of_pixels=[]
        for idx in range(0,12):
#            print('user_'+str(self.user_idx)+'_'+str(self.mylist.get(tk.ACTIVE))+'_'+str(idx))
            list_of_pixels=list_of_pixels+self.dataset.get('user_'+str(self.user_idx)+'_'+str(self.mylist.get(tk.ACTIVE))+'_'+str(idx))
#            print(len(list_of_pixels))
            time.sleep(0.1)
        self.img = Image.new(self.img.mode, self.img.size)
        self.img.putdata(list_of_pixels)    
#        print(os.path.join(dataset_address,self.ID,self.mylist.get(tk.ACTIVE)))
#        self.img=self.dataset.get('user_'+str(self.user_idx)+'_image_'+str(self.num_img))
#        self.img=Image.open(os.path.join(dataset_address,self.ID,self.mylist.get(tk.ACTIVE)))
        self.img=self.img.resize((300,300),Image.ANTIALIAS)
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def load_fun(self):
        file_dir=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
#        print(file_dir)
        if file_dir:
            self.img=Image.open(file_dir)
            self.img=self.img.resize((300,300),Image.ANTIALIAS)
            self.img_r=self.img
            img_tk=ImageTk.PhotoImage(self.img)
            self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
            self.image_edit_frame.mainloop()
    def save_fun(self):
#         self.img
#        self.img_list=os.listdir(os.path.join(dataset_address,ID))  
#         self.img.convert('RGB').save(os.path.join(dataset_address,self.ID,'image'+str(len(self.img_list)+1)+'.jpg'),"JPEG")
         self.img=self.img.convert('RGB')
         self.num_img=self.num_img+1
#         print('user_'+str(self.user_idx)+'_image_'+str(self.num_img))
#         print(self.num_img)

         self.save_img_to_dataset()
         
         
         self.user_info[-1]=self.num_img
         self.dataset.set('user_'+str(self.user_idx),self.user_info)
         time.sleep(0.5)
         self.aupdate_list()
    
    def save_img_to_dataset(self):
        img_data_list=list(list(self.img.getdata()))
        for idx in range(0,12):
#            print('user_'+str(self.user_idx)+'_image_'+str(self.num_img)+'_'+str(idx))
            self.dataset.set('user_'+str(self.user_idx)+'_image_'+str(self.num_img)+'_'+str(idx),img_data_list[0+idx*7500:7500+idx*7500])
            time.sleep(0.1)
#        for idx in range(0,12):
#            w1=self.dataset.get('user_'+str(self.user_idx)+'_image_'+str(self.num_img)+'_'+str(idx))
#            print(len(w1))
#            time.sleep(0.3)
            
         
    def log_out_fun(self):
        self.image_edit_frame.destroy()
        main_app_fun(self.dataset) 
    
    
    def reset_fun(self):
        self.img=self.img_r
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
        
    def gray_fun(self):
        self.img=self.img.convert('LA')
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def rotate_fun(self):
        self.img=self.img.rotate(10)
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def blur_fun(self):
        self.img = self.img.filter(ImageFilter.BLUR)
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def contrast_fun(self): 
        self.img = ImageEnhance.Contrast(self.img).enhance(1.5)
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def brightness_fun(self):
        self.img =ImageEnhance.Brightness(self.img).enhance(1.5) 
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def sharpness_fun(self):    
        self.img =ImageEnhance.Sharpness(self.img).enhance(1.5)
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()
    def edges_fun(self):
        self.img =self.img.filter(ImageFilter.FIND_EDGES)
        img_tk=ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_on_canvas, image = img_tk)
        self.image_edit_frame.mainloop()


class my_profile_window():
    def __init__(self, master,dataset,user_idx):
        self.dataset=dataset
        self.user_idx=user_idx
        self.user_info=self.dataset.get('user_'+str(user_idx))
        time.sleep(0.5)
        self.user_ID=self.user_info[0]
        self.user_profile = master
        self.user_profile.title('Parsa -'+ self.user_ID)
        tk.Label(master=self.user_profile, text='First Name').place(x=100, y=50)
        self.first_name_entry = tk.Entry(self.user_profile) 
        self.first_name_entry.place(x=200, y=50)
        self.first_name_entry.insert(0,self.user_info[2])
        
        tk.Label(master=self.user_profile, text='Last Name').place(x=100, y=100)
        self.last_name_entry = tk.Entry(self.user_profile,textvariable=tk.StringVar()) 
        self.last_name_entry.place(x=200, y=100)
        self.last_name_entry.insert(0,self.user_info[3])
        
        tk.Label(master=self.user_profile, text='Age').place(x=100, y=150)
        self.age_entry = tk.Entry(self.user_profile,textvariable=tk.StringVar()) 
        self.age_entry.place(x=200, y=150)
        self.age_entry.insert(0,self.user_info[4])
        
        tk.Label(master=self.user_profile, text='Job').place(x=100, y=200)
        self.job_entry = tk.Entry(self.user_profile,textvariable=tk.StringVar()) 
        self.job_entry.place(x=200, y=200)
        self.job_entry.insert(0,self.user_info[5])
        
        tk.Label(master=self.user_profile, text='Password').place(x=100, y=250)
        self.password_entry = tk.Entry(self.user_profile,textvariable=tk.StringVar()) 
        self.password_entry.place(x=200, y=250)
        self.password_entry.insert(0,self.user_info[1])
    
        tk.Button(master=self.user_profile, text ="  Close  ", command = self.close_fun).place(x=150, y=350)
        tk.Button(master=self.user_profile, text ="  Save  ", command = self.save_fun).place(x=250, y=350)
        
    def save_fun(self):
        user_info_list=[self.user_ID,self.password_entry.get(),self.first_name_entry.get(), 
                   self.last_name_entry.get(),self.age_entry.get(),self.job_entry.get(),self.user_info[-1]]
        
        
        self.dataset.set('user_'+str(self.user_idx),user_info_list)
        time.sleep(0.5)
        
    def close_fun(self):
        self.user_profile.destroy()


  




