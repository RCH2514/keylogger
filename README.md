# Keylogger Project: 

This project demonstrates a keylogging tool that captures keystrokes, records audio, takes screenshots, and gathers system information. It is designed for educational purposes only and should never be used for any malicious or unethical activity. Always seek explicit consent before running any software that monitors or records user activity.

## Features

  1- Keylogging: Captures keystrokes and logs them with a timestamp.
  2- Audio Recording: Records audio from the microphone and sends the audio file via email.
  3- Screenshot Capture: Takes screenshots of the user's desktop.
  4- System Information: Gathers details about the system such as hostname, IP address, processor type, etc.
  5- Periodic Email Reports: Sends logs, screenshots, and audio recordings via email to a predefined address.
## Setup

### Requirements

To run this script, ensure you have the required Python packages installed:


1- Install dependencies by running the following command:

pip install pyscreenshot sounddevice keyboard

2- Update the EMAIL_ADDRESS and EMAIL_PASSWORD variables with your email credentials to send reports.4

### Usage

Clone the repository:

git clone https://github.com/your-username/keylogger-project.git

Navigate to the project folder:

cd keylogger-project

Run the Python script:

python keylogger.py

The program will start logging keystrokes, capturing screenshots, and recording audio as per the interval defined. It will send periodic email reports with the captured data.

## Ethical Use

This tool is strictly for educational purposes. It can be used to understand how keylogging works, but it should not be deployed on any machine without explicit permission from the user. Unauthorized use of keylogging software is illegal in many countries and can lead to severe consequences.

## Disclaimer

This project is provided for educational purposes only. The creator of this project does not support or condone the use of this software for malicious purposes, and it is the responsibility of the user to ensure they follow all relevant laws and ethical guidelines.
