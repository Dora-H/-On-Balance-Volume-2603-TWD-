'''此範例呈現2603淨額交易量
OBV is a cumulative total of volume (positive and negative).'''
import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md
import datetime as dt
from matplotlib.font_manager import FontProperties

# 將文字轉換成中文
mp.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
mp.rcParams['axes.unicode_minus'] = False

mp.figure("On Balance Volumes淨額成交量", facecolor="lightgrey", figsize=(16, 7))
mp.title("Oct/5 2020 - Jan/21 2021\n 2603.TWD 長榮淨額成交量/成交量 ", fontsize=20)
mp.xlabel("Dates 日期", fontsize=14)
mp.ylabel("Volumes(K) 成交量(萬）", fontsize=14)
mp.ylim(-80, 100)


# 日期轉換函數
def y2ce(ymd):
    ymd = str(ymd, encoding="utf-8")
    y, m, d = ymd.split("/")
    ymd = str(int(y)+1911) + "-" + m + "-" + d          # 將中華民國轉西元年
    ymd = dt.datetime.strptime(ymd, "%Y-%m-%d").date()
    return ymd

# 從資料中輸入日期、收盤價格、成交量
dates, close_prices, volumes = np.loadtxt("./2603.TWD.csv", delimiter=',',
                                          usecols=(1, 6, 7), unpack=True,
                                          dtype="M8[D],f4,f4",
                                          converters={1: y2ce})
# 找出每一天收盤價減去前一天的差額
diff_close_prices = np.diff(close_prices)
# 提取差額的正負數值
sign_close_prices = np.sign(diff_close_prices)
# 也可使用np.piecewise(來源數組，條件，條件成立取值) >> 返回目標數組(滿足條件的取出值)
sign_close_prices2 = np.piecewise(diff_close_prices, [diff_close_prices > 0,
                                                      diff_close_prices == 0,
                                                      diff_close_prices < 0],
                                                    [1, 0, -1])

# 以每天收盤價減去前一天收盤價＝利潤，以(以正負0符號分組，呈現)利潤*成交量=obv。故第一天的無法計算(前一天沒有數據)，從[1:]開始
obvs = volumes[1:]*sign_close_prices
obvs2 = volumes[1:]*sign_close_prices2

# 繪製網格線
ax = mp.gca()
ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MONDAY))
ax.xaxis.set_minor_locator(md.DayLocator())
ax.yaxis.set_minor_locator(mp.MultipleLocator(10))
ax.xaxis.set_major_formatter(md.DateFormatter('%d-%b'))
mp.tick_params(labelsize=10)
mp.xticks(rotation=35)
mp.grid(which='both', linestyle=":")

# 將成交量除以"萬"單位呈現
obvs2 /= 10000
volumes /= 10000

# 繪製長條圖
mp.bar(dates[1:], obvs2, 0.8, color="limegreen", label="OBV(淨額成交量)", zorder=3)
mp.bar(dates, volumes, 0.8, color='coral', label="Volumes成交量", zorder=3)
mp.text(dates[10], 50, s='20210121\nDora practise.', fontsize=20, alpha=0.15)
mp.legend()
mp.show()
