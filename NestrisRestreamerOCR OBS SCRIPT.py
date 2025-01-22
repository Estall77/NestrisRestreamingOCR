from obswebsocket import obsws, requests
import os
import re
import time

TEXT_SOURCE_NAME_1 = "score_difference_1"
TEXT_SOURCE_NAME_2 = "score_difference_2"
FILE_PATH_1 = os.path.expanduser("~/Downloads/score_difference_1.txt") 
FILE_PATH_2 = os.path.expanduser("~/Downloads/score_difference_2.txt")

def connect():
    host = "localhost"
    port = 4455
    password = "xQACaES8W9ECPaDG"
    ws = obsws(host, port, password)
    ws.connect()
    while(True):
        run(ws)
        time.sleep(0.1)
def run(ws):
    start_time = time.time()
    try:
        # Read the file content
        with open(FILE_PATH_1, "r") as file:
            content_1 = file.read().strip()
        with open(FILE_PATH_2, "r") as file:
            content_2 = file.read().strip()    
        match1 = re.search(r"Score Difference:\s*([+-]?\d+)", content_1)
        match2 = re.search(r"Score Difference:\s*([+-]?\d+)", content_2)    
        
        if match1:
            value_1 = match1.group(1)  # Extract the number as a string
                        
            if int(value_1) < 0:
                color = 0x4E4EEE
            else:
                color = 0x07DD1A
            ws.call(requests.SetInputSettings(
            overlay=True,
            inputName=TEXT_SOURCE_NAME_1,
            inputSettings={
                "text": f"Score Difference: {value_1}",
                "color": color
            }            
        ))
        if match2:
            value_2 = match2.group(1)  # Extract the number as a string
                        
            if int(value_2) < 0:
                color = 0x4E4EEE
            else:
                color = 0x07DD1A
            ws.call(requests.SetInputSettings(
            overlay=True,
            inputName=TEXT_SOURCE_NAME_2,
            inputSettings={
                "text": f"Score Difference: {value_2}",
                "color": color
            }            
        ))            
        elapsed_time = time.time() - start_time
        print(f"update took {elapsed_time:.2f} seconds")    
    except Exception as e:
        print(f"Error reading file or updating text value/color: {e}")
        
if __name__ == '__main__':
    connect()