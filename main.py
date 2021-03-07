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
import threading
import clipboard
from python_imagesearch.imagesearch import imagesearch_count
pyautogui.PAUSE = 0.3

"""
These are [x,y] coordinates based on a 640x480 csgo window fixed on x=0, y=0
To capture just use print(pyautogui.position()) on a While True
"""
c_open_sidebar = [308,56]
c_open_invite = [249,70]
c_input_field = [140,110]
c_copy_code_btn = [174,132]
c_open_invite_options = [174,109]
c_invite_click_area = [140,124]
c_invite_send = [251,113]
c_cancel = [198,141]
c_enter_party = [308, 62]
c_enter_party_wm = [262, 61]
c_open_search = [9,30]
c_select_mm = [35,41]
c_select_wm = [61,41]
c_start_search = [251,220]
c_accept_match = [159,131]
c_reconnect_btn = [254,12]
c_screen_center = [160, 115]

g_start_delay = 130
g_reconnect_delay = 13
g_disconnect_delay = 42
g_status = 'Doing nothing'
g_screenSize = pyautogui.size()

g_team1 = []
g_team2 = []
g_wm_team1 = []
g_wm_team2 = []        

def closeAllAccounts():
    #need to close csgo first so it doesn't crash
    for proc in psutil.process_iter(['name']):
        if proc.info["name"] == ("csgo.exe"):
            proc.kill()
    for proc in psutil.process_iter(['name']):
        if proc.info["name"] == ("steam.exe"):
            proc.kill()
    return

def openAllAccounts(_type=''):
    closeAllAccounts()
    utils.logger('openAll')
    team1 = g_team1
    team2 = g_team2
    if _type == 'wm':
        team1 = g_wm_team1
        team2 = g_wm_team2

    accounts = team1 + team2
    for i, account in enumerate(accounts):
        x = utils.positions[i]["x"]
        y = utils.positions[i]["y"]
        steamdir = utils.parseSteamDir()
        args = utils.parseSteamArgs(account["username"], account["password"], x, y)
        subprocess.Popen(steamdir + args, close_fds=True)

    return

def openInviteMenu(account):
    utils.mouse(account, c_open_sidebar, 'move')
    time.sleep(0.1)
    utils.mouse(account, c_open_sidebar, 'click', 2)
    time.sleep(0.2)
    utils.mouse(account, c_open_invite, 'click', 2)
    time.sleep(0.2)
    return

def inviteWithCode(receiver, sender):
    r_x1 = receiver["coords"]["x1"]
    r_y1 = receiver["coords"]["y1"]
    s_x1 = sender["coords"]["x1"]
    s_y1 = sender["coords"]["y1"]
    pyautogui.moveTo(r_x1 + c_open_sidebar[0], r_y1 + c_open_sidebar[1])
    time.sleep(0.3)
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
    time.sleep(0.3)
    keyboard.press_and_release('esc')
    return
    

def invite(receiver, sender):
    #sender = guy who will invite the rest of the accounts
    #receiver = account who will receive the invite
    openInviteMenu(sender)
    inviteWithCode(receiver, sender)
    return

def inviteSingleTeam(team):
    for i, account in enumerate(team):
        if i != 0:
            invite(account, team[0])
    return

def inviteTeams(_type):
    team1 = g_team1
    team2 = g_team2
    if _type == 'wm':
        team1 = g_wm_team1
        team2 = g_wm_team2

    utils.logger('inviting', '1')
    for i, account in enumerate(team1):
        if i != 0:
            invite(account, team1[0])
    utils.logger('inviting', '2')
    for i, account in enumerate(team2):
        if i != 0:
            invite(account, team2[0])
    return 

