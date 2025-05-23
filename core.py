import requests
import re
from dataclasses import dataclass

@dataclass
class Cookies:
    core_mail: str
    core_mail_referer: str
    sid: str
    

class PostMan:
    cookies = Cookies(
        core_mail="", sid="", core_mail_referer=r"https%3A%2F%2Fdwm6.digiwin.com%2F"
    )

    _user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

    

    def __init__(self, username, password, email_content):
        self.username = username
        self.password = password
        self.email_content = email_content

    def _get_cookie_line(self):
        return f"face=undefined; locale=zh_CN; Coremail={self.cookies.core_mail}; CoremailReferer=https%3A%2F%2Fdwm6.digiwin.com%2F; Coremail.sid={self.cookies.sid}"

    def _load_sid(self, data):
        # sid是token，用于后续请求
        sid_match = re.search(r"sid=([A-Za-z0-9]+)", data)
        if sid_match:
            sid = sid_match.group(1)
            # 添加sid到cookies
            self.cookies.sid = sid
            return sid
        else:
            return None

    def login(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": self._user_agent,
        }
        data = f"locale=zh_CN&nodetect=false&destURL=&supportLoginDevice=true&accessToken=&timestamp=&signature=&nonce=&device=%7B%22uuid%22%3A%22webmail_1747909434426%22%2C%22imie%22%3A%22webmail_1747909434426%22%2C%22friendlyName%22%3A%22chrome+136%22%2C%22model%22%3A%22windows%22%2C%22os%22%3A%22windows%22%2C%22osLanguage%22%3A%22zh-CN%22%2C%22deviceType%22%3A%22Webmail%22%7D&supportDynamicPwd=true&uid={self.username}&password={self.password}&hiddenUseSSL=true&action%3Alogin="
        url = "https://dwm6.digiwin.com/coremail/index.jsp?cus=1"
        rep = requests.post(url, headers=headers, data=data)
        if self._load_sid(rep.text):
            self.cookies.core_mail = rep.cookies.get("Coremail")
            return True
        return False

    def get_mail_id(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self._get_cookie_line(),
            "User-Agent": self._user_agent,
        }
        url = f"https://dwm6.digiwin.com/coremail/XT5/jsp/mail.jsp?func=getInitCompose&sid={self.cookies.sid}"
        data = r"ctype=normal&to=&isHtml=1&content=&subject=undefined&returnInfo=false"
        rep = requests.post(url, headers=headers, data=data)
        data = rep.json()
        if data["code"] == "S_OK":
            id = data["var"]["id"]
            return id
        return None

    def send_email(self, id, content):
        headers = {
            "Content-Type": "text/x-json",
            "Cookie": self._get_cookie_line(),
            "User-Agent": self._user_agent,
        }
        data = (
            '{"attrs":'
            + content
            + ',"action":"deliver","id":"'
            + id
            + '","returnInfo":true,"autosaveHitCounter":true,"encryptPassword":""}'
        )
        print(data)
        url = f"https://dwm6.digiwin.com/coremail/s/json?func=mbox:compose&sid={self.cookies.sid}&isUserConfirmed=true"
        rep = requests.post(url, headers=headers, data=data)
        return rep.json()

    def do_send_email(self):
        self.login()
        id = self.get_mail_id()
        return self.send_email(id, self.email_content)


if __name__ == "__main__":
    pm = PostMan(
        username="malyb",
        password="DGW23574",
        email_content=r"""{"scheduleDate":null,"account":"\"马路遥 Luyao Ma\" <malyb@digiwin.com>","to":["\"贾旭光 xuguang jia\" <jiaxg@digiwin.com>",
"\"翟高峰 gaofeng zhai\" <zhaigf@digiwin.com>"],"cc":[],"bcc":[],"showOneRcpt":false,"smimeSign":false,"smimeEncrypt":false,"smimeEnvelopId":"","saveSentCopy":true,"subject":"工作日报","isHtml":true,"content":"<p>\n\t<br />\n</p>\n<p>\n\t<a href=\"https://www.yuque.com/luyao-sxof0/efatct/ubuoa7owpeh8ss4t?singleDoc# 《工作日报》\" title=\"https://www.yuque.com/luyao-sxof0/efatct/ubuoa7owpeh8ss4t?singleDoc# 《工作日报》\" target=\"_blank\">点击查看</a>\n</p>\n<p>\n\t<span style=\"text-wrap-mode:wrap;\">https://www.yuque.com/luyao-sxof0/efatct/ubuoa7owpeh8ss4t?singleDoc# 《工作日报》</span>\n</p>\n<p>\n\t<br />\n</p>","attachments":[]}""",
    )
    print(pm.do_send_email())
    
