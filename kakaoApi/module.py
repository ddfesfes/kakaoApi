import time, re
import pyautogui as pg
import pyperclip as pc
import pygetwindow as gw
import win32gui as wg
import win32api as wa
import win32con as wc
from pywinauto import Application, clipboard

from warnings import simplefilter
simplefilter('ignore', UserWarning)

class Config:
    def setWindow(self, room: str):
        w = gw.getWindowsWithTitle(room)
        
        if len(w) == 0:
            self.openChatRoom(room)
        else:
            w = gw.getWindowsWithTitle(room)[0]
            w.resizeTo(380, 640)
            time.sleep(0.001)
            Application(backend='win32').connect(title=room).window(title=room).set_focus()

        return w

    def openChatRoom(self, room: str):
        hwndkakao = wg.FindWindow(None, "카카오톡")
        hwndkakao_edit1 = wg.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
        hwndkakao_edit2_1 = wg.FindWindowEx(hwndkakao_edit1, None, "EVA_Window", None)
        hwndkakao_edit2_2 = wg.FindWindowEx(hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
        hwndkakao_edit3 = wg.FindWindowEx(hwndkakao_edit2_2, None, "Edit", None)

        wa.SendMessage(hwndkakao_edit3, wc.WM_SETTEXT, 0, room)
        time.sleep(1)
        wa.PostMessage(hwndkakao_edit3, wc.WM_KEYDOWN, wc.VK_RETURN, 0)
        time.sleep(0.01)
        wa.PostMessage(hwndkakao_edit3, wc.WM_KEYUP, wc.VK_RETURN, 0)
        time.sleep(1)

    def backGrond(self, room: str):
        self.setWindow(room)
        time.sleep(0.01)
        pg.hotkey('shift', 'tab')

class messageBuilder(Config):
    def __init__(self, openChat = False):
        self.openChat = openChat

    def reply(self, room: str, text: str, mention = False, reply = False):
        if mention == True:
            text = text.split('[')
        
        if reply == True:
            w = self.setWindow(room)
            time.sleep(0.001)
            center = pg.locateOnScreen('images/chat.png')
            pg.leftClick(center)
            pg.moveTo(w.left + 76, w.top + 497) #1151, 619
            pg.rightClick()
            center2 = pg.locateOnScreen('images/copy.png')
            pg.leftClick(center2)
        else:
            self.setWindow(room)
            time.sleep(0.001)
            pg.press('tab')
        
        if type(text) == str:
            pc.copy(text)
        else:
            pc.copy(text[0])

        time.sleep(0.001)
        pg.hotkey('ctrl', 'v')
        time.sleep(0.001)

        if type(text) == list:
            rightText = text[1].split(']')
            pc.copy('@' + rightText[0])
            time.sleep(0.001)
            pg.hotkey('ctrl', 'v')
            pg.press('tab')
            pg.press('backspace')
            pc.copy(rightText[1])
            time.sleep(0.001)
            pg.hotkey('ctrl', 'v')

        pg.press('enter')
        time.sleep(0.001)
        self.backGrond(room)

    def sendFile(self, room, filePath):
        pc.copy(filePath)
        self.setWindow(room)
        center = pg.locateOnScreen('images/file.png')
        pg.leftClick(center)
        pg.hotkey('ctrl', 'v')
        time.sleep(0.001)
        pg.press('enter')
        time.sleep(0.001)
        self.backGrond(room)

    def sendCapture(self, room, mosaic = 0, background = 0):
        w = self.setWindow(room)
        center = pg.locateOnScreen('images/capture.png')
        pg.leftClick(center)
        center2 = pg.locateOnScreen('images/chatCapt.png')
        pg.leftClick(center2)
        pg.moveTo(w.left + 184, w.top + 89) #1284, 226
        pg.leftClick()
        pg.moveTo(w.left + 184, w.top + 552) #1284, 689
        pg.leftClick()
        if mosaic !=  0 or background != 0:
            pushCount = 4 - mosaic
            center3 = pg.locateOnScreen('images/option.png')
            pg.leftClick(center3)
            if mosaic != 0:
                pg.press('tab', presses=mosaic)
                pg.press('space')
            pg.press('tab', presses=pushCount)
            if background != 0:
                pg.press('space')
            center4 = pg.locateOnScreen('images/optionAcc.png')
            pg.leftClick(center4)
        center5 = pg.locateOnScreen('images/captureAcc.png')
        pg.leftClick(center5)
        center6 = pg.locateOnScreen('images/deliver.png')
        pg.leftClick(center6)
        center7 = pg.locateOnScreen('images/ok.png')
        pg.leftClick(center7)
        self.backGrond(room)

class KakaoActivity(Config):
    def __init__(self, openChat = False):
        self.openChat = openChat
        pass

    def changeGroupName(self, room: str, changedName: str):
        if self.openChat == False:
            print('오픈 채팅에서만 가능한 기능입니다.')
            return
        
        pc.copy(changedName)
        self.setWindow(room)
        center = pg.locateOnScreen('images/options.png')
        pg.leftClick(center)
        center2 = pg.locateOnScreen('images/manageChat.png')
        pg.leftClick(center2)
        pg.hotkey('ctrl', 'a')
        pg.hotkey('ctrl', 'v')
        center3 = pg.locateOnScreen('images/ok.png')
        pg.leftClick(center3)
        pg.press('tab', presses=2)
        time.sleep(0.001)
        self.backGrond(room)

    def shout(self, room: str, text: str):
        if self.openChat == False:
            print('오픈 채팅에서만 사용이 가능한 기능입니다.')
            return
        
        pc.copy(text)
        self.setWindow(room)
        center = pg.locateOnScreen('images/shout.png')
        pg.leftClick(center)
        # pg.press('tab', presses=4)
        # pg.press('space')
        pg.hotkey('ctrl', 'v')
        center2 = pg.locateOnScreen('images/send.png')
        pg.leftClick(center2)
        pg.press('esc')
        time.sleep(0.001)
        self.backGrond(room)

    def post(self, room: str, text: str):
        pc.copy(text)
        self.setWindow(room)
        center = pg.locateOnScreen('images/options.png')
        pg.leftClick(center)
        center1 = pg.locateOnScreen('images/talk.png')
        pg.leftClick(center1)
        center2 = pg.locateOnScreen('images/write.png')
        pg.leftClick(center2)
        # pg.press('tab')
        # pg.press('space')
        pg.hotkey('ctrl', 'v')
        center3 = pg.locateOnScreen('images/submit.png')
        pg.leftClick(center3)
        time.sleep(0.1)
        pg.press('esc')
        pg.press('tab', presses=2)
        self.backGrond(room)

    def copyInfo(self, room: str):
        if self.openChat == False:
            print('오픈채팅에서만 사용이 가능한 기능입니다.')
            return
        self.setWindow(room)
        centera = pg.locateOnScreen('images/options.png')
        pg.leftClick(centera)
        center = pg.locateOnScreen('images/copyLink.png')
        pg.click(center)
        link = clipboard.GetData()
        pg.press('space')
        center2 = pg.locateOnScreen('images/manageChat.png')
        pg.click(center2)
        pg.press('tab', presses=8)
        pg.hotkey('ctrl', 'a')
        pg.hotkey('ctrl', 'c')
        pc.copy('link: ' + link + '\ncode: ' + clipboard.GetData())
        center3 = pg.locateOnScreen('images/cancel.png')
        pg.click(center3)
        pg.press('tab', presses=2)
        self.backGrond(room)

class Client(Config):
    def __init__(self, room: str, myName: str, detectMine = False):
        self.room = room
        self.myName = myName
        self.detectMine = False

    def response(self, sender: str, msg: str, replier = messageBuilder(False), Api = KakaoActivity(False)):
        pass

    def getData(self, room: str):
        self.setWindow(room)
        time.sleep(0.001)
        center = pg.locateOnScreen('images/chat.png')
        pg.click(center)
        pg.hotkey('ctrl', 'a')
        time.sleep(0.001)
        pg.hotkey('ctrl', 'c')
        time.sleep(0.001)
        data = clipboard.GetData().replace('\r', '').split('\n')[-2]
        if f'[{self.myName}]' not in data or self.detectMine == True:
            name = re.sub(r'\[(.*)\] \[.*\] .*', r'\g<1>', data)
            data = re.sub(r'\[.*\] \[.*\] (.*)', r'\g<1>', data)
            self.response(name, data)

    def run(self):
        while True:
            self.getData(self.room)
            time.sleep(0.2)