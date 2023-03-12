import time
import tkinter
import customtkinter
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
import os
import cv2


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = Tk()  # create CTk window like you do with the Tk window
app.geometry("400x240")


def generate_video(link, fps=25):
    try:
        image_folder = '.'  # make sure to use your folder
        video_name = 'new_video.mp4'
        os.chdir(link)
        num_of_images = len(os.listdir('.'))

        img_name = os.listdir('.')[0]
        img_name = img_name.split('1')
        images = []
        for i in range(1, num_of_images + 1):
            images.append(f'{img_name[0]}{i}{img_name[1]}')

        print(images)
        # Array images should only consider
        # the image files ignoring others if any

        frame = cv2.imread(os.path.join(image_folder, images[0]))

        # setting the frame width, height width
        # the width, height of first image
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, int(fps), (width, height))

        # Appending the images to the video one by one

        for i in range(len(images)):
            print(images[i])
            video.write(cv2.imread(os.path.join(image_folder, images[i])))
            progressbar.set((i+1)/num_of_images)

            # Deallocating memories taken for window creation
        cv2.destroyAllWindows()
        video.release()  # releasing the video generated
    except:
        return False
    return True


def button_function():
    link = link_field.get()
    fps = fps_field.get()
    print(link)
    print(generate_video(link, fps))


def get_path(event):
    print(event.data)
    link_field.insert(0, event.data)


link_label = ctk.CTkLabel(app, text="Введите путь до файла с изображениями")
link_label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

link_field = ctk.CTkEntry(app)
link_field.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

link_field.drop_target_register(DND_ALL)
link_field.dnd_bind("<<Drop>>", get_path)

fps_label = ctk.CTkLabel(app, text="fps")
fps_label.place(relx=0.2, rely=0.45, anchor=tkinter.CENTER)

fps_field = ctk.CTkEntry(app)
fps_field.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

# Use CTkButton instead of tkinter Button
button = ctk.CTkButton(master=app, text="Создать видео", command=button_function)
button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

progressbar = ctk.CTkProgressBar(app)
progressbar.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
progressbar.set(0)

app.mainloop()