#Import Libraries
from tkinter import *
from tkinter.messagebox import *
import json
import random
import csv
import os
import time
import threading

#Main Window
root=Tk()
root.state("zoomed")
theme_mode = "light"
root.title("Technical Quiz application")
font=("Arial",30,"bold")

# Load questions
with open("quiz_questions_complete.json") as f:
	all_data = json.load(f)

current_category = StringVar(value=list(all_data.keys())[0])
current_level = StringVar(value="Easy")
quiz_questions_complete = []
current_qn_index = 0
score = 0
timer_running = False
seconds_left = 60
selected_option = StringVar()
entry_name = StringVar()

#defining functions

def toggle_theme():
    global theme_mode
    if theme_mode == "light":
        # Switch to dark theme
        theme_mode = "dark"

        root.configure(bg="black")
        lab_title.config(bg="black", fg="#f7c948")
        timer_label.config(bg="black", fg="white")

        info_frame.config(bg="black")
        lab_name.config(bg="black", fg="white")
        lab_category.config(bg="black", fg="white")
        lab_difficulty.config(bg="black", fg="white")
        entry_name.config(bg="white", fg="black", insertbackground="black")
        category_menu.config(bg="#333333", fg="white", activebackground="#8358d4", activeforeground="white")
        Difficulty_menu.config(bg="#333333", fg="white", activebackground="#8358d4", activeforeground="white")
        btn_start.config(bg="#f7c948", fg="black")
        btn_restart.config(bg="#d9534f", fg="white")

        quiz_frame.config(bg="#222222")
        question_label.config(bg="#222222", fg="white")
        for rb in quiz_frame.winfo_children():
            if isinstance(rb, Radiobutton):
                rb.config(bg="#222222", fg="white", selectcolor="#444444")

        btn_toggle.config(bg="#222222", fg="white")
        nav_frame.config(bg="#222222")
        btn_previous.config(bg="black", fg="white")
        btn_next.config(bg="blue", fg="white")
        btn_submit.config(bg="green", fg="white")

    else:
        # Switch to light theme
        theme_mode = "light"

        root.configure(bg="white")
        lab_title.config(bg="black", fg="#8358d4")
        timer_label.config(bg="black", fg="white")

        info_frame.config(bg="white")
        lab_name.config(bg="white", fg="black")
        lab_category.config(bg="white", fg="black")
        lab_difficulty.config(bg="white", fg="black")
        entry_name.config(bg="white", fg="black", insertbackground="black")
        category_menu.config(bg="white", fg="black", activebackground="#8358d4", activeforeground="black")
        Difficulty_menu.config(bg="white", fg="black", activebackground="#8358d4", activeforeground="black")
        btn_start.config(bg="#8358d4", fg="black")
        btn_restart.config(bg="green", fg="white")

        quiz_frame.config(bg="#d6cee6")
        question_label.config(bg="#d6cee6", fg="black")
        for rb in quiz_frame.winfo_children():
            if isinstance(rb, Radiobutton):
                rb.config(bg="#d6cee6", fg="black", selectcolor="white")

        btn_toggle.config(bg="black", fg="white")
        nav_frame.config(bg="#d6cee6")
        btn_previous.config(bg="black", fg="white")
        btn_next.config(bg="blue", fg="white")
        btn_submit.config(bg="green", fg="white")



def update_timer():
    global seconds_left, timer_running
    while timer_running and seconds_left > 0:
        mins, secs = divmod(seconds_left, 60)
        timer_var.set(f"⏱ {mins:02}:{secs:02}")
        time.sleep(1)
        seconds_left -= 1
    if seconds_left <= 0:
        show_final_result()

def start_timer():
    global timer_running, seconds_left
    seconds_left = 60
    timer_running = True
    threading.Thread(target=update_timer, daemon=True).start()

def load_question():
    global quiz_questions_complete, current_qn_index, selected_option
    if current_qn_index >= len(quiz_questions_complete):
        show_final_result()
        return
    q = quiz_questions_complete[current_qn_index]
    question_var.set(f"Q{current_qn_index + 1}: {q['question']}")
    for i, opt in enumerate(q['options']):
        options[i].config(text=f"{chr(65+i)}. {opt}", value=opt)
    selected_option.set(None)

def next_question():
    global current_qn_index, score
    if selected_option.get():
        if selected_option.get() == quiz_questions_complete[current_qn_index]['answer']:
            score += 1
    current_qn_index += 1
    load_question()

def prev_question():
    global current_qn_index
    if current_qn_index > 0:
        current_qn_index -= 1
        load_question()

def restart_quiz():
    global quiz_questions_complete, current_qn_index, score, seconds_left, timer_running
    if not entry_name.get().strip():
        showerror("Input Error", "Please enter your name before starting the quiz.")
        return
    score = 0
    current_qn_index = 0
    seconds_left = 60
    timer_running = False
    selected_option.set(None)
    load_question()
    start_timer()

