import vk_api
from App_search import VKphoto
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from config import token1

session = vk_api.VkApi(token=token1)

upload = VkUpload(session)

def send_mess_photo(user_id, message):
    post = {
        'user_id': user_id,
        'message': message,
        'attachment': ','.join(attachments),
        'random_id': get_random_id(),
        'keyboard': keyboard.get_keyboard()

    }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        pass

    session.method('messages.send', post)


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id()
    }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        pass

    session.method('messages.send', post)


def send_message_start(user_id, message):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id(),
        'keyboard': keyboard.get_keyboard()

    }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        pass

    session.method('messages.send', post)


vk_api = session.get_api()

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        list_load_photo = []

        if text == "start":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('дальше', VkKeyboardColor.PRIMARY)
            usr = vk_api.users.get(user_id=user_id, fields="city, sex", v=5.131)

            city_id = usr[0]['city']['id']

            list_load_photo = VKphoto.get_users(city_id)
            print(f'@@@@@@@@@{list_load_photo}')                  #Для внесения в БД: Список ID искомых людей
            send_message_start(user_id, 'Ваши данные получены')


        elif text == "дальше":
            finde_user_id = 304302303       #Получение из БД одного ID  (с удалением его из БД)
            z = VKphoto.get_photos(finde_user_id)
            print(f'((((((() {z}')
            attachments = []
            for i in z[0]:
                # attachments = []
                upload_image = upload.photo_messages(photos=i)[0]
                attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
                print(attachments)
            send_mess_photo(user_id, f'Ваши данные ')# {z[0]}')

        elif text == "привет":
            send_message(user_id, "Хай")
        elif text == "пока":
            send_message(user_id, "Пока((")
        else:
            send_message(user_id, "Не поняла вашего ответа...")
