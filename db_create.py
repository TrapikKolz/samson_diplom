import psycopg2

from config import dbname, user, password, host


def create_BD(vakuum_on_AV_reduce, UA_on_AV_increase, water_on_AV, vakuum_on_NV_reduce, UA_on_NV_increase,
              water_on_NV, UA_on_TO, UA_APP, UW_OA_on_RB, UA_on_AV_RB, rezult):
    '''
    :param vakuum_on_AV_reduce: Вакуум в АВ снижается?
    :param UA_on_AV_increase: Уровень активности воздуха в АВ повышается?
    :param water_on_AV: Присутствует вода на настиле АВ?
    :param vakuum_on_NV_reduce: Вакуум в НВ снижается?
    :param UA_on_NV_increase: Уровень активности воздуха в НВ растет?
    :param water_on_NV: Присутствует вода на настиле НВ?
    :param UA_on_TO: Уровень активности в турбинном отсеке растет?
    :param UA_APP: Уровень активности за АПП повышен?
    :param UW_OA_on_RB: Уровень воды и объемная активность в РБ растут?
    :param UA_on_AV_RB: Уровень активности воздуха в АВ на выходе газа из РБ растет?
    :param rezult: Итог (Все в норме, течь в АВ, течь в НВ, течь во 2 контур, течь в 3 контур)
    :return: Вводит данные в таблицу
    '''
    connect = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = connect.cursor()
    insert_create = f'INSERT INTO main_table (time_check, interval_check, "vakuum_on_AV_reduce", "UA_on_AV_increase",' \
                      f' "water_on_AV", "vakuum_on_NV_reduce", "UA_on_NV_increase", "water_on_NV", "UA_on_TO", "UA_APP", ' \
                      f'"UW_OA_on_RB", "UA_on_AV_RB", rezult) ' \
                      f'VALUES ' \
                      f"(current_timestamp, current_timestamp - current_date, {vakuum_on_AV_reduce}, " \
                      f"{UA_on_AV_increase}, {water_on_AV}, {vakuum_on_NV_reduce}, {UA_on_NV_increase}, " \
                      f"{water_on_NV}, {UA_on_TO}, {UA_APP}, {UW_OA_on_RB}, {UA_on_AV_RB}, '{rezult}')"

    # TO DO:
    # Сделать нормальное время интервалов в таблице

    cursor.execute(insert_create)
    connect.commit()

    cursor.close()
    connect.close()


for i in range(70):
    create_BD(False, False, False, False, False, False, False, False, False, False, 'Все в норме')


test_list = [
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [True, True, True, False, False, False, False, False, False, False],
    [False, False, False, True, True, True, False, False, False, False],
    [False, False, False, False, False, False, True, True, False, False],
    [False, False, False, False, False, False, False, False, True, True]
]