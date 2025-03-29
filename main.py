import sys
import os
import json
import cv2 as cv
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi


class KeilThemer(QWidget):
    THEME_FOLDER = "./themes"

    def __init__(self):
        super().__init__()

        # 设置工作目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        # 加载 UI 文件
        loadUi("KeilThemer.ui", self)
        self.setWindowTitle("Keil Theme")
        self.setWindowIcon(QIcon("icon.jpeg"))

        # 主题相关变量
        self.themes = []
        self.previews = {}
        self.theme_conf_path = None
        self.theme_preview = None
        self.theme = "default"

        # 初始化 UI
        self.list_refresh()

        # 读取 MDK 路径
        self.mdk_path = None
        self.load_mdk_path()
        self.target = (
            os.path.join(self.mdk_path, "UV4", "global.prop") if self.mdk_path else None
        )

    def list_refresh(self):
        """刷新主题列表"""
        self.listThemes.clear()
        self.themes.clear()
        self.previews.clear()

        theme_list = os.listdir(self.THEME_FOLDER)
        for theme in theme_list:
            self.listThemes.addItem(theme)
            self.themes.append(theme)
            preview_path = os.path.join(self.THEME_FOLDER, theme, "preview.png")
            self.previews[theme] = QPixmap(preview_path) if os.path.exists(preview_path) else None

        # 默认选择 "default" 主题
        self.theme = "default"
        if "default" in self.themes:
            self.listThemes.setCurrentRow(self.themes.index("default"))

    def load_theme_preview(self):
        """加载主题预览"""
        if self.previews.get(self.theme):
            self.labelPreview.setPixmap(self.previews[self.theme])
            self.labelPreview.setScaledContents(True)
        else:
            self.labelPreview.clear()
            self.labelPreview.setText("没有预览图, 请放置名为 preview.png 的预览图到主题文件夹内")

    def on_btn_themeCreate(self):
        """创建新主题"""
        name = self.nameCreate.text().strip()
        if not name:
            QMessageBox.warning(self, "错误", "请输入主题名称")
            return
        if name in self.themes:
            QMessageBox.warning(self, "错误", "主题名称已存在")
            return

        theme_path = os.path.join(self.THEME_FOLDER, name)
        os.makedirs(theme_path, exist_ok=True)

        if self.target and os.path.exists(self.target):
            with open(self.target, "r") as f:
                theme_conf = f.read()
            with open(os.path.join(theme_path, "global.prop"), "w") as f:
                f.write(theme_conf)

        QMessageBox.information(self, "提示", "主题创建成功")
        self.list_refresh()

    def on_btn_themeEffect(self):
        """应用当前选中的主题"""
        print(f"应用主题: {self.theme}")
        if self.theme_conf_path and os.path.exists(self.theme_conf_path):
            with open(self.theme_conf_path, "r") as f:
                theme_conf = f.read()
            with open(self.target, "w") as f:
                f.write(theme_conf)
            QMessageBox.information(self, "提示", "主题应用成功")
        else:
            QMessageBox.warning(self, "错误", "没有找到主题配置文件")

    def on_btn_themeReset(self):
        """重置为默认主题"""
        self.theme_conf_path = os.path.join(self.THEME_FOLDER, "default", "global.prop")
        if os.path.exists(self.theme_conf_path):
            with open(self.theme_conf_path, "r") as f:
                theme_conf = f.read()
            with open(self.target, "w") as f:
                f.write(theme_conf)
            QMessageBox.information(self, "提示", "主题重置成功")
        else:
            QMessageBox.warning(self, "错误", "没有找到默认主题配置文件")

    def on_btn_listRefresh(self):
        """刷新主题列表"""
        print("主题列表刷新")
        self.list_refresh()

    def on_list_selection(self):
        """当用户选择一个主题时，更新主题相关信息"""
        self.theme = self.listThemes.currentItem().text()
        print(f"选中主题: {self.theme}")

        self.theme_conf_path = os.path.join(self.THEME_FOLDER, self.theme, "global.prop")
        self.theme_preview = os.path.join(self.THEME_FOLDER, self.theme, "preview.png")

        if os.path.exists(self.theme_conf_path):
            self.load_theme_preview()
        else:
            self.theme_conf_path = None
            self.theme_preview = None
            if "default" in self.themes:
                self.listThemes.setCurrentRow(self.themes.index("default"))
            self.labelPreview.clear()
            self.labelPreview.setText("没有配置文件, 请在主题文件夹内放置名为 global.prop 的配置文件")

    def set_mdk_path(self):
        """设置 MDK 安装路径"""
        QMessageBox.information(self, "提示", "设置 MDK 的安装路径, 请选择包含 UV4 文件夹的目录")
        path = QFileDialog.getExistingDirectory(self, "选择 MDK 安装路径")
        if path and os.path.exists(os.path.join(path, "UV4")):
            self.labelMDK.setText(path)
            with open("config.json", "w") as f:
                json.dump({"mdk_path": path}, f)
        else:
            QMessageBox.warning(self, "错误", "选择的路径不正确, 请重新选择")
        self.load_mdk_path()

    def load_mdk_path(self):
        """加载 MDK 安装路径"""
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
            self.mdk_path = config.get("mdk_path", None)
            self.labelMDK.setText(self.mdk_path if self.mdk_path else "没有选择路径")
        else:
            self.labelMDK.setText("没有选择路径")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeilThemer()
    window.show()
    sys.exit(app.exec())
