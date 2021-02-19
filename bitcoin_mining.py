#SHA-256 hash function 이용
#입력된 숫자나 문자열을 256비트의 이진수로 바꾸어서 출력
#해시 함수에 이전 블록의 해시 값과 현재 블록의 거래 내역(transaction), 임의의 숫자 nonce를 입력하여 
#얻은 결과값이 주어진 숫자보다 작은 nonce를 찾는 것이 채굴 작업

  
from hashlib import sha256
import time

# http://tcpschool.com/webbasic/bitcoin

MAX_NONCE = int(1e10)
#hash의 앞자리에 0이 반복하는 횟수 
DIFFICULTY = 10

# https://www.blockchain.com/btc/block/00000000000000000006dfdf4ae77bc817ae825858884e68c016fbf36298e793
block_number = 668861

#거래내역
transactions = '''
A->B:10
D->A:999
C->Z:1
'''
previous_hash = '00000000000000000006dfdf4ae77bc817ae825858884e68c016fbf36298e793'

new_hash = None

start_time = time.time()

for nonce in range(MAX_NONCE):
    text = str(block_number) + transactions + previous_hash + str(nonce)
    new_hash = sha256(text.encode('ascii')).hexdigest()

    if new_hash.startswith('0' * DIFFICULTY):
        print(f'Hash: {new_hash}')
        print(f'Nonce: {nonce}')
        break

if new_hash is None:
    print('hash를 찾지 못했습니다.')

print(f'소요시간 : {time.time() - start_time}s!')