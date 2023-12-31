import os
import platform
import shutil
import tarfile
from requests import get
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("sshman")

GH_USERNAME, REPOSITORY = "auth-xyz", "sshman"


class VersionManager:
    @staticmethod
    def get_installed_version():
        version_file = os.path.join(os.path.expanduser("~/.sshm/.bin/"), "version")  # Updated path here
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                return f.read().strip()
        return "Unknown"

    @staticmethod
    def get_latest_version(user: str, repo: str):
        url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
        response = get(url)
        if response.status_code == 200:
            release_data = response.json()
            return release_data.get("tag_name", "Unknown")
        return "Unknown"

    @staticmethod
    def download_latest(user: str, repo: str, path="./"):
        os_name = platform.system().lower()
        if os_name not in ["linux", "windows"]:
            logger.info(f"[ sshman: Unsupported OS '{os_name}'. Only Linux and Windows are supported. ]")
            return

        os_suffix = "linux" if os_name == "linux" else "windows"
        url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
        response = get(url)
        ins_ver = VersionManager.get_installed_version()
        lat_ver = VersionManager.get_latest_version(GH_USERNAME, REPOSITORY)

        if ins_ver == lat_ver:
            logger.info("[ sshman : You already have the latest version downloaded. ]")
        else:
            if response.status_code == 200:
                release_data = response.json()
                assets = release_data.get("assets", [])

                # Find the correct asset for the user's OS
                asset = next((a for a in assets if os_suffix in a["name"].lower()), None)
                if not asset:
                    logger.info(f"[ sshman: No release found for {os_name}. ]")
                    return

                download_url = asset["browser_download_url"]
                filename = os.path.join(path, asset["name"])

                try:
                    with get(download_url, stream=True) as download_response:
                        download_response.raise_for_status()
                        with open(filename, "wb") as f:
                            for chunk in download_response.iter_content(chunk_size=8192):
                                f.write(chunk)

                    logger.info(f"[ sshman : Finished downloading: {asset['name']} ]")
                    downloaded_version = VersionManager.get_latest_version(GH_USERNAME, REPOSITORY)

                    with tarfile.open(filename, "r:gz") as tar:
                        tar.extractall(path=path)

                    extracted_sshman = os.path.join(path, "sshman")
                    target_sshman = os.path.expanduser("~/.local/bin/sshman")
                    version_file = os.path.expanduser("~/.sshm/.bin/version")

                    if os.path.exists(target_sshman):
                        os.remove(target_sshman)
                    if os.path.exists(version_file):
                        os.remove(version_file)

                    shutil.move(extracted_sshman, target_sshman)
                    logger.info("[ sshman : Moved binary to .local/bin/ ]")

                    version_file_path = os.path.join(os.path.expanduser("~/.sshm/.bin/"), "version")
                    with open(version_file_path, "w") as vf:
                        vf.write(downloaded_version)

                    if os.path.exists(filename):
                        os.remove(filename)
                        logger.info("[ sshman: Cleaned up extracted files. ]")
                    else:
                        logger.info(f"[ sshman: Failed to fetch release data. Status code: {response.status_code} ]")
                except Exception as e:
                    logger.error(f"[ sshman : Failed to download or install the latest version. Error: {e}]")
