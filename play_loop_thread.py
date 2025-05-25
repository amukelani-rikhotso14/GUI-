from PyQt5.QtCore import *
from GameClient  import *

class play_loop_thread(QThread, GameClient):
    
    # create signal
    update_signal = pyqtSignal(str)
    
    def __init__(self):
        super(play_loop_thread, self).__init__()
        GameClient.__init__(self)
       
    # connects to server
    def connect_server(self, server):
        while True:
            try:
                self.connect_to_server(server)
                break
            except Exception as error:
                print(error)
                break
    
    # checks if move is valid
    def move(self, position):
        while True:
            try:
                self.send_message(str(position))
                break
            except:
                pass
               
    # tells server if user wants to play again or if not 
    def play_again(self, ans):
        while True:
            try: 
                self.send_message(str(ans))
                break
            except:
                pass
    
    def run(self):
        while True:
            try:
                msg = self.receive_message()
                if len(msg):
                    self.update_signal.emit(str(msg))
                else: break
            except:
                self.update_signal.emit('Error')
                break

        
        
        