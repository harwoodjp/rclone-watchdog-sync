import time
import logging
import subprocess
import os
import yaml
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from datetime import date


def config():
  config = {}
  with open("config.yaml", "r") as stream:
    try:
      obj = yaml.safe_load(stream)
      config["log_folder"] = obj["log_folder"]
      config["bucket"] = obj["bucket"]
    except yaml.YAMLError as e:
      logger().error(e)
  return config


def logger():
  log_file = f"{config()['log_folder']}/{date.today()}.txt"
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
    time.sleep(2)
    cmd = f"rclone sync {config()['bucket']['local']} {config()['bucket']['remote']}"
    run_and_log(cmd)


if __name__ == "__main__":
  observer = Observer()
  observer.schedule(RcloneSyncHandler(), config()["bucket"]["local"], recursive=True)
  observer.schedule(LoggingEventHandler(), config()["bucket"]["local"], recursive=True)
  observer.start()  
  try:
    while True:
      command = f"rclone copy {config()['bucket']['remote']} {config()['bucket']['local']}"
      run_and_log(command)
      time.sleep(30)

  finally:
    observer.stop()
    observer.join()

