import requests

import json
import time
import base64
import asyncio

import time

import os

API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        """
        Запрос данных API-модели
        :return: id API-модели
        """
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt: str, model, images=1, width=1024, height=1024):
        """
        Отправка запроса на генерацию
        :param prompt: Строка запроса для генерации изображения
        :param model: id API-модели
        :param images: Количество запрашиваемых картинок
        :param width: Ширина картинки
        :param height: Высота картинки
        :return: id запроса для дальнейшего отслеживания
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    async def check_generation(self, request_id, attempts=10, delay=10):
        """
        Проверка и ожидание готовности генерации
        :param request_id: id запроса
        :param attempts: Количество попыток проверки
        :param delay: Задержка времени между попытками
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            # await time.sleep(delay)
            print('ожидаем....')
            await asyncio.sleep(delay)


async def gen(prom: str, dirr="image", file_name=f"img_{time.time_ns()}.jpg") -> str:
    """
    Генерация картинки через API Kandinsky
    :param prom: Строка запроса для генерации изображения
    :param dirr: Директория для сохранения сгенерированной картинки
    :param file_name: Имя файла сгенерированной картинки
    :return: Полное имя файла, куда была сохранена картинка
    """
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    # api2 =
    model_id = api.get_model()
    uuid = api.generate(prom, model_id)
    images = await api.check_generation(uuid)

    # Здесь image_base64 - это строка с данными изображения в формате base64
    image_base64 = images[0]

    # Декодируем строку base64 в бинарные данные
    image_data = base64.b64decode(image_base64)

    # Открываем файл для записи бинарных данных изображения
    try:
        with open(os.path.join(dirr, file_name), "wb") as file:
            file.write(image_data)
    except:
        try:
            file_name = f"{file_name.split(' ')[0]}{time.time_ns()}.jpg"
            with open(f"{dirr}/{file_name}", "wb") as file:
                file.write(image_data)
        except:
            file_name = f'image{time.time_ns()}.jpg'
            with open(f"{dirr}/{file_name}", "wb") as file:
                file.write(image_data)
    return f"{dirr}/{file_name}"


if __name__ == '__main__':
    while 1:
        zapros = input("prompt: ")

        try:
            os.mkdir(os.getcwd().replace("\\", "/") + f'/' + zapros.replace("\n", " ").split(".")[0])
        except FileExistsError:
            print('exist')

        for j in range(4):
            gen(zapros.replace("\n", " "), zapros.replace("\n", " ").split(".")[0])
            print(f"сделано {j + 1}")

        print("завершено")
