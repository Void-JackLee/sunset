import yaml

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

lbs_config = load_config("lbs.yml")
print(f'Use lbs backbone={lbs_config["use"]}')
