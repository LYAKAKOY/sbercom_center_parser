# Парсер сайта [Сберком](http://www.cikrf.ru/)


## Как запустить проект
1. Установите браузер google chrome
2. Требуется создать любую папку и открыть ее через терминал.
В терминале требуется прописать следующую команду для создания виртуального окружения
```bash
python -m venv venv
```
3. Активация виртуального окружения
```bash
.\venv\Scripts\activate
```
4. Требуется сделать git clone проекта
```bash
git clone https://github.com/LYAKAKOY/sbercom_center_parser.git
```
5. Перейти в папку sbercom_center_parser
```bash
cd sbercom_center_parser
```
6. Установить все зависимости
```bash
pip install -r requirements.txt
```
7 Запуск программы
```bash
python main.py
```
## Как остановить проект
Чтобы остановить парсер:
```bash
Ctrl+C или закрыть google chrome
```
Если у вас плохой интернет поменяйте значение TIME_WAIT

Для лучшей работы парсера лучше использовать proxy сервер и добавить его ip
в опции. Например:
```
 options.add_argument('--proxy-server=94.228.194.18:41890')
```
