import serial
import random
import time
import threading
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk

# Serial communication setup
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

hand_pos = {1: 'Rock', 2 : 'Paper', 3 : 'Scissors'} #Hand position 1 = rock, 2 = paper, 3 = scissors

def flush_serial_buffer(): #clears the serial input and output buffers
    ser.reset_input_buffer() #ensures that program starts with an empty buffer and only process new incoming data
    ser.reset_output_buffer() #ensures that there is no leftover data from previous operations that might interfere with current communication

#funtion for serial write to arduino
def send_command(command): 
    ser.write(str(command).encode('utf-8'))
    print(f"Sent: {command}")

    # Wait for acknowledgment
    response = ser.readline().strip().decode('utf-8')
    if response:
        print(f"{response}")
        return True
    else:
        print("No Acknowledgment received")
        return False

def clear_message_label(): #clears tkinter message label
    message_label.config(text="")

def control_finger_1(): #def funtion called to control finger 1
    try:
        sent_int = 4 #finger 1 responds to int 4
        ack = send_command(sent_int)
        message_label.config(text="Moving finger 1", foreground="#00FF00")
        if ack:
            message_label.config(text="Moving finger 1", foreground="#00FF00") #Acknowledgement from arduino
        root.after(1000, clear_message_label) #message dissappers after 1000 ms
    except serial.SerialException: #error handling
        message_label.config(text="Error: Serial port not available.", foreground="#FF0000")
    except Exception as e:
        message_label.config(text="Error: " + str(e), foreground="#FF0000")

def control_finger_2(): #def funtion called to control finger 2
    try:
        sent_int = 5 #finger 1 responds to int 5
        ack = send_command(sent_int)
        message_label.config(text="Moving finger 2", foreground="#00FF00")
        if ack:
            message_label.config(text="Moving finger 2", foreground="#00FF00") #Acknowledgement from arduino
        root.after(1000, clear_message_label) #message dissappers after 1000 ms
    except serial.SerialException: #error handling
        message_label.config(text="Error: Serial port not available.", foreground="#FF0000")
    except Exception as e:
        message_label.config(text="Error: " + str(e), foreground="#FF0000")

def control_finger_3(): #def funtion called to control finger 3
    try:
        sent_int = 6 #finger 1 responds to int 5
        ack = send_command(sent_int)
        message_label.config(text="Moving finger 3", foreground="#00FF00")
        if ack:
            message_label.config(text="Moving finger 3", foreground="#00FF00") #Acknowledgement from arduino
        root.after(1000, clear_message_label) #message dissappers after 1000 ms
    except serial.SerialException: #error handling
        message_label.config(text="Error: Serial port not available.", foreground="#FF0000")
    except Exception as e:
        message_label.config(text="Error: " + str(e), foreground="#FF0000")

def open_rock_paper_scissors_window(): #tkinter window for rock paper scissors
    new_window = tk.Toplevel(root)
    new_window.title("Rock Paper Scissors Mode")

    try:
        new_window.tk.call("source", "/home/maksiel/Downloads/Azure/azure.tcl") #Installed custom tkinter theme from github repository
    except tk.TclError:
        pass
    new_window.tk.call("set_theme", "dark") #sets custom theme

    # Create message label2 in the new window
    message_label2 = tk.Label(new_window, text="", foreground="#00FF00", font=font_style)
    message_label2.pack()

    def recogniser(source, recognizer): #speech recogition setup, initialization of recognizer
        with source as audio_source:
            try:
                assert audio_source.stream is not None
                recognizer.adjust_for_ambient_noise(audio_source)
                audio = recognizer.listen(audio_source)
            except AssertionError: #error handling
                message_label2.config(text="Audio stream is None. Please check your microphone connection.")
                return
            except Exception as e:
                message_label2.config(text=f'Error occurred while listening: {e}')
                return
        try:
            words = recognizer.recognize_google(audio) #Initializes Google Web Speech API
            if "play" in words:
                random_int = random.randint(1, 3) #imports random integer 1-3 using 'random' library
                print(hand_pos[random_int]) #prints hand position
                ack = send_command(random_int)
                message_label2.config(text=f"Hand Position {random_int}") #random integer determines hand position
                if ack:
                    message_label2.config(text=f"Hand Position {random_int}") #Prints as tkinter message label if serial is acknowladged ny Aruino
            else:
                message_label2.config(text="Desired game not detected. Not sending to Arduino.") #If no acknowledgment is received from Arduino
            return words
        except sr.UnknownValueError: #error handling
            message_label2.config(text='Speech was not discernable :(')
        except sr.RequestError as e:
            message_label2.config(text=f"Could not request results from Google Speech Recognition service; {e}")

    def run_recogniser(): #funtion to initialize microphone and run recognizer
        recognizer = sr.Recognizer()
        mic = sr.Microphone(device_index=2)  # Adjust the device index as needed
        message_label2.config(text="Start Talking!")
        for _ in range(10):  # Adjust the number of attempts as needed
            recogniser(mic, recognizer)

    threading.Thread(target=run_recogniser).start()

# Main Window
root = tk.Tk()
root.title("Welcome to Robohand!")

# Set up the Azure theme
root.tk.call("source", "/home/maksiel/Downloads/Azure/azure.tcl")
root.tk.call("set_theme", "dark")

# Custom font for a futuristic feel
font_style = ("Arial", 12)

# Frame for the buttons
button_frame = ttk.LabelFrame(root, text="Controls", padding=10)
button_frame.pack(padx=10, pady=10)

button_style = {
    "style": "Accent.TButton",
    "padding": (5, 5)
}

# Separate frame for the Rock Paper Scissors button
rps_button_frame = ttk.LabelFrame(root, text="Game Mode", padding=10)
rps_button_frame.pack(padx=10, pady=10)

#buttons to control fingers
button1 = ttk.Button(button_frame, text="Move Finger 1", command=control_finger_1, **button_style)
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = ttk.Button(button_frame, text="Move Finger 2", command=control_finger_2, **button_style)
button2.grid(row=0, column=1, padx=5, pady=5)

button3 = ttk.Button(button_frame, text="Move Finger 3", command=control_finger_3, **button_style)
button3.grid(row=0, column=2, padx=5, pady=5)

#Rock Paper Scissors button
button4 = ttk.Button(rps_button_frame, text="Play Rock Paper Scissors", command=open_rock_paper_scissors_window, **button_style)
button4.pack(pady=10)

message_label = ttk.Label(root, text="", font=font_style)
message_label.pack(pady=10)

root.mainloop()


