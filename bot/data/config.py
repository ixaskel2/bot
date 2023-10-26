from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
LOGS_CHAT = env.str("logs_chat") #Тут канал логов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
