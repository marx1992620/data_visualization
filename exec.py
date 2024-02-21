import uvicorn
import multiprocessing
import os
import logging
import json
import sys
from core.settings import AppSettings


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    dst_dir = os.path.join(current_dir, "dst")
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    # Read config in dst directory
    config_dir = os.path.join(dst_dir, "setting.json")
    if os.path.exists(config_dir):
        with open(config_dir, "r") as f:
            print("Set app setting config from json file.")
            config = json.loads(f.read())
            AppSettings.load_configuration(config)
    AppSettings.configuration()

    default_port = AppSettings.FastAPI_PORT
    logging.info(f"setting.json: {AppSettings.to_dict()}")
    logging.info(f"FastAPI default port in setting.json: {default_port}")

    # Store current config
    config_dir = os.path.join(AppSettings.DATA_DIR, "setting.json")

    # To avoid pyinstaller exeuteable file error.
    multiprocessing.freeze_support()
    # AppSettings.set_port(port=default_port)
    with open(config_dir, "w") as f:
        f.write(json.dumps(AppSettings.to_dict(), indent=4))

    uvicorn.run("main:app", host="0.0.0.0", port=default_port)
