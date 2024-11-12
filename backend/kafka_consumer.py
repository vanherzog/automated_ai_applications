from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
import json
from typing import Optional
import threading
import queue
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Updated to match React app port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a queue to store messages
message_queue = queue.Queue()


# Kafka Consumer setup
def kafka_consumer_thread():
    retry_count = 0
    max_retries = 5

    while retry_count < max_retries:
        try:
            logger.info("Attempting to connect to Kafka...")
            consumer = KafkaConsumer(
                'job-applications',
                bootstrap_servers=['kafka:9092'],  # Use internal Docker network address
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='web_app_group',
                api_version_auto_timeout_ms=30000,
                request_timeout_ms=30000
            )

            logger.info("Successfully connected to Kafka")

            for message in consumer:
                logger.info(f"Received message: {message.value}")
                # Transform the message to match your frontend's expected format
                job_data = {
                    "JOB_ID": message.offset,
                    "JOB_DESCRIPTION": message.value["project_description"],
                    "APPLICATION": message.value["job_application"]
                }
                message_queue.put(job_data)

        except Exception as e:
            retry_count += 1
            logger.error(f"Error in Kafka consumer (attempt {retry_count}/{max_retries}): {str(e)}")
            if retry_count < max_retries:
                import time
                time.sleep(5)  # Wait 5 seconds before retrying
            else:
                logger.error("Max retries reached. Kafka consumer thread stopping.")
                return


@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI application...")
    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consumer_thread, daemon=True)
    consumer_thread.start()
    logger.info("Kafka consumer thread started")


@app.get("/api/jobs/next")
async def get_next_job():
    try:
        logger.info("Received request for next job")
        job = message_queue.get_nowait()
        logger.info(f"Returning job: {job}")
        return job
    except queue.Empty:
        logger.warning("No jobs available in queue")
        raise HTTPException(status_code=404, detail="No jobs available")
    except Exception as e:
        logger.error(f"Unexpected error in get_next_job: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)