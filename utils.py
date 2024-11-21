from io import BytesIO
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from urllib import request
from models import RecommendedProblem
import boto3, os, dotenv
from PIL import Image
from reportlab.lib.utils import ImageReader


dotenv.load_dotenv()


# Heading 그리기
def draw_heading(c, orange_color=HexColor('#FC6C02'), lightgrey_color=HexColor('#D9D9D9')):
    logo = "모플"
    c.setFont("Pretendard-Regular", 40)
    c.setFillColor(orange_color)
    c.drawString(20, 785, logo)
    
    # 가로선
    c.setStrokeColor(lightgrey_color)
    c.setLineWidth(4)
    c.line(20, 770, 575, 770)


# 주황색 세로선 그리기
def draw_vertical_orange(canvas, x1, y1, x2, y2, color, width=3):
    canvas.setStrokeColor(color)
    canvas.setLineWidth(width)  # 선의 두께
    canvas.line(x1, y1, x2, y2)  # 세로선 좌표


# 점선 상자
def draw_dashed_box(c, x, y, width, height, orange_color=HexColor('#FC6C02')):
    c.setStrokeColor(orange_color)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.rect(x, y, width, height, stroke=1, fill=0)

def draw_page_number(c, page_number):
    c.setFont("Pretendard-Regular", 12)
    c.setFillColor(HexColor("#333333"))
    c.drawString(550, 20, f'{page_number}')

def convert_image_to_imagereader(image):
    """
    BytesIO 또는 PIL.Image 객체를 ImageReader로 변환
    """
    if isinstance(image, BytesIO):  # BytesIO 객체인 경우
        return ImageReader(image)
    elif isinstance(image, Image.Image):  # PIL.Image 객체인 경우
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')  # PNG 포맷으로 저장
        image_bytes.seek(0)  # 포인터를 처음으로 이동
        return ImageReader(image_bytes)
    else:
        raise TypeError("Unsupported image format. Must be BytesIO or PIL.Image")


# 문제별 페이지 생성
def draw_problem_page(c, data:RecommendedProblem, orange_color=HexColor('#FC6C02'), lightgrey_color=HexColor('#D9D9D9'), black_color=HexColor("#333333"), page_number=2, flag=0):
    A4_width, A4_height = A4
    
    draw_heading(c, orange_color, lightgrey_color)
    draw_page_number(c, page_number)
    
    # 세로선 그리기 (오렌지 색상)
    c.setDash([])
    draw_vertical_orange(c, 22, 755, 22, 730, orange_color)  # 세로선 좌표

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 20)

    if flag == 0:
        c.drawString(28, 736, "현재 등급에서 맞췄어야 하는 문제")  # 텍스트 위치 설정
    elif flag == 1:
        c.drawString(28, 735, "다음 등급을 위해 맞춰야 하는 문제")
    else:
        c.drawString(28, 735, "등급 다지기")

    draw_dashed_box(c, 22, 40, A4_width-60, A4_height-165)

    ## 문제 정보
    p_num_width = c.stringWidth(f'{data["problemNumber"]}번', "Pretendard-Bold", 28)

    box_width = p_num_width + 20
    box_height = 40
    box_x = 30
    box_y = 666

    # 박스 그리기 (배경)
    c.setDash([])
    c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
    c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
    c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

    # 텍스트 그리기
    c.setFont("Pretendard-Regular", 28)  # 글꼴과 크기 설정
    c.setFillColor(orange_color)
    c.drawString(box_x+10, box_y+10, f'{data["problemNumber"]}번')

    c.setFont("Pretendard-Regular", 18)
    c.setFillColor(black_color)
    c.drawString(130, 680, "난이도")
    c.drawString(250, 680, "정답률")
    c.drawString(400, 680, "문제등급")

    c.setFont("Pretendard-Bold", 18)
    c.setFillColor(orange_color)
    c.drawString(190, 680, f'{data["difficultLevel"]}')
    c.drawString(310, 680, f'{data["correctRate"]}%')
    c.drawString(470, 680, f'{data["rating"]}')

    res = request.urlopen(data["imageUrl"]).read()
    
    image_reader = convert_image_to_imagereader(Image.open(BytesIO(res)))

    # 원본 이미지 크기 가져오기
    img_width, img_height = image_reader.getSize()

    # 비율 계산: width를 기준으로 높이를 조정
    target_width = A4_width - 300
    scale = target_width / img_width
    scaled_width = target_width
    scaled_height = img_height * scale

    # 이미지를 가로 방향으로 정 가운데 위치시키기
    x = (A4_width - scaled_width) / 2
    
    c.drawImage(image_reader, x=x, y=A4_height-scaled_height-200, width=scaled_width, height=scaled_height)
