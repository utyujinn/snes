import sys
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QImage, QPixmap, qRgb
from PySide6.QtCore import Qt

# 提供されたバイナリの16進数ダンプ
HEX_DUMP = """
00000000    98 E0 E0 E8 F0 F8 48 90 70 58 A0 80 68 B0 90 78
00000010    C0 A0 88 D0 B0 98 E0 C0 98 E0 E0 00 00 00 D8 38
00000020    18 58 F8 58 98 E0 E0 00 00 00 E8 F0 F8 F8 58 58
00000030    98 E0 E0 E8 F0 F8 F8 F8 F8 00 00 00 00 C8 F8 00
00000040    E0 F8 00 F8 F8 00 F8 F8 98 E0 E0 00 00 00 58 A8
00000050    F0 F8 F8 F8 98 E0 E0 00 00 00 D8 A0 38 F8 D8 70
00000060    98 E0 E0 E8 F0 F8 00 00 00 48 78 00 60 A8 00 78
00000070    C8 00 C8 E0 00 F0 F8 A0 00 00 00 F8 F8 F8 00 00
00000080    00 00 C8 00 B0 00 00 F8 00 00 F8 58 00 F8 A0 00
00000090    98 E0 E0 E8 F0 F8 00 00 00 00 00 00 00 00 00 78
000000A0    20 78 C0 70 C0 F8 98 F8 00 00 00 F8 F8 F8 00 00
000000B0    00 00 C8 00 E8 18 68 F0 40 A8 F8 78 C8 F8 C0 F0
000000C0    98 E0 E0 E8 F0 F8 70 70 70 00 00 00 C0 C0 C0 A0
000000D0    C8 F8 A8 E0 F8 C0 F8 F8 00 00 00 F8 F8 F8 00 00
000000E0    00 00 C8 00 00 E0 00 88 F8 38 C8 F8 00 F8 F8 98
000000F0    98 E0 E0 E8 F0 F8 00 00 00 B8 A8 60 D8 F8 C8 00
00000100    80 00 00 C8 00 00 F8 00 00 00 00 00 00 00 00 00
00000110    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00000120    98 E0 E0 E8 F0 F8 00 00 00 88 58 18 F8 08 F8 D8
00000130    A0 38 F8 D8 20 F8 F8 00 00 00 00 00 00 00 00 00
00000140    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00000150    98 E0 E0 E8 F0 F8 00 00 00 B8 00 50 F8 00 80 48
00000160    48 88 68 68 B0 80 80 C8 00 00 00 00 00 00 00 00
00000170    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00000180    98 E0 E0 F8 F8 F8 00 00 00 C0 A0 00 D8 A0 38 F8
00000190    D8 70 F8 D0 C0 E8 00 B0 50 00 00 F8 80 F8 20 30
000001A0    88 80 F8 00 80 D8 C8 B0 28 60 B0 B0 B0 F8 F8 00
000001B0    98 E0 E0 F8 F8 F8 00 00 00 70 70 70 A0 A0 A0 C0
000001C0    C0 C0 E0 E0 E0 F8 10 58 00 00 00 F8 F8 F8 00 00
0CHAPTER_A1D0    00 00 C8 00 B0 00 00 F8 00 00 F8 58 00 F8 A0 00
000001E0    98 E0 E0 F8 F8 F8 00 00 00 F8 78 00 F8 C0 00 F8
000001F0    F8 00 B8 28 00 F8 88 00 00 00 00 F8 F8 F8 00 00
00000200    00 00 C8 00 E8 18 68 F0 40 A8 F8 78 C8 F8 C0 F0
00000210    98 E0 E0 F8 F8 F8 00 00 00 40 40 D8 68 68 D8 88
00000220    88 F8 B8 28 00 F8 88 00 00 00 00 F8 F8 F8 00 00
00000230    00 00 C8 00 00 E0 00 88 F8 38 C8 F8 00 F8 F8 98
00000240    98 E0 E0 F8 F8 F8 00 00 00 88 00 00 B8 00 00 F8
00000250    00 00 B8 28 00 F8 88 00 00 00 00 00 00 00 00 00
00000260    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00000270    98 E0 E0 F8 F8 F8 00 00 00 00 78 00 00 B8 00 00
00000280    F8 00 B8 28 00 F8 88 00 00 00 00 00 00 00 00 00
00000290    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
000002A0    98 E0 E0 F8 F8 F8 00 00 00 28 30 48 48 50 58 68
000002B0    68 58 98 90 40 C0 C0 78 00 00 00 00 00 00 00 00
000002C0    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
000002D0    98 E0 E0 F8 F8 F8 18 48 48 20 70 68 28 88 78 30
000002E0    A0 88 38 B8 98 F8 00 80 00 00 00 00 00 00 00 00
000002F0    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
"""

def parse_hex_dump(dump: str) -> bytes:
    """
    16進数ダンプ文字列からバイナリデータを抽出する
    """
    hex_string = ""
    # 各行から16進数部分のみを抽出
    for line in dump.strip().split('\n'):
        # '00000000    XX XX ...' のような形式を想定
        parts = line.split('   ')
        if len(parts) > 1:
            # 16進数部分を取得し、スペースを除去
            hex_part = parts[1].split('  ')[0]
            hex_string += hex_part.replace(' ', '')
    return bytes.fromhex(hex_string)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RGB Binary Image Viewer")

        # 画像の仕様
        image_width = 16
        bytes_per_pixel = 3

        # バイナリデータをパース
        binary_data = parse_hex_dump(HEX_DUMP)
        
        # データ長から画像の高さを計算
        data_length = len(binary_data)
        if data_length % (image_width * bytes_per_pixel) != 0:
             print("警告: データサイズが画像の幅に合っていません。")

        image_height = data_length // (image_width * bytes_per_pixel)

        # QImageを作成
        self.image = QImage(image_width, image_height, QImage.Format_RGB888)
        
        # ピクセルデータをQImageに書き込む
        for y in range(image_height):
            for x in range(image_width):
                index = (y * image_width + x) * bytes_per_pixel
                if index + 2 < data_length:
                    r, g, b = binary_data[index], binary_data[index+1], binary_data[index+2]
                    self.image.setPixel(x, y, qRgb(r, g, b))

        # 画像を表示するためのQLabel
        self.image_label = QLabel()
        # QImageからQPixmapを作成し、拡大表示
        pixmap = QPixmap.fromImage(self.image)
        # 画像が小さいので、見やすいように拡大する (例: 32倍)
        self.image_label.setPixmap(pixmap.scaled(image_width * 32, image_height * 32, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.image_label)
        self.resize(image_width * 32 + 40, image_height * 32 + 40)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