def show_final_result():
    global timer_running
    timer_running = False
    total = len(quiz_questions_complete)
    msg = f"{entry_name.get()}, your score is {score}/{total}"
    showinfo("Quiz Completed", msg)
    save_result()

def start_quiz():
    global quiz_questions_complete, score, current_qn_index
    if not entry_name.get().strip():
        showerror("Input Error", "Please enter your name before starting the quiz.")
        return
    score = 0
    current_qn_index = 0
    category = current_category.get()
    level = current_level.get()
    quiz_questions_complete = all_data[category].get(level, [])
    if not quiz_questions_complete:
        showerror("No Questions", "No questions available for this category and level.")
        return
    random.shuffle(quiz_questions_complete)
    load_question()
    start_timer()

def save_result():
    filename = "techquiz_results.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Category", "Level", "Score", "Total"])
        writer.writerow([entry_name.get(), current_category.get(), current_level.get(), score, len(quiz_questions_complete)])

def on_closing():
    if timer_running:
        if askyesno("Exit", "Quiz is running. Do you want to quit?"):
            save_result()
            root.destroy()
    else:
        root.destroy()


#Label
lab_title=Label(root,text="🧠 Technical Quiz application",font=font,bg="black",fg="#8358d4")
lab_title.pack(fill=X)

#Timer
timer_var=StringVar(value="⏱ 01:00")
timer_label=Label(root,textvariable=timer_var,font=("Arial",20,"bold"),bg="black",fg="white")
timer_label.place(x=1200,y=10)

#info frame
info_frame=Frame(root,bd=2,relief=SOLID,bg="white")
info_frame.pack(padx=20,pady=20,fill=X)

lab_name=Label(info_frame,text="Enter Name:",font=("Arial",20,"bold"),bg="white",fg="black")
lab_name.grid(row=0,column=0)
entry_name=Entry(info_frame,textvariable=entry_name,font=("Arial",20,"bold"),bg="white",fg="black",relief=SOLID,bd=2)
entry_name.grid(row=0,column=1,padx=10)
lab_category=Label(info_frame,text="Category:",font=("Arial",20,"bold"),bg="white",fg="black")
lab_category.grid(row=0,column=2,padx=10)
category_menu = OptionMenu(info_frame, current_category, *all_data.keys())
category_menu.config(font=("Arial", 15), bg="white", fg="black", activebackground="#8358d4", activeforeground="black")
category_menu.grid(row=0, column=3, padx=10)
lab_difficulty=Label(info_frame,text="Difficulty:",font=("Arial",20,"bold"),bg="white",fg="black")
lab_difficulty.grid(row=0,column=4,padx=10)
Difficulty_menu = OptionMenu(info_frame,current_level, "Easy", "Medium", "Hard")
Difficulty_menu.config(font=("Arial", 15), bg="white", fg="black", activebackground="#8358d4", activeforeground="black")
Difficulty_menu.grid(row=0, column=5, padx=10)

#Quiz Frame
quiz_frame=Frame(root,bd=2,relief=SOLID,bg="#d6cee6")
quiz_frame.pack(padx=20,pady=10,fill=BOTH,expand=True)

question_var=StringVar()
question_label=Label(quiz_frame,textvariable=question_var,font=("Arial",20),bg="#d6cee6",fg="black",wraplength=1000,justify=LEFT)
question_label.pack(pady=30, anchor="w", padx=30)

options=[]
for i in range(4):
	rb=Radiobutton(quiz_frame,text="",variable=selected_option,value="",font=("Arial",20),bg="#d6cee6", fg="black", anchor="w", justify=LEFT, wraplength=950)
	rb.pack(padx=50,pady=5,fill=X)
	options.append(rb)
#buttons
btn_start=Button(info_frame,text="Start Quiz",bg="#8358d4",fg="black",font=("Arial",20,"bold"),command=start_quiz)
btn_start.grid(row=0,column=6,padx=20)
btn_restart=Button(info_frame,text="Restart Quiz",bg="green",fg="white",font=("Arial",20,"bold"),command=restart_quiz)
btn_restart.grid(row=0,column=7,padx=10)
btn_toggle=Button(quiz_frame,text="🌙 Toggle Theme",font=("Arial",15,"bold"),bg="black",fg="white",command=toggle_theme)
btn_toggle.place(x=1300,y=10)

nav_frame=Frame(quiz_frame,bg="#d6cee6")
nav_frame.pack(pady=20)
btn_previous=Button(nav_frame,text="⬅️ Previous",font=("Arial",15,"bold"),bg="black",fg="white",width=12,command=prev_question)
btn_previous.grid(row=0,column=0,padx=20)
btn_submit=Button(nav_frame,text="✅ Submit",font=("Arial",15,"bold"),bg="green",fg="white",width=12,command=show_final_result)
btn_submit.grid(row=0,column=1,padx=20)
btn_next=Button(nav_frame,text="➡️ Next",font=("Arial",15,"bold"),bg="blue",fg="white",width=12,command=next_question)
btn_next.grid(row=0,column=2,padx=20)




root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()