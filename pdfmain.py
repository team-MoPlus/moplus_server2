import os, re, io
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from models import DetailResultApplication
from utils import draw_dashed_box, draw_heading, draw_page_number, draw_problem_page, draw_vertical_orange

pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?"

def create_review_note(data: DetailResultApplication, file_name: str, buffer):

    # 한글 폰트 등록
    pdfmetrics.registerFont(TTFont('Pretendard-Regular', "pdffonts/Pretendard-Regular.ttf"))
    pdfmetrics.registerFont(TTFont('Pretendard-Bold', "pdffonts/Pretendard-Bold.ttf"))
    pdfmetrics.registerFont(TTFont('Pretendard-Thin', "pdffonts/Pretendard-Thin.ttf"))
    c = canvas.Canvas(buffer, pagesize=A4)
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
    c.drawString(35, height - 220, f'{data.score}')
    score_width = c.stringWidth(f'{data.score}', "Pretendard-Regular", 80)

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 60)
    c.drawString(35 + score_width, height - 217, "점")

    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(164, height - 248, "점수")

    # 내 등급
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(245, height - 220, f'{data.estimatedRatingGetResponses[0].estimatedRating}')

    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 30)
    c.drawString(270, height - 220, "등급")

    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(280, height - 246, "내 등급")

    # 내 풀이 시간
    match = re.match(pattern, data.solvingTime)
    h, m = f'{match.group(1) if match and match.group(1) else 0}', f'{match.group(2) if match and match.group(2) else 0}'
    c.setFillColor(orange_color)
    c.setFont("Pretendard-Regular", 40)
    c.drawString(392, height - 220, h)
    c.drawString(440, height - 220, m)


    c.setFillColor(black_color)
    c.setFont("Pretendard-Regular", 36)
    h_width = c.stringWidth(h, "Pretendard-Regular", 40)
    c.drawString(392+h_width, height - 220, "h")

    m_width = c.stringWidth(m, "Pretendard-Regular", 40)
    c.drawString(440+m_width, height - 220, "m")
    
    c.setFillColor(grey_color)
    c.setFont("Pretendard-Regular", 20)
    c.drawString(418, height - 246, "내 풀이 시간")

    ##### 전체 틀린 문제 #####
    # 세로선 그리기 (오렌지 색상)
    draw_vertical_orange(c, 22, height - 284, 22, height - 314, orange_color)  # 세로선 좌표
    
    c.setFillColor(black_color)
    c.setFont("Pretendard-Bold", 24)
    c.drawString(30, height - 307, "전체 틀린 문제")  # 텍스트 위치 설정

    ## 문제들
    text_y = 500
    if len(data.incorrectProblems) <= 10:
        for i, problem in enumerate(data.incorrectProblems):
            
            if i%5 == 0 and i > 0:
                text_y -= 30
            
            c.setFillColor(black_color)
            c.setFont("Pretendard-Regular", 20)
            p_num = f'{problem.problemNumber}번'
            c.drawString(25 + (i%5)*105, text_y, p_num)

            p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 24)

            box_width = 40
            box_height = 20
            box_x = 24 + (i%5)*105 + p_num_width
            box_y = text_y - 3

            # 텍스트 그리기
            c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
            c.setFillColor(orange_color)
            c.drawString(box_x + 6, box_y + 4, f'{int(problem.correctRate)}%')  # 박스 안 텍스트 위치 조정
            rate_width = c.stringWidth(f'{int(problem.correctRate)}%', "Pretendard-Regular", 14)

            # 박스 그리기 (배경)
            c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
            c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
            c.roundRect(box_x, box_y, rate_width + 2, box_height, radius=4, stroke=1, fill=0)

            
        else:
            for i, problem in enumerate(data.incorrectProblems):
                if i%5 == 0 and i > 0:
                    text_y -= 30
                
                c.setFillColor(black_color)
                c.setFont("Pretendard-Regular", 20)
                p_num = f'{problem.problemNumber}번'
                c.drawString(25 + (i%5)*105, text_y, p_num)

                p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 24)

                box_width = 40
                box_height = 20
                box_x = 24 + (i%5)*105 + p_num_width
                box_y = text_y - 3

                # 박스 그리기 (배경)
                c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
                c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
                c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

                # 텍스트 그리기
                c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
                c.setFillColor(orange_color)
                c.drawString(box_x + 6, box_y + 4, f'{int(problem.correctRate)}%')  # 박스 안 텍스트 위치 조정
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

    if len(data.forCurrentRating) == 0:
        c.setFillColor(HexColor("#95E0BB"))
        c.setFont("Pretendard-Bold", 20)
        c.drawString(52, 348, "모두 맞았어요!")
    else:
        text_y = 355
        for i, problem in enumerate(data.forCurrentRating):
            
            if i%5 == 0 and i > 0:
                text_y -= 30
            
            c.setFillColor(black_color)
            c.setFont("Pretendard-Regular", 18)
            p_num = f'{problem.problemNumber}번'
            c.drawString(45 + (i%5)*105, text_y, p_num)

            p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 18)

            box_width = 40
            box_height = 20
            box_x = 50 + (i%5)*105 + p_num_width
            box_y = text_y - 4

            # 박스 그리기 (배경)
            c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
            c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
            c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

            # 텍스트 그리기
            c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
            c.setFillColor(orange_color)
            c.drawString(box_x + 6, box_y + 5, f'{int(problem.correctRate)}%')  # 박스 안 텍스트 위치 조정

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

    if len(data.forNextRating) == 0:
        c.setFillColor(HexColor("#95E0BB"))
        c.setFont("Pretendard-Bold", 20)
        c.drawString(52, 230, "모두 맞았어요!")
    else:
        text_y = 240
        for i, problem in enumerate(data.forNextRating):
            
            if i%5 == 0 and i > 0:
                text_y -= 30
            
            c.setFillColor(black_color)
            c.setFont("Pretendard-Regular", 18)
            p_num = f'{problem.problemNumber}번'
            c.drawString(45 + (i%5)*105, text_y, p_num)

            p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 18)

            box_width = 40
            box_height = 20
            box_x = 50 + (i%5)*105 + p_num_width
            box_y = text_y - 4

            # 박스 그리기 (배경)
            c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
            c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
            c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

            # 텍스트 그리기
            c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
            c.setFillColor(orange_color)
            c.drawString(box_x + 6, box_y + 5, f'{int(problem.correctRate)}%')

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
    text.textLine("현재 등급 대비 난이도가 낮은 문제예요. 다시 한번 풀어보세요.")
    c.drawText(text)

    if len(data.forBeforeRating) == 0:
        c.setFillColor(HexColor("#95E0BB"))
        c.setFont("Pretendard-Bold", 20)
        c.drawString(52, 83, "모두 맞았어요!")
    else:
        text_y = 90
        for i, problem in enumerate(data.forBeforeRating):
            if i%5 == 0 and i > 0:
                text_y -= 30
            
            c.setFillColor(black_color)
            c.setFont("Pretendard-Regular", 18)
            p_num = f'{problem.problemNumber}번'
            c.drawString(45 + (i%5)*105, text_y, p_num)

            p_num_width = c.stringWidth(p_num, "Pretendard-Regular", 18)

            box_width = 40
            box_height = 20
            box_x = 50 + (i%5)*105 + p_num_width
            box_y = text_y - 4

            # 박스 그리기 (배경)
            c.setLineWidth(1)  # 테두리 두께 설정 (얇게)
            c.setStrokeColor(HexColor("#FFA500"))  # 주황색 테두리
            c.roundRect(box_x, box_y, box_width, box_height, radius=4, stroke=1, fill=0)

            # 텍스트 그리기
            c.setFont("Pretendard-Regular", 14)  # 글꼴과 크기 설정
            c.setFillColor(orange_color)
            c.drawString(box_x + 6, box_y + 5, f'{int(problem.correctRate)}%')


    page_num = 2
    
    
    for problem_data in data.forCurrentRating:
        c.showPage()
        draw_problem_page(c, data=problem_data, page_number=page_num, flag=0)
        page_num += 1

    for problem_data in data.forNextRating:
        c.showPage()
        draw_problem_page(c, data=problem_data, page_number=page_num, flag=1)
        page_num += 1

    for problem_data in data.forBeforeRating:
        c.showPage()
        draw_problem_page(c, data=problem_data, page_number=page_num, flag=2)
        page_num += 1
    
    c.save()

    # 버퍼의 시작 위치로 이동
    buffer.seek(0)

    headers = {
        f"Content-Disposition": "attachment; filename={file_name}.pdf",  # 파일명 설정
    }

    # StreamingResponse로 PDF 반환
    return StreamingResponse(buffer, headers=headers, media_type="application/pdf")
