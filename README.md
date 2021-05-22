# Energo
This is our project for hackaton
Реализованная функциональность
Интерактивная карта


Особенность проекта в следующем:
прогноз по типам, испольхование машинного обучения


Основной стек технологий:
Python Streamlit HTML
pandas sklearn geopandas plotly
lightgbm xgboost
pyDeck JavaScript, TypeScript.
Git, Mercurial.
GitHab.
Демо
Демо сервиса доступно по адресу: http://185.137.232.102:19050/

Реквизиты тестового пользователя: без пароля

СРЕДА ЗАПУСКА
развертывание сервиса производится на ubuntu linux (Ubuntu 18+);
требуется установленный web-сервер с поддержкой PHP(версия 7.4+)
Python
УСТАНОВКА
Установка пакета name
Выполните

sudo apt-get python3
git clone https://github.com/irumata/Energo/
cd Energo
pip3 install -r requirements.txt
streamlit run run_app.py --server.port=<port>
 
сервис доступен localhost:port
После этого выполнить команду в директории проекта:

composer install
РАЗРАБОТЧИКИ

Николай Князев
Корсаков Иван
Веретенников Александр
Владислав Глебов
