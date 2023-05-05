import base64
import sys

from PyQt5.QtGui import QDoubleValidator, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QAbstractItemView, QTableWidgetItem, QMessageBox
import calc_util
from rbaf_gui import Ui_RbafWin


class MyMainWindow(QMainWindow, Ui_RbafWin):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.result = list()
        self.tableWidgetOutput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetOutput.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetOutput.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetOutput.horizontalHeader().setVisible(False)
        self.pushButtonCalc.clicked.connect(self.btn_clicked)
        self.tableWidgetOutput.setShowGrid(False)
        self.tableWidgetOutput.setVisible(False)
        self.editor_validator()

    def editor_validator(self):
        double_validator = QDoubleValidator()
        double_validator.setRange(0, double_validator.top())
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setDecimals(2)
        self.lineEditInvestmentScale.setValidator(double_validator)
        self.lineEditPositionRatio.setValidator(double_validator)
        self.lineEditRateOfReturn.setValidator(double_validator)
        self.lineEditAverageRateOfReturn.setValidator(double_validator)
        self.lineEditAverageLossRate.setValidator(double_validator)
        self.lineEditAverageAccuracy.setValidator(double_validator)

    def btn_clicked(self):
        cur_average_rate_of_return = self.lineEditAverageRateOfReturn.text()
        cur_input = self.lineEditInvestmentScale.text()
        cur_average_loss_rate = self.lineEditAverageLossRate.text()
        cur_average_accuracy = self.lineEditAverageAccuracy.text()
        cur_target_rate_of_return = self.lineEditRateOfReturn.text()
        cur_position_ratio = self.lineEditPositionRatio.text()

        if cur_position_ratio and cur_input and cur_average_accuracy and cur_average_loss_rate and cur_target_rate_of_return and cur_average_rate_of_return:
            cur_input = float(cur_input)*10000
            cur_average_accuracy = float(cur_average_accuracy)/100
            cur_average_rate_of_return = float(cur_average_rate_of_return)/100
            cur_average_loss_rate = float(cur_average_loss_rate)/100
            cur_target_rate_of_return = float(cur_target_rate_of_return)/100
            cur_position_ratio = float(cur_position_ratio)/100
            result = calc_util.calc_count(cur_average_rate_of_return, cur_average_loss_rate, cur_average_accuracy,
                                          cur_target_rate_of_return, cur_position_ratio)
            if result == 0 or result < 0:
                QMessageBox.information(self, "提示", "~~当前输入无法计算,可能是平均收益率低于平均亏损率或平均交易成功率过低导致~~")
            else:
                success_count = result * cur_average_accuracy
                fail_count = result * (1 - cur_average_accuracy)
                target_return = cur_input * cur_target_rate_of_return
                once_input = cur_input * cur_position_ratio
                net_amount_per_transaction = target_return / result
                roi_per_transaction = net_amount_per_transaction / once_input
                benefit_risk_ratio = cur_average_rate_of_return / cur_average_loss_rate
                xy_value = calc_util.calc_return_loss(success_count, fail_count, target_return, benefit_risk_ratio)
                average_return_on_successful = xy_value[0]
                average_loss_on_failed = xy_value[1]
                self.result.append([round(average_return_on_successful, 2)])
                self.result.append([round(success_count, 2)])
                self.result.append([round(average_loss_on_failed, 2)])
                self.result.append([round(fail_count, 2)])
                self.result.append([round(benefit_risk_ratio, 2)])
                self.result.append([round(once_input, 2)])
                self.result.append([round(roi_per_transaction, 2)])
                self.result.append([round(net_amount_per_transaction, 2)])
                self.result.append([round(target_return, 2)])
                self.result.append([round(result, 2)])
                self.show_result()
                self.result.clear()  # reset result for re-computing

        else:
            QMessageBox.information(self, "提示", "~~输入的数据不完整~~")

    def show_result(self):
        self.tableWidgetOutput.setVisible(True)
        for i in range(self.tableWidgetOutput.rowCount()):
            for j in range(self.tableWidgetOutput.columnCount()):
                new_item = QTableWidgetItem(str(self.result[i][j]))
                self.tableWidgetOutput.setItem(i, j, new_item)


