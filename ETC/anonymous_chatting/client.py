import socket
import select
import sys

# 서버에 접속
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

name = None

while True:
    read, write, fail = select.select((s, sys.stdin), (), ())
    # 메세지 도착시 소켓에서 4096바이트 읽기
    for desc in read:
        if desc == s:
            data = s.recv(4096)
            # 바이트를 문자열로 출력
            print(data.decode())

            # 처음 접속시 부여받은 이름 저장 후
            # 다른 접속자에게 접속 문구 출력
            if name is None:
                name = data.decode()
                s.send(f'{name} is connected!'.encode())
        else:
            msg = desc.readline()
            # 엔터 두번 중복 방지
            msg = msg.replace('\n', '')
            # 접속자 이름과 문구 같이 출력
            s.send(f'{name} {msg}'.encode())