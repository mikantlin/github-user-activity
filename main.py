import json
from urllib.error import URLError
from urllib.request import Request, urlopen


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
        print(events)
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

    print(event_grps)
    return event_grps


def main():
    events = get_github_activity("mikantlin")
    if events:
        # roll up events
        grouped_events = group_events(events)


if __name__ == "__main__":
    main()
