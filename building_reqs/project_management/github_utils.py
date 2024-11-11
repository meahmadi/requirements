import requests
from django.conf import settings

def create_github_issue(project, title, description):
    url = f"https://api.github.com/repos/{project.github_repo_url}/issues"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": description
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        issue_data = response.json()
        return issue_data["html_url"]  # Returns the URL of the created issue
    else:
        raise Exception(f"Failed to create issue: {response.content}")
