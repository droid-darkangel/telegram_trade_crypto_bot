from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



#пополнение баланса
def top_up():
    topupMenu = InlineKeyboardMarkup(row_width=1)
    btnTopUp = InlineKeyboardButton(text='Пополнить', callback_data="top_up")
    topupMenu.insert(btnTopUp)

    return topupMenu


def buy_menu(isUrl=True,url='',bill=''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQiwi = InlineKeyboardButton(text='оплатить', url=url)
        qiwiMenu.insert(btnUrlQiwi)

    btnCheckQiwi = InlineKeyboardButton(text='Проверить платёж', callback_data='check_'+bill)
    qiwiMenu.insert(btnCheckQiwi)

    btnBack = InlineKeyboardButton(text='Отмена', callback_data='back')
    qiwiMenu.insert(btnBack)

    return qiwiMenu


#аккаунт и основное меню
def main_menu():
    main_menu = InlineKeyboardMarkup(row_width=2)

    btnAcc = InlineKeyboardButton(text='Личный кабинет', callback_data='acc')
    btnShop = InlineKeyboardButton(text='биржа', callback_data='shop')
    btnAbout = InlineKeyboardButton(text='о сервисе', callback_data='about_we')
    btnHelp = InlineKeyboardButton(text='тех. поддержка', callback_data='help')
    main_menu.insert(btnAcc)
    main_menu.insert(btnShop)
    main_menu.insert(btnAbout)
    main_menu.insert(btnHelp)

    return main_menu



def trade_menu():
    trade_menu = InlineKeyboardMarkup(row_width=2)

    btnBTC = InlineKeyboardButton(text='BTC', callback_data='btc')
    btnETH = InlineKeyboardButton(text='ETH', callback_data='eth')
    btnLiteCoin = InlineKeyboardButton(text='Litecoin', callback_data='lt')
    btnRipple = InlineKeyboardButton(text='Ripple', callback_data='ripple')
    btnTron = InlineKeyboardButton(text='Tron', callback_data='tron')
    btnIota = InlineKeyboardButton(text='Iota', callback_data='iota')
    btnSolana = InlineKeyboardButton(text='Solana', callback_data='solana')
    btnFileCoin = InlineKeyboardButton(text='FileCoin', callback_data='filecoin')


    trade_menu.insert(btnBTC)
    trade_menu.insert(btnETH)
    trade_menu.insert(btnRipple)
    trade_menu.insert(btnLiteCoin)
    trade_menu.insert(btnTron)
    trade_menu.insert(btnIota)
    trade_menu.insert(btnSolana)
    trade_menu.insert(btnFileCoin)


    return trade_menu


def back_to_trade():
    back_trade = InlineKeyboardMarkup(row_width=1)

    btnBack = InlineKeyboardButton(text='Отмена', callback_data='back')

    back_trade.insert(btnBack)

    return back_trade



def all_trade_btns():
    all_trade_menu = InlineKeyboardMarkup(row_width=1)
    btnUp = InlineKeyboardButton(text='Вверх', callback_data='up')
    btnNone = InlineKeyboardButton(text='Не изменится', callback_data='none_tr')
    btnDown = InlineKeyboardButton(text='Вниз', callback_data='down')

    all_trade_menu.insert(btnUp)
    all_trade_menu.insert(btnNone)
    all_trade_menu.insert(btnDown)

    return all_trade_menu


def acc_menu():
    account_menu = InlineKeyboardMarkup(row_width=2)

    btnTopUp = InlineKeyboardButton(text='Пополнить', callback_data='top_up')
    btnCashBack = InlineKeyboardButton(text='Вывести', callback_data='cash')
    btnVerif = InlineKeyboardButton(text='Верификация', callback_data='verif')

    account_menu.insert(btnTopUp)
    account_menu.insert(btnCashBack)
    account_menu.insert(btnVerif)

    return account_menu

def cash_back():
    cash_back_menu = InlineKeyboardMarkup(row_width=2)

    btnCancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
    btnConfirm = InlineKeyboardButton(text='Подтвердить', callback_data='confirm')

    cash_back_menu.insert(btnConfirm)
    cash_back_menu.insert(btnCancel)

    return cash_back_menu


def cash_back_return():
    cash_back_returns = InlineKeyboardMarkup(row_width=2)

    btnReturn = InlineKeyboardButton(text='Личный кабинет',callback_data='acc')
    btnTrade = InlineKeyboardButton(text='Тех. Поддержка', callback_data='help')

    cash_back_returns.insert(btnReturn)
    cash_back_returns.insert(btnTrade)

    return cash_back_returns

def new_game_trade():
    new_game_trade_menu = InlineKeyboardMarkup(row_width=2)

    btnNewTrade = InlineKeyboardButton(text='Заново', callback_data='new_trade')
    btnBackAcc = InlineKeyboardButton(text='Аккаунт', callback_data='acc')

    new_game_trade_menu.insert(btnBackAcc)
    new_game_trade_menu.insert(btnNewTrade)

    return new_game_trade_menu


def top_up_from_acc():
    top_up_menu = InlineKeyboardMarkup(row_width=2)

    btnQiwi = InlineKeyboardButton(text='Qiwi', callback_data='qiwi')
    btnSber = InlineKeyboardButton(text='Банковская карта', callback_data='credit_card')
    btnBTC = InlineKeyboardButton(text='Криптовалюта', callback_data='crypto')

    top_up_menu.insert(btnQiwi)
    top_up_menu.insert(btnSber)
    top_up_menu.insert(btnBTC)

    return top_up_menu


def falsed_check_top_up_card():
    falsed_check_menu = InlineKeyboardMarkup(row_width=2)

    btnCheck = InlineKeyboardButton(text='Проверить оплату',callback_data='falsed_check')

    falsed_check_menu.insert(btnCheck)

    return falsed_check_menu


def verif():
    falsed_verif_menu = InlineKeyboardMarkup(row_width=1)

    btnToHelp = InlineKeyboardButton(text='Пройти верефикацию',callback_data='help')

    falsed_verif_menu.insert(btnToHelp)

    return falsed_verif_menu


def start_buttons():
    start_buttons_menu = InlineKeyboardMarkup(row_width=1)
    url = 'https://telegra.ph/Polzovatelskoe-soglashenie-Metamask-11-26'

    btnUserAgrees = InlineKeyboardButton(text='Пользовательское соглащение', url=url)
    btnUserAgreeAgrees = InlineKeyboardButton(text='✅Я принимаю условия', callback_data='i_agree')

    start_buttons_menu.insert(btnUserAgrees)
    start_buttons_menu.insert(btnUserAgreeAgrees)

    return start_buttons_menu


def about_we():
    about_we_menu = InlineKeyboardMarkup(row_width=1)
    url = 'https://telegra.ph/Polzovatelskoe-soglashenie-Metamask-11-26'

    btnUserAgrees = InlineKeyboardButton(text='Условия', url=url)
    btnUserHelp = InlineKeyboardButton(text='Тех. Поддержка', callback_data='help')
    btnWeb = InlineKeyboardButton(text='Состояние сети', callback_data='web')

    about_we_menu.insert(btnUserAgrees)
    about_we_menu.insert(btnUserHelp)
    about_we_menu.insert(btnWeb)

    return about_we_menu


def send_msg_helped_usr():
    url = 'https://t.me/help_metamask'
    falsed_help_menu = InlineKeyboardMarkup(row_width=1)

    btnToHelp = InlineKeyboardButton(text='Написать',url=url)

    falsed_help_menu.insert(btnToHelp)

    return falsed_help_menu