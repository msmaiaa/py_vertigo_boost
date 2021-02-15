import sys
import subprocess
import utils
import time
import os
import psutil
import keyboard 
import pyautogui
import clipboard
from python_imagesearch.imagesearch import imagesearch_region_loop
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

def openAllAccounts(accounts):
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
    pyautogui.click(r_x1 + c_open_invite[0], r_y1 + c_open_invite[1], 2, 0.1)
    time.sleep(0.1)
    pyautogui.click(r_x1 + c_copy_code_btn[0], r_y1 + c_copy_code_btn[1], 2, 0.1)
    time.sleep(0.1)
    keyboard.press_and_release('esc')

    #goes back to the account that send the invites
    pyautogui.click(s_x1 + c_input_field[0], s_y1 + c_input_field[1], 2, 0.1)
    keyboard.write(clipboard.paste())
    pyautogui.click(s_x1 + c_open_invite_options[0], s_y1 + c_open_invite_options[1], 2, 0.1)
    time.sleep(0.2)
    pyautogui.click(s_x1 + c_invite_click_area[0], s_y1 + c_invite_click_area[1], 2, 0.1)
    time.sleep(0.3)
    pyautogui.click(s_x1 + c_invite_send[0], s_y1 + c_invite_send[1], 2, 0.1)
    time.sleep(0.2)
    pyautogui.click(s_x1 + c_cancel[0], s_y1 + c_cancel[1], 2, 0.1)
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
            pyautogui.click(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1], 2, 0.1)
    for i, account in enumerate(g_team2):
        if i > 0:
            pyautogui.moveTo(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1])
            time.sleep(0.3)
            pyautogui.click(account["coords"]["x1"] + c_enter_party[0], account["coords"]["y1"] + c_enter_party[1], 2, 0.1)
    return

def startInvites():
    inviteTeams()
    time.sleep(10)
    acceptInvites()
    return

def startMM():
    return

def startSearch():
    return
    

def main():
    accounts = utils.parseAccounts()
    global g_team1
    global g_team2
    g_team1 = utils.calcAccountsCoords(accounts)["team1"]
    g_team2 = utils.calcAccountsCoords(accounts)["team2"]
    print('F3 - Test key')
    print('F4 - Open all accounts')
    print('F5 - invite single team (f5 doesnt work on windows)')
    print('F6 - Invite all teams')
    print('F7 - Invite one person')
    print('F8 - Close all accounts')
    print('F9 - Panic button')

    keyboard.add_hotkey('f6', keyboard.press_and_release, args=['esc'])
    keyboard.add_hotkey('f4', openAllAccounts, args=[accounts])
    keyboard.add_hotkey('f5', inviteSingleTeam, args=[g_team1])
    keyboard.add_hotkey('f3', startInvites)
    keyboard.add_hotkey('f7', inviteWithCode, args=[g_team1[1], g_team1[0]])
    keyboard.add_hotkey('f8', closeAllAccounts)
    keyboard.add_hotkey('f9', sys.exit)
    # while True:
    #     time.sleep(1)
    #     print(pyautogui.position())
    input('Press enter on the console to exit the program\n')



if __name__ == '__main__':
    main()