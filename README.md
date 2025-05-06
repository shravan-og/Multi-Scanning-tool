# URL Port Scanner

A Python tool to scan open and closed ports of a given website URL or IP address. This tool resolves the IP address of the input URL or accepts a raw IP address, checks connectivity by pinging the host, and scans a specified range of ports concurrently for faster results. The scan results are saved in a timestamped file with a clear table format.

## Features

- Accepts both URLs (with or without http/https) and raw IP addresses as input.
- Resolves hostname to IP address.
- Pings the target IP to check connectivity before scanning.
- Concurrent port scanning using multithreading for faster performance.
- Scans a user-specified range of ports (default 1 to 1024).
- Saves scan results in a neatly formatted table in a timestamped file named with hostname and IP.
- Displays a stylish ASCII banner using pyfiglet.

## Requirements

- Python 3.x
- pyfiglet module (`pip install pyfiglet`)

## Usage

1. Clone or download this repository.
2. Install the required Python module:
   ```
   pip install pyfiglet
   ```
3. Run the script:
   ```
   python url_port_scanner.py
   ```
4. Enter the URL or IP address to scan when prompted.
5. Enter the port range to scan (or press Enter to use defaults).
6. View the scan results in the console and find the saved results file in the current directory.

## Example

```
Enter the URL or IP to scan (e.g. https://website.gov./ or 8.8.8.8): https://.gov./
Enter start port (default 1): 1
Enter end port (default 1024): 1024
```

The script will resolve the IP, ping the host, scan the ports concurrently, and save the results in a file named like `scan_results_target.gov.uk_123.45.67.89_20250504_152945.txt`.

## Notes

- The script uses a socket timeout of 0.3 seconds per port scan to balance speed and accuracy.
- Ensure you have permission to scan the target host to avoid legal issues.
- The tool is intended for educational and authorized security testing purposes only.

## License

This Under MTI License