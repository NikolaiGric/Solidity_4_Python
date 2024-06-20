from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract
import re
from datetime import datetime

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

def check_password_complexity(password):
    try:
        # Проверка длины пароля
        if len(password) < 12:
            print("Ошибка: Ваш пароль должен содержать минимум 12 символов.")
            return False

        # Проверка наличия хотя бы одной заглавной буквы
        if not re.search(r'[A-Z]', password):
            print("Ошибка: Ваш пароль должен содержать хотя бы одну заглавную букву.")
            return False

        # Проверка наличия хотя бы одной строчной буквы
        if not re.search(r'[a-z]', password):
            print("Ошибка: Ваш пароль должен содержать хотя бы одну строчную букву.")
            return False

        # Проверка наличия хотя бы одной цифры
        if not re.search(r'[0-9]', password):
            print("Ошибка: Ваш пароль должен содержать хотя бы одну цифру.")
            return False

        # Проверка на наличие букв, находящихся рядом на клавиатуре
        for i in range(len(password) - 2):
            if password[i + 1] in 'qwertyuiop' and password[i] in 'qwertyuiop' and password[i + 2] in 'qwertyuiop':
                print("Ошибка: Ваш пароль содержит буквы, находящиеся рядом на клавиатуре.")
                return False
            elif password[i + 1] in 'asdfghjkl' and password[i] in 'asdfghjkl' and password[i + 2] in 'asdfghjkl':
                print("Ошибка: Ваш пароль содержит буквы, находящиеся рядом на клавиатуре.")
                return False
            elif password[i + 1] in 'zxcvbnm' and password[i] in 'zxcvbnm' and password[i + 2] in 'zxcvbnm':
                print("Ошибка: Ваш пароль содержит буквы, находящиеся рядом на клавиатуре.")
                return False

        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

    def AuthorizeUser():
        # Авторизация пользователя
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        try:
            web3.geth.personal.unlock_account(public_key, password)
            print("Авторизация успешна!")
            return public_key
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
            return None

    def RegisterNewUser():
        # Регистрация нового пользователя
        password = input("Введите пароль: ")
        if check_password_complexity(password):
            try:
                new_account = web3.geth.personal.new_account(password)
                print(f"Ваш публичный ключ: {new_account}")
                with open('info.txt', 'a', encoding="utf-8") as file:
                    file.write(f'\nПубличный ключ: {new_account}, Пароль: {password}')
            except Exception as e:
                print(f"Ошибка регистрации: {e}")
        else:
            print("Пароль не соответствует требованиям безопасности!")

    def CreateEstate(account):
        # Создание новой недвижимости
        try:
            street_name = input("Введите название улицы: ")
            street_number = int(input("Введите номер улицы: "))
            property_type = int(input("Тип недвижимости (1-Дом, 2-Квартира, 3-Промышленный объект, 4-Дача): "))

            if property_type not in range(1, 5):
                print("Некорректный тип недвижимости!")
                return

            if street_number <= 2 or len(street_name) < 2:
                print("Некорректные данные!")
                return

            tx_hash = contract.functions.CreateEstate(street_name, street_number, property_type - 1).transact(
                {"from": account})
            print(f"Транзакция отправлена: {tx_hash.hex()}")
        except Exception as e:
            print(f"Ошибка при создании недвижимости: {e}")

    def GetEstates():
        # Вывод списка всех недвижимости
        try:
            estates = contract.functions.GetEstates().call()
            if estates:
                for estate in estates:
                    print(
                        f"Адрес: {estate[0]}, Номер: {estate[1]}, Тип: {['Дом', 'Квартира', 'Промышленный объект', 'Дача'][estate[2]]}, Статус: {'Активный' if estate[4] else 'Неактивный'}, ID: {estate[5]}")
            else:
                print("Список недвижимости пуст.")
        except Exception as e:
            print(f"Ошибка получения списка: {e}")

    def createAdd(account):
        # Создание объявления о продаже
        try:
            GetMyEstates(account)
            price = int(input("Введите цену продажи: "))
            estate_id = int(input("Введите ID недвижимости: "))
            date_today = int(datetime.now().strftime("%d%m%Y"))

            tx_hash = contract.functions.createAdd(price, estate_id, date_today).transact({"from": account})
            print(f"Транзакция отправлена: {tx_hash.hex()}")
        except Exception as e:
            print(f"Ошибка при создании объявления: {e}")

    def GetMyEstates(account):
        # Вывод списка недвижимости пользователя
        try:
            estates = contract.functions.GetEstates().call()
            user_estates = [estate for estate in estates if estate[3] == account]

            if user_estates:
                for estate in user_estates:
                    print(
                        f"Адрес: {estate[0]}, Номер: {estate[1]}, Тип: {['Дом', 'Квартира', 'Промышленный объект', 'Дача'][estate[2]]}, Статус: {'Активный' if estate[4] else 'Неактивный'}, ID: {estate[5]}")
            else:
                print("У вас нет недвижимости.")
        except Exception as e:
            print(f"Ошибка получения списка недвижимости: {e}")

    def GetAdds():
        # Вывод всех объявлений
        try:
            ads = contract.functions.GetAdds().call()
            if ads:
                for ad in ads:
                    print(
                        f"ID объявления: {ad[0]}, Цена: {ad[1]}, ID недвижимости: {ad[2]}, Создатель: {ad[3]}, Покупатель: {'Отсутствует' if ad[4] == '0x0000000000000000000000000000000000000000' else ad[4]}, Дата: {ad[5]}, Статус: {'Открыт' if ad[6] == 0 else 'Закрыт'}")
            else:
                print("Объявлений нет.")
        except Exception as e:
            print(f"Ошибка получения списка объявлений: {e}")

    def UpdateEstateStatus(account):
        # Изменение статуса недвижимости
        try:
            GetMyEstates(account)
            property_id = int(input("Введите ID недвижимости: "))
            action = input("Активировать (1) или Деактивировать (2): ")

            if action == "1":
                status = True
            elif action == "2":
                status = False
            else:
                print("Некорректный выбор!")
                return

            contract.functions.updateEstateActive(property_id, status).transact({"from": account})
            print("Статус изменен.")
        except Exception as e:
            print(f"Ошибка изменения статуса: {e}")

    def GetMyAdds(account):
        # Вывод объявлений пользователя
        try:
            ads = contract.functions.GetAdds().call()
            user_ads = [ad for ad in ads if ad[3] == account]

            if user_ads:
                for ad in user_ads:
                    print(
                        f"ID объявления: {ad[0]}, Цена: {ad[1]}, ID недвижимости: {ad[2]}, Покупатель: {'Отсутствует' if ad[4] == '0x0000000000000000000000000000000000000000' else ad[4]}, Дата: {ad[5]}, Статус: {'Открыт' if ad[6] == 0 else 'Закрыт'}")
            else:
                print("У вас нет объявлений.")
        except Exception as e:
            print(f"Ошибка получения объявлений: {e}")

    def UpdateAddStatus(account):
        # Изменение статуса объявления
        try:
            GetMyAdds(account)
            ad_id = int(input("Введите ID объявления: "))
            action = input("Открыть (1) или Закрыть (2): ")

            if action == "1":
                status = 0
            elif action == "2":
                status = 1
            else:
                print("Некорректный выбор!")
                return

            contract.functions.updateAdType(ad_id, status).transact({"from": account})
            print("Статус объявления изменен.")
        except Exception as e:
            print(f"Ошибка изменения статуса объявления: {e}")

    def GetBalanceContract(account):
        # Получение баланса контракта
        try:
            balance = contract.functions.getBalance().call({"from": account})
            print(f"Баланс контракта: {balance}")
        except Exception as e:
            print(f"Ошибка получения баланса: {e}")

    def DepositContract(account):
        # Пополнение баланса контракта
        try:
            amount = int(input("Введите сумму для депозита: "))
            tx_hash = contract.functions.Deposit().transact({"from": account, "value": amount})
            print(f"Транзакция отправлена: {tx_hash.hex()}")
        except Exception as e:
            print(f"Ошибка пополнения: {e}")

    def Deposit(account):
        try:
            amount = int(input("Введите сумму пополнения: "))
            tx_hash = contract.functions.Deposit().transact({
                "from": account,
                "value": amount
            })
            print(f"Транзакция отправлена: {tx_hash.hex()}, счет: {account}")
        except Exception as e:
            print(f"Ошибка при депозите средств на контракт: {e}")

    def Withdraw(account):
        # Вывод средств с контракта
        try:
            amount = int(input("Введите сумму для вывода: "))
            tx_hash = contract.functions.withdraw(amount).transact({"from": account})
            print(f"Транзакция отправлена: {tx_hash.hex()}")
        except Exception as e:
            print(f"Ошибка вывода: {e}")

    def GetBalanceAccount(account):
        # Получение баланса аккаунта
        try:
            balance = web3.eth.get_balance(account)
            print(f"Баланс аккаунта: {balance}")
        except Exception as e:
            print(f"Ошибка получения баланса: {e}")

    def BuyEstate(account):
        # Покупка недвижимости
        try:
            GetAdds()
            property_id = int(input("Введите ID недвижимости для покупки: "))
            tx_hash = contract.functions.BuyEstate(property_id).transact({"from": account})
            print(f"Недвижимость куплена успешно, транзакция отправлена: {tx_hash.hex()}")
        except Exception as e:
            print(f"Ошибка при покупке недвижимости: {e}")

