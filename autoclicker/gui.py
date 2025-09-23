import tkinter as tk
import threading, pyautogui, keyboard, time, math

running = False
button_area = None

def auto_clicker(delay, duration, follow_8, fixed_x, fixed_y, click_type):

    global running, button_area
    start = time.time()

    if button_area:
        while running:
            x, y = pyautogui.position()
            if not (button_area[0] <= x <= button_area[2] and button_area[1] <= y <= button_area[3]):
                break
            time.sleep(0.05)
    while running:
        if fixed_x is not None and fixed_y is not None:
            pyautogui.moveTo(fixed_x, fixed_y)
        if follow_8:
            t = time.time()
            cx, cy = pyautogui.size()
            cx //= 2; cy //= 2
            r = 100
            x = cx + int(r * math.sin(t)/(1+math.cos(t)**2))
            y = cy + int(r * math.sin(t)*math.cos(t)/(1+math.cos(t)**2))
            pyautogui.moveTo(x, y)
        pyautogui.click(button=click_type)
        time.sleep(delay)
        if duration>0 and (time.time()-start)>=duration:
            running=False
            status_label.config(text="STOPP", fg="red")
            break

def toggle_clicker():

    global running
    running = not running

    if running:
        try: d = float(delay_entry.get())
        except: d=0.1
        try: du = float(duration_entry.get())
        except: du=0
        f8 = follow_8_var.get()
        try: fx=int(x_entry.get()); fy=int(y_entry.get())
        except: fx=fy=None
        click = click_type_var.get()
        bx1=start_button.winfo_rootx(); by1=start_button.winfo_rooty()
        bx2=bx1+start_button.winfo_width(); by2=by1+start_button.winfo_height()
        global button_area; button_area=(bx1,by1,bx2,by2)
        threading.Thread(target=auto_clicker, args=(d,du,f8,fx,fy,click), daemon=True).start()
        status_label.config(text="LÄUFT", fg="green")
    else:
        status_label.config(text="STOPP", fg="red")

root = tk.Tk(); root.title("AutoClicker"); root.geometry("400x300")

tk.Label(root,text="Delay:").pack(); delay_entry=tk.Entry(root); delay_entry.insert(0,"0.1"); delay_entry.pack()
tk.Label(root,text="Dauer:").pack(); duration_entry=tk.Entry(root); duration_entry.insert(0,"0"); duration_entry.pack()

follow_8_var=tk.BooleanVar(); tk.Checkbutton(root,text="8-Schleife",variable=follow_8_var).pack()

tk.Label(root,text="X:").pack(); x_entry=tk.Entry(root); x_entry.pack()
tk.Label(root,text="Y:").pack(); y_entry=tk.Entry(root); y_entry.pack()

click_type_var=tk.StringVar(value="left")

tk.Radiobutton(root,text="Links",variable=click_type_var,value="left").pack()
tk.Radiobutton(root,text="Rechts",variable=click_type_var,value="right").pack()

start_button=tk.Button(root,text="Start/Stop",command=toggle_clicker); start_button.pack(pady=5)
status_label=tk.Label(root,text="STOPP",fg="red"); status_label.pack()

keyboard.add_hotkey("f6", toggle_clicker); keyboard.add_hotkey("esc", lambda: root.quit())

root.mainloop()
