import json
from urllib.error import URLError
from urllib.request import Request, urlopen

import pandas as pd


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


def group_events(events: list[dict]):
    # clean up event data that we need
    stripped_events = [
        {
            "event_type": event.get("type"),
            "repo": event.get("repo").get("name"),
        }
        for event in events
    ]

    # get counts for each event type and associated repo
    events_df = pd.DataFrame(stripped_events)
    event_grp_df = (
        events_df.groupby(["event_type", "repo"]).size().reset_index(name="count")
    )

    return event_grp_df


def main():
    events = get_github_activity("mikantlin")
    if events:
        # roll up events
        grouped_events = group_events(events)
        print(grouped_events)


if __name__ == "__main__":
    main()
