def size():
    return ['Ведёрко', 'Ведро', 'Ведрище']


def prices():
    return [100, 200, 300, 400, 500]


def size_to_price(price, siz):
    return price * siz * 0.9


def typ():
    type_data = ['Стандартный\n',
                 'Классика любимая всеми нами с детства. Тающий во рту попкорн и чуть солоноватый вкус оставит после себя приятные воспоминания.\n',
                 'Карамельный\n',
                 'Сладкий, хрустящий, с неповторимым вкусом карамели попкорн не оставит никого к себе равнодушным.\n',
                 'Шоколадный\n',
                 'Новая классика в мире попкорна. Оставляющий после себя приятный вкус шоколада, наш фаворит поселиться в вашем сердце надолго.\n',
                 'Карамель “Питер стайл”\n',
                 'Подражая своему предшественнику попкорн оставил фирменный хруст и сладость, но добавил своего солоноватого характера.\n',
                 'Микс\n', 'Идеальный вариант для тех, кто разрывается в своем выборе.']
    return type_data


def photo():
    temp = ['Menu/photo/Classic.png', 'Menu/photo/Caramel.png', 'Menu/photo/Chocko.png', 'Menu/photo/Piter.png',
            'Menu/photo/Mix.png']
    data = []
    for i in temp:
        data.append(open(i, 'rb'))
    return data


def combo():
    f = open('combo.txt')
    combo_data = f.readlines()
    return combo_data


def menu():
    data = {'size': size(), 'type': typ(), 'combo': combo()}
    return data


def menu_info(name):
    return name()


print(menu_info(photo))
