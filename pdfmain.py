import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from utils import draw_vertical_orange

if __name__ == "__main__":
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

    # 모플 로고
    logo = "모플"
    c.setFont("Pretendard-Regular", 40)
    c.setFillColor(orange_color)
    str_width = c.stringWidth(logo)
    c.drawString(20, 785, logo)
    
    # 가로선
    c.setStrokeColor(lightgrey_color)
    c.setLineWidth(4)
    c.line(20, 770, 575, 770)

    ##### 결과 #####
    # 세로선 그리기 (오렌지 색상)
    draw_vertical_orange(c, 22, height - 100, 22, height - 130, orange_color)  # 세로선 좌표
    
    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 24)
    c.drawString(30, height - 123, "결과")  # 텍스트 위치 설정

    
    # 점수
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 80)
    c.drawString(35, height - 230, "80")

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 80)
    c.drawString(135, height - 230, "점")

    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(164, height - 258, "점수")

    # 내 등급
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(245, height - 230, "3")

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(270, height - 230, "등급")

    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(280, height - 256, "내 등급")

    # 내 풀이 시간
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(392, height - 230, "1")
    c.drawString(440, height - 230, "10")

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

    # 점선 상자1
    c.setStrokeColor(orange_color)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.rect(30, 190, width - 60, 270, stroke=1, fill=0)

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

    # 점선 상자2
    c.setStrokeColor(orange_color)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.rect(30, 40, width - 60, 140, stroke=1, fill=0)

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

    
    c.save()