def get_icon():
    icon_bytes = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAH5klEQVR4nO2d' \
                 b'+1MTVxTH94e2v7e/1u4jAobdECEJEJBneYlSRIooIMhDDEIQUCMQQERbaq2tgA+qg6O21tZnFUtRMNaqdVrLtI7toO1' \
                 b'/0eqv9XTuJcsQ5LUJkg17vjNnIuzlcO' \
                 b'/57Lnn3nXnwjAoFAqFQqFQKBQKhUKhUCgUCoVCoVAoFAr1ysXzYctYXmzkeOkWK4hPOEF8zgkSqNfE57SfpL' \
                 b'+82Ej6vyhuk3d0BgvHSy7' \
                 b'/B1hym2HSpwLjxZ9YnbSCCUSZzebXWV48xgnSCzKYYL2ZDqqoshmqHAehof1zcHxwclrjBGnG6962J+1i7j6dtT3pH' \
                 b'+lnYWUzbRusN8lgXnC8dISMjwkULVkivsUK4g9kALogI6xcWw4N7ccUBZnzM5DJP1O' \
                 b'/uxdW5pTR8ZCvWUG8zbJhbzIBkRmCeJt0Wi9FQ0X9h14FmVMZEPnflQ0fQajB6p7CpLuiKL7BqFnuaQpCpWiwN3d7HWROpUCI' \
                 b'1Ti7QW+IlqEcZtSqJYIUSeZYktab6zt9CjKnEIhojF0wIMQq6jtBCFpOawq7NMzMqFHyVEVqhq9B5hQCUeJ3PoAQy1hTJmfJMK' \
                 b'M2cZxBL6+mSAHXApD63b3jqy9B0IcwahKnE5tIx5Iy1s9LkLkAAEIsMSN/bNXFSw5GTSI7Wnmf4Q8g4gLXENkKN4/tUzheH' \
                 b'GLUJJaX/iYdq9r1qc9Bc6hslTVTv8nm0b0vecqoSRwvPaMbqD0z78ADMUMcMxgZr7uwP2PUJPl5z3wM0qGyGjIXn8SYQAPy' \
                 b'KqcsxysEMlu/AxbIYizqDgRy0ieACGSBMoSbQ/uNtlYQxEjg9Sb6WWRr0faU5c9lb5GtBYJNCWDqvQDRw4/oZ1BE/JyhLEog83' \
                 b'3HOxS0N1rTwNR7ntYP2QgUY0w6AvEHEN0yE1iHfvcAQjKFfB8zxA9AwmiGXPDMkOMX6fc1W0P8OWUV2VpozSBQrMOPwXz8Mg' \
                 b'SZEuj/mfvqO2CB+PtZVpGtBQTRArw+AnjRAgUVjb753tcHWXmVgQvE38tee3O3xz4kv3Sn174b2nshISUXklNzEIjDSyDv5Vd5' \
                 b'ALHMoX5M5btq10GIiEyG4rJtMHTnMQJxeAnEFPWuB5DImFQorelQBGRb6xEINUTDns6j4Lo/Sk1zU1atswckYyzUtR312veW7' \
                 b'R/DclO8B5C2fd0Qn7LWox2pK0ZTAv2dU/nOXFsOJeV14zA0CSQjuwSCQsIhZ4Pda9' \
                 b'+ZOWVQVdviAWTw9iMQw6x0CtrRcQLSs4rBHJkMeQWVkJJZ8JJvkh16KQouXrurXSC1zh7QS5Gw/2AfhFsS6cpGqe+d' \
                 b'+/pAWh4LZ7654QGEBNPesBviU3LBbE2DtevKYWB4BL4bGgHJGENfipvoe1VuBWws3eYBQ3NA0rNLoHJrIx14VEwalNo7FP' \
                 b'veVL0HYuIzx4M3EciVgQcghkVDS8dnHkFu7TgEMfGrx33XtR2j2XH+2zvaBVLr7KFvQF79/mc68MbWA5Ccka' \
                 b'/Yd8qqAnA4908JZDobvvsnWGMzoHCLk7Zd/X4lFJbUTNlWM0DSsorBVtM8PvD+Gw9hWahlyuI+2feOvSdoMBPT18Ey0QKX' \
                 b'+u8rAkKs6+hXsNycSNuGSlFw7rJLG0Aqt+8HMSyGTk' \
                 b'/25q7xtiQIVwfHskO2dQVbpizuE33bnd0gGa2QnJYLbXu74drgLx7BmysQYiuzNtC26zdunbbNogJC7nZjRByds201zRRC6up' \
                 b'C2tZmd740+N6TlyHckjSj7xVJa6C2oX3a4CkBIi8EpsuORQVk594+iE3Igi3VTR7Tkr2+nba9esMzO2SLtKa+VNxl33kl2yEu' \
                 b'YRUM/fjHvACRf2a266oFYo3LpMvDkup2aNhzfEYgmTmlkLEqnxZQJUFonKK4k/Y1TYfoSuiL8zdnDJ6mgBw+fh5q6togKTUHQ' \
                 b'kItdGdLloyTgWyoaIQISyLNCKVB6L/xEERDNGRkb4LalrEdNQ10/GrY3tQ5a/A0BWRiR8nKZmPZNnrXZrsf7BVXtUFieh6IUj' \
                 b'ScPjfodRCuDDyACpuD+iZgSPuklDVTZhsCmRSEc5duQe66chq0uKQsaO3ogv6bv/p0V7omgZmt8GKG+BBkl8K2StprespCIH' \
                 b'4UApEwQ1w4ZWGGuLCGjGJRxxoyiqssXPYuslWWOSoZ9yFqAuJS4Bc3hggk8DPEPMcpCKesacTy0r8k4AOu3xZ8GnL58VkWe' \
                 b'W2IXGd56R9GTWJ56S/6xPXSLU0BOXtheAyIID5h1CRyRBHp2MHu05oCcqDrlAzkJqMm0SNgBQkKS' \
                 b'+yaqiGFxdXylLWTUZPIubbyqzvkVUwtLHuvD41AqBRJr7' \
                 b'+tCw1m1Cb5fN7qulZNAKmqdar3RLnxQ5MF6UVQSAT0fXl9UQPpO9MPS0PCybX/WFZvYtQqcsgwGUC4OR4u9t9bMCDmBawhl' \
                 b'/rv0Zf73HuvHkbt5/bKUxfpNLmTFgIIt0CrrFNnB+jrSwFzbi8ROfFZPqF0aXA4bK1tpYU+kIFcHxqhNYOMxw3DFRAnW0' \
                 b'/KlMPy2e+iIQrkfQrZTM20o3epAAjpH+nnJ12naVt5NcXrDGQ8PUxi4mtMIGqJTm/gePG6' \
                 b'/KzL76aTP7356wjSsKoLuBKRdTo5SpWc3un' \
                 b'+uxz0jEbVGi89YwVxlOzAWcHwtSr3GSgUCoVCoVAoFAqFQqFQKBQKhUKhUCgU46P+B/irsZar6wz7AAAAAElFTkSuQmCC '
    icon_img = base64.b64decode(icon_bytes)
    icon_pixmap = QPixmap()
    icon_pixmap.loadFromData(icon_img)
    return icon_pixmap


if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_win = MyMainWindow()
    my_win.setWindowIcon(QIcon(get_icon()))
    my_win.show()
    sys.exit(app.exec_())
