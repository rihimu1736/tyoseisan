from flask import Flask
from datetime import datetime, date
from flask import request
import calendar

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def show_datetime():
    now = datetime.now()
    time = now.strftime('%H時%M分%S秒')
    
    # 月の選択を先に取得
    selected_month = request.form.get('month', '4')
    
    # 月の値から数字のみを取得（"1月" → "1"）
    if "月" in str(selected_month):
        selected_month = selected_month.replace("月", "")
    
    # 各月の最終日を設定
    days_in_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    
    # 選択された月の最大日数を取得
    max_days = days_in_month[int(selected_month)]
    
    # 月が変更された場合は日付を初期化、そうでない場合は選択値を使用
    if 'month' in request.form:
        if request.form.get('start_day') is None:
            selected_start_day = '1'
            selected_end_day = str(max_days)
        else:
            selected_start_day = request.form.get('start_day')
            selected_end_day = request.form.get('end_day')
    else:
        selected_start_day = request.form.get('start_day', '1')
        selected_end_day = request.form.get('end_day', str(max_days))
    
    # 曜日の配列
    weekdays = ['日', '月', '火', '水', '木', '金', '土']

    # 祝日の設定
    holidays = {
        1: [1, 8],  # 元日、成人の日
        2: [11, 23],  # 建国記念日、天皇誕生日
        3: [21],  # 春分の日
        4: [29],  # 昭和の日
        5: [3, 4, 5],  # 憲法記念日、みどりの日、こどもの日
        7: [17],  # 海の日
        8: [11],  # 山の日
        9: [18, 23],  # 敬老の日、秋分の日
        10: [9],  # スポーツの日
        11: [3, 23]  # 文化の日、勤労感謝の日
    }
    
    # 2025年の指定された月の最初の曜日を取得（0=月曜日, 6=日曜日）
    first_day_of_week = calendar.weekday(2025, int(selected_month), 1)
    # カレンダーモジュールは月曜日始まりなので、日曜日始まりに調整
    first_day_of_week = (first_day_of_week + 1) % 7
    
    months = [f"{i}月" for i in range(1, 13)]
    
    month_options = ""
    for i, month in enumerate(months, 1):
        selected = "selected" if str(i) == selected_month else ""
        month_options += f'<option value="{i}" {selected}>{month}</option>'
    
    # カレンダー形式の日付選択用のテーブルを作成（開始日用）
    start_calendar = '<table border="1" class="calendar-table">'
    start_calendar += '<tr><th>日</th><th>月</th><th>火</th><th>水</th><th>木</th><th>金</th><th>土</th></tr>'
    day = 1
    start_calendar += '<tr>'
    
    # 月初めまでの空白を追加
    for i in range(first_day_of_week):
        start_calendar += '<td></td>'
    
    # 日付を追加（開始日用）
    for i in range(first_day_of_week, 7):
        if day <= max_days:
            holiday_text = "(祝)" if int(selected_month) in holidays and day in holidays[int(selected_month)] else ""
            start_calendar += f'''<td class="calendar-cell">
                <input type="radio" name="start_day" value="{day}" {"checked" if str(day) == selected_start_day else ""}>
                <span>{day}{holiday_text}</span>
            </td>'''
            day += 1
    
    start_calendar += '</tr>'
    
    while day <= max_days:
        start_calendar += '<tr>'
        for i in range(7):
            if day <= max_days:
                holiday_text = "(祝)" if int(selected_month) in holidays and day in holidays[int(selected_month)] else ""
                start_calendar += f'''<td class="calendar-cell">
                    <input type="radio" name="start_day" value="{day}" {"checked" if str(day) == selected_start_day else ""}>
                    <span>{day}{holiday_text}</span>
                </td>'''
                day += 1
            else:
                start_calendar += '<td></td>'
        start_calendar += '</tr>'
    
    start_calendar += '</table>'

    # カレンダー形式の日付選択用のテーブルを作成（終了日用）
    end_calendar = '<table border="1" class="calendar-table">'
    end_calendar += '<tr><th>日</th><th>月</th><th>火</th><th>水</th><th>木</th><th>金</th><th>土</th></tr>'
    day = 1
    end_calendar += '<tr>'
    
    for i in range(first_day_of_week):
        end_calendar += '<td></td>'
    
    for i in range(first_day_of_week, 7):
        if day <= max_days:
            holiday_text = "(祝)" if int(selected_month) in holidays and day in holidays[int(selected_month)] else ""
            end_calendar += f'''<td class="calendar-cell">
                <input type="radio" name="end_day" value="{day}" {"checked" if str(day) == selected_end_day else ""}>
                <span>{day}{holiday_text}</span>
            </td>'''
            day += 1
    
    end_calendar += '</tr>'
    
    while day <= max_days:
        end_calendar += '<tr>'
        for i in range(7):
            if day <= max_days:
                holiday_text = "(祝)" if int(selected_month) in holidays and day in holidays[int(selected_month)] else ""
                end_calendar += f'''<td class="calendar-cell">
                    <input type="radio" name="end_day" value="{day}" {"checked" if str(day) == selected_end_day else ""}>
                    <span>{day}{holiday_text}</span>
                </td>'''
                day += 1
            else:
                end_calendar += '<td></td>'
        end_calendar += '</tr>'
    
    end_calendar += '</table>'

    # 決定ボタンが押された場合の処理
    schedule_display = ""
    if request.method == 'POST':
        start = int(selected_start_day)
        end = int(request.form.get('end_day', selected_end_day))  # フォームから直接終了日を取得
        for day in range(start, end + 1):
            weekday = calendar.weekday(2025, int(selected_month), day)
            weekday = (weekday + 1) % 7
            is_weekday = 1 <= weekday <= 5
            holiday_text = "(祝)" if int(selected_month) in holidays and day in holidays[int(selected_month)] else ""
            
            if is_weekday and not (int(selected_month) in holidays and day in holidays[int(selected_month)]):
                schedule_display += f'{day}日({weekdays[weekday]}){holiday_text} 前枠\n後枠\n'
            else:
                time_slots = ["8:45-9:45", "9:45-10:45", "10:45-11:45", "12:15-13:15", "13:15-14:15", "14:15-15:15", "15:45-16:45", "16:45-17:45", "17:45-18:45"]
                schedule_display += f'{day}日({weekdays[weekday]}){holiday_text} {time_slots[0]}\n'
                for slot in time_slots[1:]:
                    schedule_display += f'{slot}\n'
    
    return f'''
    <html>
    <head>
        <title>調整さん用コピペ作成（2025年）</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }}
            .calendar-table {{
                border-collapse: collapse;
                margin: 20px auto;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .calendar-table th {{
                background-color: #4CAF50;
                color: white;
                padding: 12px;
            }}
            .calendar-cell {{
                padding: 10px;
                text-align: center;
                border: 1px solid #ddd;
            }}
            .calendar-cell:hover {{
                background-color: #f0f0f0;
            }}
            select {{
                padding: 8px;
                font-size: 16px;
                border-radius: 4px;
                border: 1px solid #ddd;
            }}
            input[type="submit"] {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                display: block;
                margin: 0 auto;
            }}
            input[type="submit"]:hover {{
                background-color: #45a049;
            }}
            #schedule_display {{
                white-space: pre;
                text-align: center;
                font-family: monospace;
                margin: 20px auto;
                background-color: white;
                padding: 15px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: inline-block;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <h1>調整さん用コピペ作成（2025年）</h1>
        <form method="post">
            <select name="month" onchange="this.form.submit()">
                {month_options}
            </select>
            <h3>選択された月: 2025年{selected_month}月</h3>
            <p>開始日を選択してください：</p>
            {start_calendar}
            <p>終了日を選択してください：</p>
            {end_calendar}
            <br><br>
            <input type="submit" value="決定">
        </form>
        <hr>
        <div style="text-align: center;">
            <div id="schedule_display">{schedule_display}</div>
        </div>
        <hr>
        <p>現在時刻: {time}</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
