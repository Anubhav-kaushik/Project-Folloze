from asyncio import sleep
import pyperclip as clip
import time
import pyautogui as gui
from output import speak

def copy(text):
    clip.copy(text)

def paste():
    return clip.paste()

def find_image(img):
    return gui.locateCenterOnScreen(img, confidence=0.8)

def moveTo(file_location, file_name, wait_time=1):
    pos = find_image(file_location)
    if pos == None:
        print(f'{file_name} not found on screen')
        speak(f'{file_name} not found on screen. Program is going to sleep for {wait_time} seconds')
        time.sleep(wait_time)
        wait_time *= 2
        if wait_time >= 4:
            return False
        speak('program is awake')
        speak(f'searching for {file_name} again')
        return moveTo(file_location, file_name, wait_time)
    
    gui.moveTo(pos)
    return True

def screenshot():
    return gui.screenshot()

def personalizeAccount(account_domains: list):
    '''
        steps in personalization:
            1. open personalization window
            2. check if personalization happens before or not
                if starting from start:
                    3. click on 'create rules block'
                    4. click on 'Account Domain'
                    5. click on 'Add account domain'
                    6. add account domain by pasting and separate using Enter
                    7. click on 'Add'
                    8. click on 'Done'
                else:
                    3. click on 'Add alternative rule'
                    4. click on 'Account Domain'
                    5. click on 'Add account domain'
                    6. add account domain by pasting and separate using Enter
                    7. click on 'Add'
                    8. click on 'Done'
    '''
    # 1. open personalization window
    ## Assuming that the personalization window is already open

    # 2. check if personalization happens before or not
    if find_image('img/designer/personalization/create_rules_block.png') != None:
        found = moveTo('img/designer/personalization/create_rules_block.png', 'create rules block button')
        if not found:  ## found variable is used to check if the button is found or not, if not then the program will sleep for a while and try again
            speak('create rules block button not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(1)
            gui.scroll(-1000)
            return personalizeAccount(account_domains)
    else:
        status = find_image('img/designer/personalization/add_alternative_rule.png')

        while status == None:
            screenBeforeScroll = screenshot()
            gui.scroll(-1000)
            status = find_image('img/designer/personalization/add_alternative_rule.png')
            screenAfterScroll = screenshot()
            time.sleep(0.5)
            
            if screenBeforeScroll == screenAfterScroll:
                break

        found = moveTo('img/designer/personalization/add_alternative_rule.png', 'add alternative rule button')
        if not found:
            speak('add alternative rule button not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(1)
            gui.scroll(-1000)
            return personalizeAccount(account_domains)
    gui.click()
    time.sleep(1)

    # 4. click on 'Account Domain'
    found = moveTo('img/designer/personalization/account_domain_option.png', 'account domain option')
    if not found:
        speak('account domain option not found. Program is going to start adding account domains again')
        gui.press('x')
        time.sleep(1)
        gui.scroll(-1000)
        return personalizeAccount(account_domains)

    gui.click()
    time.sleep(1)

    # 5. click on 'Add account domain'
    found = moveTo('img/designer/personalization/add_account_domain.png', 'add account domain')
    if not found:
        speak('add account domain window not found. Program is going to start adding account domains again')
        gui.press('x')
        time.sleep(1)
        gui.scroll(-1000)
        return personalizeAccount(account_domains)

    gui.click()
    time.sleep(1)

    # 6. add account domain by pasting and separate using Enter
    if find_image('img/designer/personalization/add_btn.png') != None:
        for domain in account_domains:
            copy(domain)
            gui.hotkey('ctrl', 'v')
            gui.press('enter')
    else:
        speak('add account domain window not found. Program is going to start adding account domains again')
        gui.press('x')
        time.sleep(1)
        gui.scroll(-1000)
        personalizeAccount(account_domains)
    
    # 7. click on 'Add'
    found = moveTo('img/designer/personalization/add_btn.png', 'add button')
    if not found:
        speak('add button not found. Program is going to start adding account domains again')
        gui.press('x')
        time.sleep(1)
        gui.scroll(-1000)
        return personalizeAccount(account_domains)

    gui.click()
    time.sleep(1)
    
    # 8. click on 'Done'    
    found = moveTo('img/designer/personalization/account_done.png', 'done button')
    if not found:
        speak('done button not found. Program is going to start adding account domains again')
        gui.press('x')
        time.sleep(1)
        gui.scroll(-1000)
        return personalizeAccount(account_domains)

    gui.click()
    time.sleep(1)

def personalizeText(text: str):
    gui.hotkey('shift', 'tab')
    gui.hotkey('ctrl', 'a')
    copy(text)
    gui.hotkey('ctrl', 'v')
    gui.scroll(-1000)

personalizeAccount(['gmail.com', 'yahoo.com', 'hotmail.com'])
personalizeText('Hello World')
