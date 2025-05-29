import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon

class RadioApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arabesk Radio Player")
        self.setWindowIcon(QIcon("src/icon.png"))

        self.setGeometry(200, 200, 500, 500)  
        self.setFixedSize(500, 500)  

        
        
        main_layout = QVBoxLayout()

       
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("src/background.jpg"))
        self.bg_label.setScaledContents(True)
        self.bg_label.resize(self.width(), self.height())

      
        self.song_label = QLabel("Select Radio")
        self.song_label.setFont(QFont("Arial", 14))
        self.song_label.setStyleSheet("color: white; font-weight: bold;")
        main_layout.addWidget(self.song_label, alignment=Qt.AlignmentFlag.AlignCenter)

     
        button_layout = QHBoxLayout()
        self.stations = {
            "Radyo Arabesk": ("https://yayin.radyoarabesk.com.tr:8000/stream", "src/radyo-arabesk.png"),
            "Damar FM": ("https://yayin.damarfm.com:8080", "src/DamarFM.png"),
            "Radyo 11": ("http://95.173.161.131:9832", "src/radyo11.png"),
            "Arabesk FM": ("https://yayin.arabeskfm.biz:8042", "src/arabeskFM.png")
        }
        self.station_buttons = []

        for name, (url, icon_path) in self.stations.items():
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))  
            btn.setIconSize(QSize(64, 64))  
            btn.setStyleSheet("border: none;") 
            btn.clicked.connect(lambda checked, url=url, name=name: self.change_station(url, name))
            button_layout.addWidget(btn)
            self.station_buttons.append(btn)

        main_layout.addLayout(button_layout)

       
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("src/play.png"))  
        self.play_button.setIconSize(QSize(80, 80))  
        self.play_button.setStyleSheet("border: none; border-radius: 40px; padding: 10px;")  
        main_layout.addWidget(self.play_button, alignment=Qt.AlignmentFlag.AlignCenter)

        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        main_layout.addWidget(self.volume_slider, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(self.volume_slider.value() / 100)
        self.current_station = None
        self.is_playing = False

        self.play_button.clicked.connect(self.toggle_play_stop)
        self.volume_slider.valueChanged.connect(self.change_volume)

    def toggle_play_stop(self):
        if self.is_playing:
            self.player.stop()
            self.play_button.setIcon(QIcon("src/play.png"))  
            self.song_label.setText("Now Playing: None")
        else:
            self.player.play()
            self.play_button.setIcon(QIcon("src/stop.png"))  
            self.song_label.setText("")
        self.is_playing = not self.is_playing

    def change_station(self, url, name):
        self.player.setSource(QUrl(url))
        self.current_station = url
        self.song_label.setText(f"Now Playing: {name}")
        self.player.play()
        self.play_button.setIcon(QIcon("src/stop.png")) 
        self.is_playing = True

        
        

    def change_volume(self):
        self.audio_output.setVolume(self.volume_slider.value() / 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadioApp()
    window.show()
    sys.exit(app.exec())
