# Keylogger Project: 

This project demonstrates a keylogging tool that captures keystrokes, records audio, takes screenshots, and gathers system information. It is designed for educational purposes only and should never be used for any malicious or unethical activity. Always seek explicit consent before running any software that monitors or records user activity.

## Features

  1- Keylogging: Captures keystrokes and logs them with a timestamp.
  
  2- Audio Recording: Records audio from the microphone and sends the audio file via email.
  
  3- Screenshot Capture: Takes screenshots of the user's desktop.
  
  4- System Information: Gathers details about the system such as hostname, IP address, processor type, etc.
  
  5- Periodic Email Reports: Sends logs, screenshots, and audio recordings via email to a predefined address.

  6- Deletes itself automatically when discovered by the user to simulate real-world keylogger behavior.
  
## Setup

### Requirements

This script automatically installs any missing dependencies when run. If a module is not found, the script will attempt to install the necessary packages using ```pip```.

### Usage

Clone the repository:

```git clone https://github.com/RCH2514/keylogger.git```

Navigate to the project folder:

```cd keylogger```

Run the Python script:

```python keyloggerr.py```

The program will start logging keystrokes, capturing screenshots, and recording audio as per the interval defined. It will send periodic email reports with the captured data.

## Ethical Use

This tool is strictly for educational purposes. It can be used to understand how keylogging works, but it should not be deployed on any machine without explicit permission from the user. Unauthorized use of keylogging software is illegal in many countries and can lead to severe consequences.

## Disclaimer

This project is provided for educational purposes only. The creator of this project does not support or condone the use of this software for malicious purposes, and it is the responsibility of the user to ensure they follow all relevant laws and ethical guidelines.
