import subprocess
import time
import json
from datetime import datetime, timedelta, timezone
import os
from colorama import Fore, Style, init

class LightsailLogger:
    def __init__(self, service_name, fetch_interval_seconds=10):
        self.service_name = service_name
        self.container_names = []
        self.unique_log_events = set()
        self.fetch_interval_seconds = fetch_interval_seconds
        init(autoreset=True)
        self.colors = {
            "fastapi": Fore.GREEN,
            "nginx": Fore.BLUE,
            "rq-worker": Fore.RED,
            "default": Fore.RESET
        }

    def fetch_container_names(self):
        command = [
            "aws", "lightsail", "get-container-services",
            "--service-name", self.service_name
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                output_data = json.loads(result.stdout)
                container_services = output_data.get("containerServices", [])
                if container_services:
                    current_deployment = container_services[0].get("currentDeployment", {})
                    containers = current_deployment.get("containers", {})
                    return list(containers.keys())
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print(f"Command failed with exit code {result.returncode}")
        return []

    def fetch_logs(self, container_name, start_time=None, next_page_token=None):
        command = [
            "aws", "lightsail", "get-container-log",
            "--service-name", self.service_name,
            "--container-name", container_name
        ]
        if start_time:
            command.extend(["--start-time", start_time])
        if next_page_token:
            command.extend(["--page-token", next_page_token])
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                output_data = json.loads(result.stdout)
                log_events = output_data.get("logEvents", [])
                next_page_token = output_data.get("nextPageToken")
                for log_event in log_events:
                    log_event_with_container = {
                        "containerName": container_name,
                        **log_event
                    }
                    log_event_frozenset = frozenset(log_event_with_container.items())
                    self.unique_log_events.add(log_event_frozenset)
                return next_page_token
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print(f"Command failed with exit code {result.returncode}")
        return None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def format_log_entry(self, container_name, timestamp, message):
        container_name_padded = (container_name[:10]).ljust(10)
        color = self.colors.get(container_name, self.colors["default"])
        return f"{timestamp} {color}{container_name_padded}{Style.RESET_ALL} {message}"

    def start_logging(self, minutes):
        start_time = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()
        self.container_names = self.fetch_container_names()
        if not self.container_names:
            print("No containers found in current deployment.")
            return
        while True:
            for container_name in self.container_names:
                next_page_token = None
                while True:
                    next_page_token = self.fetch_logs(container_name, start_time=start_time, next_page_token=next_page_token)
                    if not next_page_token:
                        break
            logs_list = [dict(log) for log in self.unique_log_events]
            sorted_logs = sorted(logs_list, key=lambda log: log.get('createdAt', ''))
            self.clear_screen()
            print("#### Start of Log ####")
            for log in sorted_logs:
                formatted_log = self.format_log_entry(
                    container_name=log.get('containerName', ''),
                    timestamp=log.get('createdAt', '')[:-9],
                    message=log.get('message', '')
                )
                print(formatted_log)
            print(f"\n\nFetched: {len(sorted_logs)} Fetched logs from onwards: ", str((datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat())[:-16], ' Last updated at: ', str((datetime.now(timezone.utc)).isoformat())[:-16])

            time.sleep(self.fetch_interval_seconds)
