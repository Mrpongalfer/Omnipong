import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from omnipong.omnipong_core import OmnipongCore
from omnipong.utils.agent_factory import create_agent
from omnipong.gui.user_interaction_agent import UserInteractionAgent
from omnipong.gui.data_visualization_agent import DataVisualizationAgent

class OmnipongApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Omnipong Dashboard")
        self.core = OmnipongCore()
        self.user_agent = UserInteractionAgent()
        self.viz_agent = DataVisualizationAgent()

        # Create and register agents
        self.create_agents()

        # Set up GUI components
        self.setup_ui()

        # Start background task processing
        self.start_processing()

    def create_agents(self):
        curiosity_engine = create_agent('CuriosityEngine', 'CuriosityEngine_1')
        problem_solver = create_agent('ProblemSolver', 'ProblemSolver_1')
        edge_node_agent = create_agent('EdgeNodeAgent', 'EdgeNodeAgent_1')
        fog_node_agent = create_agent('FogNodeAgent', 'FogNodeAgent_1')

        self.core.register_agent(curiosity_engine)
        self.core.register_agent(problem_solver)
        self.core.register_agent(edge_node_agent)
        self.core.register_agent(fog_node_agent)

    def setup_ui(self):
        self.tab_control = ttk.Notebook(self.root)

        self.dashboard_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.dashboard_tab, text="Dashboard")
        self.setup_dashboard_tab()

        self.visualization_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.visualization_tab, text="Visualizations")
        self.setup_visualization_tab()

        self.tab_control.pack(expand=1, fill='both')

    def setup_dashboard_tab(self):
        ttk.Label(self.dashboard_tab, text="Omnipong Dashboard", font=("Arial", 16)).pack(pady=10)
        
        self.status_label = ttk.Label(self.dashboard_tab, text="System Status: Running", font=("Arial", 12))
        self.status_label.pack(pady=5)

        ttk.Button(self.dashboard_tab, text="Add Task", command=self.add_task).pack(pady=5)
        ttk.Button(self.dashboard_tab, text="Interact", command=self.interact).pack(pady=5)

        self.task_list = tk.Listbox(self.dashboard_tab, height=10, width=50)
        self.task_list.pack(pady=10)
        self.update_task_list()

    def setup_visualization_tab(self):
        ttk.Label(self.visualization_tab, text="Data Visualizations", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.visualization_tab, text="Show Line Chart", command=lambda: self.show_visualization('line')).pack(pady=5)
        ttk.Button(self.visualization_tab, text="Show Bar Chart", command=lambda: self.show_visualization('bar')).pack(pady=5)
        ttk.Button(self.visualization_tab, text="Show Scatter Plot", command=lambda: self.show_visualization('scatter')).pack(pady=5)

    def add_task(self):
        task_window = tk.Toplevel(self.root)
        task_window.title("Add Task")

        task_type_label = ttk.Label(task_window, text="Task Type:")
        task_type_label.pack(pady=5)
        self.task_type = ttk.Combobox(task_window, values=["explore", "solve_problem", "collect_data", "preprocess_data"])
        self.task_type.pack(pady=5)

        task_detail_label = ttk.Label(task_window, text="Task Detail:")
        task_detail_label.pack(pady=5)
        self.task_detail = ttk.Entry(task_window)
        self.task_detail.pack(pady=5)

        add_button = ttk.Button(task_window, text="Add", command=self.confirm_add_task)
        add_button.pack(pady=10)

    def confirm_add_task(self):
        task_type = self.task_type.get()
        task_detail = self.task_detail.get()

        if task_type == "explore":
            task = {'type': task_type, 'topic': task_detail}
        elif task_type == "solve_problem":
            task = {'type': task_type, 'problem': task_detail}
        elif task_type == "collect_data":
            task = {'type': task_type, 'sensor_id': task_detail}
        elif task_type == "preprocess_data":
            task = {'type': task_type, 'data': task_detail}
        else:
            messagebox.showerror("Error", "Invalid task type")
            return

        self.core.send_task(task)
        self.update_task_list()

    def interact(self):
        interact_window = tk.Toplevel(self.root)
        interact_window.title("Interact")

        ttk.Label(interact_window, text="Enter your message:").pack(pady=10)
        self.user_input = ttk.Entry(interact_window, width=50)
        self.user_input.pack(pady=10)
        ttk.Button(interact_window, text="Send", command=self.send_input).pack(pady=10)

        self.response_label = ttk.Label(interact_window, text="", font=("Arial", 14))
        self.response_label.pack(pady=20)

    def send_input(self):
        user_text = self.user_input.get()
        self.user_agent.handle_user_input(user_text, self.display_response)

    def display_response(self, response):
        self.response_label.config(text=response)

    def show_visualization(self, chart_type):
        sample_data = {'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]}
        self.viz_agent.update_data(sample_data)
        self.viz_agent.display_visualization(chart_type)

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.core.task_queue:
            self.task_list.insert(tk.END, f"Task: {task['type']} - {task.get('topic', task.get('problem', task.get('sensor_id', task.get('data', ''))))}")

    def start_processing(self):
        self.processing_thread = threading.Thread(target=self.process_tasks)
        self.processing_thread.start()

    def process_tasks(self):
        while True:
            self.core.distribute_tasks()
            self.update_task_list()
            time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = OmnipongApp(root)
    root.mainloop()
