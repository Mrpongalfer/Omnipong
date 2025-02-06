import logging
import heapq
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime=s - %(levelname=s - %(message=s')

class TaskScheduler:
    def __init__(self):
        self.task_queue = []
        self.task_id_counter = 0
        self.lock = threading.Lock()
        logging.info("TaskScheduler initialized")

    def add_task(self, task, priority=1):
        with self.lock:
            self.task_id_counter += 1
            heapq.heappush(self.task_queue, (priority, self.task_id_counter, task))
            logging.info(f"Task added: {task} with priority {priority}")

    def get_next_task(self):
        with self.lock:
            if self.task_queue:
                return heapq.heappop(self.task_queue)[2]
            else:
                return None

    def schedule_tasks(self, core, interval=5):
        def scheduler():
            while True:
                task = self.get_next_task()
                if task:
                    core.send_task(task)
                    logging.info(f"Scheduled task: {task}")
                time.sleep(interval)
        threading.Thread(target=scheduler, daemon=True).start()

# Example usage
if __name__ == '__main__':
    class DummyCore:
        def send_task(self, task):
            logging.info(f"DummyCore received task: {task}")

    scheduler = TaskScheduler()
    core = DummyCore()
    scheduler.add_task({'type': 'explore', 'topic': 'artificial intelligence'}, priority=2)
    scheduler.add_task({'type': 'solve_problem', 'problem': 'climate change'}, priority=1)
    scheduler.schedule_tasks(core)
    time.sleep(10)  # Let the scheduler run for a while
