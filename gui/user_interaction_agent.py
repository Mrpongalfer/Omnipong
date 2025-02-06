import logging
import threading
from transformers import AutoModel, AutoTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')

class UserInteractionAgent:
    def __init__(self):
        model_name = "openbmb/MiniCPM-o-2_6"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        logging.info("UserInteractionAgent initialized with MiniCPM model")

    def interpret_input(self, user_input):
        inputs = self.tokenizer(user_input, return_tensors="pt")
        outputs = self.model.generate(inputs["input_ids"], max_length=150)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logging.info(f"Generated response: {response}")
        return response

    def handle_user_input(self, user_input, callback):
        threading.Thread(target=self.process_input, args=(user_input, callback)).start()

    def process_input(self, user_input, callback):
        response = self.interpret_input(user_input)
        callback(response)

# Example usage with Tkinter GUI
class UserInteractionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Interaction")

        self.agent = UserInteractionAgent()

        self.label = ttk.Label(root, text="Enter your message:")
        self.label.pack(pady=10)

        self.user_input = ttk.Entry(root, width=50)
        self.user_input.pack(pady=10)

        self.send_button = ttk.Button(root, text="Send", command=self.send_input)
        self.send_button.pack(pady=10)

        self.response_label = ttk.Label(root, text="", font=("Arial", 14))
        self.response_label.pack(pady=20)

    def send_input(self):
        user_text = self.user_input.get()
        self.agent.handle_user_input(user_text, self.display_response)

    def display_response(self, response):
        self.response_label.config(text=response)

if __name__ == '__main__':
    root = tk.Tk()
    app = UserInteractionApp(root)
    root.mainloop()
