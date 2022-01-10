import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import uic
#import mysql.connector
from mysql.connector import Error
import time

class AppDemo(QWidget):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.pushButton.clicked.connect(self.get_data)

    def get_data(self):
        try:
            from_tanggal = self.dateEdit_from.date().toPyDate()
            print(from_tanggal)
            to_tanggal = self.dateEdit_to.date().toPyDate()
            print(to_tanggal)
            connection = mysql.connector.connect(host='localhost',
                                                database='sensorPY',
                                                user='reissme',
                                                password='reissmyhandnow')

            sql_select_Query = """select Temperature,
                                    TDS,
                                    Resistance,
                                    Conductivity,
                                    Capacitance,
                                    Inductance,
                                    Time,
                                    Date_Recorded
                                    from temppy1
                                    WHERE (date_recorded BETWEEN '%s' AND '%s')"""%(from_tanggal, to_tanggal)
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            #records = cursor.fetchall()
            # print("Total number of rows in table: ", cursor.rowcount)

            # print("\nPrinting each row")
            # for row in records:
            #     print("TDS = ", row[0], )
            #     print("Resistance = ", row[1])
            #     print("Conductivity  = ", row[2])
            #     print("Capacitance = ", row[3], "\n")
            result = cursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number , data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            
            
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")



if __name__ == '__main__' :
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()

    try:
        sys.exit(app.exec_())
    except:
        print('cLOSING wINDOWS...')
