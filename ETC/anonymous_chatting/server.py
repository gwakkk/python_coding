from twisted.internet import protocol, reactor
import names

# 사용자 구분을 위한 색상 이용
COLORS = [
    '\033[31m', # RED
    '\033[32m', # GREEN
    '\033[33m', # YELLOW
    '\033[34m', # BLUE
    '\033[35m', # MAGENTA
    '\033[36m', # CYAN
    '\033[37m', # WHITE
    '\033[4m',  # UNDERLINE
]

transports = set()
users = set()

class Chat(protocol.Protocol):
    # 사용자가 서버에 접속하면 connected 메세지 출력
    def connectionMade(self):
        # 이름을 랜덤으로 생성해서 users에 추가
        name = names.get_first_name()
        # 색상은 한정개수이기 때문에 돌려쓰기
        color = COLORS[len(users) % len(COLORS)]
        users.add(name)
        # 사용 접속자 추가        
        transports.add(self.transport)

        # \033[0m : 컬러를 리셋(메세지에는 색상 X)
        self.transport.write(f'{color}{name}\033[0m'.encode())

    def dataReceived(self, data):
        # 모든 클라이언트에게 메시지 전달
        # 자신이 보낸 메시지가 아닐경우만!
        for t in transports:
            if self.transport is not t:
                t.write(data)
# 통신 프로토콜 정의
class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()