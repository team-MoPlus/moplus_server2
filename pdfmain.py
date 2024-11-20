import os, re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from models import DetailResultApplication
from utils import draw_dashed_box, draw_heading, draw_page_number, draw_problem_page, draw_vertical_orange

pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?"

def create_review_note(data: DetailResultApplication):
    # 현재 파일의 디렉토리 경로를 기준으로 폰트 경로 설정
    # base_dir = os.path.dirname(__file__)
    
    # 한글 폰트 등록
    pdfmetrics.registerFont(TTFont('Pretendard-Regular', "pdffonts/Pretendard-Regular.ttf"))
    pdfmetrics.registerFont(TTFont('Pretendard-Bold', "pdffonts/Pretendard-Bold.ttf"))
    pdfmetrics.registerFont(TTFont('Pretendard-Thin', "pdffonts/Pretendard-Thin.ttf"))
    c = canvas.Canvas("./output.pdf", pagesize=A4)
    width, height = A4  # (595.2755905511812, 841.8897637795277)
    

    # 색상 설정
    orange_color = HexColor('#FC6C02')
    lightgrey_color = HexColor('#D9D9D9')
    grey_color = HexColor('#828282')
    black_color = HexColor("#333333")

    draw_heading(c, orange_color, lightgrey_color)
    draw_page_number(c, "1")

    ##### 결과 #####
    # 세로선 그리기 (오렌지 색상)
    draw_vertical_orange(c, 22, height - 100, 22, height - 130, orange_color)  # 세로선 좌표
    
    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 24)
    c.drawString(30, height - 123, "결과")  # 텍스트 위치 설정

    
    # 점수
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 80)
    c.drawString(35, height - 230, f'{data["score"]}')

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 80)
    c.drawString(135, height - 230, "점")

    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(164, height - 258, "점수")

    # 내 등급
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(245, height - 230, f'{data["estimatedRatingGetResponses"][0]["estimatedRating"]}')

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(270, height - 230, "등급")

    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(280, height - 256, "내 등급")

    # 내 풀이 시간
    match = re.match(pattern, data["solvingTime"])
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(392, height - 230, f'{match.group(1) if match else 0}')
    c.drawString(440, height - 230, f'{match.group(2) if match else 0}')

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(408, height - 230, "h")
    c.drawString(482, height - 230, "m")
    
    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(418, height - 256, "내 풀이 시간")

    ##### 전체 틀린 문제 #####
    # 세로선 그리기 (오렌지 색상)
    draw_vertical_orange(c, 22, height - 284, 22, height - 314, orange_color)  # 세로선 좌표
    
    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 24)
    c.drawString(30, height - 307, "전체 틀린 문제")  # 텍스트 위치 설정

    ## 문제들
    text_y = 500
    for i, problem in enumerate(data["incorrectProblems"]):
        
        if i%5 == 0 and i > 0:
            text_y -= 30
        
        c.setFillColor(black_color)
        c.setFont("Pretendard-Regular", 24)
        p_num = f'{problem["problemNumber"]}번'
        c.drawString(25 + (i%5)*110, text_y, p_num)

        p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 24)

        box_width = 40
        box_height = 20
        box_x = 30 + (i%5)*110 + p_num_width
        box_y = text_y

        # 박스 그리기 (배경)
        c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
        c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
        c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

        # 텍스트 그리기
        c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
        c.setFillColor(orange_color)
        c.drawString(box_x + 6, box_y + 4, f'{problem["correctRate"]}%')  # 박스 안 텍스트 위치 조정

    # 점선 상자1
    draw_dashed_box(c, 30, 190, width - 60, 270)

    ### 현재 등급에서 맞췄어야 하는 문제 ###
    # 세로선 그리기 (오렌지 색상)
    c.setDash([])
    draw_vertical_orange(c, 40, 445, 40, 420, orange_color)  # 세로선 좌표

    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 20)
    c.drawString(48, 426, "현재 등급에서 맞췄어야 하는 문제")  # 텍스트 위치 설정
    c.setFillColor(grey_color)
    text = c.beginText(53, 400)
    text.setFont("Pretendard-Regular", 14)
    text.setTextOrigin(53, 400)
    text.textLine("현재 틀린 문제 중 현재 등급에서 다음 등급으로 넘어가기 위해서 반드시 공부하고")
    text.textLine("넘어가야하는 문제들이예요.")
    c.drawText(text)

    ## 현재 등급에서 맞췄어야 하는 문제
    text_y = 355
    for i, problem in enumerate(data["forCurrentRating"]):
        
        if i%5 == 0 and i > 0:
            text_y -= 30
        
        c.setFillColor(black_color)
        c.setFont("Pretendard-Regular", 18)
        p_num = f'{problem["problemNumber"]}번'
        c.drawString(45 + (i%5)*110, text_y, p_num)

        p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 18)

        box_width = 40
        box_height = 20
        box_x = 50 + (i%5)*110 + p_num_width
        box_y = text_y - 4

        # 박스 그리기 (배경)
        c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
        c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
        c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

        # 텍스트 그리기
        c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
        c.setFillColor(orange_color)
        c.drawString(box_x + 6, box_y + 5, f'{problem["correctRate"]}%')  # 박스 안 텍스트 위치 조정

    ### 다음 등급을 위해 맞춰야 하는 문제 ###
    # 세로선 그리기 (오렌지 색상)
    c.setDash([])
    draw_vertical_orange(c, 40, 311, 40, 286, orange_color)  # 세로선 좌표

    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 20)
    c.drawString(48, 292, "다음 등급을 위해 맞춰야 하는 문제")  # 텍스트 위치 설정

    c.setFillColor(grey_color)
    text = c.beginText(53, 266)
    text.setFont("Pretendard-Regular", 14)
    text.setTextOrigin(53, 266)
    text.textLine("다음 등급에서 맞춰야하는 문제들이예요.")
    c.drawText(text)

    text_y = 240
    for i, problem in enumerate(data["forNextRating"]):
        
        if i%5 == 0 and i > 0:
            text_y -= 30
        
        c.setFillColor(black_color)
        c.setFont("Pretendard-Regular", 18)
        p_num = f'{problem["problemNumber"]}번'
        c.drawString(45 + (i%5)*110, text_y, p_num)

        p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 18)

        box_width = 40
        box_height = 20
        box_x = 50 + (i%5)*110 + p_num_width
        box_y = text_y - 4

        # 박스 그리기 (배경)
        c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
        c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
        c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

        # 텍스트 그리기
        c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
        c.setFillColor(orange_color)
        c.drawString(box_x + 6, box_y + 5, f'{problem["correctRate"]}%')

    # 점선 상자2
    draw_dashed_box(c, 30, 40, width - 60, 140)

    ### 등급 다지기 ###
    # 세로선 그리기 (오렌지 색상)
    c.setDash([])
    draw_vertical_orange(c, 40, 166, 40, 141, orange_color)  # 세로선 좌표

    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 20)
    c.drawString(48, 147, "등급 다지기")  # 텍스트 위치 설정

    c.setFillColor(grey_color)
    text = c.beginText(53, 119)
    text.setFont("Pretendard-Regular", 14)
    text.setTextOrigin(53, 119)
    text.textLine("현재 등급 이상을 안정적으로 받기 위해 체크해볼 만한 문제예요.")
    c.drawText(text)

    text_y = 90
    for i, problem in enumerate(data["forBeforeRating"]):
        if i%5 == 0 and i > 0:
            text_y -= 30
        
        c.setFillColor(black_color)
        c.setFont("Pretendard-Regular", 18)
        p_num = f'{problem["problemNumber"]}번'
        c.drawString(45 + (i%5)*110, text_y, p_num)

        p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 18)

        box_width = 40
        box_height = 20
        box_x = 50 + (i%5)*110 + p_num_width
        box_y = text_y - 4

        # 박스 그리기 (배경)
        c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
        c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
        c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

        # 텍스트 그리기
        c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
        c.setFillColor(orange_color)
        c.drawString(box_x + 6, box_y + 5, f'{problem["correctRate"]}%')


    all_wrong_problems = data["forCurrentRating"] + data["forNextRating"] + data["forBeforeRating"]
    cnt1, cnt2, cnt3 = len(data["forCurrentRating"]), len(data["forNextRating"]), len(data["forBeforeRating"])

    page_num = 2
    
    
    for problem_data in data["forCurrentRating"]:
        c.showPage()
        draw_problem_page(c, data=problem_data, page_number=page_num, flag=0)
        page_num += 1

    for problem_data in data["forNextRating"]:
        c.showPage()
        draw_problem_page(c, data=problem_data, page_number=page_num, flag=1)
        page_num += 1

    for problem_data in data["forBeforeRating"]:
        c.showPage()
        draw_problem_page(c, data=problem_data, page_number=page_num, flag=2)
        page_num += 1
    
    c.save()

