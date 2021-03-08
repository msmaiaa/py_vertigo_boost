from colorclass import Color, Windows
from terminaltables import SingleTable
import colorclass
import psutil
import pyautogui
from datetime import datetime
pyautogui.PAUSE = 0.3
Windows.enable(auto_colors=True, reset_atexit=True)


positions = [
    {"x": 0, "y": 0},
    {"x": 0, "y": 510},
    {"x": 320, "y": 510},
    {"x": 0, "y": 770},
    {"x": 320, "y": 770},
    {"x": 640, "y": 0},
    {"x": 640, "y": 510},
    {"x": 960, "y": 510},
    {"x": 640, "y": 770},
    {"x": 960, "y": 770},
]

def calcAccountsCoords(accounts, _type):
    team1 = []
    team2 = []
    for i, account in enumerate(accounts):
        #x1/y1 => starts from top left
        #x2/y2 => starts from bottom right
        x1 = positions[i]["x"]
        y1 = positions[i]["y"]
        x2 = x1 + 320
        y2 = y1 + 230
        if _type == 'mm':
            if i <= 4:
                team1.append({
                    "username": account["username"],
                    "password": account["password"],
                    "coords":{
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    }
                })
            else:
                team2.append({
                    "username": account["username"],
                    "password": account["password"],
                    "coords":{
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    }
                })
        elif _type == 'wm':
            if i <= 1:
                team1.append({
                    "username": account["username"],
                    "password": account["password"],
                    "coords":{
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    }
                })
            else:
                team2.append({
                    "username": account["username"],
                    "password": account["password"],
                    "coords":{
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    }
                })
    return {"team1": team1, "team2": team2}

def parseAccounts():
    accounts = []
    try:
        with open('team1.txt', 'r') as r:
            for line in r:
                parsedLine = line.rstrip().split(':')
                if parsedLine:
                    newAcc = {
                        "username": parsedLine[0],
                        "password": parsedLine[1]
                    }
                    accounts.append(newAcc)
            if(len(accounts)) < 5:
                return
    except FileNotFoundError:
        print(Color('{autored}[ERROR]{/autored} {autogreen}team1.txt not found!{/autogreen}'))
    
    try:
        with open('team2.txt', 'r') as r:
            for line in r:
                parsedLine = line.rstrip().split(':')
                if parsedLine:
                    newAcc = {
                        "username": parsedLine[0],
                        "password": parsedLine[1]
                    }
                    accounts.append(newAcc)
            if(len(accounts)) < 10:
                return
    except FileNotFoundError:
        print(Color('{autored}[ERROR]{/autored} {autogreen}team2.txt not found!{/autogreen}'))
    return accounts

def parseWMAccounts():
    accounts = []
    try:
        with open('wingman.txt', 'r') as r:
            for i, line in enumerate(r):
                parsedLine = line.rstrip().split(':')
                if parsedLine:
                    newAcc = {
                        "username": parsedLine[0],
                        "password": parsedLine[1]
                    }
                    if i > 1:
                        accounts.append(newAcc)
                    else:
                        accounts.append(newAcc)
            if(len(accounts)) < 2:
                return
    except FileNotFoundError:
        print(Color('{autored}[ERROR]{/autored} {autogreen}wingman.txt not found!{/autogreen}'))
    return accounts

def parseSteamDir():
    line = open('steam_directory.txt', 'r')
    dirr = line.read()
    return dirr

def parseSteamArgs(username, password, x=0, y=0):
    str = " -noverifyfiles -nochatui -no-browser -silent -login {} {} -applaunch 730 -x {} -y {} -sw -w 640 -h 480 +fps_max 30  +fps_max_menu 29 -nosound -novid -nojoy -noshader -nofbo -nodcaudio -nomsaa +set vid level 0 +sethdmodels 0 +log off +noshaderapi +lv -16bpp -low -threads 1 -noborder -nohltv -low +exec boost".format(username, password, x, y)
    return str

