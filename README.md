# Spotify Charts 台灣音樂聆聽趨勢分析

**Spotify Taiwan Music Listening Trend Analysis**

本專案以 Spotify Charts
的台灣排行榜資料為研究基礎，透過資料爬取、清理、曲目去重，以及串接 ISRC
與 ReccoBeats 音樂特徵，建立可供後續分析的資料集。

專案主要目的為觀察台灣 Spotify
排行榜中的歌曲變化，並從歌曲的音樂特徵探索不同時期的音樂聆聽趨勢。

## 專案目標

-   蒐集不同年份、週次與國家的 Spotify Charts 排行榜資料。
-   將週榜資料整理為月份層級的資料集。
-   建立年度及跨年度的唯一曲目清單。
-   取得歌曲的 ISRC 與 ReccoBeats 專屬識別 ID。
-   蒐集歌曲音樂特徵，供後續資料庫建置與分析使用。

## 資料流程

``` text
Spotify Charts
    │
    ▼
[1] 爬取排行榜資料
    爬資料/專案爬蟲.py
    │
    ▼
[2] 合併與整理資料
    清理用的code/clear_data_2.py
    清理用的code/clear_data2mon.2.py
    │
    ▼
[3] 建立唯一曲目清單
    清理用的code/year_uniq_track.py
    清理用的code/all_uniq_track.py
    │
    ▼
[4] 取得歌曲 ISRC
    爬資料/get_isrc_ms.py
    │
    ▼
[5] 取得 ReccoBeats Search ID
    爬資料/get_search_id.2.py
    │
    ▼
[6] 蒐集音樂特徵
    爬資料/get_music_features.py
    │
    ▼
[7] 資料庫建置與後續分析
    sql/
```

## 專案檔案架構

``` text
.
├── 爬資料/
│   ├── 專案爬蟲.py
│   ├── get_isrc_ms.py
│   ├── get_search_id.2.py
│   └── get_music_features.py
│
├── 清理用的code/
│   ├── clear_data_2.py
│   ├── clear_data2mon.2.py
│   ├── year_uniq_track.py
│   └── all_uniq_track.py
│
├── sql/
│   └── 資料庫建置與匯入相關檔案
│
└── README.md
```

> 上述架構依目前專案流程整理。實際輸出資料夾、檔案名稱與資料庫腳本，請以
> repository 中的內容為準。

## 執行流程

### Step 1：爬取 Spotify Charts 排行榜資料

**執行檔案：** `爬資料/專案爬蟲.py`

此程式用於爬取 Spotify Charts 排行榜，可指定：

  參數   說明                   範例
  ------ ---------------------- ------------------
  年份   欲蒐集的排行榜年份     `2023`
  週數   欲蒐集的排行榜週次     依程式設定輸入
  國家   國家／地區二位元代碼   `TW`、`US`、`JP`

國家代碼使用 ISO 3166-1 alpha-2
格式。爬取完成後，程式會自動建立資料夾並儲存檔案。

**注意事項**

-   網路連線、網站流量或網站回應狀況可能導致爬取失敗。
-   若資料未完整下載，請確認網路狀況後重新執行。
-   建議在進行清理前，先確認預期週次的檔案是否完整。

