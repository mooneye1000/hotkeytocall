# Hotkeytocall
## Description
Webex Call Shortcut that allows a user to make calls from anywhere, regardless
of what Window is open. Calling from any highlighted number in a browser or
Microsoft Office application. Shortcut (F8) to Webex Teams Calling.
It provides a function commonly referred to as Click to Call or Click to Dial.

It is a workaround as there is no such function in Webex yet. See:
https://ciscocollabcustomer.ideas.aha.io/ideas/WXCUST-I-5650

## Installation
No install required just run the exe. (The exe is not signed so make sure to set
an exception in Windows Defender. Tip: Make an exception for the folder
containing the exe)

## Usage
A login to you Webex Account opens up. After login you just select some phone
number in any program and hit F8. Your Webex Phones should ring. Pick the phone
and it will automatically call the selected number.

## Test
```
cd C:\Users\user\AppData\Local\Programs\Python\Python312
.\python.exe C:\Users\user\Desktop\hotkeytocall.py
```

## Building
```
python -m pip install keyboard, pyautogui, pyperclip, requests, socket, webbrowser
python -m pip install pyinstaller
cd to hotkeytocall.py: cd C:\Users\user\Desktop\hotkeytocall
C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller "C:\Users\user\Desktop\hotkeytocall\hotkeytocall2.py"
```

## Auth Procedure for Webex API
### Step 1: v1/authorize
```
https://webexapis.com/v1/authorize?client_id=xxxxxx&response_type=code&redirect_uri=http%3A%2F%2Ftest.com&scope=spark%3Acalls_write%20spark%3Aall%20spark%3Akms%20spark%3Acalls_read&state=set_state_here
```
### Step 2: use code to get token with get_access_token function
curl -X POST https://webexapis.com/v1/access_token \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'accept: application/json' \
-d 'grant_type=authorization_code&client_id=xxxxx&client_secret=xxxx&code=xxxx&state=set_state_here&redirect_uri=http://test.com'
```
