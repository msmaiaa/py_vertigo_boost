import sys
import subprocess
import utils
import time
import os
import psutil


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
    username = account["username"]
    password = account["password"]
    steamdir = utils.parseSteamDir()
    args = utils.parseSteamArgs(username,password)
    proc = subprocess.Popen(steamdir + args, close_fds=True)

    return

def startMM():
    return

def startSearch():
    return

def main():
    openAllAccounts(accounts)
    #closeAllAccounts()
    #accounts = utils.parseAccounts()
    #openSingleAccount(accounts[0])



if __name__ == '__main__':
    main()