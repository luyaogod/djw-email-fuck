attrs = r"""
{"scheduleDate":null,"account":"\"马路遥 Luyao Ma\" <malyb@digiwin.com>","to":["\"贾旭光 xuguang jia\" <jiaxg@digiwin.com>",
"\"翟高峰 gaofeng zhai\" <zhaigf@digiwin.com>"],"cc":[],"bcc":[],"showOneRcpt":false,"smimeSign":false,"smimeEncrypt":false,"smimeEnvelopId":"","saveSentCopy":true,"subject":"工作日报","isHtml":true,"content":"<p>\n\t<br />\n</p>\n<p>\n\t<a href=\"https://www.yuque.com/luyao-sxof0/efatct/ubuoa7owpeh8ss4t?singleDoc# 《工作日报》\" title=\"https://www.yuque.com/luyao-sxof0/efatct/ubuoa7owpeh8ss4t?singleDoc# 《工作日报》\" target=\"_blank\">点击查看</a>\n</p>\n<p>\n\t<span style=\"text-wrap-mode:wrap;\">https://www.yuque.com/luyao-sxof0/efatct/ubuoa7owpeh8ss4t?singleDoc# 《工作日报》</span>\n</p>\n<p>\n\t<br />\n</p>","attachments":[]}
"""

id = "11111"
result = (
    '{"attrs":'
    + attrs
    + ',"action":"deliver","id":"'
    + id
    + '","returnInfo":true,"autosaveHitCounter":true,"encryptPassword":""}'
)

print(result)
