def parse_config(path: str) -> dict:
    config = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError("Invalid config line")

            key, value = line.split("=")
            config[key.strip()] = value.strip()

    return {
        "width": int(config["WIDTH"]),
        "height": int(config["HEIGHT"]),
        "entry": tuple(map(int, config["ENTRY"].split(","))),
        "exit": tuple(map(int, config["EXIT"].split(","))),
        "output": config["OUTPUT_FILE"],
        "perfect": config["PERFECT"] == "True"
    }
