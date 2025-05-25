# Fatgeyah Zoutenberg (ZTNFAT001)
# Amukelani Rikhotso (RKHAMU004)
#this is an oxo game for ten-eleven games 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from play_loop_thread import *
from collections import Counter


class TutorialWindow(QWidget):# create a tutorial window 
    def __init__(self,parent = None):
        QScrollArea.__init__(self)
        QWidget.__init__(self)
        self.setWindowTitle("How to play") # set a title
        self.setGeometry(0,0,600,700)
      
        heading = QLabel('DON\'T KNOW HOW TO PLAY?!\nHAVE NO WORRIES, HERE IS A TUTORIAL!')
        heading.setFont(QFont('Britannic Bold',12) )# set a heading
        
        connecting = QLabel('> First you have to connect to the server. Enter the server name in the space provided, then click the connect button.\n> Messages will appear in the messages box.')
        connecting.setFont(QFont('Cascadia Code',10))
        connecting.setWordWrap(True)
        
        play = QLabel('> Now, how to actually play the game: Once you get the \'Your move\' message in the message box, click any empty box on the game board. If the move is invalid you will get another \'your move\' message and you will need enter another move. If you get the \'opponents move\' message then wait until your opponent has made a move. If your opponent has made an invalid move you will get another \'opponents move\' message.')
        play.setFont(QFont('Cascadia Code',10))
        play.setWordWrap(True)
        
        win = QLabel('> The most important question is, \'How do I win?\'. Well it\'s simple really you just have to get 3 of your shapes in a row. It can be vertically, horizontally or diagonally, as long as it is 3 in a row you will win!')
        win.setFont(QFont('Cascadia Code',10))
        win.setWordWrap(True)
        
        score = QLabel('> There is also a scoreboard. If you are playing multiple games the scoreboard will keep track of how many times each player has won, how many games you have played and a timer')
        score.setFont(QFont('Cascadia Code',10))
        score.setWordWrap(True)     

        end = QLabel('GOODLUCK!!! HAVE FUN!')
        end.setFont(QFont('Britannic Bold',11))
            
        close = QPushButton('Close')
        close.setFont(QFont('Britannic Bold',10))
        
        # set baclground colour
        self.setPalette(QPalette(QColor(220,180,255)))
        self.setAutoFillBackground(True)
        
        # picture of gui
        gui_pixmap = QPixmap('gui.png')
        gui_pic_label = QLabel()
        gui_pic_label.setPixmap(gui_pixmap)     
        
        # layout the tutorial window
        vbox = QVBoxLayout()
        vbox.addWidget(heading)
        vbox.addWidget(connecting)
        vbox.addWidget(play)
        vbox.addWidget(win)
        vbox.addWidget(score)
        vbox.addWidget(gui_pic_label)
        vbox.addWidget(end)
        vbox.addWidget(close)
        self.setLayout(vbox)

        #close clicked
        close.clicked.connect(self.close_clicked)
        
    #close window if close button is clicked
    def close_clicked(self):
        self.close()

class PlayAgainWindow(QWidget):# create a play again window
    # Define a signal for play again and for exit game
    play_again_signal = pyqtSignal(str)
    exit_game_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Again")
        self.setGeometry(300, 300, 300, 200)
        self.play_again_window()
        self.setWindowIcon(QIcon("images.jpeg"))

    def play_again_window(self):
        play_again_label = QLabel("Do you want to play again?")
        play_again_label.setAlignment(Qt.AlignCenter)
        play_again_label.setFont(QFont('Cascadia Code',15))

        yes_button = QPushButton("Yes")
        yes_button.setFont(QFont('Britannic Bold',11))
        no_button = QPushButton("No")
        no_button.setFont(QFont('Britannic Bold',11))
        
        self.setPalette(QPalette(QColor(225,180,255))) 
        self.setAutoFillBackground(True)
        #layout for thw play again window
        layout = QVBoxLayout()
        layout.addWidget(play_again_label)
        layout.addWidget(yes_button)
        layout.addWidget(no_button)
        self.setLayout(layout)
        
        #yes button clicked
        yes_button.clicked.connect(self.on_play_again)
        no_button.clicked.connect(self.no_clicked)

    def on_play_again(self):
        # Emit the play_again_signal when "Yes" button is clicked
        try:
            self.play_again_signal.emit('y')
            self.close()
            
        except Exception as p:
            print(p)
        
        #Emit signal if exit game is clicked
    def no_clicked(self):
        try:
            self.exit_game_signal.emit('n')
            self.close() 
            
        except Exception as d:
            print(d)

    

