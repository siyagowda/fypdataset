import pyautogui
import pyperclip
import time

'''
try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: X={x}, Y={y}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped.")
'''

# Read the links
with open("suno_links.txt", "r") as file:
    links = file.readlines()

# Check if the link exists in the source file
with open("processed_suno_links.txt", 'r') as processed_file:
    old_links = processed_file.readlines()


cnt = 1
total = len(links)
for link in links:

    '''
    if link in old_links:
        print("link already processed")
        with open("suno_links.txt", 'w') as source_file:
            source_file.writelines(links[cnt:])  # Write all lines except the first one
        cnt += 1
        continue
    '''

    # comment this out if you won't be interacting with laptop while program is running
    # also make sure to check its clicking in the right place
    pyautogui.moveTo(1340, 1045, duration=1)
    pyautogui.click(1340, 1045)

    print(link)
    pyperclip.copy(link)
    pyautogui.click(1440, 180)  # Adjust to input field location
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "v")
    
    print("GET SONGS")
    pyautogui.moveTo(1725, 185, duration=1)
    pyautogui.click(1725, 185)  # Adjust to download button location
    time.sleep(7)  # Adjust the wait time or add a download detection step

    print("DOWNLOAD SONGS")

    pyautogui.moveTo(1725, 850, duration=1)
    pyautogui.click(1725, 850)  # Adjust to download button location

    with open("processed_suno_links.txt", 'a') as target_file:
        target_file.write(link) 

    with open("suno_links.txt", 'w') as source_file:
        source_file.writelines(links[cnt:])  # Write all lines except the first one

    for i in range(20):
        print(i)
        time.sleep(1)

    print("LINK " + str(cnt) + "/" + str(total) + " PROCESSED")
    cnt += 1

    

print("All links processed.")
