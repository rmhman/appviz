# Algosec Application Import Tool

A Python script for importing applications into Algosec AppViz via the REST API.

**Author:** Ross Heilman  
**Version:** 1.0  
**Date:** Nov 04, 2024

## Overview

This script provides a client for interacting with the Algosec API, allowing users to log in and import applications into Algosec AppViz. It supports both command-line arguments and environment variables for configuration.

## Requirements

- Python 3.x
- `requests` library

## Installation

```bash
pip install requests
```

## Configuration

### Environment Variables

The script supports the following environment variables:
- `ALGO_SERVER`: Algosec server URL
- `ALGO_USER`: Username for authentication
- `ALGO_PASS`: Password for authentication
- `ALGO_APPS_FILE`: Path to file containing application names

### Application Input File

Create a text file containing application names, one per line. Example:
```
app1
app2
app3
```

## Usage

```bash
python import_apps.py [options]
```

### Command Line Options

```
--server     Algosec server URL (with or without https://)
--username   Username for authentication
--password   Password for authentication
--file       Path to file containing application names
```

### Examples

Using command line arguments:
```bash
python import_apps.py \
  --server https://algosec-server.com \
  --username your_username \
  --password your_password \
  --file applications.txt
```

Using environment variables:
```bash
export ALGO_SERVER="https://algosec-server.com"
export ALGO_USER="your_username"
export ALGO_PASS="your_password"
export ALGO_APPS_FILE="applications.txt"
python import_apps.py
```

## Features

- Secure HTTPS communication
- Automatic HTTPS protocol addition if not specified
- Session-based authentication using JSESSIONID
- Sorted application import
- Duplicate application handling
- Comprehensive error handling and reporting

## Error Handling

The script includes error handling for:
- Missing credentials
- Authentication failures
- File not found errors
- Duplicate applications
- Network connection issues
- API response errors

## Security Notes

- Credentials can be provided via environment variables for increased security
- Session-based authentication using JSESSIONID

## Logging

The script provides feedback for:
- Authentication status
- Number of applications found
- Success/failure of each application import
- Error details when operations fail

## Exit Status

- The script will exit with a non-zero status if authentication fails
- Individual application import failures are logged but don't stop execution