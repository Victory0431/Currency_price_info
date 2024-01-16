import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

currency_dict = {
    'GBP': '英镑', 'HKD': '港币', 'USD': '美元', 'CHF': '瑞士法郎', 'DEM': '德国马克',
    'FRF': '法国法郎', 'SGD': '新加坡元', 'SEK': '瑞典克朗', 'DKK': '丹麦克朗', 'NOK': '挪威克朗',
    'JPY': '日元', 'CAD': '加拿大元', 'AUD': '澳大利亚元', 'EUR': '欧元', 'MOP': '澳门元',
    'PHP': '菲律宾比索', 'THB': '泰国铢', 'NZD': '新西兰元', 'KRW': '韩元', 'RUB': '卢布',
    'MYR': '林吉特', 'TWD': '新台币', 'ESP': '西班牙比塞塔', 'ITL': '意大利里拉', 'NLG': '荷兰盾',
    'BEF': '比利时法郎', 'FIM': '芬兰马克', 'INR': '印度卢比', 'IDR': '印尼卢比', 'BRL': '巴西里亚尔',
    'AED': '阿联酋迪拉姆', 'ZAR': '南非兰特', 'SAR': '沙特里亚尔', 'TRY': '土耳其里拉'
}

#日期验证函数
def validate_date_format(date_string):
    try:
        if len(date_string) != 8:
            raise ValueError("日期长度不正确")
        year = int(date_string[0:4])
        month = int(date_string[4:6])
        day = int(date_string[6:8])
        if year < 2001 or year > int(time.asctime().split(' ')[-1]):
            raise ValueError("年份超出范围")
        if month < 1 or month > 12:
            raise ValueError("月份超出范围")
        if day < 1 or day > 31:
            raise ValueError("日期超出范围")
        return True
    except ValueError as e:
        print("日期格式错误:", str(e))
        return False
    
#验证日期输入是否正确
while True:
    date = input('请输入日期')
    if not validate_date_format(date):
        print('请输入合适的日期，例如20211231')
        continue
    break

#验证货币代码输入是否正确
while True:
    currency = input('请输入货币代码')
    try:
        currency_name = currency_dict[currency]
    except Exception:
        print('请输入合适的货币代码，例如USD')
        continue
    else:
        break

# 初始化浏览器
browser = webdriver.Chrome()
browser.get('https://www.boc.cn/sourcedb/whpj/')

#获取起始日期元素并赋值
erect_date = browser.find_element("id","erectDate")
erect_date.send_keys(date)

#获取结束日期元素并赋值
end_date = browser.find_element("id","nothing")
end_date.send_keys(date)

#获取下拉框元素并选中
select = Select(browser.find_element("tag name","select"))
select.select_by_visible_text(currency_name)

#获取搜索按钮并点击
search_btn = browser.find_elements("class name","search_btn")[1]
search_btn.click()

#涉及页面切换，网络加载速度不定，引入异常处理
#直到页面元素获取完整 最多等待10秒钟
wait = WebDriverWait(browser, 10)

try:
    div_BOC = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "BOC_main")))
    table_rows = div_BOC.find_elements("tag name","tr")
except Exception:
    print('网页未成功加载，请重试')

#检索不到异常处理
if '没有检索结果' in table_rows[1].text:
    print(table_rows[1].text)
else:
    prices = table_rows[1].find_elements("tag name","td")[3].text
    print(currency_name + ' 现汇卖出价:',prices)

# 关闭浏览器
#browser.close()
