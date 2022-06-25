import sys
import time
import logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
import subprocess


logging.basicConfig(
  filename="./log.txt", 
  level=logging.INFO, 
  format='%(asctime)s - %(message)s', 
  datefmt='%Y-%m-%d %H:%M:%S'
)

bucket = {
  "local": "/Users/justin/Projects/pywatch-test/vols/b2/",
  "remote": "B2:"
}

def run_and_log(command):
    try:
      process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)      
      output = process.communicate()[0].decode("utf-8")
      if len(output) > 0:
        logging.info(output)
    except Exception as e:
      logging.error(e)
    logging.info(command)

class RcloneSyncHandler(FileSystemEventHandler):
  @staticmethod  
  def on_created(event):
    command = f"rclone sync {bucket['local']} {bucket['remote']}"
    run_and_log(command)
 
  @staticmethod
  def on_modified(event):
    file_modified = isinstance(event, FileModifiedEvent)
    if file_modified:
      command = f"rclone sync {bucket['local']} {bucket['remote']}"
      run_and_log(command)

  @staticmethod
  def on_moved(event):
    command = f"rclone sync {bucket['local']} {bucket['remote']}"
    run_and_log(command)

observer = Observer()
observer.schedule(RcloneSyncHandler(), bucket["local"], recursive=True)
observer.schedule(LoggingEventHandler(), bucket["local"], recursive=True)
observer.start()

try:
  while True:
    time.sleep(5)
    command = f"rclone copy {bucket['remote']} {bucket['local']}"
    run_and_log(command)

finally:
  observer.stop()
  observer.join()

