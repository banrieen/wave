import httpx
from typing import Any

from prefect import flow, task # Prefect flow and task decorators

@flow(log_prints=True)
def show_stars(github_repos: list[str]) -> None:
    """Show the number of stars that GitHub repos have"""
    
    for repo in github_repos:
        repo_stats = fetch_stats(repo)
        stars = get_stars(repo_stats)
        print(f"{repo}: {stars} stars")

@task(retries=3)
def fetch_stats(github_repo: str)->dict[str, Any]:
    """Fetch the statistics for a GitHub repo"""
    api_response = httpx.get(f"https://api.github.com/repos/{github_repo}").json()
    api_response.raise_for_status()
    return api_response

@task
def get_stars(repo_stats: dict):
    """Get the number of stars from GitHub repo statistics"""
    return repo_stats['stargazers_count']


if __name__ == "__main__":
    show_stars([
        "PrefectHQ/prefect",
        "pydantic/pydantic",
        "huggingface/transformers"
    ])