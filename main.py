import sys
from PyQt5.QtWidgets import QApplication
from app import TaskManagerApp
import db


if __name__ == '__main__':
    db.init_db()
    
    app_qt = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app_qt.exec_())