資料來源：[Spotify Charts](https://charts.spotify.com/)

### Step 2：清理與合併排行榜資料

此階段將原始週榜資料整理成適合後續月份分析的格式。

#### 2.1 兩兩合併

**執行檔案：** `清理用的code/clear_data_2.py`

將爬取完成的原始檔案進行兩兩合併，作為下一階段的資料整理基礎。

#### 2.2 合併為每年 12 個月份的資料

**執行檔案：** `清理用的code/clear_data2mon.2.py`

將前一步整理後的資料合併為年度月份檔案，以利後續分析每月曲目及音樂特徵。

**重要注意事項**

-   執行前請先確認各月份對應的檔案數量。
-   部分月份可能會有三個檔案的特殊情況。
-   由於分析單位為「月份」，遇到跨月資料時，請依照程式既有規則處理：不同月份的檔案統一跟隨前一個月份的檔案歸類。
-   請特別檢查特殊月份，避免月份歸屬錯誤。

### Step 3：建立唯一曲目清單

#### 3.1 建立年度唯一曲目

**執行檔案：** `清理用的code/year_uniq_track.py`

以年度為單位，整理該年度曾出現在排行榜中的唯一曲目。

#### 3.2 建立跨年度唯一曲目

**執行檔案：** `清理用的code/all_uniq_track.py`

將各年度的唯一曲目整合為跨年度總表，作為後續 ISRC 與音樂特徵蒐集的基礎。

### Step 4：取得歌曲 ISRC

**執行檔案：** `爬資料/get_isrc_ms.py`

此程式透過 Spotify Web API 查詢歌曲資訊，取得曲目的 ISRC（International
Standard Recording Code，國際標準錄音錄影資料代碼）。

**執行前準備**

請先依照程式使用的授權方式，設定 Spotify API 憑證。若使用 Client
Credentials Flow，通常需要：

-   `Client ID`
-   `Client Secret`
-   Access Token（由授權流程取得）

官方文件：

-   [Spotify Developer
    Dashboard](https://developer.spotify.com/dashboard)
-   [Spotify Web API
    官方文件](https://developer.spotify.com/documentation/web-api)
-   [Getting started with Web
    API](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
-   [Client Credentials
    Flow](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow)
-   [Search for Item
    API](https://developer.spotify.com/documentation/web-api/reference/search)

**注意事項**

-   請依照官方文件及程式實際需求設定憑證。
-   不要將 Client Secret、Access Token 或其他私密資訊提交至 GitHub。
-   建議使用環境變數或 `.env` 檔案管理憑證，並將 `.env` 加入
    `.gitignore`。
-   若歌曲搜尋結果不正確或未取得
    ISRC，請檢查歌曲名稱、歌手及版本是否匹配。

### Step 5：取得 ReccoBeats Search ID

**執行檔案：** `爬資料/get_search_id.2.py`

取得音樂特徵前，需要先查詢 ReccoBeats 對應的歌曲識別 ID。

此程式會讀取前一步產生的 ISRC 檔案，查詢對應的 Search
ID，並將結果儲存至新的資料檔案。

官方資源：

-   [ReccoBeats 官方網站](https://reccobeats.com/)
-   [ReccoBeats API 文件](https://reccobeats.com/docs/)

### Step 6：取得音樂特徵資料

**執行檔案：** `爬資料/get_music_features.py`

使用前一步取得的 ReccoBeats ID，蒐集歌曲的音樂特徵資料。

可能使用的特徵包含：

-   Energy
-   Valence
-   Danceability
-   Acousticness
-   Instrumentalness
-   Tempo
-   Loudness
-   Speechiness
-   Liveness

實際欄位以程式請求內容及 API 回傳結果為準。

ReccoBeats 音訊特徵文件：[Audio
Features](https://reccobeats.com/docs/apis/get-track-audio-features)

### Step 7：資料庫建置

完成資料蒐集與清理後，可參考專案中的 `sql/` 資料夾進行後續資料庫建置。

資料庫可依分析需求，建立排行榜、曲目識別資訊與音樂特徵之間的關聯，供後續查詢及視覺化使用。

## 使用工具與資料來源

  工具／來源           用途
  -------------------- ----------------------------------
  Python               資料爬取、清理與處理
  Spotify Charts       排行榜資料來源
  Spotify Web API      查詢歌曲資訊與 ISRC
  ReccoBeats API       查詢歌曲識別資訊及音樂特徵
  SQL                  資料庫建置與查詢
  Power BI / Tableau   後續資料視覺化（依實際使用情況）

## 研究方向

本專案以台灣 Spotify Charts 為主要研究對象，預計探討：

1.  台灣熱門歌曲在不同年份與月份的變化。
2.  排行榜曲目的音樂特徵分布。
3.  Energy、Valence 等特徵在不同時期的變化。
4.  排行榜變化與歌曲音樂特徵之間的關係。

本研究希望將排行榜資料轉化為可比較的音樂趨勢資訊，作為理解台灣流行音樂聆聽樣貌的資料基礎。

## 注意事項與資料使用聲明

-   本專案資料來自第三方平台，使用時請遵守 Spotify 與 ReccoBeats
    的服務條款及 API 使用規範。
-   爬蟲可能受到網路狀況、網站結構變動及請求限制影響。
-   歌曲版本、地區或資料庫收錄狀況可能造成 API 回傳差異。
-   請勿公開提交 API 私密憑證、個人帳號資訊或其他敏感資料。
-   本專案為個人研究與資料分析用途，分析結果應以實際蒐集資料及研究方法為依據。
