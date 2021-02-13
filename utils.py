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



def parseAccounts():
    with open('accounts.txt', 'r') as r:
        accounts = []
        for line in r:
            parsedLine = line.rstrip().split(':')
            newAcc = {
                "username": parsedLine[0],
                "password": parsedLine[1]
            }
            accounts.append(newAcc)
        if(len(accounts)) < 10:
            print("Missing accounts on accounts.txt, only found " + str(len(accounts)))
            sys.exit()
        else:
            return accounts

def parseSteamDir():
    line = open('steam_directory.txt', 'r')
    dirr = line.read()
    return dirr

def parseSteamArgs(username, password, x=0, y=0):
    str = " -noverifyfiles -nochatui -no-browser -silent -login {} {} -applaunch 730 -x {} -y {} -sw -w 640 -h 480 +fps_max 30  +fps_max_menu 29 -nosound -novid -nojoy -noshader -nofbo -nodcaudio -nomsaa +set vid level 0 +sethdmodels 0 +log off +noshaderapi +lv -16bpp -low -threads 1 -noborder -nohltv -low +exec boost".format(username, password, x, y)
    return str