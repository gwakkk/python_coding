import numpy as np
import os
from glob import glob
from tqdm import tqdm


# Dataset from https://gomocup.org/results/

game_rule = 'Freestyle' 
# Freestyle, Fastgame, Standard, Renju 중 Freestyle 데이터 사용
base_path = '/Users/chan/Desktop/Git Upload/py_coding/Omok_AI/gomocup2020results/FreeStyle'
output_path = os.path.join('dataset', os.path.basename(base_path))
os.makedirs(output_path, exist_ok=True)

file_list = glob(os.path.join(base_path, '%s*/*.psq' % (game_rule, )))
# psq파일 로드

for index, file_path in enumerate(tqdm(file_list)):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        # line별 split

    w, h = lines[0].split(' ')[1].strip(',').split('x')
    # 첫번째 행의 정보중 가로, 세로길이를 제외하고는 불필요
    w, h = int(w), int(h)
    # 정수형 변경

    lines = lines[1:]
    # 첫줄 제외하고 넣어준다

    inputs, outputs = [], []
    board = np.zeros([h, w], dtype=np.int8)
    # 0으로 채워진 numpy array 바둑판 생성

    for i, line in enumerate(lines):
        if ',' not in line:
            break

        x, y, t = np.array(line.split(','), np.int8)

        # 한 턴씩 돌아가며 진행
        # 바뀔때마다 상대방과 나의 순서를 바꾸면서 데이터셋을 형성
        if i % 2 == 0:
            player = 1
        else:
            player = 2

        input = board.copy().astype(np.int8)
        # input(x) 이미 둔 수를 보는것
        # 내가 둔수는 1, 상대방이 둔수는 -1 로 표시
        input[(input != player) & (input != 0)] = -1
        input[(input == player) & (input != 0)] = 1

        output = np.zeros([h, w], dtype=np.int8)
        output[y-1, x-1] = 1
        # 입력데이터는 시작이 (1,1)이기 때문에 (0,0)으로 변경
        # output(y) 앞으로 두어야 할 수 
        # 순서에 상관없이 내가 두었던 자리나 두어야하는 자리는 1로 표시하고
        # 상대방이 둔 자리는 전부 -1로 표시한다

        # augmentation(좌우, 상하 반전 / 90도 씩 변경)
        for k in range(4):
            input_rot = np.rot90(input, k=k)
            output_rot = np.rot90(output, k=k)

            inputs.append(input_rot)
            outputs.append(output_rot)

            inputs.append(np.fliplr(input_rot))
            outputs.append(np.fliplr(output_rot))

            inputs.append(np.flipud(input_rot))
            outputs.append(np.flipud(output_rot))
        # roataion과 Flip을 통해 데이터 생성(12배를 늘릴 수 있다.)

        
        board[y-1, x-1] = player

    # .npz 형식으로 파일저장
    np.savez_compressed(os.path.join(output_path, '%s.npz' % (str(index).zfill(5))), inputs=inputs, outputs=outputs)
