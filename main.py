from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from db import Db
import operator
import backend
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import os
# seaborn data

# Show savings had





CITIES = ["Vancouver", "Edmonton", "Toronto", "Montreal", "Ottawa", \
          "Calgary", "Hamilton", "Winnipeg", "Quebec-City", "Newmarket-ON-Canada","Halifax"]


PROVINCES = ["Ontario","Quebec","British Columbia","Alberta","Manitoba","Saskatchewan",\
             "Nova Scotia","New Brunswick",]



PROVINCES_CITIES ={"Toronto,Ottawa,Hamilton,Newmarket-ON-Canada":"Ontario","Montreal,Quebec-City":"Quebec",\
                   "Vancouver":"British Columbia","Edmonton,Calgary":"Alberta",
                    "Winnipeg":"Manitoba","Halifax":"NovaScotia"}





class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()

        self.Explabel = QLabel("Rent Expense App")

        self.Explabel.setFont(QFont('Monospace', 50))

        self.sallabel = QLabel("Salary")
        self.salqline = QLineEdit()

        self.salqline.setWindowIcon(QIcon("images/home.png"))

        self.sallabel.setFont(QFont('Monospace', 25))
        self.sallabel.setAlignment(Qt.AlignCenter)
        image = QLabel()
        # Resize images
        image.setScaledContents(True)

        image.setPixmap(QPixmap('images/rentsign.jpg'))
        image.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.desiredsavings = QLabel("Desired Savings")

        self.desiredsavings.setFont(QFont('Monospace', 25))

        self.desiredsavings.setAlignment(Qt.AlignCenter)

        self.desavqline = QLineEdit()

        self.wherebutton = QPushButton("Where can I afford to live ?")
        palette = self.wherebutton.palette()
        role = self.wherebutton.backgroundRole()  # choose whatever you like
        palette.setColor(role, QColor('green'))
        self.wherebutton.setPalette(palette)

        self.wherebutton.pressed.connect(self.live_button_pressed)
        self.labels = [image, self.Explabel, self.sallabel, self.salqline, self.desiredsavings, self.desavqline,
                       self.wherebutton]
        for label in self.labels:
            layout.addWidget(label)
        self.desavqline.returnPressed.connect(self.return_Pressed)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # self.widget = QLineEdit()
        self.setWindowTitle("Expense App")

        # self.widget.setMaxLength(10)
        # self.widget.setPlaceholderText("Enter your text")
        # widget.setReadOnly(True) # uncomment this to make readonly
        # self.widget.returnPressed.connect(self.return_pressed)
        # self.setCentralWidget(self.widget)

    def live_button_pressed(self):
        self.return_Pressed()

    def return_Pressed(self):
        if self.error_check():
            return 0

        X = []
        Y = []

        layout = QVBoxLayout()
        self.toolbar = QToolBar("This is a tool bar")
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(30, 30))
        button_action = QAction(QIcon("images/arrow-180.png"), "Your button", self)
        button_action.triggered.connect(self.back_button_triggered)
        self.toolbar.addAction(button_action)
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        self.affordable_places = self.compute_places_to_live()
        counter = 1
        db = Db("CityExpenses")

        for city, saving in self.affordable_places[2]:
            X.append(city[:3])
            Y.append(float(saving))
            image = QLabel()
            # Resize images

            image.setPixmap(QPixmap('images/' + city))
            image.setAlignment(Qt.AlignCenter)
            image.setScaledContents(True)
            deductables = ""
            all_vals = ''
            data = db.get_data(city)
            description = data[0][3]
            layout = QVBoxLayout()

            widget = QWidget()
            label = QLabel(city)
            label.setFont(QFont('Courier', 50))
            label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            title = str(counter) + "-" + city
            counter += 1
            layout.addWidget(label)
            for key, value in self.affordable_places[1][city].items():
                # Deduc Label

                deductables += str(key).capitalize() + " : " + str(value) + '\n'

                deductables_label = QLabel(deductables)
                deductables_label.setFont(QFont('Courier', 20))
                deductables_label.font().setBold(True)
                deductables_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            layout.addWidget(image)
            layout.addWidget(deductables_label)
            rent = "1br Rent Cost: $" + str(self.affordable_places[0][city]) + ' '
            rent_label = QLabel(rent)
            rent_label.setFont(QFont('Courier', 15))
            layout.addWidget(rent_label)
            saving = str(saving)[:2] + ',' + str(saving)[2:]
            saving_label = QLabel("Savings :$" + str(saving))
            saving_label.setFont(QFont('Courier', 15))
            layout.addWidget(saving_label)

            description = '\n' + '\n' \
                          + self.formatdata(description)

            label_description = QLabel(description)
            label_description.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            layout.addWidget(label_description)

            widget.setLayout(layout)
            self.setCentralWidget(widget)
            tabs.addTab(widget, title)

            if len(self.affordable_places[2]) == counter - 1:
                layout_stats = QVBoxLayout()
                stats_widget = QWidget()
                stats_image = QLabel()

                header = QLabel("Savings Statistics")
                header.setFont(QFont('Monospace', 50))
                self.create_statistics_pic(X, Y)
                stats_image.setPixmap(QPixmap("images/savings.jpg"))
                header.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                stats_image.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
                layout_stats.addWidget(stats_image)
                layout_stats.addWidget(header)

                stats_widget.setLayout(layout_stats)

                self.setCentralWidget(stats_widget)
                tabs.addTab(stats_widget, "Savings Statistics")

        self.setCentralWidget(tabs)

    def back_button_triggered(self):
        self.removeToolBar(self.toolbar)
        layout = QVBoxLayout()

        self.Explabel = QLabel("Rent Expense App")

        self.Explabel.setFont(QFont('Monospace', 50))

        self.sallabel = QLabel("Salary")
        self.salqline = QLineEdit()

        self.sallabel.setFont(QFont('Monospace', 25))
        self.sallabel.setAlignment(Qt.AlignCenter)
        image = QLabel()
        # Resize images

        image.setPixmap(QPixmap('images/rentsign.jpg'))
        image.setAlignment(Qt.AlignTop | Qt.AlignRight)
        image.setScaledContents(True)
        self.desiredsavings = QLabel("Desired Savings")

        self.desiredsavings.setFont(QFont('Monospace', 25))

        self.desiredsavings.setAlignment(Qt.AlignCenter)

        self.desavqline = QLineEdit()

        self.wherebutton = QPushButton("Where can I afford to live ?")
        palette = self.wherebutton.palette()
        role = self.wherebutton.backgroundRole()  # choose whatever you like
        palette.setColor(role, QColor('green'))
        self.wherebutton.setPalette(palette)

        self.wherebutton.pressed.connect(self.live_button_pressed)
        self.labels = [image, self.Explabel, self.sallabel, self.salqline, self.desiredsavings, self.desavqline,
                       self.wherebutton]
        for label in self.labels:
            layout.addWidget(label)
        self.desavqline.returnPressed.connect(self.return_Pressed)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # self.widget = QLineEdit()
        self.setWindowTitle("Expense App")

    def compute_places_to_live(self):
        PROVINCES = {"Ontario": ["Toronto", "Ottawa", "Hamilton", "Newmarket-ON-Canada"],
                     "Quebec": ["Montreal", "Quebec-City"], "British Columbia": ["Vancouver"], \
                     "Alberta": ["Edmonton", "Calgary"],
                     "Manitoba": ["Winnipeg"], "Nova Scotia": ["Halifax"]}
        CITIES = ["Vancouver", "Edmonton", "Toronto", "Montreal", "Ottawa", \
                  "Calgary", "Hamilton", "Winnipeg", "Quebec-City", "Newmarket-ON-Canada", "Halifax"]
        salary = self.salqline.text()
        desired_savings = self.desavqline.text()
        db = Db("CityExpenses")
        rent = {}
        deductable_info = {}
        savings = {}
        for city in CITIES:
            data = db.get_data(city=city)
            province = data[0][4]
            net_inc_and_deduc = backend.get_netincome(province, salary)
            net_pay = ''.join([i for i in net_inc_and_deduc['Net pay'] if i.isdigit() or i == '.'])
            income_to_spend = float(net_pay) - float(desired_savings)
            monthly_income_to_spend = income_to_spend
            if data[0][1] <= monthly_income_to_spend / 12:
                post_savings = income_to_spend - (data[0][1] * 12)
                total_savings = float(desired_savings) + post_savings
                savings[city] = total_savings
                deductable_info[city] = net_inc_and_deduc
                rent[city] = data[0][1]
        # sorted_afford_citites = sorted(affordable_cities.items(), key=operator.itemgetter(1))
        sorted_savings = sorted(savings.items(), key=operator.itemgetter(1), reverse=True)
        return rent, deductable_info, sorted_savings

    @staticmethod
    def formatdata(data, freq=15, sentenceamt=5):
        data = data.split(".")
        data = data[:sentenceamt]
        data = ".".join(data).split(" ")
        counter = 0
        newdata = []
        for word in data:
            counter += 1
            if counter % freq == 0:
                newdata.append(word)
                newdata.append('\n')
                newdata.append('\n')

            else:
                newdata.append(word)
        return " ".join(newdata)

    def error_check(self):
        number_check_sal = [i.isdigit() for i in self.salqline.text()]

        number_check_des = [i.isdigit() for i in self.desavqline.text()]

        if not self.desavqline.text() or not self.salqline.text():
            dlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(
                QLabel("Please ensure both fields are filled"))
            dlg.setLayout(layout)

            dlg.setWindowTitle("Error!")

            dlg.exec_()
            return 1


        elif False in number_check_sal:
            dlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(
                QLabel("Please enter numbers for salary and desired savings and ensure value greater than 0"))
            dlg.setLayout(layout)

            dlg.setWindowTitle("Error!")

            dlg.exec_()
            return 1

        elif False not in number_check_sal:
            sal = float(''.join([i for i in self.salqline.text()]))
            des = float(''.join([i for i in self.desavqline.text()]))
            if des > sal:

                dlg = QDialog(self)
                layout = QVBoxLayout()
                layout.addWidget(QLabel("Please ensure your Salary is greater than your desired savings"))
                dlg.setLayout(layout)

                dlg.setWindowTitle("Error!")

                dlg.exec_()
                return 1
            elif sal < 7000:
                dlg = QDialog(self)
                layout = QVBoxLayout()
                layout.addWidget(QLabel("Please ensure your Salary is greater than 7000"))
                dlg.setLayout(layout)

                dlg.setWindowTitle("Error!")

                dlg.exec_()
                return 1
            elif sal <= 0 or des <= 0:
                dlg = QDialog(self)
                layout = QVBoxLayout()
                layout.addWidget(QLabel("Please ensure your Salary and desired savings are greater than 0"))
                dlg.setLayout(layout)

                dlg.setWindowTitle("Error!")

                dlg.exec_()
                return 1
            elif sal - des <= 19999:
                dlg = QDialog(self)
                layout = QVBoxLayout()
                layout.addWidget(
                    QLabel("The difference between your salary and desired savings must be $20,000 or greater"))
                dlg.setLayout(layout)
                dlg.setWindowTitle("Error!")

                dlg.exec_()
                return 1
        return 0
    @staticmethod
    def create_statistics_pic(x, y):

        y_pos = np.arange(len(x))
        performance = y

        plt.bar(y_pos, performance, align='center', color='g', alpha=0.5)
        plt.xticks(y_pos, x)
        plt.ylabel('Savings')
        plt.title('Savings Compared By City')

        plt.savefig("images/savings.jpg")

if __name__ == "__main__":
    db_created = [content for content in os.listdir() if content == 'CityExpenses']
    if not db_created:
        backend.create_and_store(PROVINCES_CITIES)
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

