# psloco
카카오톡 비공식 Api.

example
```py
from pywinauto import clipboard
from module import Client, messageBuilder, KakaoActivity

room = 'test1'
myName = 'test'
isOpenChat = True

class myClass(Client):
    def response(self, sender: str, msg: str, replier = messageBuilder(isOpenChat), Api = KakaoActivity(isOpenChat)):
        if msg == '!test':
            replier.reply(room, f'Hello, [{sender}]!', True, True)

        if msg == '!capture':
            replier.sendCapture(room, 1, 1)
            # 1, 2 모자이크, 카카오프렌즈
            # 1 기본 배경으로 전환

        if msg == '!getInfo':
            Api.copyInfo(room)
            replier.reply(room, f'[{sender}]님\n{clipboard.GetData()}', True, True)

        if msg == '!file':
            replier.sendFile(room, 'filePath')

        if msg.startswith('!그룹명변경 '):
            Api.changeGroupName(room, msg[7:])
            replier.reply(room, f'그룹명을 {msg[7:]}로 변경하였습니다.')

        if msg.startswith('!외치기 '):
            Api.shout(room, msg[5:])

        if msg.startswith('!공지 '):
            Api.post(room, msg[4:])

        if msg == '!exit':
            replier.reply(room, '봇을 종료합니다.')
            exit()

cli = myClass(room, myName)
cli.run()
```