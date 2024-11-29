# Author: Ross Heilman
# Version: 1.0
# Date: Nov 03, 2024
# Usage: python(3) import_apps.py --server https://algosec-server.com --username your_username --password your_password --file path/to/applications.txt
# Note: Environment variables can also be used to provide these values if not specified in the command line.
# Description: This script provides a client for interacting with the Algosec API, allowing users to log in and import applications into Algosec AppViz. 
import requests
import json
import os
from requests.auth import HTTPBasicAuth 
from typing import Optional
from urllib.parse import urlparse

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
class AlgosecClient:
    def __init__(self, server: str, username: str, password: str):
        # Ensure server URL has HTTPS protocol
        if not urlparse(server).scheme:
            server = f"https://{server}"
        self.server = server.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.jsessionid: Optional[str] = None

    def login(self) -> bool:
        """Login to Algosec and get JSESSIONID"""
        url = f"{self.server}/BusinessFlow/rest/v1/login"
        try:
            response = requests.post(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
            response.raise_for_status()
            
            # Extract JSESSIONID from response
            data = response.json()
            self.jsessionid = data.get('jsessionid')
            
            if not self.jsessionid:
                print("No JSESSIONID received in response")
                return False
                
            # Set the cookie for subsequent requests
            self.session.cookies.set('JSESSIONID', self.jsessionid)
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {str(e)}")
            return False

    def create_application(self, app_name: str) -> bool:
        """Create a new application in AppViz"""
        if not self.jsessionid:
            print("Not authenticated. Please login first.")
            return False

        url = f"{self.server}/BusinessFlow/rest/v1/applications/new"
        payload = {"name": app_name}

        try:
            # Session will automatically include the JSESSIONID cookie
            response = self.session.post(url, json=payload, verify=False)
            # Check for 400 Bad Request specifically
            if response.status_code == 400:
                print(f"Application {app_name} already exists.")
                return False
            response.raise_for_status()  # Raise an error for other HTTP errors
            print(f"Successfully created application: {app_name}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to create application {app_name}: {str(e)}")
            return False

def import_applications(server: str, username: str, password: str, file_path: str):
    """Import applications from file into Algosec AppViz"""
    if not all([server, username, password]):
        print("Error: Missing required credentials. Please provide server, username, and password either via arguments or environment variables.")
        return

    client = AlgosecClient(server, username, password)
    
    if not client.login():
        print("Failed to login to Algosec. Exiting.")
        return

    try:
        with open(file_path, 'r') as file:
            # Read and sort the applications
            apps = sorted([line.strip() for line in file if line.strip()])
            
        print(f"Found {len(apps)} applications to import")
        
        for app in apps:
            client.create_application(app)
            
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Import applications into Algosec AppViz')
    parser.add_argument('--server', 
                       help='Algosec server URL (with or without https://), will also try to read env var ALGO_SERVER',
                       default=os.environ.get('ALGO_SERVER', 'algosec-cm.corp.internal.citizensbank.com'))
    parser.add_argument('--username',
                       help='Username, will also try to read env var ALGO_USER',
                       default=os.environ.get('ALGO_USER'))
    parser.add_argument('--password',
                       help='Password secret, will also try to read env var ALGO_PASS',
                       default=os.environ.get('ALGO_PASS'))
    parser.add_argument('--file',
                       help='Path to file containing application names, will also try to read env var ALGO_APPS_FILE',
                       default=os.environ.get('ALGO_APPS_FILE', '../Illumio/IllumioApps.txt'))
    
    args = parser.parse_args()
    
    import_applications(args.server, args.username, args.password, args.file)