Overview
* Uses `watchdog` and `rclone` to sync local/remote storage
* `rclone sync [local] [remote]` on file system changes
* `rclone copy [remote] [local]` every 30 seconds

Setup
* Install `rclone`
* Run `rclone config`
* `pip install -r requirements`
* Add log folder/bucket details to `config.yaml`

Use
* `python3 app.py`
* `python3 app.py &` <- background
* Check logs for status/errors