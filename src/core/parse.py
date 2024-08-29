from requests_html import HTMLSession, AsyncHTMLSession
import bs4
import re
import requests

async def parse_data(url: str):

    asession = AsyncHTMLSession()

    response = await asession.get(url)

    await response.html.arender(sleep=10)

    options = sorted(element.text for element in response.html.find('.jsx-706577070.desc'))
    colors = []
    sizes = []
    for size in options:
        if not(re.match(r"\d\d.\d|\d\d", size)):
            colors.append(size)
        else:
            sizes.append(size)
    min_price = sorted(element.text for element in response.html.find('.jsx-2407367240.amount'))[0]
    values = [element.text for element in response.html.find('.jsx-1209583269.item-value')]
    title = [element.text for element in response.html.find('.jsx-1513790581.title')]

    style, max_price = values[0], values[1][1:]

    step = (int(max_price) - int(min_price)) // len(sizes)

    price = {}

    p = int(min_price)

    for i in range(len(sizes)):
        price[sizes[i]] = str(p)
        p += step

    return title, price, style, colors


async def parse_currency(url: str) -> float:

    response = requests.get(url=url)

    bs = bs4.BeautifulSoup(response.text, "html.parser")

    currencies = bs.find_all("td")
    currency = 0
    for i in range(len(currencies)):
        if currencies[i].text == 'Китайский юань':
            currency = float(currencies[i + 1].text.replace(',', '.'))
            break
    
    return currency

