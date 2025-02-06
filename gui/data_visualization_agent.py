import logging
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime=s - %(levelname=s - %(message=s')

class DataVisualizationAgent:
    def __init__(self):
        self.data = pd.DataFrame()
        logging.info("DataVisualizationAgent initialized")

    def update_data(self, new_data):
        try:
            self.data = pd.DataFrame(new_data)
            logging.info(f"Data updated: {new_data}")
        except Exception as e:
            logging.error(f"Error updating data: {e}")

    def create_visualization(self, chart_type='line'):
        try:
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)

            if chart_type == 'line':
                ax.plot(self.data.index, self.data.values)
            elif chart_type == 'bar':
                ax.bar(self.data.index, self.data.values)
            elif chart_type == 'scatter':
                ax.scatter(self.data.index, self.data.values)

            ax.set_title(f'{chart_type.capitalize()} Chart')
            ax.set_xlabel('Index')
            ax.set_ylabel('Values')
            logging.info(f"Created {chart_type} chart")
            return fig
        except Exception as e:
            logging.error(f"Error creating visualization: {e}")
            return None

    def display_visualization(self, chart_type='line'):
        fig = self.create_visualization(chart_type)
        if fig is not None:
            root = tk.Tk()
            root.title(f'{chart_type.capitalize()} Chart')
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            ttk.Button(root, text="Quit", command=root.quit).pack(side=tk.BOTTOM)
            tk.mainloop()

# Example usage
if __name__ == '__main__':
    viz_agent = DataVisualizationAgent()
    sample_data = {'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]}
    viz_agent.update_data(sample_data)
    viz_agent.display_visualization('line')
