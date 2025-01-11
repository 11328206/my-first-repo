from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QColorDialog
from PyQt6 import uic
from PyQt6.QtCore import QDateTime, QTimer
from PyQt6.QtGui import QColor
import sys
import json
import os


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        # 載入 UI
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'todo_final.ui'), self)

        # 初始化功能
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.markCompleteButton.clicked.connect(self.mark_complete)
        self.sortButton.clicked.connect(self.sort_tasks)
        self.changeColorButton.clicked.connect(self.change_task_color)  # 新功能按鈕
        self.priorityComboBox.addItems(["High", "Medium", "Low"])  # 優先級選項

        # 初始化 QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_due_tasks)

        # 連接通知時間設定
        self.notificationIntervalSpinBox.valueChanged.connect(self.update_timer_interval)
        self.notificationIntervalSpinBox.setValue(60)  # 預設 60 分鐘
        self.update_timer_interval()

        # 載入任務
        self.load_tasks()

    def update_timer_interval(self):
        """更新通知時間間隔"""
        interval_minutes = self.notificationIntervalSpinBox.value()
        self.timer.start(interval_minutes * 60000)  # QTimer 使用毫秒

    def add_task(self):
        task = self.taskInput.text()
        priority = self.priorityComboBox.currentText()
        due_date = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm")
        if task.strip():
            task_text = f"[{priority}] {task} - Due: {due_date}"
            self.taskList.addItem(task_text)
            self.taskInput.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Error", "Task cannot be empty")

    def delete_task(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            self.taskList.takeItem(self.taskList.row(selected_task))
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Error", "No task selected")

    def mark_complete(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            font = selected_task.font()
            font.setStrikeOut(True)
            selected_task.setFont(font)
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Error", "No task selected")

    def sort_tasks(self):
        items = [self.taskList.item(i).text() for i in range(self.taskList.count())]
        # 排序方式：按優先級 -> 任務名稱
        items.sort(key=lambda x: ("High" not in x, "Medium" not in x, x.lower()))
        self.taskList.clear()
        self.taskList.addItems(items)
        self.save_tasks()

    def check_due_tasks(self):
        """檢查即將到期的任務，並突出顯示"""
        now = QDateTime.currentDateTime()

        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            task_text = item.text()

            if "Due:" in task_text:
                due_date_str = task_text.split("Due:")[1].strip()
                due_date = QDateTime.fromString(due_date_str, "yyyy-MM-dd HH:mm")

                # 設定任務的顏色
                if now.secsTo(due_date) <= 1800 and now.secsTo(due_date) > 0:  # 距離 30 分鐘以內
                    item.setBackground(QColor("orange"))
                elif now.secsTo(due_date) <= 0:  # 已過期
                    item.setBackground(QColor("red"))
                else:  # 正常任務
                    item.setBackground(QColor("white"))

    def change_task_color(self):
        """讓使用者選擇任務的背景顏色"""
        selected_task = self.taskList.currentItem()
        if selected_task:
            # 打開顏色選擇對話框
            color = QColorDialog.getColor()
            if color.isValid():  # 如果選擇了有效顏色
                selected_task.setBackground(color)
                self.save_tasks()
        else:
            QMessageBox.warning(self, "Error", "No task selected")

    def save_tasks(self):
        tasks = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            tasks.append({
                'text': item.text(),
                'completed': item.font().strikeOut(),
                'background': item.background().color().name()  # 保存背景顏色
            })
        with open(os.path.join(os.path.dirname(__file__), 'tasks.json'), 'w') as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'tasks.json'), 'r') as f:
                tasks = json.load(f)
                for task in tasks:
                    item = QListWidgetItem(task['text'])
                    font = item.font()
                    font.setStrikeOut(task['completed'])
                    item.setFont(font)
                    item.setBackground(QColor(task.get('background', 'white')))  # 恢復背景顏色
                    self.taskList.addItem(item)
        except FileNotFoundError:
            pass


# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
