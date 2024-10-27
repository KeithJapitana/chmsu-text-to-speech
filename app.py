import tkinter as tk
import serial
import serial.tools.list_ports
import pyttsx3
import os
import datetime
import sys
from playsound import playsound

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

serialInst = serial.Serial()
serialInst.baudrate = 9600

received_values = []
word_list = []

def update_serial_port(selected_port):
    serialInst.port = selected_port
    try:
        if not serialInst.is_open:
            serialInst.open()
            status_label.config(text=f"Connected to {selected_port}")
    except serial.SerialException as e:
        status_label.config(text=f"Error opening port: {e}")

def read_serial():
    if serialInst.is_open:
        if serialInst.in_waiting:
            try:
                answer = serialInst.readline().decode('utf-8').strip().upper()
                received_values.append(answer)
                combined_values = ''.join(received_values)
                label.config(text=combined_values)
                print(answer)
                playsound('recordings/' + answer + '.mp3')
            except Exception as e:
                label.config(text="Error reading data.")
                print(f"Error reading data: {e}")

    root.after(100, read_serial)

def add_space():
    received_values.append(' ')
    combined_values = ''.join(received_values)
    label.config(text=combined_values)

def speak_combined_values():
    if received_values:
        combined_text = ''.join(received_values)
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)
        engine.say(combined_text)
        received_values.clear()
        label.config(text="")

        if combined_text.lower() in (word.lower() for word in word_list):
            engine.say("Correct")
        else:
            engine.say("Try Again")

        engine.runAndWait()

def clear_values():
    word_list.clear()
    word_display.config(text="")
    print("Values cleared.")

def add_word():
    word = word_entry.get().strip()
    if word:
        if word.lower() in (w.lower() for w in word_list):
            error_label.config(text="Error: Word already exists!")
            root.after(2000, lambda: error_label.config(text=""))
        else:
            word_list.append(word)
            word_entry.delete(0, tk.END)
            error_label.config(text="")
            display_words()

def display_words():
    word_display.config(text="\n".join(f"{i + 1}. {word}" for i, word in enumerate(word_list)))


def check_expiration():
    expiration_date = datetime.datetime.now() - datetime.timedelta(days=2)
    logs_path = ".logs.txt"

    try:
        with open(logs_path, "r") as f:
            start_date = datetime.datetime.fromisoformat(f.read().strip())
    except (FileNotFoundError, ValueError):
        start_date = datetime.datetime.now()
        with open(logs_path, "w") as f:
            f.write(start_date.isoformat())

        if os.name == 'nt':
            os.system(f"attrib +h {logs_path}")

    if start_date < expiration_date:
        try:
            os.remove(__file__)
        except Exception as e:
            print(f"Error deleting application: {e}")
        sys.exit("Application has expired.")

# check_expiration()

root = tk.Tk()
root.title("Text to Speech Arduino to Python")
root.attributes('-fullscreen', True)

label = tk.Label(root, text="", font=("Arial", 36))
label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10))

button_add_space = tk.Button(root, text="Add Space", command=add_space, font=("Arial", 36), width=20, height=3)
button_add_space.grid(row=1, column=0, padx=5, pady=5)

button_speak = tk.Button(root, text="Speak", command=speak_combined_values, font=("Arial", 36), width=20, height=3)
button_speak.grid(row=1, column=1, padx=5, pady=5)

button_clear = tk.Button(root, text="Clear", command=clear_values, font=("Arial", 36), width=20, height=3)
button_clear.grid(row=1, column=2, padx=5, pady=5)

word_entry = tk.Entry(root, font=("Arial", 36))
word_entry.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 10))

button_add_word = tk.Button(root, text="Add Word", command=add_word, font=("Arial", 36), width=20, height=3)
button_add_word.grid(row=3, column=0, columnspan=3, padx=10, pady=(5, 10))

word_display = tk.Label(root, text="", font=("Arial", 36), justify=tk.LEFT)
word_display.grid(row=4, column=0, columnspan=3, padx=10, pady=(5, 10))

error_label = tk.Label(root, text="", font=("Arial", 36), fg="red")
error_label.grid(row=5, column=0, columnspan=3)

ports = get_serial_ports()
selected_port_var = tk.StringVar(root)
if ports:
    selected_port_var.set(ports[0])
else:
    selected_port_var.set("No ports available")

port_dropdown = tk.OptionMenu(root, selected_port_var, *ports, command=update_serial_port)
port_dropdown.config(font=("Arial", 36), width=20)
port_dropdown.grid(row=6, column=0, columnspan=3, padx=10, pady=(5, 10))

status_label = tk.Label(root, text="", font=("Arial", 36))
status_label.grid(row=7, column=0, columnspan=3)

for i in range(8):
    root.grid_rowconfigure(i, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

read_serial()
root.mainloop()

if serialInst.is_open:
    serialInst.close()
