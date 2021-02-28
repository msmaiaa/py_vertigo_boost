from elevate import elevate
elevate()
import sys
import subprocess
import utils
import time
import os
import psutil
import keyboard 
import pyautogui
import clipboard
from python_imagesearch.imagesearch import imagesearch_count
pyautogui.PAUSE = 0.3

#to capture these coordinates you just need to start an instance of csgo with -x 0 and -y 0 parameters
#then use something to capture the coordinates, in this case i just used pyautogui.position() on a while true loop
c_open_sidebar = [308,58]
c_open_invite = [249,70]
c_input_field = [140,110]
c_copy_code_btn = [174,132]
c_open_invite_options = [174,109]
c_invite_click_area = [140,124]
c_invite_send = [251,113]
c_cancel = [198,141]
c_enter_party = [308, 62]
c_open_search = [9,30]
c_select_mm = [35,41]
c_start_search = [251,220]
c_accept_match = [159,131]
c_reconnect_btn = [254,12]
c_screen_center = [160, 115]
c_mm_btn = [36, 40]
g_start_delay = 130
g_reconnect_delay = 16
g_disconnect_delay = 36
g_status = ''

def restart_program():
    os.execv(__file__, sys.argv)

g_team1 = []
g_team2 = []        

def closeAllAccounts():
    #need to close csgo first so it doesn't crash
    for proc in psutil.process_iter(['name']):
        if proc.info["name"] == ("csgo.exe"):
            proc.kill()
    for proc in psutil.process_iter(['name']):
        if proc.info["name"] == ("steam.exe"):
            proc.kill()
    return

def openAllAccounts():
    if len(g_team1 + g_team2) == 10:
        accounts = g_team1 + g_team2
        for i, account in enumerate(accounts):
            x = utils.positions[i]["x"]
            y = utils.positions[i]["y"]
            steamdir = utils.parseSteamDir()
            args = utils.parseSteamArgs(account["username"], account["password"], x, y)
            subprocess.Popen(steamdir + args, close_fds=True)
    return

def openSingleAccount(account):
    steamdir = utils.parseSteamDir()
    args = utils.parseSteamArgs(account["username"],account["password"])
    proc = subprocess.Popen(steamdir + args, close_fds=True)
    return

def openInviteMenu(account):
    x1 = account["coords"]["x1"]
    y1 = account["coords"]["y1"]
    pyautogui.click(x1 + c_open_sidebar[0], y1 + c_open_sidebar[1])
    time.sleep(0.2)
    pyautogui.click(x1 + c_open_sidebar[0], y1 + c_open_sidebar[1])
    time.sleep(0.1)
    pyautogui.click(x1 + c_open_invite[0], y1 + c_open_invite[1], 2, 0.1)
    time.sleep(0.2)
    return

def sendAndInvite(receiver, sender):
    r_x1 = receiver["coords"]["x1"]
    r_y1 = receiver["coords"]["y1"]
    s_x1 = sender["coords"]["x1"]
    s_y1 = sender["coords"]["y1"]
    pyautogui.moveTo(r_x1 + c_open_sidebar[0], r_y1 + c_open_sidebar[1])
    time.sleep(0.1)
    pyautogui.click(r_x1 + c_open_sidebar[0], r_y1 + c_open_sidebar[1])
    time.sleep(0.1)
    pyautogui.click(r_x1 + c_open_sidebar[0], r_y1 + c_open_sidebar[1])
    time.sleep(0.2)
    pyautogui.click(r_x1 + c_open_invite[0], r_y1 + c_open_invite[1], 2, 0.05)
    time.sleep(0.1)
    pyautogui.click(r_x1 + c_copy_code_btn[0], r_y1 + c_copy_code_btn[1], 2, 0.05)
    time.sleep(0.1)
    keyboard.press_and_release('esc')

    #goes back to the account that send the invites
    pyautogui.click(s_x1 + c_input_field[0], s_y1 + c_input_field[1], 2, 0.05)
    keyboard.write(clipboard.paste())
    pyautogui.click(s_x1 + c_open_invite_options[0], s_y1 + c_open_invite_options[1], 2, 0.05)
    time.sleep(0.2)
    pyautogui.click(s_x1 + c_invite_click_area[0], s_y1 + c_invite_click_area[1], 2, 0.05)
    time.sleep(0.3)
    pyautogui.click(s_x1 + c_invite_send[0], s_y1 + c_invite_send[1], 2, 0.05)
    time.sleep(0.2)
    pyautogui.click(s_x1 + c_cancel[0], s_y1 + c_cancel[1], 2, 0.05)
    return
    

def inviteWithCode(receiver, sender):
    #sender = guy who will invite the rest of the accounts
    #receiver = account who will receive the invite
    openInviteMenu(sender)
    sendAndInvite(receiver, sender)
    return

def inviteSingleTeam(team):
    for i, account in enumerate(team):
        if i != 0:
            inviteWithCode(account, team[0])
    return

def inviteTeams():
    for i, account in enumerate(g_team1):
        if i != 0:
            inviteWithCode(account, g_team1[0])
    for i, account in enumerate(g_team2):
        if i != 0:
            inviteWithCode(account, g_team2[0])
    return 

def acceptInvites():
    for i, account in enumerate(g_team1):
        if i > 0:
            pyautogui.moveTo(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1])
            time.sleep(0.3)
            pyautogui.click(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1], 2, 0.05)
    for i, account in enumerate(g_team2):
        if i > 0:
            pyautogui.moveTo(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1])
            time.sleep(0.3)
            pyautogui.click(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1], 2, 0.05)
    return

