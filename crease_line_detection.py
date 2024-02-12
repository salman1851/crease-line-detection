import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
import sys
import csv
from datetime import datetime
import datetime as dt
import pyscreenshot
import sys

if os.path.exists("frozen.jpg"):
  os.remove("frozen.jpg")

def restart():
    import sys
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)

class LineApp:
    def __init__(self, root):

        self.root = root
        
        self.root.title("Line Distance Calculator")

        self.root.geometry("1066x700")

        self.cap = cv2.VideoCapture(0)

        self.latest_frame = None

        self.create_widgets()

        self.freeze_toggle = 0

        self.line1 = None
        # self.line1_drawn = False

        self.line2 = None
        # self.line2_drawn = False

        self.line3 = None
        # self.line3_drawn = False

        self.line4 = None
        # self.line4_drawn = False

        self.active_line = 0

        self.rotation_angle = 0

        self.line_coor = [0,0,0,0]
        self.line_colors = ['yellow', 'red', 'green', 'blue']
        self.point_ser_num = 1

    def create_widgets(self):
        
        title_label = tk.Label(self.root, text="Crease Line Inspection", font=("Helvetica", 20))
        title_label.pack(pady=20)

        date = dt.datetime.now()
        date_label = tk.Label(self.root, text=f"{date:%A, %B %d, %Y}", font=("Helvetica", 10))
        date_label.place(relx = 0.95, rely = 0.04, anchor ='ne')

        self.video_canvas = tk.Canvas(self.root, width=400, height=400, bd=0, highlightthickness=0)
        self.video_canvas.place(x=100, y=100, anchor=tk.NW)

        close_app = tk.Button(self.root, text="Close Application", width=15, height=2, command = self.close_application)
        close_app.place(x=10, y=10)

        L1 = tk.Button(self.root, text="L1", width=10, height=5, bg="yellow", fg="white", command = self.set_active_line1)
        L1.place(x=10, y=100)

        L2 = tk.Button(self.root, text="L2", width=10, height=5, bg="red", fg="white", command = self.set_active_line2)
        L2.place(x=10, y=200)

        L3 = tk.Button(self.root, text="L3", width=10, height=5, bg="green", fg="white", command = self.set_active_line3)
        L3.place(x=10, y=300)

        L4 = tk.Button(self.root, text="L4", width=10, height=5, bg="blue", fg="white", command = self.set_active_line4)
        L4.place(x=10, y=400)

        button_take_pic = tk.Button(self.root, text="Take Picture", width=10, height=2, command = self.take_picture)
        button_take_pic.place(x=150, y=520)

        button_proc_pic = tk.Button(self.root, text="Process Picture", width=15, height=2, command = self.process_picture)
        button_proc_pic.place(x=300, y=520)

        button_reset_pts = tk.Button(self.root, text="Reset Points", width=10, height=2, command = self.reset_points)
        button_reset_pts.place(x=550, y=520)

        button_del_pt = tk.Button(self.root, text="Delete Last Point", width=15, height=2, command = self.delete_last_row)
        button_del_pt.place(x=650, y=520)

        button_next_pt = tk.Button(self.root, text="Next Point", width=10, height=2, command = self.next_point)
        button_next_pt.place(x=780, y=520)        

        button_save_pt = tk.Button(self.root, text="Save all Points", width=10, height=2, command = self.save_all_points)
        button_save_pt.place(x=880, y=520)

        rotation_slider = tk.Scale(self.root, from_=0, to=360, orient=tk.HORIZONTAL, length=200,
                                                             label="Set Anti-clockwise Rotation Angle", command = self.update_rotation_angle)
        rotation_slider.set(0)
        rotation_slider.place(x=600, y=100)

        button_rot_img = tk.Button(self.root, text="Rotate Image", width=10, height=2, command = self.rotate_image)
        button_rot_img.place(x=850, y=110)

        self.video_canvas.bind("<Button-1>", self.move_line)

        self.create_empty_table()

    def close_application(self):
        sys.exit()

    def delete_last_row(self):
        if len(self.tree.get_children()) > 0:
            last_item = self.tree.get_children()[-1]
            self.tree.delete(last_item)
            self.point_ser_num = self.point_ser_num - 1
        else:
            print("No rows to delete")

    def next_point(self):
        if len(self.tree.get_children()) < 4:
            self.freeze_toggle = 0
            if os.path.exists("frozen.jpg"):
                os.remove("frozen.jpg")
            self.update_video()

    def create_empty_table(self):

        fields = ['Point', 'X1', 'X2', 'Diff']

        self.tree = ttk.Treeview(self.root, columns=(0, 1, 2, 3), show="headings", height=4)
        self.tree.place(x=550, y=300)

        for col in range(0, 4):
            self.tree.heading(col, text=fields[col], anchor=tk.CENTER)
            self.tree.column(col, width=100)        

    def update_video(self):

        if self.freeze_toggle == 0:
            _, frame = self.cap.read()

            self.latest_frame = frame

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = cv2.resize(frame, (400, 400))

            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)

            # Delete previous image on the canvas and display the new one
            self.video_canvas.delete("all")
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img)  # Set anchor to the top-left corner
            self.video_canvas.img = img

            self.root.after(10, self.update_video)

        return

    def take_picture(self):
        cv2.imwrite('frozen.jpg', self.latest_frame)
        
        frame = cv2.cvtColor(self.latest_frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 400))   
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        self.video_canvas.delete("all")
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img)  # Set anchor to the top-left corner
        self.video_canvas.img = img

        self.freeze_toggle = 1

    def reset_points(self):
        self.freeze_toggle = 0
        if os.path.exists("frozen.jpg"):
            os.remove("frozen.jpg")
        restart()

    def save_csv(self, path):
        with open(path + "/point.csv", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            for row_id in self.tree.get_children():
                row = self.tree.item(row_id)['values']
                # print('save row:', row)
                csvwriter.writerow(row)

    def move_line(self, event):
        if self.active_line == 1:
            self.line1 = self.draw_or_move_line(self.line1, event.x)
        elif self.active_line == 2:
            self.line2 = self.draw_or_move_line(self.line2, event.x)
        elif self.active_line == 3:
            self.line3 = self.draw_or_move_line(self.line3, event.x)
        elif self.active_line == 4:
            self.line4 = self.draw_or_move_line(self.line4, event.x)

    def set_active_line1(self):
        self.active_line = 1

    def set_active_line2(self):
        self.active_line = 2

    def set_active_line3(self):
        self.active_line = 3

    def set_active_line4(self):
        self.active_line = 4

    def draw_or_move_line(self, line, x_coord):
        if line is not None:
            self.video_canvas.delete(line)  # Delete the existing line
        line = self.video_canvas.create_line(x_coord, 0, x_coord, 400, fill=self.line_colors[self.active_line-1], width=2)
        # print(f"Line {self.active_line} moved to x-coordinate: {x_coord}")
        self.line_coor[self.active_line - 1] = x_coord
        # print('line coordinates ', self.line_coor)
        return line

    def update_rotation_angle(self, value):
        self.rotation_angle = int(value)

    def rotate_image(self):
        angle = self.rotation_angle
        img = self.latest_frame
        rows, cols, _ = img.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        rotated_image = cv2.warpAffine(img, rotation_matrix, (cols, rows))
        
        frame = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 400))   
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        self.video_canvas.delete("all")
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img)  # Set anchor to the top-left corner
        self.video_canvas.img = img

    def process_picture(self):
        if len(self.tree.get_children()) < 4:
            x1 = self.line_coor[1] - self.line_coor[0]
            x2 = self.line_coor[3] - self.line_coor[2]
            diff = x1 - x2
            self.tree.insert("", "end", values=(str(self.point_ser_num), str(x1), str(x2), str(diff)))
            self.point_ser_num += 1

    def take_ss(self, path):
       ss=pyscreenshot.grab()
       ss.save(path + "/screenshot.png")

    def save_all_points(self):
        self.freeze_toggle = 0
        if os.path.exists("frozen.jpg"):
            os.remove("frozen.jpg")

        date_time = datetime.now()
        format = '%Y-%m-%d-%H-%M-%S'
        date_string = date_time.strftime(format)
        os.makedirs(date_string)
        self.take_ss(date_string)
        self.save_csv(date_string)

        restart()

if __name__ == "__main__":
    root = tk.Tk()
    app = LineApp(root)
    app.update_video()
    root.mainloop()