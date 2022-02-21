import pyperclip as clip
import time
import pyautogui as gui
from output import speak
import keyboard


def copy(text):
    clip.copy(text)


def paste():
    return clip.paste()


class Account:
    def __init__(self, account_name: str, domains: list, text: str = None):
        self.name = account_name
        self.domains = domains
        self.text = text

    def find_image(self, img):
        return gui.locateCenterOnScreen(img, confidence=0.9)

    def translate(self, x=0, y=0):
        [curX, curY] = gui.position()
        gui.moveTo(curX+x, curY+y)

    def moveTo(self, file_location, file_name, wait_time=1):
        pos = self.find_image(file_location)
        if pos == None:
            print(f'{file_name} not found on screen')
            speak(
                f'{file_name} not found on screen. Program is going to sleep for {wait_time} seconds')
            time.sleep(wait_time)
            wait_time *= 2
            if wait_time >= 4:
                return False
            speak('program is awake')
            speak(f'searching for {file_name} again')
            return self.moveTo(file_location, file_name, wait_time)

        gui.moveTo(pos)
        return True

    def moveToAny(self, files_location: list, wait_time=1):
        pos = None
        for file_location in files_location:
            pos = self.find_image(file_location)
            if pos != None:
                gui.moveTo(pos)
                return True
        
        if pos == None:
            print(f'file not found on screen')
            speak(
                f'file not found on screen.')
            time.sleep(wait_time)
            wait_time *= 2
            if wait_time >= 4:
                return False
            speak('program is awake')
            return self.moveToAny(files_location)

    def screenshot(self):
        return gui.screenshot()

    def personalizeDomains(self, wait_time=1):
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
        # Assuming that the personalization window is already open

        # 2. check if personalization happens before or not
        if self.find_image('img/designer/personalization/create_rules_block.png') != None:
            found = self.moveTo(
                'img/designer/personalization/create_rules_block.png', 'create rules block button')
            if not found:  # found variable is used to check if the button is found or not, if not then the program will sleep for a while and try again
                speak(
                    'create rules block button not found. Program is going to start adding account domains again')
                gui.press('x')
                time.sleep(wait_time)
                gui.scroll(-1000)
                return self.personalizeDomains()
        else:
            status = self.find_image(
                'img/designer/personalization/add_alternative_rule.png')

            while status == None:
                screenBeforeScroll = self.screenshot()
                gui.scroll(-1000)
                status = self.find_image(
                    'img/designer/personalization/add_alternative_rule.png')
                screenAfterScroll = self.screenshot()
                time.sleep(wait_time/2)

                if screenBeforeScroll == screenAfterScroll:
                    break

            found = self.moveTo(
                'img/designer/personalization/add_alternative_rule.png', 'add alternative rule button')
            if not found:
                speak(
                    'add alternative rule button not found. Program is going to start adding account domains again')
                gui.press('x')
                time.sleep(wait_time)
                gui.scroll(-1000)
                return self.personalizeDomains()
        gui.click()
        self.translate(x=800, y=0)
        time.sleep(wait_time)

        # 4. click on 'Account Domain'
        found = self.moveTo(
            'img/designer/personalization/account_domain_option.png', 'account domain option')
        if not found:
            speak(
                'account domain option not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(wait_time)
            gui.scroll(-1000)
            return self.personalizeDomains()

        gui.click()
        self.translate(x=800, y=0)
        time.sleep(wait_time)

        # 5. click on 'Add account domain'
        found = self.moveTo(
            'img/designer/personalization/add_account_domain.png', 'add account domain')
        if not found:
            speak(
                'add account domain window not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(wait_time)
            gui.scroll(-1000)
            return self.personalizeDomains()

        gui.click()
        time.sleep(wait_time)

        # 6. add account domain by pasting and separate using Enter
        if self.find_image('img/designer/personalization/add_btn.png') != None:
            for domain in self.domains:
                copy(domain)
                gui.hotkey('ctrl', 'v')
                gui.press('enter')
        else:
            speak(
                'add account domain window not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(wait_time)
            gui.scroll(-1000)
            self.personalizeDomains()

        # 7. click on 'Add'
        found = self.moveTo(
            'img/designer/personalization/add_btn.png', 'add button')
        if not found:
            speak(
                'add button not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(wait_time)
            gui.scroll(-1000)
            return self.personalizeDomains()

        gui.click()
        time.sleep(wait_time)

        # 8. click on 'Done'
        found = self.moveTo(
            'img/designer/personalization/account_done.png', 'done button')
        if not found:
            speak(
                'done button not found. Program is going to start adding account domains again')
            gui.press('x')
            time.sleep(wait_time)
            gui.scroll(-1000)
            return self.personalizeDomains()

        gui.click()
        time.sleep(wait_time)

    def personalizeText(self):
        '''this function add the text to the last text block'''
        # gui.hotkey('shift', 'tab')
        # gui.hotkey('shift', 'tab')
        [x, y] = self.find_image(
            'img/designer/personalization/add_alternative_rule.png')
        gui.moveTo(x, y-120)
        gui.click()
        copy(self.text)
        gui.hotkey('ctrl', 'v')
        gui.scroll(-1000)

    def searchAsset(self):
        self.moveToAny(['img/designer/personalization/search.png', 'img/designer/personalization/cross.png'])
        [x, y] = gui.position()
        gui.moveTo(x-100, y)
        gui.click()
        gui.hotkey('ctrl', 'a')
        gui.press('delete')
        copy(self.text)
        gui.hotkey('ctrl', 'v')
        gui.press('enter')

        time.sleep(2)
        # drag and drop the asset to the text block
        [dropX, dropY] = self.find_image(
            'img/designer/personalization/drop_here.png')
        gui.moveTo(x-100, y+50)
        gui.dragTo(dropX, dropY, 3, button='left')


class PersonalizationBot:
    def __init__(self, cleanData, what2personalize: str):
        self.accounts = cleanData['Company Name']
        self.domains = cleanData['Domain']

        self.what2personalize = what2personalize

        if what2personalize == 'Leading Asset':
            self.texts = cleanData['AE/Rep Email']
        else:
            self.texts = cleanData[what2personalize]

        if self.texts == None:
            texts = []
            for _ in range(len(self.domains)):
                texts.append(' ')
            self.texts = texts

        self.isSpecificAEs = False

        if (self.what2personalize == 'AE/Rep Email') or (self.what2personalize == 'AE/Rep Name') or (self.what2personalize == 'Leading Asset'):
            isSpecfic = input(
                'Do you want to personalize the contact card of some specific AEs? (y/n): ')
            if isSpecfic == 'y':
                uniqueAEs = list(set(self.texts))
                print('The following AEs are available: ')
                for i, ae in enumerate(uniqueAEs):
                    print(f'{i+1}. {ae}')

                self.specificAEs = input(
                    'Please enter the number corresponding to the specific AEs email (separate by comma): ')
                self.specificAEs = self.specificAEs.split(',')
                self.specificAEs = [
                    uniqueAEs[int(x)-1] for x in self.specificAEs]
                self.isSpecificAEs = True

    def personalize(self):
        speak(
            f'Open the {self.what2personalize} personalization window. Bot is waiting...')
        speak('Press Ctrl+q to start')
        keyboard.wait('ctrl+q')
        speak(f'Start personalizing the {self.what2personalize}')

        for account, domains, text in zip(self.accounts, self.domains, self.texts):
            if self.isSpecificAEs:
                if text.strip().lower() not in self.specificAEs:
                    continue
            accountObj = Account(account, domains, text)
            accountObj.personalizeDomains()

            if self.what2personalize not in ['Logo', 'Asset', 'Leading Asset', 'Banner']:
                accountObj.personalizeText()

            if self.what2personalize == 'Leading Asset':
                accountObj.searchAsset()

        speak(f'All the {self.what2personalize} are personalized')


if __name__ == '__main__':
    pass
