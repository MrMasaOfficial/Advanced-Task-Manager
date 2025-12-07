import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, 
                             QComboBox, QLabel, QDialog, QMessageBox, QHeaderView, QFrame,
                             QScrollArea)
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
import db

CATEGORY_COLORS = {
    "عام": "#3498db",
    "عمل": "#e74c3c",
    "دراسة": "#f39c12",
    "صحة": "#27ae60",
    "شخصي": "#9b59b6"
}

STATUS_COLORS = {
    "pending": "#e74c3c",
    "in_progress": "#f39c12",
    "completed": "#27ae60"
}


class StyledButton(QPushButton):
    def __init__(self, text, style_type="primary"):
        super().__init__(text)
        self.style_type = style_type
        self.apply_style()
        
    def apply_style(self):
        if self.style_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1f618d;
                }
            """)
        elif self.style_type == "success":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
                QPushButton:pressed {
                    background-color: #1e8449;
                }
            """)
        elif self.style_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
                QPushButton:pressed {
                    background-color: #a93226;
                }
            """)
        elif self.style_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #34495e;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #2c3e50;
                }
                QPushButton:pressed {
                    background-color: #1a252f;
                }
            """)


class AddTaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()
        self.apply_styles()
        
    def init_ui(self):
        self.setWindowTitle("إضافة مهمة جديدة" if not self.task else "تعديل المهمة")
        self.setGeometry(100, 100, 550, 500)
        self.setStyleSheet("background-color: #ecf0f1;")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("العنوان:")
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("أدخل عنوان المهمة...")
        self.title_input.setMinimumHeight(35)
        if self.task:
            self.title_input.setText(self.task['title'])
        layout.addWidget(self.title_input)
        
        desc_label = QLabel("الوصف:")
        desc_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(desc_label)
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("أدخل وصف المهمة...")
        self.desc_input.setMinimumHeight(120)
        if self.task:
            self.desc_input.setText(self.task['description'] or "")
        layout.addWidget(self.desc_input)
        
        category_label = QLabel("التصنيف:")
        category_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(category_label)
        self.category_input = QComboBox()
        self.category_input.addItems(["عام", "عمل", "دراسة", "صحة", "شخصي"])
        self.category_input.setMinimumHeight(35)
        categories = db.get_categories()
        for cat in categories:
            if cat not in ["عام", "عمل", "دراسة", "صحة", "شخصي"]:
                self.category_input.addItem(cat)
        if self.task:
            self.category_input.setCurrentText(self.task['category'])
        layout.addWidget(self.category_input)
        
        if self.task:
            status_label = QLabel("الحالة:")
            status_label.setFont(QFont("Arial", 11, QFont.Bold))
            layout.addWidget(status_label)
            self.status_combo = QComboBox()
            self.status_combo.addItems(["قيد الانتظار", "قيد الإنجاز", "مكتملة"])
            self.status_combo.setMinimumHeight(35)
            status_map = {"pending": "قيد الانتظار", "in_progress": "قيد الإنجاز", "completed": "مكتملة"}
            self.status_combo.setCurrentText(status_map.get(self.task['status'], "قيد الانتظار"))
            layout.addWidget(self.status_combo)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        save_btn = StyledButton("حفظ المهمة", "success")
        cancel_btn = StyledButton("إلغاء", "secondary")
        save_btn.setMinimumHeight(40)
        cancel_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def apply_styles(self):
        self.title_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
        self.desc_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
        self.category_input.setStyleSheet("""
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
        """)
        
        if hasattr(self, 'status_combo'):
            self.status_combo.setStyleSheet("""
                QComboBox {
                    border: 2px solid #bdc3c7;
                    border-radius: 4px;
                    padding: 6px;
                    font-size: 12px;
                    background-color: white;
                }
                QComboBox:focus {
                    border: 2px solid #3498db;
                }
            """)
        
    def get_data(self):
        status_reverse_map = {"قيد الانتظار": "pending", "قيد الإنجاز": "in_progress", "مكتملة": "completed"}
        return {
            'title': self.title_input.text(),
            'description': self.desc_input.toPlainText(),
            'category': self.category_input.currentText(),
            'status': status_reverse_map.get(getattr(self, 'status_combo', None) and self.status_combo.currentText(), "pending")
        }


