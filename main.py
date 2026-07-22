import json
from urllib.error import URLError
from urllib.request import Request, urlopen


def format_event_output(
    event_type: str, repo_name: str, event_count: int
) -> str | None:
    match event_type:
        case "CreateEvent":
            output = f"- Created {str(event_count) + ' branch' if event_count == 1 else str(event_count) + ' branches'} in {repo_name}"
        case "PushEvent":
            output = f"- Pushed {str(event_count)} commit(s) to {repo_name}"
        case "WatchEvent":
            output = f"- Starred {repo_name}"
        case _:
            return None

    return output


def get_github_activity(username: str) -> list[dict] | None:
    # test if username exists
    req = Request(f"https://api.github.com/users/{username}/events")
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, "code") and e.code == 404:
            print("Github username does not exist.")
        elif hasattr(e, "code"):
            print("The Github API couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e, "reason"):
            print("We failed to reach the Github API.")
            print("Reason: ", e.reason)
    else:
        user_activity = response.read().decode("utf8")
        events = json.loads(user_activity)
        return events


def group_events(gh_events: list[dict]):
    event_grps = {}
    for event in gh_events:
        event_type = event.get("type")
        if not event_grps.get(event_type):
            event_grps[event_type] = {}

        repo_name = event.get("repo").get("name")

        if repo_name not in event_grps[event_type]:
            event_grps[event_type][repo_name] = 0

        event_grps[event_type][repo_name] += 1
    return event_grps


def output_event_groups(event_grps: list):
    print("Output:")

    for event_type, repos in event_grps.items():
        for repo, count in repos.items():
            line = format_event_output(event_type, repo, count)
            if line:
                print(line)


def main():
    events = get_github_activity("mikantlin")
    if events:
        # roll up events
        grouped_events = group_events(events)
        output_event_groups(grouped_events)


if __name__ == "__main__":
    main()
