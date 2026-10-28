#=======================================
#  此為專案爬蟲.2.py的登入檔案，幫助匯入餅乾
#=======================================
import json
class LogIN:
    def __init__(self, drive_name):
        self.drive_name=drive_name

    def import_cookie(self):
    
        with open('cookie.json','r',encoding='utf8')as f:
            cookies=json.load(f)
        for cookie in cookies:
            try:
                self.drive_name.add_cookie(cookie)
                print('加入cookie成功')
            except Exception as e:
                print(f"略過一個有問題的 cookie: {e}")
    
        self.drive_name.refresh()
        print('已進入登入狀態')
        return

