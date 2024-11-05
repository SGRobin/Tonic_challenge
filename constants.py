# Jira project keys
JIRA_URL = "https://shlomogdd.atlassian.net/"
PROJECT_KEY = "KAN"
JIRA_API_TOKEN = "ATATT3xFfGF0QJ9vbs0YmLBG4KbYvRKTZfhu0-8GSXD_UL2TFMc9VwfAP85SVdF0zZ_B3HyUNnz9JKnH2PpJyg9pk6j46RyIyE3ldXpDCwWEXxKU21jHo2pJIISTy5W7cUyL_mvwzhCMmocgIahZbMy8ap8yscF2xzV7KgjfcFRPgxilH9SMNyA=0B6510B3"
JIRA_EMAIL = "shlomogdd@gmail.com"

# the servers
SERVERS = ["srv-1", "srv-2", "srv-3", "srv-4", "srv-5"]

# possible issues
ISSUES = [
    "Unable to connect to {server}.",
    "Experiencing high latency on {server}.",
    "Authentication failure on {server}.",
    "{server} is unresponsive.",
    "Frequent disconnects from {server}.",
    "Cannot retrieve data from {server}.",
    "Server {server} is down."
]
# issues when there is no server
GENERAL_ISSUES = [
    "Unable to connect to the database.",
    "Experiencing intermittent network issues.",
    "Frequent timeouts observed in the application.",
    "Server is unresponsive, affecting service availability.",
]