class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_styles()
        self.load_tasks()
        
    def init_ui(self):
        self.setWindowTitle("مدير المهام المتقدم")
        self.setGeometry(100, 100, 1400, 750)
        self.setMinimumSize(1000, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        header_widget = QFrame()
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(10)
        
        title_label = QLabel("مدير المهام")
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("تنظيم مهامك اليومية بكفاءة")
        subtitle_font = QFont("Arial", 10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #7f8c8d;")
        header_layout.addWidget(subtitle_label)
        
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #ecf0f1; border-radius: 8px; border: 1px solid #bdc3c7;")
        main_layout.addWidget(header_widget)
        
        controls_widget = QFrame()
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(15, 10, 15, 10)
        controls_layout.setSpacing(15)
        
        add_btn = StyledButton("+ إضافة مهمة جديدة", "primary")
        add_btn.setMinimumHeight(40)
        add_btn.setMinimumWidth(150)
        add_btn.clicked.connect(self.add_task)
        controls_layout.addWidget(add_btn)
        
        controls_layout.addWidget(QLabel("التصنيف:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("الكل")
        self.category_filter.addItems(["عام", "عمل", "دراسة", "صحة", "شخصي"])
        self.category_filter.setMinimumHeight(35)
        self.category_filter.setMinimumWidth(120)
        self.category_filter.currentTextChanged.connect(self.load_tasks)
        controls_layout.addWidget(self.category_filter)
        
        controls_layout.addWidget(QLabel("الحالة:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("الكل")
        self.status_filter.addItems(["قيد الانتظار", "قيد الإنجاز", "مكتملة"])
        self.status_filter.setMinimumHeight(35)
        self.status_filter.setMinimumWidth(120)
        self.status_filter.currentTextChanged.connect(self.load_tasks)
        controls_layout.addWidget(self.status_filter)
        
        controls_layout.addWidget(QLabel("بحث:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن مهمة...")
        self.search_input.setMinimumHeight(35)
        self.search_input.setMaximumWidth(250)
        self.search_input.textChanged.connect(self.load_tasks)
        controls_layout.addWidget(self.search_input)
        
        controls_layout.addStretch()
        
        controls_widget.setLayout(controls_layout)
        controls_widget.setStyleSheet("background-color: #fff; border-radius: 8px; border: 1px solid #ecf0f1;")
        main_layout.addWidget(controls_widget)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["#", "العنوان", "الوصف", "التصنيف", "الحالة", "الإجراءات"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(400)
        main_layout.addWidget(self.table)
        
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet("background-color: #f8f9fa;")
        
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTableWidget {
                border: 1px solid #ecf0f1;
                border-radius: 6px;
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
    def load_tasks(self):
        self.table.setRowCount(0)
        
        category_filter = self.category_filter.currentText()
        status_filter = self.status_filter.currentText()
        search_text = self.search_input.text().lower()
        
        status_map_reverse = {"قيد الانتظار": "pending", "قيد الإنجاز": "in_progress", "مكتملة": "completed"}
        status_filter_db = status_map_reverse.get(status_filter, None)
        
        if category_filter == "الكل" and (status_filter == "الكل" or not status_filter):
            tasks = db.get_all_tasks()
        elif category_filter != "الكل" and (status_filter == "الكل" or not status_filter):
            tasks = db.get_tasks_by_category(category_filter)
        elif category_filter == "الكل" and status_filter != "الكل":
            tasks = db.get_tasks_by_status(status_filter_db)
        else:
            all_tasks = db.get_all_tasks()
            tasks = [t for t in all_tasks if t['category'] == category_filter and t['status'] == status_filter_db]
        
        if search_text:
            tasks = [t for t in tasks if search_text in t['title'].lower() or search_text in (t['description'] or "").lower()]
        
        status_map = {"pending": "قيد الانتظار", "in_progress": "قيد الإنجاز", "completed": "مكتملة"}
        
        for i, task in enumerate(tasks):
            self.table.insertRow(i)
            
            id_item = QTableWidgetItem(str(task['id']))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, id_item)
            
            self.table.setItem(i, 1, QTableWidgetItem(task['title']))
            
            desc = task['description'] or ""
            if len(desc) > 60:
                desc = desc[:57] + "..."
            self.table.setItem(i, 2, QTableWidgetItem(desc))
            
            category_item = QTableWidgetItem(task['category'])
            category_color = CATEGORY_COLORS.get(task['category'], "#95a5a6")
            category_item.setBackground(QColor(category_color))
            category_item.setForeground(QColor("white"))
            category_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, category_item)
            
            status_text = status_map.get(task['status'], "قيد الانتظار")
            status_item = QTableWidgetItem(status_text)
            status_color = STATUS_COLORS.get(task['status'], "#95a5a6")
            status_item.setBackground(QColor(status_color))
            status_item.setForeground(QColor("white"))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 4, status_item)
            
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(5)
            actions_widget = QWidget()
            
            edit_btn = StyledButton("✎", "primary")
            edit_btn.setMaximumWidth(35)
            delete_btn = StyledButton("✕", "danger")
            delete_btn.setMaximumWidth(35)
            
            edit_btn.clicked.connect(lambda checked, tid=task['id']: self.edit_task(tid))
            delete_btn.clicked.connect(lambda checked, tid=task['id']: self.delete_task(tid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            actions_widget.setLayout(actions_layout)
            
            self.table.setCellWidget(i, 5, actions_widget)
            
            if task['status'] == 'completed':
                for j in range(6):
                    item = self.table.item(i, j)
                    if item:
                        font = item.font()
                        font.setStrikeOut(True)
                        item.setFont(font)
        
        self.table.resizeRowsToContents()
        
    def add_task(self):
        dialog = AddTaskDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            if data['title'].strip():
                db.add_task(data['title'], data['description'], data['category'])
                self.load_tasks()
            else:
                QMessageBox.warning(self, "تنبيه", "يجب إدخال عنوان المهمة")
    
    def edit_task(self, task_id):
        tasks = db.get_all_tasks()
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if task:
            dialog = AddTaskDialog(self, task)
            if dialog.exec_():
                data = dialog.get_data()
                if data['title'].strip():
                    db.update_task(task_id, data['title'], data['description'], data['category'], data['status'])
                    self.load_tasks()
                else:
                    QMessageBox.warning(self, "تنبيه", "يجب إدخال عنوان المهمة")
    
    def delete_task(self, task_id):
        reply = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذه المهمة بشكل نهائي؟", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db.delete_task(task_id)
            self.load_tasks()
