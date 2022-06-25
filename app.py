import time
import logging
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from datetime import date


bucket = {
  "local": "/Users/justin/Volumes/B2/",
  "remote": "B2:"
}

def logger():
  log_file = f"/Users/justin/Projects/rclone-watchdog-sync/logs/{date.today()}.txt"
  os.makedirs(os.path.dirname(log_file), exist_ok=True)
  logging.basicConfig(
    filename=log_file, 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
  )
  return logging


def run_and_log(cmd):
    try:
      process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
      output = process.communicate()[0].decode("utf-8")
      if len(output) > 0:
        logger().info(output)
    except Exception as e:
      logging.error(e)
    logger().info(cmd)


class RcloneSyncHandler(FileSystemEventHandler):
  @staticmethod
  def on_any_event(event):
    cmd = f"rclone sync {bucket['local']} {bucket['remote']}"
    run_and_log(cmd)


observer = Observer()
observer.schedule(RcloneSyncHandler(), bucket["local"], recursive=True)
observer.schedule(LoggingEventHandler(), bucket["local"], recursive=True)
observer.start()


if __name__ == "__main__":
  try:
    while True:
      time.sleep(30)
      command = f"rclone copy {bucket['remote']} {bucket['local']}"
      run_and_log(command)

  finally:
    observer.stop()
    observer.join()

