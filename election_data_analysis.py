import json

with open("election_data.json", "r") as f:
    data = f.read()
    data = json.loads(data)


def candidates_two_constituency():
    candidates = dict()
    for constituency in data:
        for candidate in constituency["candidates"]:
            if candidate["party_name"] == "independent":
                continue
            name = candidate["candidate_name"] + " (" + candidate["party_name"] + ")"
            candidates[name] = candidates[name] + 1 if name in candidates else 1
    print("List of candidates contesting from two constituencies")
    print(json.dumps({name: seats for name, seats in candidates.items() if seats == 2}, indent=2))


def candidate_highest_votes():
    highest_votes = 0
    candidate_name = None
    constituency_name = None
    for constituency in data:
        for candidate in constituency["candidates"]:
            if candidate["total_votes"] > highest_votes:
                candidate_name = candidate["candidate_name"]
                constituency_name = constituency["constituency"]
                highest_votes = candidate["total_votes"]

    print("Highest votes:", candidate_name, "from", constituency_name, "got", highest_votes, "votes")


def highest_margin():
    highest_margin_count = 0
    candidate_name = None
    constituency_name = None
    for constituency in data:
        candidates = constituency["candidates"]

        if len(candidates) < 2:
            # probably voting was rescinded
            continue

        candidates = sorted(candidates, key=lambda candidate: candidate['total_votes'], reverse=True)
        margin = candidates[0]["total_votes"] - candidates[1]["total_votes"]

        if margin > highest_margin_count:
            candidate_name = candidates[0]["candidate_name"]
            constituency_name = constituency["constituency"]
            highest_margin_count = margin

    print("Highest Margin:", candidate_name, "from", constituency_name, "won by", highest_margin_count, "votes")


def lowest_margin():
    lowest_margin_count = 99999999
    candidate_name = None
    constituency_name = None
    for constituency in data:
        candidates = constituency["candidates"]

        if len(candidates) < 2:
            # probably voting was rescinded
            continue

        candidates = sorted(candidates, key=lambda candidate: candidate['total_votes'], reverse=True)
        margin = candidates[0]["total_votes"] - candidates[1]["total_votes"]

        if margin < lowest_margin_count:
            candidate_name = candidates[0]["candidate_name"]
            constituency_name = constituency["constituency"]
            lowest_margin_count = margin

    print("Lowest Margin:", candidate_name, "from", constituency_name, "won by", lowest_margin_count, "votes")


def total_votes():
    total_votes_count = sum(
        [candidate["total_votes"] for constituency in data for candidate in constituency["candidates"]])
    print("Total votes casted:", total_votes_count)


def nota_votes():
    nota_votes_count = sum(
        [candidate["total_votes"] for constituency in data for candidate in constituency["candidates"] if
         candidate["candidate_name"] == "nota"])
    print("NOTA votes casted:", nota_votes_count)


candidates_two_constituency()
candidate_highest_votes()
highest_margin()
lowest_margin()
total_votes()
nota_votes()
