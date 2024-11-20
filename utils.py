
# 주황색 세로선 그리기
def draw_vertical_orange(canvas, x1, y1, x2, y2, color, width=3):
    canvas.setStrokeColor(color)
    canvas.setLineWidth(width)  # 선의 두께
    canvas.line(x1, y1, x2, y2)  # 세로선 좌표