if __name__ == '__main__':
    account = ""
    is_auth = False
    while True:
        if not is_auth:
            choice = input("1. Авторизация\n2. Регистрация\n3. Выход\nВыш выбор: ")
            match choice:
                case "1":
                    account = AuthorizeUser()
                    if account != "" and account != None:
                        is_auth = True
                case "2":
                    RegisterNewUser()
                case "3":
                    break
                case _:
                    print("Некорректный выбор!")
        elif is_auth:
            choice = input(
                """Выберите действие:
                1. Пополнить баланс контракта\n     2. Вывод средств с контракта\n      3. Создать новую запись о недвижимости
                4. Создать объявление о продаже недвижимости\n      5. Изменить статус недвижимости      
                6. Изменить статус объявления\n     7. Купить недвижимость
                8. Получить информацию о доступных недвижимостях\n      9. Посмотреть объявления о текущих продажах недвижимости
                10. Посмотреть свой баланс на контракте\n       11. Посмотреть свой баланс на аккаунте
                12. Посмотреть свои объявления\n        13. Посмотреть свои недвижимости
                14. Посмотреть свой публичный адрес\n       15. Выход из аккаунта\nВыш выбор: """)
            match choice:
                case "1":
                    Deposit(account)
                case "2":
                    WithDraw(account)
                case "3":
                    CreateEstate(account)
                case "4":
                    createAdd(account)
                case "5":
                    UpdateEstateStatus(account)
                case "6":
                    UpdateAddStatus(account)
                case "7":
                    BuyEstate(account)
                case "8":
                    GetEstates()
                case "9":
                    GetAdds()
                case "10":
                    GetBalanceContract(account)
                case "11":
                    GetBalanceAccount(account)
                case "12":
                    GetMyAdds(account)
                case "13":
                    GetMyEstates(account)
                case "14":
                    print(account)
                case "15":
                    account = ""
                    account = AuthorizeUser()
                case _:
                    print("Некорректный выбор!")