def startInvites():
    inviteTeams()
    time.sleep(10)
    acceptInvites()
    return

def startMM():
    if len(g_team1 + g_team2) == 10:
        startSearch(queue='mm')
        startMMIngame()
    return

def startMMIngame():
    global g_status
    g_status = 'Starting Match'
    time.sleep(g_start_delay)
    g_status = 'Playing Match'
    for i in range(16):
        if i > 0:
            time.sleep(g_disconnect_delay)
        for account in g_team2:
            pyautogui.moveTo(account["coords"]["x1"] + c_screen_center[0], account["coords"]["y1"] + c_screen_center[1])
            time.sleep(0.1)
            pyautogui.click(account["coords"]["x1"] + c_screen_center[0], account["coords"]["y1"] + c_screen_center[1])
            keyboard.press_and_release('k')
            time.sleep(0.5)
        time.sleep(g_reconnect_delay)
        for account in g_team2:
            pyautogui.moveTo(account["coords"]["x1"] + c_reconnect_btn[0], account["coords"]["y1"] + c_reconnect_btn[1])
            pyautogui.click(account["coords"]["x1"] + c_reconnect_btn[0], account["coords"]["y1"] + c_reconnect_btn[1])
    g_status = 'Finished playing Match'
    return

def startSearch(queue):
    global g_status
    g_status = 'Searching for Match'
    clickSearchBtn()
    while True:
        count = imagesearch_count('./pics/Accept.png')
        if queue == 'mm':
            if count == 5:
                g_status = 'Found match only in one team'
                pyautogui.moveTo(g_team2[0]["coords"]["x1"] + c_start_search[0], g_team2[0]["coords"]["y1"] + c_start_search[1])
                pyautogui.click(g_team2[0]["coords"]["x1"] + c_start_search[0], g_team2[0]["coords"]["y1"] + c_start_search[1])

                pyautogui.moveTo(g_team1[0]["coords"]["x1"] + c_start_search[0], g_team1[0]["coords"]["y1"] + c_start_search[1])
                pyautogui.click(g_team1[0]["coords"]["x1"] + c_start_search[0], g_team1[0]["coords"]["y1"] + c_start_search[1])
                time.sleep(60)
                clickSearchBtn()
            elif count == 10:
                g_status = 'Both teams found a match'
                for i, account in enumerate(g_team1):
                    pyautogui.moveTo(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1])
                    pyautogui.click(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1], 2)
                for i, account in enumerate(g_team2):
                    pyautogui.moveTo(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1])
                    pyautogui.click(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1], 2)
                startMMIngame()
                break
        else:
            #todo
            return
    return

def clickSearchBtn():
    pyautogui.click(g_team1[0]["coords"]["x1"] + c_open_search[0], g_team1[0]["coords"]["y1"] + c_open_search[1])
    time.sleep(0.3)
    pyautogui.click(g_team1[0]["coords"]["x1"] + c_mm_btn[0], g_team1[0]["coords"]["y1"] + c_mm_btn[1])
    pyautogui.moveTo(g_team2[0]["coords"]["x1"] + c_open_search[0], g_team2[0]["coords"]["y1"] + c_open_search[1])
    time.sleep(0.2)
    pyautogui.click(g_team2[0]["coords"]["x1"] + c_open_search[0], g_team2[0]["coords"]["y1"] + c_open_search[1])

    time.sleep(0.2)

    pyautogui.click(g_team1[0]["coords"]["x1"] + c_start_search[0], g_team1[0]["coords"]["y1"] + c_start_search[1])
    time.sleep(0.3)
    pyautogui.click(g_team1[0]["coords"]["x1"] + c_mm_btn[0], g_team1[0]["coords"]["y1"] + c_mm_btn[1])
    pyautogui.moveTo(g_team2[0]["coords"]["x1"] + c_start_search[0], g_team2[0]["coords"]["y1"] + c_start_search[1])
    time.sleep(0.2)
    pyautogui.click(g_team2[0]["coords"]["x1"] + c_start_search[0], g_team2[0]["coords"]["y1"] + c_start_search[1])
    return

def loadAccounts():
    accounts = utils.parseAccounts()
    global g_team1
    global g_team2
    g_team1 = utils.calcAccountsCoords(accounts)["team1"]
    g_team2 = utils.calcAccountsCoords(accounts)["team2"]
    printStatus()
    return

def printStatus():
    global g_status
    os.system('cls')
    utils.table_keybinds()
    if len(g_team1) == 5 or len(g_team2) == 5:
        utils.table_accounts(g_team1, g_team2)
    else:
        print('Accounts not loaded')
    print('Status: ' + g_status)
    return


def main():
    
    keyboard.add_hotkey('f3', startInvites)
    keyboard.add_hotkey('f4', openAllAccounts)
    keyboard.add_hotkey('f5', loadAccounts)
    keyboard.add_hotkey('f6', startMM)
    keyboard.add_hotkey('f7', clickSearchBtn)
    keyboard.add_hotkey('f8', closeAllAccounts)
    keyboard.add_hotkey('f9', restart_program)
    while True:
        time.sleep(5)
        printStatus()
        #print(pyautogui.position())
        #count = imagesearch_count('./pics/Accept.png')
        #print(count)

if __name__ == '__main__':
    main()