def table_keybinds():
    table_data = [
        [Color('{autoyellow}F3{/autoyellow}'), 'Invite MM Accounts'],
        [Color('{autoyellow}F4{/autoyellow}'), 'Open all accounts'],
        [Color('{autoyellow}F5{/autoyellow}'), 'Load or Refresh accounts'],
        [Color('{autogreen}F6{/autogreen}'), 'Start MM Search (15x0)'],
        [Color('{autogreen}F7{/autogreen}'), 'Wingman (8x8)'],
        [Color('{autogreen}F8{/autogreen}'), 'Close all accounts'],
        [Color('{autored}F9{/autored}'), 'Invite Wingman Accounts'],
        [Color('{autored}F10{/autored}'), 'Open Wingman Accounts'],
        [Color('{autored}F11{/autored}'), 'Run Wingman 8x8 forever'],
        [Color('{autored}F12{/autored}'), 'Stop everything'],
        ['\033[31m{}\033[0m'.format(psutil.cpu_percent()), 'CPU Usage'],
        ['\033[31m{}\033[0m'.format(psutil.virtual_memory().percent), 'RAM Usage'],
    ]
    table_instance = SingleTable(table_data)
    table_instance.inner_heading_row_border = False
    print(table_instance.table)
    return

def table_accounts(team1, team2):
    table_data = []

    for i in range(len(team1)):
        passw = '*' *  len(team1[i]["password"])
        table_data.append(
            [team1[i]["username"],  passw]
        )
    t1_table = SingleTable(table_data, 'Team 1')
    t1_table.inner_heading_row_border = False
    print(t1_table.table)

    table_data.clear()
    for i in range(len(team2)):
        passw = '*' * len(team2[i]["password"])
        table_data.append(
            [team2[i]["username"],  passw]
        )
    t2_table = SingleTable(table_data, 'Team 2')
    t2_table.inner_heading_row_border = False
    print(t2_table.table)
    return

def mouse(account = '', target = [0,0], _type='', clicks=1):
    x1 = 0
    y1 = 0
    if _type == 'outside':
        pyautogui.moveTo(account["coords"]["x2"] + 5, account["coords"]["y2"] + 5)
        pyautogui.click(account["coords"]["x2"] + 5, account["coords"]["y2"] + 5)
        return
    if account:
        x1 = account["coords"]["x1"] + target[0]
        y1 = account["coords"]["y1"] + target[1]
    if _type == 'click':
        pyautogui.click(x1, y1, clicks)
    elif _type == 'move':
        pyautogui.moveTo(x1, y1)
    return

logMsgs = [
    {"name": "botStart", "content": "Bot has started", "color": "magenta"},
    {"name": "notLoaded", "content": "{} accounts not loaded!", "color": "yellow"},
    {"name": "loaded", "content": "{} accounts are loaded!", "color": "cyan"},
    {"name": "searchingMatch", "content": "Searching for a {} match", "color": "cyan"},
    {"name": "foundHalf", "content": "Found a match only on 1 team", "color": "yellow"},
    {"name": "foundAll", "content": "Found a match on both teams!", "color": "green"},
    {"name": "finishedPlaying", "content": "Finished playing a match :)", "color": "cyan"},
    {"name": "startingMatch", "content": "Starting match", "color": "green"},
    {"name": "playingMatch", "content": "Playing match", "color": "green"},
    {"name": "acceptingInvites", "content": "Accepting team {} invites", "color": "cyan"},
    {"name": "inviting", "content": "Inviting team {}", "color": "cyan"},
    {"name": "openAll", "content": "Opening all accounts", "color": "cyan"},
    {"name": "disconnectedAccounts", "content": "Disconnected accounts from match, rejoining in {} seconds", "color": "green"},
    {"name": "loadingAccounts", "content": "Loading accounts", "color": "cyan"},
    {"name": "matchCount", "content": "Starting match sequence number {}", "color": "magenta"},
]

def buildLogMsg(msgName, date, data='', raw=False):
    dateNow = date.strftime("%d/%m/%Y-%H:%M:%S: ")
    msg = ''
    

    for m in logMsgs:
        if m["name"] == msgName:
            if raw:
                msg += dateNow
                msg += m["content"].format(data)
                return msg
            color = m["color"]
            content = Color('{%s}%s{/%s}' % (color, m["content"], color))
            msg += Color('{%s}%s{/%s}' % ('white', dateNow, 'white'))
            if data:
                msg += content.format(data)
            else:
                msg += content
    return msg


def logger(msgName, data=False):
    fullMsg = ''
    rawMsg = buildLogMsg(msgName, datetime.now(), '', True)
    if data:
        fullMsg = buildLogMsg(msgName, datetime.now(), data)
    else:
        fullMsg = buildLogMsg(msgName, datetime.now())
    with open('logs.txt', 'a') as l:
        l.write(rawMsg + '\n')
    print(fullMsg)
    return
    

if __name__ == '__main__':
    for m in logMsgs:
        logger(m["name"], 1)