class MainWindow(QWidget, GameClient):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        GameClient.__init__(self)
        self.setGeometry(50, 100, 900, 550)
        self.setWindowIcon(QIcon("images.jiif"))
        self.setWindowTitle('OXO Game')# set a window title
        self.shape = None
        
        #Create an instance of PlayAgainWindow
        self.play_again_window = PlayAgainWindow()
        self.play_again_window.play_again_signal.connect(self.play_again)# receive play_again signal
        self.play_again_window.exit_game_signal.connect(self.exit_game)#receive the exit game signal
        
        
        # create labels and buttons
        self.server_label = QLabel('Server:')#server label
        self.server_label.setFont(QFont('Britannic Bold',11))
        self.server_editBox = QLineEdit()# server edit box
       
        self.server_editBox.setPlaceholderText('Enter server')
        self.server_editBox.setFont(QFont('Cascadia Code',9))
        
        self.Connect_button = QPushButton('Connect')#connect button
        self.Connect_button.setFont(QFont('Britannic Bold',10))
        
        self.tutorial_button = QPushButton('Tutorial')#tutorial button
        self.tutorial_button.setFont(QFont('Britannic Bold',10))
        
        self.Close = QPushButton('Close')
        self.Close.setFont(QFont('Britannic Bold',10))
        #**************************************************************************
        
        
        
       
        # buttons for board and setting size for buttons
        
        self.button_0 = QPushButton()
        self.button_0.setMinimumSize(100,100)
        self.button_1 = QPushButton()
        self.button_1.setMinimumSize(100,100)
        self.button_2 = QPushButton()
        self.button_2.setMinimumSize(100,100)
        self.button_3 = QPushButton()
        self.button_3.setMinimumSize(100,100)
        self.button_4 = QPushButton()
        self.button_4.setMinimumSize(100,100)
        self.button_5 = QPushButton()
        self.button_5.setMinimumSize(100,100)
        self.button_6 = QPushButton()
        self.button_6.setMinimumSize(100,100)
        self.button_7 = QPushButton()
        self.button_7.setMinimumSize(100,100)
        self.button_8 = QPushButton()
        self.button_8.setMinimumSize(100,100)
        #**************************************************************************
        
        
      
        # labels for scoreboard
        self.scoreboard_heading = QLabel('SCOREBOARD ')
        self.scoreboard_heading.setFont(QFont('Britannic Bold',11))
        
        self.player1_label = QLabel('Player X:')#player X label
        self.player1_label.setFont(QFont('Cascadia Code',9))
        self.p1 = QLabel('0')
        self.p1.setFont(QFont('Cascadia Code',9))
        self.player2_label = QLabel('Player O:')# player O label
        self.player2_label.setFont(QFont('Cascadia Code',9))
        self.p2 = QLabel('0')
        self.p2.setFont(QFont('Cascadia Code',9))
        
        self.tie_label = QLabel('Tie:')# tie label
        self.tie_label.setFont(QFont('Cascadia Code',9))
        self.tie = QLabel('0')
        self.tie.setFont(QFont('Cascadia Code',9))
        
        self.total_games_label = QLabel('Games played: ')# number of games played label
        self.total_games_label.setFont(QFont('Cascadia Code',9))
        self.games = QLabel('0')
        self.games.setFont(QFont('Cascadia Code',9))
        
        self.time_label = QLabel('Time:')# time label
        self.time_label.setFont(QFont('Cascadia Code',9))
        self.time = QLabel('00:00')
        self.time.setFont(QFont('Cascadia Code',9))
        #************************************************************************
        
        
             
        # labels for message box
        self.message_heading = QLabel('MESSAGES')
        self.message_heading.setFont(QFont('Britannic Bold',11))
        self.message_heading.setMinimumSize(30,50)
        self.messages_edit_box = QTextEdit()#messages box
        self.messages_edit_box.setFont(QFont('Cascadia Code',9))
        self.messages_edit_box.setReadOnly(True)
        self.messages_edit_box.setOverwriteMode(False)
        self.messages_edit_box.setMinimumSize(250,350)
        #************************************************************************
        
        
               
        # board layout
        self.board_grid = QGridLayout()
        self.board_grid.addWidget(self.button_0,0,0)
        self.board_grid.addWidget(self.button_1,0,1)
        self.board_grid.addWidget(self.button_2,0,2)
        self.board_grid.addWidget(self.button_3,1,0)
        self.board_grid.addWidget(self.button_4,1,1)
        self.board_grid.addWidget(self.button_5,1,2)
        self.board_grid.addWidget(self.button_6,2,0)
        self.board_grid.addWidget(self.button_7,2,1)
        self.board_grid.addWidget(self.button_8,2,2)
        self.board_grid_widget = QWidget()
        self.board_grid_widget.setLayout(self.board_grid)
        #************************************************************************
        
        
        # change background colour of game board
        self.board_grid_widget.setPalette(QPalette(QColor(225,180,255))) 
        self.board_grid_widget.setAutoFillBackground(True)
        self.board_grid_widget.setMinimumSize(350,350) # set minimum size of board
        self.board_grid_widget.setMaximumSize(700,700)
        #************************************************************************
        
        # scoreboard layout
        self.score_grid = QGridLayout()
        self.score_grid.addWidget(self.scoreboard_heading,0,0)
        self.score_grid.addWidget(self.player1_label,1,0)
        self.score_grid.addWidget(self.p1,1,1)
        self.score_grid.addWidget(self.player2_label,2,0)
        self.score_grid.addWidget(self.p2,2,1)
        self.score_grid.addWidget(self.tie_label,3,0)
        self.score_grid.addWidget(self.tie,3,1)
        self.score_grid.addWidget(self.total_games_label,4,0)
        self.score_grid.addWidget(self.games,4,1)
        self.score_grid.addWidget(self.time_label,6,0)
        self.score_grid.addWidget(self.time,6,1)
        self.score_grid_widget = QWidget()
        self.score_grid_widget.setLayout(self.score_grid)
        self.score_grid_widget.setMinimumSize(250,200) # set minimum size 
        self.score_grid_widget.setStyleSheet('border:1px solid black;') # create border around score board
        #************************************************************************
        
        
        
        # messages layout
        self.message_vbox = QVBoxLayout()
        self.message_vbox.addWidget(self.message_heading)
        self.message_vbox.addWidget(self.messages_edit_box)
        #************************************************************************
        
        self.message_vbox_widget = QWidget()
        self.message_vbox_widget.setLayout(self.message_vbox)  
        self.message_vbox_widget.setStyleSheet('border:1px solid black;') # create border around message box and heading
        #************************************************************************
        
        # server edit boxes and buttons layout
        self.server_hbox = QHBoxLayout()
        self.server_hbox.addWidget(self.server_label)
        self.server_hbox.addWidget(self.server_editBox)
        self.server_hbox.addWidget(self.Connect_button)
        self.server_hbox.addWidget(self.tutorial_button)
        self.server_hbox.addWidget(self.Close)
        self.server_hbox_widget = QWidget()
        self.server_hbox_widget.setMinimumSize(100,75)
        self.server_hbox_widget.setLayout(self.server_hbox)
        #************************************************************************
        
        # middle of window layout
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.score_grid_widget)
        self.hbox.addWidget(self.board_grid_widget)
        self.hbox.addWidget(self.message_vbox_widget)
        self.hbox_widget = QWidget()
        self.hbox_widget.setLayout(self.hbox)
        #************************************************************************
        
        # final layout
        self.final_vbox = QVBoxLayout()
        self.final_vbox.addWidget(self.hbox_widget)
        self.final_vbox.addWidget(self.server_hbox_widget)
        self.final_vbox_widget = QWidget()
        self.setLayout(self.final_vbox)
        #************************************************************************
        
        # change background colour
        self.setPalette(QPalette(QColor(227,227,227)))
        self.setAutoFillBackground(True) 
        #************************************************************************
        
        # create thread for play loop
        self.thread = play_loop_thread()
        self.thread.update_signal.connect(self.play_loop_slot)
        #************************************************************************
        
        #connect buttons to slots
        self.Close.clicked.connect(self.close_clicked)
        self.Connect_button.clicked.connect(self.connect)
        self.tutorial_button.clicked.connect(self.tutorial_clicked)
        self.enable_signal()
        #************************************************************************
        
        # connect board buttons to slots
        self.button_0.clicked.connect(self.button_0_clicked)
        self.button_1.clicked.connect(self.button_1_clicked)
        self.button_2.clicked.connect(self.button_2_clicked)
        self.button_3.clicked.connect(self.button_3_clicked)
        self.button_4.clicked.connect(self.button_4_clicked)
        self.button_5.clicked.connect(self.button_5_clicked)
        self.button_6.clicked.connect(self.button_6_clicked)
        self.button_7.clicked.connect(self.button_7_clicked)
        self.button_8.clicked.connect(self.button_8_clicked)   
        #************************************************************************
        
        # Initialize scoreboard counters
        self.playerX_score = 0
        self.playerO_score = 0
        self.tie_count = 0
        self.total_games_played = 0
        
        # Create a QTimer for updating the time label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_label)
        self.time_elapsed = 0

             
    def update_time_label(self):
        # Update the time label every second
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.time.setText(f"{minutes:02d}:{seconds:02d}")    
        
 
    def play_loop_slot(self, msg):
    # receives signal from the thread
        try:
            self.write_msg(msg)
                      
        except Exception as s:
            print(s)
            
    # checks sends move to play loop thread when clicked to check if it's valid  
    def button_0_clicked(self): 
        self.thread.move(0)
        self.thread.start()
        
    def button_1_clicked(self): 
        self.thread.move(1)
        self.thread.start()
        
    def button_2_clicked(self): 
        self.thread.move(2)
        self.thread.start()

    def button_3_clicked(self): 
        self.thread.move(3)
        self.thread.start()
        
    def button_4_clicked(self): 
        self.thread.move(4)
        self.thread.start()
        
    def button_5_clicked(self): 
        self.thread.move(5)
        self.thread.start()
        
    def button_6_clicked(self): 
        self.thread.move(6)
        self.thread.start()
        
    def button_7_clicked(self): 
        self.thread.move(7)
        self.thread.start() 
    
    def button_8_clicked(self):
        self.thread.move(8)
        self.thread.start()  
        
             
    def enable_signal(self):
        # starts loop thread
        try:
            self.thread = play_loop_thread()
            self.thread.update_signal.connect(self.play_loop_slot)  # connect signals to slots    
            self.thread.start() 
        except Exception as r:
            print(r)
            
                
    def connect(self):
        # connects to server
        try:
            self.server=self.server_editBox.text() # get the server the user input
            if self.server == 'localhost' or len(self.server.split('.')) == 4:  
                self.thread.connect_server(self.server)
                self.thread.start() # call thread to start
                self.messages_edit_box.append('Connected to server')
                self.Connect_button.setEnabled(False)
            elif self.server == '':
                self.messages_edit_box.append('No server entered')
        except Exception as t:
            print(t)
            
            
    # function to handle messages    
    def write_msg(self, msg):  
        msg_list = msg.split() # split message into a list
        
        if msg_list[0] == "new":
            self.clear_board_buttons() # clear board
            self.clear_messages() # clear messages           
            self.shape = msg_list[-1][-1] # gets shpe from message
            self.messages_edit_box.append('New Game Started!')
            self.messages_edit_box.append('Your shape: ' + self.shape)
            self.timer.start(1000) # starts timer
                       
            self.server_editBox.setText("") # sets the server edit box to nothing

        elif msg_list[0] == "your":
            self.Connect_button.setEnabled(False) # disable connect butto
            self.messages_edit_box.append(msg)
            # enable all board buttons
            self.button_0.setEnabled(True)
            self.button_1.setEnabled(True)
            self.button_2.setEnabled(True)
            self.button_3.setEnabled(True)
            self.button_4.setEnabled(True)
            self.button_5.setEnabled(True)
            self.button_6.setEnabled(True)
            self.button_7.setEnabled(True)
            self.button_8.setEnabled(True)


        elif msg_list[0] == "opponents": 
            self.Connect_button.setEnabled(False) # disable connect button
            self.messages_edit_box.append(msg)
            # disable all board buttons
            self.button_0.setEnabled(False)
            self.button_1.setEnabled(False)
            self.button_2.setEnabled(False)
            self.button_3.setEnabled(False)
            self.button_4.setEnabled(False)
            self.button_5.setEnabled(False)
            self.button_6.setEnabled(False)
            self.button_7.setEnabled(False)
            self.button_8.setEnabled(False)
            
           
        elif msg_list[0] == "valid":  
            self.Connect_button.setEnabled(False) # disable connect button
            position = str(msg_list[-1][-1]) # gets position from messge
            self.shape = msg_list[-1][-3] # gets shape from message
            
            # changes the buttons icon to player character
            if position == '0':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_0.setIcon(icon)      
                self.button_0.setIconSize(QSize(self.button_0.width(),self.button_0.height()))
                
            elif position == '1':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_1.setIcon(icon)
                self.button_1.setIconSize(QSize(self.button_1.width(),self.button_1.height()))
                
            elif position == '2':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_2.setIcon(icon)
                self.button_2.setIconSize(QSize(self.button_2.width(),self.button_2.height()))
                
            elif position == '3':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_3.setIcon(icon)
                self.button_3.setIconSize(QSize(self.button_3.width(),self.button_3.height()))
                
            elif position == '4':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_4.setIcon(icon)
                self.button_4.setIconSize(QSize(self.button_4.width(),self.button_4.height()))
                
            elif position == '5':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_5.setIcon(icon)
                self.button_5.setIconSize(QSize(self.button_5.width(),self.button_5.height()))
            
            elif position == '6':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_6.setIcon(icon)
                self.button_6.setIconSize(QSize(self.button_6.width(),self.button_6.height()))
            
            elif position == '7':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_7.setIcon(icon)
                self.button_7.setIconSize(QSize(self.button_7.width(),self.button_7.height()))
            
            elif position == '8':
                icon = QIcon()
                icon.addPixmap(QPixmap(str(self.shape)+'.png'))
                self.button_8.setIcon(icon)  
                self.button_8.setIconSize(QSize(self.button_8.width(),self.button_8.height()))
                
        elif msg_list[0] == "invalid":  
            self.Connect_button.setEnabled(False)
            self.messages_edit_box.append(msg)
            self.messages_edit_box.append('try again!')  
            
        elif msg_list[0] == "game": 
            self.Connect_button.setEnabled(False)
            self.timer.stop()
            
            if msg_list[-1][-1] == 'X': # if winner is X
                self.messages_edit_box.append('Game over, the winner is X!')
                self.playerX_score += 1
                self.p1.setText(str(self.playerX_score))
                
            elif msg_list[-1][-1] == 'O': # if winner is O
                self.messages_edit_box.append('Game over, the winner is O!')
                self.playerO_score += 1
                self.p2.setText(str(self.playerO_score))
        
            else: # if it's a tie
                self.messages_edit_box.append('It\'s a tie!')
                self.tie_count += 1
                self.tie.setText(str(self.tie_count))
                
            self.total_games_played += 1
            self.games.setText(str(self.total_games_played))    
         
                
        elif msg_list[0] == 'play':
            #show play again window
            self.play_again_window.show()
        
            
        elif msg_list[-1]=='game':
            self.play_again_window.exit_game_signal.connect(self.exit_game) # exits play again window
            
    def tutorial_clicked(self): # slot that displays tutorial window when tutorial button is clicked
        try:
            self.tutorial_window()
        except Exception as e:
            print(e)
    
    def tutorial_window(self): # slot that calls tutorial window
        self.tutorial_window = TutorialWindow()
        self.tutorial_window.show()    
        
    def clear_board_buttons(self):
        # Clear the icons from all the game board button
        try:
            icon = QIcon()
            icon.addPixmap(QPixmap('blank.gif'))
            self.button_0.setIcon(icon)
            self.button_1.setIcon(icon)
            self.button_2.setIcon(icon)
            self.button_3.setIcon(icon)
            self.button_4.setIcon(icon)
            self.button_5.setIcon(icon)
            self.button_6.setIcon(icon)
            self.button_7.setIcon(icon)
            self.button_8.setIcon(icon)
        except Exception as l:
            print(l)

    def clear_messages(self):
        # Clear the messages in the text box
        self.messages_edit_box.clear()
    
    def close_clicked(self): # closes window
        self.close() 
        
    def play_again_slot(self, ans): # receive ans from play again window
        try:
            if ans == 'y':
                self.play_again()
            elif ans == 'n':
                self.exit_game()
        except:
            pass
                
    def play_again(self):
        # Handle the play again logic here
        self.thread.play_again('y') # sends answer to play loop thread
        self.thread.start()        
        
    def exit_game(self):
        # Handle the play again logic here
        self.thread.play_again('n') # send answer to play loop thread
        self.thread.start()        
        self.clear_board_buttons()
        self.clear_messages()
        self.p2.setText('0')
        self.p1.setText('0')
        self.tie.setText('0')
        self.games.setText('0')
        self.time.setText('00:00')
        self.messages_edit_box.append('Game over!\nClose Window')

       
def main():
    
    app = QApplication(sys.argv)
    window_widget = MainWindow()
    window_widget.show()
    sys.exit(app.exec_())
    
main()