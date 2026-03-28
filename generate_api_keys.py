import string
import random

services = ["worker"]


def main():
    length = 64
    with open("api_keys", "w") as f:
        for service in services:
            key = "".join(random.choices(string.ascii_letters+string.digits,
                                         k=length))
            f.write(f"{service}={key}\n")

main()
