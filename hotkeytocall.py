import json
import keyboard
from urllib.parse import parse_qs
import pyautogui
import pyperclip
import re
import requests
import socket
import webbrowser
import os

# Fill your Webex API Integration details
client_id = ""
client_secret = ""

# You can leave these as is.
hotkey = "f8"
host = 'localhost'
port = 9000
file_path = './token.json'

def open_auth_in_browser():
    url = "https://webexapis.com/v1/authorize?client_id=" + client_id \
        + "&response_type=code&" \
        + "redirect_uri=http%3A%2F%2Flocalhost%3A9000%2Fauth&" \
        + "scope=spark%3Acalls_write%20spark%3Aall%20spark%3Akms%20spark%3Acalls_read&state=set_state_here"
    webbrowser.open(url)

def parse_http_request(request):
    method, path, _ = request.split(' ', 2)
    path, _, query_string = path.partition('?')
    query_params = parse_qs(query_string)
    return method, path, query_params

def handle_request(request):
    method, path, query_params = parse_http_request(request)
    if method == 'GET' and path == '/auth':
        if 'code' in query_params:
            test_value = query_params['code'][0]
            #return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nTest value: {test_value}'
            return test_value
        else:
            return 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing "test" parameter'
    else:
        return 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found'

def wait_for_login():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}...")

        client_socket, client_address = server_socket.accept()
        with client_socket:
            request = client_socket.recv(1024).decode('utf-8')
            if request:
                response = handle_request(request)
                #client_socket.sendall(response.encode('utf-8'))
                client_socket.sendall(f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nAuthorisierung erfolgreich: {response}'.encode('utf-8'))
                return response
                
def get_access_token(code):
    api_url = "https://webexapis.com/v1/access_token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json"
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret":client_secret,
        "code": code,
        "state":"set_state_here",
        "redirect_uri":"http://localhost:9000/auth"
    }
    try:
        response = requests.post(api_url, data=payload, headers=headers)
        if response.status_code == 200:
            print("API call successful! Got access token")
            print("Response:")
            data = response.json()
            print(data)
            with open(file_path, 'w') as file:
                json.dump(data, file)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
            print(f"Error making API call: {e}")

def clean_phone_number(text):
    # Remove all non-digit characters
    cleaned_number = re.sub(r'\D', '', text)
    return cleaned_number

def copy_selected_text():
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.sleep(0.5)
    # Retrieve the copied text from the clipboard
    selected_text = pyperclip.paste()
    return selected_text

def call_api(selected_text):
    api_url = "https://webexapis.com/v1/telephony/calls/dial"
    access_token = ""
    with open(file_path, 'r') as file:
        data = json.load(file)
        access_token = data['access_token']
        print('Got access token: ' + access_token)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    payload = {
        "destination": selected_text
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("API call successful!")
            print("Response:")
            print(response.json())
        elif response.status_code == 201:
            print(f"Success: {response.status_code} - {response.text}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error making API call: {e}")

def on_shortcut_triggered():
    print("Shortcut triggered!")
    selected_text = copy_selected_text()
    cleaned_number = clean_phone_number(selected_text)
    call_api(cleaned_number)

def main():
    if not os.path.exists(file_path):
        open_auth_in_browser()
        code = wait_for_login()
        get_access_token(code)
    else:
        print("Token file already there.")

    shortcut_combination = hotkey

    # Set up the listener for the shortcut
    keyboard.add_hotkey(shortcut_combination, on_shortcut_triggered)

    print(f"Listening for shortcut: {shortcut_combination}")
    
    # Keep the program running in the background
    keyboard.wait("esc")  # Press 'esc' to exit

if __name__ == "__main__":
    main()
