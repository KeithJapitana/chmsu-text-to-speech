import tkinter as tk
import serial
import serial.tools.list_ports
import pyttsx3

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

serialInst = serial.Serial()
serialInst.baudrate = 9600

received_values = []

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
                engine = pyttsx3.init()
                engine.setProperty('rate', 120)
                engine.say(answer.lower())
                engine.runAndWait()
                print(answer)
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
        engine.setProperty('rate', 100)
        engine.say(combined_text)
        engine.runAndWait()

def clear_values():
    received_values.clear()
    label.config(text="")
    print("Values cleared.")

root = tk.Tk()
root.title("Text to Speech Arduino to Python")

root.attributes('-fullscreen', True)

label = tk.Label(root, text="", font=("Arial", 36))  # Increased font size to 36
label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10))

button_add_space = tk.Button(root, text="Add Space", command=add_space, font=("Arial", 36), width=20, height=3)  # Increased font size to 36
button_add_space.grid(row=1, column=0, padx=5, pady=5)

button_speak = tk.Button(root, text="Speak", command=speak_combined_values, font=("Arial", 36), width=20, height=3)  # Increased font size to 36
button_speak.grid(row=1, column=1, padx=5, pady=5)

button_clear = tk.Button(root, text="Clear", command=clear_values, font=("Arial", 36), width=20, height=3)  # Increased font size to 36
button_clear.grid(row=1, column=2, padx=5, pady=5)

ports = get_serial_ports()
selected_port_var = tk.StringVar(root)
if ports:
    selected_port_var.set(ports[0])
else:
    selected_port_var.set("No ports available")

port_dropdown = tk.OptionMenu(root, selected_port_var, *ports, command=update_serial_port)
port_dropdown.config(font=("Arial", 36), width=20)  # Increased font size to 36
port_dropdown.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 10))

status_label = tk.Label(root, text="", font=("Arial", 36))  # Increased font size to 36
status_label.grid(row=3, column=0, columnspan=3)

# Center components in the full-screen window
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

read_serial()

root.mainloop()

if serialInst.is_open:
    serialInst.close()