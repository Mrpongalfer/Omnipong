import pika
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime=s - %(levelname=s - %(message=s')

class CommunicationManager:
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        logging.info("CommunicationManager initialized")

    def send_message(self, queue, message):
        try:
            self.channel.queue_declare(queue=queue)
            self.channel.basic_publish(exchange='', routing_key=queue, body=message)
            logging.info(f"Message sent to queue {queue}: {message}")
        except Exception as e:
            logging.error(f"Error sending message to queue {queue}: {e}")

    def receive_messages(self, queue, callback):
        try:
            self.channel.queue_declare(queue=queue)
            self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
            logging.info(f"Waiting for messages from queue {queue}")
            self.channel.start_consuming()
        except Exception as e:
            logging.error(f"Error receiving messages from queue {queue}: {e}")

    def close_connection(self):
        try:
            self.connection.close()
            logging.info("CommunicationManager connection closed")
        except Exception as e:
            logging.error(f"Error closing CommunicationManager connection: {e}")

# Example usage
def example_callback(ch, method, properties, body):
    logging.info(f"Received message: {body}")

if __name__ == '__main__':
    comm_manager = CommunicationManager()
    comm_manager.send_message('test_queue', 'Hello, World!')
    comm_manager.receive_messages('test_queue', example_callback)
    comm_manager.close_connection()
