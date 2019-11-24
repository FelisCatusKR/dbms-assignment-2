import requests, csv, json


def test_post_data():
    with open("contact.csv", "r", encoding="UTF-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            r = requests.post("http://localhost:8000/api/users", data=json.dumps(row))
            assert r.status_code == 201


if __name__ == "__main__":
    test_post_data()
