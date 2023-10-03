import aiohttp
import asyncio

URL = 'http://unrealsoftware.de/inc_pub/serverinfo.php?i={}&p={}'

async def data_url(url):
    '''Отправляем асинхронный запрос'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f'Received unexpected status code {response.status} for URL: {url}')
                return None

def html_to_dict(html: str) -> dict:
    '''Парсим HTML код в словарь'''
    html = html.split('<td>')
    data = {}

    for i in range(1, len(html), 2):
        key = html[i].rstrip('</td>')
        value = html[i + 1].split('</td>')[0]
        data[key.rstrip(':')] = value
            
    return data

class Server:
    '''Класс для организации данных сервера'''
    def __init__(self, ip: str, port=36963):
        self.__IP = ip
        self.__PORT = port
        self.address = ip + ':' + str(port)
        
        self.status = 'Offline'
        self.name = '<Unknow>'
        self.map = '<Unknow>'
        self.players = '<Unknow>'
        self.gamemode = '<Unknow>'

    def __str__(self):
        return f'Server {self.status}{{{self.__IP}:{self.__PORT}}}'

    async def update(self):
        url = URL.format(self.__IP, self.__PORT)
        html = await data_url(url)

        if html:
            data = html_to_dict(html)

            if data:
                self.status = 'Online'

                self.name = data['Name']
                self.map = data['Map']
                self.players = data['Players']
                self.gamemode = data['Game Mode']
            else:
                self.status = 'Offline'
            
        else:
            print(f'Failed to update {self}')
            return None
