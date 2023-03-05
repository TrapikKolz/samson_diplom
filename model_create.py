import psycopg2
from pandas import DataFrame
from sklearn import tree
from pickle import dump

from config import dbname, user, password, host

connect = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = connect.cursor()
cursor.execute('SELECT * FROM main_table')
tuples = cursor.fetchall()
cursor.close()

columns_names = ['time_check', 'interval_check', "vakuum_on_AV_reduce", "UA_on_AV_increase", "water_on_AV",
                "vakuum_on_NV_reduce", "UA_on_NV_increase", "water_on_NV", "UA_on_TO", "UA_APP", "UW_OA_on_RB",
                "UA_on_AV_RB", 'rezult']
df = DataFrame(tuples, columns=columns_names)

x = df[["vakuum_on_AV_reduce", "UA_on_AV_increase", "water_on_AV", "vakuum_on_NV_reduce", "UA_on_NV_increase",
        "water_on_NV", "UA_on_TO", "UA_APP", "UW_OA_on_RB", "UA_on_AV_RB"]]
y = df['rezult']

model = tree.DecisionTreeClassifier(criterion="entropy")
model.fit(x.values, y.values)

filename = 'finalized_model.sav'
dump(model, open(filename, 'wb'))
