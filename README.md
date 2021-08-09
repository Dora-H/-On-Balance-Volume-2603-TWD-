# -On-Balance-Volume-2603-TWD-
Uses volume flow to predict changes in stock price. 
OBV is a cumulative total of volume (positive and negative).

## Requirements
● Python 3    
● numpy   
● matplotlib   
● datetime


## Function
● y2ce    

## 基本設定 
#### 字型設定 : 使圖片說明呈現中文(微軟正黑字體)
    mp.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
    mp.rcParams['axes.unicode_minus'] = False


#### 標題設定 : 資料圖片標題、背景顏色(淺灰)、字體大小(20) 
    mp.figure("On Balance Volumes淨額成交量", facecolor="lightgrey", figsize=(16, 7))
    mp.title("Oct/5 2020 - Jan/21 2021\n 2603.TWD 長榮淨額成交量/成交量 ", fontsize=20)


#### 圖示x、y軸設定 、字體大小設定(14)、y軸由-80~100之間設定
    mp.xlabel("Dates 日期", fontsize=14)
    mp.ylabel("Volumes(K) 成交量(萬）", fontsize=14)
    mp.ylim(-80, 100)


## 輸入資料
#### 依據開盤價、最高價、最低價、收盤價使用numpy.loadtxt將資料傳入csv，須先呼叫函數 y2ce
    dates, close_prices, volumes = np.loadtxt("./2603.TWD.csv", delimiter=',',
                                          usecols=(1, 6, 7), unpack=True,
                                          dtype="M8[D],f4,f4",
                                          converters={1: y2ce})


## 函數 
#### y2ce 函數 : 轉換日期類型(將中華民國轉西元年)
    def y2ce(ymd):
        ymd = str(ymd, encoding="utf-8")
        y, m, d = ymd.split("/")
        ymd = str(int(y)+1911) + "-" + m + "-" + d          
        ymd = dt.datetime.strptime(ymd, "%Y-%m-%d").date()
        return ymd
        
        
#### 找出每一天收盤價減去前一天的差額
    diff_close_prices = np.diff(close_prices)
#### 提取差額的正負數值
    sign_close_prices = np.sign(diff_close_prices)
#### 也可使用np.piecewise(來源數組，條件，條件成立取值) >> 返回目標數組(滿足條件的取出值)
    sign_close_prices2 = np.piecewise(diff_close_prices, [diff_close_prices > 0,
                                                          diff_close_prices == 0,
                                                          diff_close_prices < 0],
                                                        [1, 0, -1])

#### 以每天收盤價減去前一天收盤價＝利潤，以(以正負0符號分組，呈現)利潤*成交量=obv。故第一天的無法計算(前一天沒有數據)，從[1:]開始
    obvs = volumes[1:]*sign_close_prices
    obvs2 = volumes[1:]*sign_close_prices2



## 設定格線繪製
#### 設定x軸主要刻度(依據每周周一，不含周末)
    ax = mp.gca()
    ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MONDAY))
#### 設定次要刻度
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.yaxis.set_minor_locator(mp.MultipleLocator(10))
#### 設定X軸主刻度顯示方式(日期/月份英文縮寫)
    ax.xaxis.set_major_formatter(md.DateFormatter('%d-%b'))
#### 設定標籤字體大小(10)、x軸上標籤旋轉35度、雙向格線虛線表示
    mp.tick_params(labelsize=10)
    mp.xticks(rotation=35)
    mp.grid(which='both', linestyle=":")


#### 將成交量除以"萬"單位呈現
    obvs2 /= 10000
    volumes /= 10000


## 圖形繪製
#### 繪製成交量使用BAR長條圖呈現
    mp.bar(dates[1:], obvs2, 0.8, color="limegreen", label="OBV(淨額成交量)", zorder=3)
    mp.bar(dates, volumes, 0.8, color='coral', label="Volumes成交量", zorder=3)
    
## 呈現
#### 在圖示日期第12個位置上標示: 日期/名字 practise.浮水印，字體大小為20，透明度0.15
    mp.text(dates[10], 50, s='20210121\nDora practise.', fontsize=20, alpha=0.15)
    mp.legend()
    mp.show()
![OBV淨額成交量](https://user-images.githubusercontent.com/70878758/128661980-62733937-f3ab-4863-b2df-7fec8a49064b.png)

