def get_description() -> str:
    with open("./docs/description.txt", "r") as file:
        description = file.read()
    return description
