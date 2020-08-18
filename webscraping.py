import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

url = "https://www.fundsexplorer.com.br/ranking"

option = Options()
option.headless = True
driver = webdriver.Chrome()

driver.get(url)

element = driver.find_element_by_xpath("/html/body/section/div/section[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div")
html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

df_full = pd.read_html(str(table))[0]
df_full.fillna('NULL', inplace=True)

df_full.columns = [ "Código do fundo", "Setor", "Preço Atual", "Liquidez Diária", "Dividendo", "Dividend Yield",
                    "DY (3M)Acumulado", "DY (6M)Acumulado", "DY (12M)Acumulado", "DY (3M)Média", "DY (6M)Média",
                    "DY (12M)Média", "DY Ano", "Variação Preço", "Rentab. Período", "Rentab. Acumulada",
                    "Patrimônio Líq.", "VPA", "P/VPA", "DY Patrimonial", "Variação Patrimonial",
                    "Rentab. Patr. no Período", "Rentab. Patr. Acumulada", "Vacância Física", "Vacância Financeira", "Quantidade Ativos"]
 
df_dict = {}
df_dict = df_full.to_dict('records')

driver.quit()

js = json.dumps(df_dict, ensure_ascii=False).encode('utf8')
fp = open('database.json', 'wb')
fp.write(js)
fp.close()
