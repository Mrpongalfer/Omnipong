import sys
import os

# Add the omnipong directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from omnipong.gui.visualization import OmnipongApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = OmnipongApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
