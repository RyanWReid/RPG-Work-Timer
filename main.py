import sys
import time
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QHBoxLayout, QSizePolicy, QProgressBar
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from enemies import get_random_enemy
from quest_stay_on_guard import get_quest_events

class RPGTimerGame(QWidget):
    def __init__(self):
        super().__init__()
        
        self.health = 100
        self.stamina = 100
        self.gold = 50
        self.xp = 0
        self.work_time = 10  # 10 seconds for testing
        self.break_time = 10  # 10 seconds for testing
        self.cycle = 1
        self.quest_cycle = 0  # Track cycles within a quest
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 0
        self.is_working = True
        self.quest_events = get_quest_events()
        self.current_event_index = 0
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("RPG Work Timer")
        self.setGeometry(100, 100, 500, 500)
        
        self.layout = QVBoxLayout()
        
        # --- Stats Layout ---
        stats_layout = QHBoxLayout()
        
        left_stats_layout = QVBoxLayout()
        self.health_label = QLabel(f"Health: {self.health}")
        self.stamina_label = QLabel(f"Stamina: {self.stamina}")
        left_stats_layout.addWidget(self.health_label)
        left_stats_layout.addWidget(self.stamina_label)
        
        right_stats_layout = QVBoxLayout()
        self.gold_label = QLabel(f"Gold: {self.gold}")
        self.xp_label = QLabel(f"XP: {self.xp}")
        right_stats_layout.addWidget(self.gold_label)
        right_stats_layout.addWidget(self.xp_label)
        
        stats_layout.addLayout(left_stats_layout)
        stats_layout.addStretch()
        stats_layout.addLayout(right_stats_layout)
        
        self.layout.addLayout(stats_layout)
        
        # --- Timer Label ---
        self.timer_label = QLabel("00:10", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # --- Quest & Enemy Info ---
        self.quest_label = QLabel("No quest assigned yet.", self)
        self.quest_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.quest_label)
        
        self.enemy_label = QLabel("No enemy encountered.", self)
        self.enemy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.enemy_label)
        
        # --- Progress Bar ---
        self.quest_progress = QProgressBar(self)
        self.quest_progress.setMaximum(len(self.quest_events))
        self.quest_progress.setValue(0)
        self.layout.addWidget(self.quest_progress)
        
        # --- Log Box ---
        self.log = QTextEdit(self)
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(80)  # Reduce log size
        self.layout.addWidget(self.log)
        
        # --- Start Button ---
        self.start_button = QPushButton("Start Work", self)
        self.start_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.start_button.setStyleSheet("background-color: blue; color: white; font-weight: bold; padding: 10px;")
        self.start_button.clicked.connect(self.start_work)
        self.layout.addWidget(self.start_button)
        
        # --- Continue & Break Buttons ---
        self.buttons_layout = QHBoxLayout()
        
        self.continue_button = QPushButton("Continue Working", self)
        self.continue_button.setEnabled(False)
        self.continue_button.setStyleSheet("background-color: grey; color: white; padding: 10px;")
        self.continue_button.clicked.connect(self.start_work)
        self.buttons_layout.addWidget(self.continue_button)
        
        self.break_button = QPushButton("Take a Break (-10 HP)", self)
        self.break_button.setEnabled(False)
        self.break_button.setStyleSheet("background-color: grey; color: white; padding: 10px;")
        self.break_button.clicked.connect(self.take_break)
        self.buttons_layout.addWidget(self.break_button)
        
        self.layout.addLayout(self.buttons_layout)
        
        self.setLayout(self.layout)
    
    def start_work(self):
        self.is_working = True
        self.time_left = self.work_time
        self.current_event_index = 0
        self.log.append("--- Work session started! ---")
        self.timer.start(1000)
        self.start_button.setText("End Work")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.end_work)
        self.update()
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")
            self.update()
        else:
            self.timer.stop()
            self.display_next_quest_event()
            self.continue_work()
    
    def display_next_quest_event(self):
        if self.current_event_index < len(self.quest_events):
            event_text = self.quest_events[self.current_event_index]
            self.log.append(event_text)
            self.current_event_index += 1
            self.quest_progress.setValue(self.current_event_index)
            
            # 20% chance for an enemy attack
            if random.random() < 0.2:
                enemy = get_random_enemy()
                self.log.append(f"An enemy appears! {enemy.name} (HP: {enemy.hp}) says: '{enemy.speak()}'")
                self.health -= enemy.attack
                self.health_label.setText(f"Health: {self.health}")
                if self.health <= 0:
                    self.log.append("You have been defeated! Game over.")
                    self.start_button.setEnabled(False)
        
    def continue_work(self):
        # Enable Continue & Break buttons
        self.continue_button.setEnabled(True)
        self.continue_button.setStyleSheet("background-color: green; color: white; padding: 10px;")
        self.break_button.setEnabled(True)
        self.break_button.setStyleSheet("background-color: red; color: white; padding: 10px;")
        
        # Schedule the next event if quest isn't over
        if self.current_event_index < len(self.quest_events):
            QTimer.singleShot(60000, self.display_next_quest_event)  # 1-minute delay per event
        else:
            self.log.append("Quest completed!")
            self.xp += 50
            self.gold += 100
            self.update_stats()
    
    def update_stats(self):
        self.xp_label.setText(f"XP: {self.xp}")
        self.gold_label.setText(f"Gold: {self.gold}")
        self.health_label.setText(f"Health: {self.health}")
        self.stamina_label.setText(f"Stamina: {self.stamina}")
    
    def take_break(self):
        self.log.append("You chose to take a break! -10 HP!")
        self.health -= 10
        self.update_stats()
        if self.health <= 0:
            self.log.append("Your health dropped to 0! Game Over.")
            self.continue_button.setEnabled(False)
            self.break_button.setEnabled(False)
            return
        self.continue_button.setEnabled(False)
        self.break_button.setEnabled(False)
        self.timer.start(1000)
    
    def end_work(self):
        self.log.append("Work session ended. Goodbye!")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RPGTimerGame()
    game.show()
    sys.exit(app.exec())