# create_review_note({
#   "testResultId": 2688,
#   "score": 83,
#   "solvingTime": "PT1H11M",
#   "averageSolvingTime": "PT1H13M10.588235294S",
#   "estimatedRatingGetResponses": [
#     {
#       "ratingProvider": "대성마이맥",
#       "estimatedRating": 2
#     },
#     {
#       "ratingProvider": "이투스",
#       "estimatedRating": 2
#     }
#   ],
#   "incorrectProblems": [
#     {
#       "problemNumber": "3",
#       "correctRate": 85
#     },
#     {
#       "problemNumber": "25",
#       "correctRate": 81
#     },
#     {
#       "problemNumber": "27",
#       "correctRate": 69
#     },
#     {
#       "problemNumber": "28",
#       "correctRate": 44
#     },
#     {
#       "problemNumber": "29",
#       "correctRate": 13
#     }
#   ],
#   "forCurrentRating": [{
#       "problemNumber": "3",
#       "difficultLevel": "중하",
#       "correctRate": 85,
#       "rating": "4등급",
#       "imageUrl": "https://s3-moplus.s3.ap-northeast-2.amazonaws.com/2025%ED%95%99%EB%85%84%EB%8F%84%20%EA%B3%A03%2010%EC%9B%94%20%EB%AA%A8%ED%8F%89%20%ED%99%95%EB%A5%A0%EA%B3%BC%20%ED%86%B5%EA%B3%84/738.png"
#     },
#     {
#       "problemNumber": "25",
#       "difficultLevel": "중하",
#       "correctRate": 81,
#       "rating": "4등급",
#       "imageUrl": "https://s3-moplus.s3.ap-northeast-2.amazonaws.com/2025%ED%95%99%EB%85%84%EB%8F%84%20%EA%B3%A03%2010%EC%9B%94%20%EB%AA%A8%ED%8F%89%20%ED%99%95%EB%A5%A0%EA%B3%BC%20%ED%86%B5%EA%B3%84/760.png"
#     }],
#   "forNextRating": [
#     {
#       "problemNumber": "28",
#       "difficultLevel": "상",
#       "correctRate": 44,
#       "rating": "1등급",
#       "imageUrl": "https://s3-moplus.s3.ap-northeast-2.amazonaws.com/2025%ED%95%99%EB%85%84%EB%8F%84%20%EA%B3%A03%2010%EC%9B%94%20%EB%AA%A8%ED%8F%89%20%ED%99%95%EB%A5%A0%EA%B3%BC%20%ED%86%B5%EA%B3%84/763.png"
#     }
#   ],
#   "forBeforeRating": [
#     {
#       "problemNumber": "3",
#       "difficultLevel": "중하",
#       "correctRate": 85,
#       "rating": "4등급",
#       "imageUrl": "https://s3-moplus.s3.ap-northeast-2.amazonaws.com/2025%ED%95%99%EB%85%84%EB%8F%84%20%EA%B3%A03%2010%EC%9B%94%20%EB%AA%A8%ED%8F%89%20%ED%99%95%EB%A5%A0%EA%B3%BC%20%ED%86%B5%EA%B3%84/738.png"
#     },
#     {
#       "problemNumber": "25",
#       "difficultLevel": "중하",
#       "correctRate": 81,
#       "rating": "4등급",
#       "imageUrl": "https://s3-moplus.s3.ap-northeast-2.amazonaws.com/2025%ED%95%99%EB%85%84%EB%8F%84%20%EA%B3%A03%2010%EC%9B%94%20%EB%AA%A8%ED%8F%89%20%ED%99%95%EB%A5%A0%EA%B3%BC%20%ED%86%B5%EA%B3%84/760.png"
#     },
#     {
#       "problemNumber": "27",
#       "difficultLevel": "중",
#       "correctRate": 69,
#       "rating": "3등급",
#       "imageUrl": "https://s3-moplus.s3.ap-northeast-2.amazonaws.com/2025%ED%95%99%EB%85%84%EB%8F%84%20%EA%B3%A03%2010%EC%9B%94%20%EB%AA%A8%ED%8F%89%20%ED%99%95%EB%A5%A0%EA%B3%BC%20%ED%86%B5%EA%B3%84/762.png"
#     }
#   ]
# })