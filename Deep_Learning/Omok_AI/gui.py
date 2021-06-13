from ursina import *
# game engine module
import numpy as np
from tensorflow.keras.models import load_model
from gomoku import Board, Gomoku
# gomoku : Omok의 규칙을 정의

model = load_model('models/chan_Omok_md.h5')

app = Ursina()

window.borderless = False
window.color = color._50

w, h = 20, 20
camera.orthographic = True
camera.fov = 23
camera.position = (w//2, h//2)

board = Board(w=w, h=h)
# 20 * 20
board_buttons = [[None for x in range(w)] for y in range(h)]
game = Gomoku(board=board)
# Gomoku를 통한 게임 제어

Entity(model=Grid(w+1, h+1), scale=w+1, color=color.black, x=w//2-0.5, y=h//2-0.5, z=0.1)
# 오목판 그리기

for y in range(h):
    for x in range(w):
        # 오목판의 각 숫자(좌표)마다 버튼을 만들어서 돌을 놓게한다.
        b = Button(parent=scene, position=(x, y), color=color.clear, model='circle', scale=0.9) 
        # 누른 버튼을 다 저장한다.
        board_buttons[y][x] = b

        # 클릭 가능 위치에 회색으로 돌을 표시
        def on_mouse_enter(b=b):
            if b.collision:
                b.color = color._100
        # 클릭 불가능하거나 범위를 벗어나면 투명으로 표시
        def on_mouse_exit(b=b):
            if b.collision:
                b.color = color.clear

        b.on_mouse_enter = on_mouse_enter
        b.on_mouse_exit = on_mouse_exit

        def on_click(b=b):
            # player 차례이기 때문에 클릭한 곳을 1(검은색)으로 표시
            b.text = '1'
            b.color = color.black
            # 더이상의 클릭을 방지
            b.collision = False

            # ursina에서는 좌표가 왼쪽아래가 0부터 시작
            # ursina <-> numpy 좌표 변환
            game.put(x=int(b.position.x), y=int(h - b.position.y - 1)) # start from top left

            # 이겼는지 확인
            won_player = game.check_won()

            if won_player > 0:
                end_session(won_player)

            game.next()

            # AI turn
            input = game.board.board.copy()
            # gomoku file에는 player turn이 1 / computer가 2
            # 이것을 각각 1과 -1로 변환
            input[(input != 1) & (input != 0)] = -1
            input[(input == 1) & (input != 0)] = 1

            # cnn에 맞도록 맨앞, 뒤를 한차원씩 늘려준다.
            input = np.expand_dims(input, axis=(0, -1)).astype(np.float32)

            # model에 input을 넣어주고 output을 받고
            # argmax를 통해 가장 confidence가 높은 값을 받는다.
            output = model.predict(input).squeeze()
            output = output.reshape((h, w))
            output_y, output_x = np.unravel_index(np.argmax(output), output.shape)
            
            # 모델 출력 값을 put을 통해 computer의 돌로 입력한다.
            game.put(x=output_x, y=output_y)

            # computer가 돌을 놓은 자리
            # text=2 / 돌은 흰색
            board_buttons[h - output_y - 1][output_x].text = '2'
            board_buttons[h - output_y - 1][output_x].text_color = color.black
            board_buttons[h - output_y - 1][output_x].color = color.white
            # 1번 입력 후 더이상 입력을 방지
            board_buttons[h - output_y - 1][output_x].collision = False

            won_player = game.check_won()

            if won_player > 0:
                end_session(won_player)

            # computer 차례가 끝나고 다시 player 차례로 넘겨준다.
            game.next()

            print(game.board)

        # 버튼 클릭시마다 on_click핸들러 실행
        b.on_click = on_click

def end_session(won_player):
    # 우승자 발생시, 우승자 표시
    Panel(z=1, scale=10, model='quad')
    t = Text(f'Player {won_player} won!', scale=3, origin=(0, 0), background=True)
    t.create_background(padding=(.5,.25), radius=Text.size/2)

app.run()