APP_STYLE = """
QMainWindow, QWidget {
    background-color: #050914;
    color: #dbf7ff;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 13px;
}
QFrame#sidebar {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #0d1730, stop:1 #0a1023);
    border-right: 1px solid #284a72;
}
QFrame#topbar {
    background-color: rgba(13, 25, 48, 0.72);
    border: 1px solid #27486d;
    border-radius: 12px;
}
QFrame#contentPane {
    background-color: rgba(9, 16, 33, 0.72);
    border: 1px solid #203a5a;
    border-radius: 14px;
}
QFrame#heroCard {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #102747, stop:1 #133969);
    border: 1px solid #3d6e9f;
    border-radius: 16px;
}
QPushButton {
    background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #14325d, stop:1 #102647);
    color: #ddf9ff;
    border: 1px solid #2b5f91;
    border-radius: 11px;
    padding: 8px 12px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1a3e70;
    border: 1px solid #48d7ff;
}
QPushButton#navButton {
    text-align: left;
    padding-left: 12px;
}
QLabel#title {
    font-size: 23px;
    font-weight: 700;
    color: #69deff;
}
QFrame#card {
    background-color: rgba(20, 34, 60, 0.82);
    border: 1px solid #2d5682;
    border-radius: 16px;
}
QLabel#kpiTitle {
    color: #8ab4d8;
    font-size: 12px;
    letter-spacing: 0.6px;
}
QLabel#kpiValue {
    font-size: 25px;
    font-weight: 700;
    color: #9ef5ff;
}
QLineEdit, QComboBox, QTextEdit {
    background-color: #0f1b34;
    border: 1px solid #2f567f;
    border-radius: 11px;
    padding: 6px;
    color: #dcf7ff;
}
QTextEdit {
    selection-background-color: #2f80bd;
}
QProgressBar {
    border: 1px solid #3a6f9f;
    border-radius: 10px;
    background-color: #0c1931;
    text-align: center;
    color: #dbf7ff;
    font-weight: 700;
}
QProgressBar::chunk {
    border-radius: 8px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #00c3ff, stop:1 #00ffc8);
}
QScrollBar:vertical {
    border: none;
    background: #0d1629;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #275886;
    border-radius: 5px;
    min-height: 20px;
}
"""
