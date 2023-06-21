import tkinter
import tkinter.messagebox as mb
import customtkinter
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
import os
import cv2
from natsort import natsorted
import pathlib, os.path
from os import startfile


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = Tk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

appdir = pathlib.Path(__file__).parent.resolve()
app.iconbitmap(os.path.join(appdir, 'ImgToVideoLogo.ico'))
app.title('ImgToVideo')

video_name = ''
file_name = os.getcwd() + 'img_to_video_settings_file.txt'
folder_link = ''


def common(file1_name, file2_name):
    def _iter():
        for a, b in zip(file1_name, file2_name):
            if a == b:
                yield a
            else:
                return

    return ''.join(_iter())


def generate_video(link, fps=25):
    global video_name

    try:
        print('link: ', link)
        link = link.replace('file:/', '')
        image_folder = '.'  # make sure to use your folder

        os.chdir(link)
        num_of_images = len(os.listdir('.'))

        images = []

        for file in os.listdir('.'):
            img = file
            images.append(img)

        print(images)
        images = natsorted(images)

        print(images)
        # Array images should only consider
        # the image files ignoring others if any

        video_name = common(file1_name=images[0], file2_name=images[1]) + '.mp4'

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
    global folder_link

    folder_link = link_field.get()
    fps = fps_field.get()

    file = open(file_name, 'w')
    file.write(fps)
    file.close()

    fps = int(fps)
    print(folder_link)
    generated_video = generate_video(folder_link, fps)
    if generated_video:
        msg = "Видео успешно создано"

        button_show_folder = ctk.CTkButton(master=app, text="Открыть папку", command=button_show_folder_function)
        button_show_folder.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)
        button_show_video = ctk.CTkButton(master=app, text="Посмотреть видео", command=button_show_video_function)
        button_show_video.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)
    else:
        msg = "Во время создания видео произошла ошибка"
    mb.showinfo("Информация", msg)


def button_show_folder_function():
    os.startfile(folder_link)


def button_show_video_function():
    startfile(video_name)


def get_path(event):
    link_field.delete(0, 'end')
    print(event.data)
    link_field.insert(0, event.data)


def callback(event):
    app.after(50, select_all, event.widget)


def select_all(widget):
    widget.select_range(0, 'end')
    widget.icursor('end')


app.drop_target_register(DND_ALL)
app.dnd_bind("<<Drop>>", get_path)

link_label = ctk.CTkLabel(app, text="Введите путь до файла с изображениями")
link_label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

link_field = ctk.CTkEntry(app)
link_field.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

link_field.drop_target_register(DND_ALL)
link_field.dnd_bind("<<Drop>>", get_path)
link_field.bind('<Control-a>', callback)

fps_label = ctk.CTkLabel(app, text="fps")
fps_label.place(relx=0.2, rely=0.45, anchor=tkinter.CENTER)

file = open(file_name, 'a+')
file.seek(0)
fps_str = file.readline()

OptionList = [
     '24',
     '25',
     '30',
     '60'
    ]

fps_field = ctk.CTkComboBox(app, values=OptionList)
fps_field.set(fps_str)
fps_field.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

# Use CTkButton instead of tkinter Button
button = ctk.CTkButton(master=app, text="Создать видео", command=button_function)
button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

progressbar = ctk.CTkProgressBar(app)
progressbar.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
progressbar.set(0)

app.bind('<Return>', lambda event=None: button.invoke())
app.mainloop()