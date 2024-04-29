import pickle

class Q_table:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
    
    def save_Q_table(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)
    
    def load_Q_table(self) -> None:
        try:
            with open(self.filename,'rb') as file:
                    self.data = pickle.load(file)
            return True
        except FileNotFoundError:
            print(f"Error: File not found - {self.filename}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    