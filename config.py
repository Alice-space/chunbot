import yaml


def parse_yaml_config(file_path: str):
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")

Config = parse_yaml_config("config.yaml")