def acceptInvites(_type):
    team1 = g_team1
    team2 = g_team2
    enter_coord = c_enter_party
    if _type == 'wm':
        team1 = g_wm_team1
        team2 = g_wm_team2
        enter_coord = c_enter_party_wm
    utils.logger('acceptingInvites', '1')
    for i, account in enumerate(team1):
        if i > 0:
            utils.mouse(account, c_enter_party, 'move')
            time.sleep(0.3)
            utils.mouse(account, enter_coord, 'click', 2)
    utils.logger('acceptingInvites', '2')
    for i, account in enumerate(team2):
        if i > 0:
            utils.mouse(account, c_enter_party, 'move')
            time.sleep(0.3)
            utils.mouse(account, enter_coord, 'click', 2)
    return

def startInvites(_type):
    inviteTeams(_type)
    time.sleep(10)
    acceptInvites(_type)
    return


def startIngameBoost(_type):
    global g_status
    utils.logger('startingMatch')
    utils.mouse(account = g_wm_team2[0], _type='outside')
    time.sleep(g_start_delay)
    utils.logger('playingMatch')

    team1 = g_team1
    team2 = g_team2
    loseTeam = team1
    ###
    ### still need to add some checking stuff
    ### can optimize by removing half of the code, but not now
    if _type == 'wm':
        team1 = g_wm_team1
        team2 = g_wm_team2
        #just draw for now
        loseTeam = team1
        for i in range(10):
            if i > 0:
                time.sleep(g_disconnect_delay)
            if i > 4:
                loseTeam = team2
            for account in loseTeam:
                pyautogui.moveTo(account["coords"]["x1"] + c_screen_center[0], account["coords"]["y1"] + c_screen_center[1])
                time.sleep(0.1)
                pyautogui.click(account["coords"]["x1"] + c_screen_center[0], account["coords"]["y1"] + c_screen_center[1])
                keyboard.press_and_release('k')
                time.sleep(0.5)

            if i != 4:
                utils.logger('disconnectedAccounts', str(g_reconnect_delay))
                time.sleep(g_reconnect_delay)

            if i != 9:
                for account in loseTeam:
                    pyautogui.moveTo(account["coords"]["x1"] + c_reconnect_btn[0], account["coords"]["y1"] + c_reconnect_btn[1])
                    pyautogui.click(account["coords"]["x1"] + c_reconnect_btn[0], account["coords"]["y1"] + c_reconnect_btn[1])
                    time.sleep(0.05)
                    utils.mouse(account = g_wm_team2[0], _type='outside')    
    else:
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
    utils.logger('finishedPlaying')
    time.sleep(40)
    return

def startSearch(_type):
    utils.logger('searchingMatch', 'Competitive')
    clickSearchBtn(_type)

    team1 = g_team1
    team2 = g_team2
    halfFound = 5
    allFound = 10

    if _type == 'wm':
        team1 = g_wm_team1
        team2 = g_wm_team2
        halfFound = 2
        allFound = 4
        utils.logger('searchingMatch', 'Wingman')
    while True:
        count = imagesearch_count('./pics/Accept.png')
        count2 = imagesearch_count('./pics/Accept2.png')
        if count == halfFound or count2 == halfFound or (count + count2) == halfFound:
            utils.logger('foundHalf')
            pyautogui.moveTo(team2[0]["coords"]["x1"] + c_accept_match[0], team2[0]["coords"]["y1"] + c_accept_match[1])
            pyautogui.click(team2[0]["coords"]["x1"] + c_accept_match[0], team2[0]["coords"]["y1"] + c_accept_match[1], 2)
            pyautogui.moveTo(team1[0]["coords"]["x1"] + c_accept_match[0], team1[0]["coords"]["y1"] + c_accept_match[1])
            pyautogui.click(team1[0]["coords"]["x1"] + c_accept_match[0], team1[0]["coords"]["y1"] + c_accept_match[1], 2)

            pyautogui.moveTo(team2[0]["coords"]["x1"] + c_start_search[0], team2[0]["coords"]["y1"] + c_start_search[1])
            pyautogui.click(team2[0]["coords"]["x1"] + c_start_search[0], team2[0]["coords"]["y1"] + c_start_search[1])

            pyautogui.moveTo(team1[0]["coords"]["x1"] + c_start_search[0], team1[0]["coords"]["y1"] + c_start_search[1])
            pyautogui.click(team1[0]["coords"]["x1"] + c_start_search[0], team1[0]["coords"]["y1"] + c_start_search[1]) 
            time.sleep(60)
            clickSearchBtn(_type)
        elif count == allFound or count2 == allFound or (count+count2) == allFound:
            utils.logger('foundAll')
            for i, account in enumerate(team1):
                pyautogui.moveTo(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1])
                pyautogui.click(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1], 2)
            for i, account in enumerate(team2):
                pyautogui.moveTo(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1])
                pyautogui.click(account["coords"]["x1"] + c_accept_match[0], account["coords"]["y1"] + c_accept_match[1], 2)
            break
    return

