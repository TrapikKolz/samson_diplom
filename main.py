from numpy import array
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys

import pickle
import time


from qt_window import Ui_MainWindow

# pyinstaller --collect-submodules "sklearn" --add-binary "finalized_model.sav;." -w main_qt.py

class Qt_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Qt_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.filename = 'finalized_model.sav'
        self.qt_model = pickle.load(open(self.filename, 'rb'))



    def init_ui(self):
        self.setWindowTitle("Программа по поиску течи")
        self.setWindowIcon(QIcon("drop.png"))

        self.ui.analysis_button.clicked.connect(self.analysis)



    def analysis(self):
        start_time = time.time()
        str_for_check = [
            self.ui.vakuum_on_AV_reduce.isChecked(),
            self.ui.UA_on_AV_increase.isChecked(),
            self.ui.water_on_AV.isChecked(),
            self.ui.vakuum_on_NV_reduce.isChecked(),
            self.ui.UA_on_NV_increase.isChecked(),
            self.ui.water_on_NV.isChecked(),
            self.ui.UA_on_TO.isChecked(),
            self.ui.UA_APP.isChecked(),
            self.ui.UW_OA_on_RB.isChecked(),
            self.ui.UA_on_AV_RB.isChecked()
        ]

        # result = loaded_model.score(X_test, Y_test)
        y_pred = self.qt_model.predict(array(str_for_check).reshape(1, -1))

        self.ui.info_list_2.setText('Значение предсказанное моделью:\n' + str(y_pred[0]))
        print("Модель:" + str(time.time() - start_time))

        start_time = time.time()

        P1k_convert_text = self.ui.P1k.text()
        urKO_convert_text = self.ui.Uroven_KO.text()

        if P1k_convert_text == '' or urKO_convert_text == '':
            rezult_P1k_urKO = 'Значения давления или уровня КО не заданы\n'
        else:
            try:
                P1k_convert = float(P1k_convert_text.replace(',', '.'))
                urKO_convert = float(urKO_convert_text.replace(',', '.'))
                if 15 <= P1k_convert <= 16 and 72 <= urKO_convert <= 82:
                    rezult_P1k_urKO = 'Показатели давления и уровня КО в норме\n'
                elif P1k_convert < 15 and 72 <= urKO_convert <= 82:
                    rezult_P1k_urKO = 'По показателям давления и уровня КО - течь по газу\n'
                elif P1k_convert < 15 and urKO_convert < 72:
                    rezult_P1k_urKO = 'По показателям давления и уровня КО - течь по воде\n'
                else:
                    rezult_P1k_urKO = 'Непредвиденные случай показателей\n'
            except ValueError:
                rezult_P1k_urKO = 'Некорректные данные давления и уровня КО\n'

        self.ui.info_list_1.setText(str(rezult_P1k_urKO))

        print("Параметры:" + str(time.time() - start_time))




app = QtWidgets.QApplication([])
application = Qt_window()
application.show()

sys.exit(app.exec())
