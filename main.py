import requests
import re


def check_current_version(package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")

    if response.status_code != 200:
        return None

    return response.json().get("info").get("version")


def parse_and_check():
    file = open("requirements.txt", "r")
    regex = "\n|==|<=|>=|>|<|\[|\]"
    response = []
    for line in file:
        if line != "\n":
            line = re.split(regex, line)
            latest_version = check_current_version(line[0])

            if latest_version == None:
                continue

            response.append(
                {
                    "packageName": line[0],
                    "currentVersion": line[1],
                    "latestVersion": latest_version,
                    "outOfDate": is_out_of_date(line[1], latest_version),
                }
            )
    file.close()

    return response


def is_out_of_date(current_version, latest_version):
    if current_version != latest_version:
        return True
    return False


if __name__ == "__main__":
    print(parse_and_check())
