import cv2
import time
import random

cap = cv2.VideoCapture('muyaho.mp4')

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 영상의 가로길이 / 세로길이

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('output_%s.mp4' % time.time(), fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
#out = cv2.VideoWriter('output_%s.mp4' % time.time(), fourcc, cap.get(cv2.CAP_PROP_FPS)/2 , (w, h))
#영상의 속도조정가능


# cap.set(1, 프레임 인덱스) : 영상 재생 시작 프레임 지정

cap.set(1, 900)

while cap.isOpened():
    ret, img = cap.read()
    # 1프레임씩 동영상 불러오기

    if not ret:
        # 영상이 끝나면 ret = false
        break

    if random.random() > 0.9:
        # 이미지의 10퍼센트만 효과 적용
        theta = random.randint(-3, 3)
        # 회전 랜덤각도
        x, y = random.randint(-10, 10), random.randint(-10, 10)
        # 상하좌우 랜덤 이동범위

        M = cv2.getRotationMatrix2D(center=(w // 2, h // 2), angle=theta, scale=1.0)
        # cv2.getRotationMatrix2D : 로테이션 매트릭스를 쉽게 구하는 함수
        M[0, 2] += x
        M[1, 2] += y
        # 상화좌우의 랜덤이동 효과

        img = cv2.warpAffine(img, M=M, dsize=(w, h))
        # cv2.warpAffine() : 이미지의 기하학적 변형

    ig = cv2.GaussianBlur(img, ksize=(9, 9), sigmaX=0)
    # 이미지를 뿌옇게 하는 함수

    '''
    sigma_s: Range between 0 to 200. Default 60.
    sigma_r: Range between 0 to 1. Default 0.07.
    shade_factor: Range between 0 to 0.1. Default 0.02.
    '''
    gray, color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.05, shade_factor=0.015)
    # 이미지를 연필로 그린 효과를 내는 함수


    cv2.imshow('gray', gray)
    # cv2.imshow('color', color)

    out.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()