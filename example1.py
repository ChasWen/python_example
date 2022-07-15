import requests
from bs4 import BeautifulSoup
import xlwt
import xlrd

savepath = 'D:/excel表格.xls'
#   访问网页的方法，并返回网页的文本
def download_page(url):
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20220714 Firefox/61.0"}
   r = requests.get(url, headers=headers)  # 增加headers, 模拟浏览器
   return r.text

# 保存为txt，已经弃用
def save_txt(*args):
   for i in args:
       with open('书旗.txt', 'a', encoding='utf-8') as f:
           f.write(i)

# 此方法用于封装网页，并将结果保存至excel中，还可以继续优化
def get_content(html, page, k, book):
    # 获取工作表
    sheet=book.get_sheet("书旗爬书")
    # 提取网页内容
    soup = BeautifulSoup(html, 'html.parser')
    con = soup.find("div", class_="store-content")
    con_list = con.findAll("li")
    # 获取到每个书单的内容开始封装
    for i in con_list:
        name = i.find("h3").get_text()  # 小说名字
        author = i.find("span", class_="bkuser-icon").get_text() #作者
        content = i.find("p", class_="store-des").get_text() # 简介
        classification = i.find("span", class_="bkcate-icon").get_text() #类别
        # 将以上信息保存为list，并将信息保存至excel表中
        data = [page,name,author,content,classification]
        for j in range(0, 5):
            sheet.write(k, j, data[j])
        k = k + 1
    #   写入后,将当前表格保存
    book.save(savepath)

if __name__ == "__main__":
    # 此处用于新建一个excel表格并保存
    book1 = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book1.add_sheet('书旗爬书', cell_overwrite_ok=True)
    col = ('第几页', '小说', '作者', '简介', '类别')
    for i in range(0, 5):
        sheet.write(0, i, col[i])
    book1.save(savepath)
    # 此处用于每次打开此表格，并将最后一行记录下来 传入处理网页的方法
    for i in range(1, 14):
      book = xlrd.open_workbook(savepath)
      sheet = book.sheet_by_name("书旗爬书")
      k = sheet.nrows+1   #用于记录最后一行
      url = 'https://www.shuqi.com/store?page='.format(i) #传入url访问每一页
      html = download_page(url) #创建请求访问url，并将页面text传回来
      get_content(html, i , k , book1) #处理网页并将结果保存进excel的方法
