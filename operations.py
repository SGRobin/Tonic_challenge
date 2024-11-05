import string
import time

import constants
import requests
import random
from requests.auth import HTTPBasicAuth
import json
import os

def create_issue(summary_input, description_input):
    url = f"{constants.JIRA_URL}/rest/api/3/issue"
    headers = {"Content-Type": "application/json"}
    payload = {
        "fields": {
            "project": {"key": constants.PROJECT_KEY},
            "summary": summary_input,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description_input
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Task"},
        }
    }
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(constants.JIRA_EMAIL, constants.JIRA_API_TOKEN),
    )
    return response.status_code, response.json()

def generate_issues():
    delete_all_issues()
    time.sleep(10)
    # Create 200 issues
    for i in range(200):
        # 90% chance to include server
        if random.random() < 0.9:
            server = random.choice(constants.SERVERS)
            # 50% chance for server name to be uppercase
            server = server.upper() if random.random() < 0.5 else server.lower()
            description = random.choice(constants.ISSUES).format(server=server)
        else:
            # 50% chance for server name to be faulty - 50% chance for no server name
            if random.random() < 0.5:
                description = random.choice(constants.GENERAL_ISSUES)
            else:
                description = random.choice(constants.ISSUES).format(
                    server=f"srv-{''.join(random.choices(string.ascii_letters, k=3))}")

        summary = f"Issue {i + 1}"
        status_code, response = create_issue(summary, description)
        print(f"Issue {i + 1} created with status {status_code}")

        if status_code != 201:
            print("Error creating issue:", response)
            break


def delete_all_issues():
    url = f"{constants.JIRA_URL}/rest/api/3/search"
    headers = {"Content-Type": "application/json"}
    start_at = 0
    max_results = 500  # Adjust this as needed

    while True:
        # Fetch a batch of issues
        params = {
            "jql": f"project={constants.PROJECT_KEY}",
            "startAt": start_at,
            "maxResults": max_results,
        }
        response = requests.get(
            url,
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(constants.JIRA_EMAIL, constants.JIRA_API_TOKEN),
        )
        data = response.json()
        issues = data.get("issues", [])

        # Stop if there are no more issues to delete
        if not issues:
            print("All issues have been deleted.")
            break

        # Delete each issue in the batch
        for issue in issues:
            issue_id = issue["id"]
            delete_url = f"{constants.JIRA_URL}/rest/api/3/issue/{issue_id}"
            delete_response = requests.delete(
                delete_url,
                auth=HTTPBasicAuth(constants.JIRA_EMAIL, constants.JIRA_API_TOKEN)
            )
            if delete_response.status_code == 204:
                print(f"Issue {issue_id} deleted successfully.")
            else:
                print(f"Failed to delete issue {issue_id}. Status code: {delete_response.status_code}")

        # Move to the next batch
        start_at += max_results




def request_num_issues(start_index, num_issues):
    url = f"{constants.JIRA_URL}rest/api/3/search"
    headers = {"Accept": "application/json"}
    query = {
        "jql": f"project = {constants.PROJECT_KEY}",
        "startAt": start_index,
        "maxResults": num_issues,
        "fields": "description"
    }

    response = requests.get(
        url,
        headers=headers,
        params=query,
        auth=HTTPBasicAuth(constants.JIRA_EMAIL, constants.JIRA_API_TOKEN)
    )
    if response.status_code == 200:
        return [issue['fields']['description']["content"][0]["content"][0]["text"] for issue in response.json()['issues']]
    else:
        print("Failed to fetch issues from Jira:", response.status_code, response.text)
        return []


def get_server_errors():
    file_name = "state.json"
    if os.path.exists(file_name):
        with open(file_name, 'r') as json_file:
            server_counts = json.load(json_file)
    else:
        server_counts = {server: 0 for server in constants.SERVERS}
        server_counts["unspecified-servers"] = 0
        server_counts["index"] = 0
        server_counts["batch_size"] = 8

    while True:
        print(f"checking issues at index: {server_counts["index"]}")
        issues_batch = request_num_issues(server_counts["index"], server_counts["batch_size"])
        if not issues_batch:
            break

        for issue in issues_batch:
            # print(issue)
            found_server = False
            for server in constants.SERVERS:
                if server in issue.lower():
                    server_counts[server] += 1
                    found_server = True
                    break
            if not found_server:
                server_counts["unspecified-servers"] += 1

        server_counts["index"] += server_counts["batch_size"]

        with open(file_name, 'w') as json_file:
            json.dump(server_counts, json_file, indent=4)

    del server_counts["index"]
    del server_counts["batch_size"]
    return server_counts