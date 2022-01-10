# bahamut-exporter

## 功能

匯出巴哈姆特文章中的所有樓層和留言到一份全新的 HTML 檔案

樓層一頁到底，留言也不需要手動展開，適合搭配瀏覽器的 Ctrl + F 快速搜尋字串

## 安裝

```
$ pip install -r requirements.txt

$ python setup.py install
```

## 使用

```
$ bahamutexporter -u https://forum.gamer.com.tw/C.php?bsn=00000&snA=00000 > output.html
```
