# StockHelper

# 啟動專案影片
[![Watch the video](https://free.com.tw/blog/wp-content/uploads/2016/10/%E5%B5%8C%E5%85%A5-YouTube-%E5%BD%B1%E7%89%87%E7%82%BA%E9%9F%B3%E6%A8%82%E6%92%AD%E6%94%BE%E5%99%A8%E6%95%99%E5%AD%B8%EF%BC%8C%E5%83%85%E4%BF%9D%E7%95%99%E9%9F%B3%E6%A8%82%E9%BB%9E%E6%93%8A%E8%87%AA%E5%8B%95%E6%92%AD%E6%94%BEyoutube-audio-player-icon.png)](https://www.youtube.com/watch?v=SfFf1UMy3Vk)
  ```
  # 首先要安裝: git, docker, docker-compose
  # git clone 此專案，專案目錄下會看到docker-compose.yml
  docker-compose up -d
  
  # 因為google oauth一定要綁domain，因此綁定的domain: www.stockhelper.com.tw
  # 使用ip:port連線，會無法登入，進到host更改，example: 35.215.134.213 www.stockhelper.com.tw
  ```
  <備註>
  - [windows更改host](https://www.albert-yu.com/blog/windows-10-%E4%BF%AE%E6%94%B9%E7%B3%BB%E7%BB%9F-hosts-%E8%A8%AD%E5%AE%9A%E5%9C%96%E6%96%87%E6%95%99%E5%AD%B8/)
  - 資料庫的股票資料只有0050, 2892
# 整體架構
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/Stockhelper_architecture.png)
- 服務皆使用docker container開啟，因為移動環境時方便，避免更換電腦，因為套件的問題，導致無法開啟專案。
- 服務架設於GCP，因為GCP提供300美元的試用期，以及對外IP，讓客戶可以連入。

Container | Function | Port | internal_network
------------ | ------------- | ------------- | -------------
Vue | 前端顯現網頁 | 8080 | 172.18.0.113
Flask | 提供API，功能是接收前端條件，對資料庫進行CRUD，並整理成前端所需格式的資料。 | 8889 | 172.18.0.112
MariaDB | 存放資料 | 3306 | 172.18.0.101
AI |LSTM: 預測未來連續五天的價格。 DNN: 預測三天後的價格漲跌機率。| | 172.18.0.114
Crawler | 爬蟲: 鉅亨、台灣證券交易所 | | 172.18.0.115
# Sitemap
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/StockHelper_SiteMap.png)

# DB-Diagram
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/Stockhelper_DBdiagram.png)

# 實際頁面
- 登入
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/StockHelper_Login.jpg)
- 使用者庫存
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/StockHelper_UserInfo.jpg)
- 股票數據
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/StockHelper_StockData.jpg)
- 智能預測
![image](https://github.com/Joyang0419/StockHelper/blob/master/readme_file/StockHelper_AIpredict.png)