def clickSearchBtn(_type=''):
    team1 = g_team1
    team2 = g_team2
    queue_btn = c_select_mm
    if _type == 'wm':
        team1 = g_wm_team1
        team2 = g_wm_team2
        queue_btn = c_select_wm
    utils.mouse(team1[0], c_open_search, 'click')
    time.sleep(0.3)
    utils.mouse(team1[0], queue_btn, 'click')
    utils.mouse(team2[0], c_open_search, 'move')
    time.sleep(0.2)
    utils.mouse(team2[0], c_open_search, 'click')

    time.sleep(0.2)

    utils.mouse(team1[0], c_start_search, 'click')
    time.sleep(0.3)
    utils.mouse(team2[0], queue_btn, 'click')
    utils.mouse(team2[0], c_start_search, 'move')
    time.sleep(0.2)
    utils.mouse(team2[0], c_start_search, 'click')
    return

def startMM():
    if len(g_team1 + g_team2) == 10:
        startSearch('mm')
        startIngameBoost('mm')
    return

def startWM():
    if len (g_wm_team1 + g_wm_team2) == 4:
        startSearch('wm')
        startIngameBoost('wm')
    return

def loadAccounts():
    utils.logger('loadingAccounts')
    accounts = utils.parseAccounts()
    wm_accounts = utils.parseWMAccounts()
    global g_team1
    global g_team2
    global g_wm_team1
    global g_wm_team2
    if accounts or wm_accounts:
        g_team1 = utils.calcAccountsCoords(accounts, 'mm')["team1"]
        g_team2 = utils.calcAccountsCoords(accounts, 'mm')["team2"]
        g_wm_team1 = utils.calcAccountsCoords(wm_accounts, 'wm')["team1"]
        g_wm_team2 = utils.calcAccountsCoords(wm_accounts, 'wm')["team2"]
        if len(g_team1) == 5 or len(g_team2) == 5:
            utils.logger('loaded', 'Matchmaking')
        else:
            utils.logger('notLoaded', 'Matchmaking')

        if len(g_wm_team1) == 2 or len(g_wm_team2) == 2:
            utils.logger('loaded', 'Wingman')
        else:
            utils.logger('notLoaded', 'Wingman')
    return

def runForever(_type):
    while True:
        startInvites(_type)
        if _type == 'wm':  
            startWM()
        elif _type == 'mm':
            startMM()

def main():
    utils.table_keybinds()
    utils.logger('botStart')
    loadAccounts()
    keyboard.add_hotkey('f3', startInvites, args=['mm'])
    keyboard.add_hotkey('f4', openAllAccounts)
    keyboard.add_hotkey('f5', loadAccounts)
    keyboard.add_hotkey('f6', startMM)
    keyboard.add_hotkey('f7', startWM)
    keyboard.add_hotkey('f8', closeAllAccounts)
    keyboard.add_hotkey('f9', startInvites, args=['wm'])
    keyboard.add_hotkey('f10', openAllAccounts, args=['wm'])
    keyboard.add_hotkey('f11', runForever, args=["wm"])
    
    while True:
        time.sleep(0.02)
        if keyboard.is_pressed('f12'):
            return
        #utils.mouse(account = g_wm_team2[0], _type='outside')
        #printStatus()
        #print(pyautogui.position())
    return

if __name__ == '__main__':
    # x = threading.Thread(target=main)
    # x.start()
    # x.join()
    main()
    