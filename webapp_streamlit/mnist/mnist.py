import cv2
from tensorflow.keras.models import load_model
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

# rerun : streamlit이 웹페이지를 최신상태로 갱신하는 과정
# 모델을 한번만 로드하기 위하여 사용
@st.cache(allow_output_mutation=True)

# 기존의 mnist model을 활용
def load():
    return load_model('pre_model.h5')
model = load()

st.write('# MNIST Recognizer')

CANVAS_SIZE = 192

col1, col2 = st.beta_columns(2)
# st.beta_columns : streamlit에서 레이아웃을 지정할 수 있게 하는 코드
# 칼럼으로 레이아웃을 지정


# 설정을 통해 그림을 그릴 수 있게 해준다.(숫자)
with col1:
    canvas = st_canvas(
        fill_color='#000000',
        stroke_width=20,
        stroke_color='#FFFFFF',
        background_color='#000000',
        width=CANVAS_SIZE,
        height=CANVAS_SIZE,
        drawing_mode='freedraw',
        key='canvas'
    )

if canvas.image_data is not None:
    img = canvas.image_data.astype(np.uint8)
    # 이미지 데이터 형태로 변환
    img = cv2.resize(img, dsize=(28, 28))
    # mnist와 같은 28*28 사이즈 변환
    preview_img = cv2.resize(img, dsize=(CANVAS_SIZE, CANVAS_SIZE), interpolation=cv2.INTER_NEAREST)
    # 사용자가 작성한 이미지를 preview로 보여준다.

    col2.image(preview_img)

    # 모델의 input 설정으로 넣고 예측
    x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x = x.reshape((-1, 28, 28, 1))
    y = model.predict(x).squeeze()

    # argmax를 통한 분류 / 막대차트를 통한 가시화
    st.write('## Result: %d' % np.argmax(y))
    st.bar_chart(y)