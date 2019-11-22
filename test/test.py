import requests, csv, json


def test_post_data():
    with open("data.csv", "r", encoding="UTF-8", newline="") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            r = requests.post("http://localhost:8000/api/users", data=json.dumps(row))
            assert r.status_code == 201


def test_search_data():
    pass


if __name__ == "__main__":
    test_post_data()
