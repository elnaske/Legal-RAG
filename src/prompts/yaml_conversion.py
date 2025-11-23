import yaml
from prompts import get_all_prompts

PATH = "./prompts/prompts.yaml" 

def dump_to_yaml(prompts_dict):
    with open(PATH, "w") as f:
        yaml.dump(prompts_dict, f)

def test_yaml(prompts_dict):
    with open(PATH, "r") as f:
        yaml_loaded = yaml

    with open(PATH, "r") as f:
        yaml_loaded = yaml.safe_load(f)
    
    for key in prompts_dict.keys():
        assert prompts_dict[key] == yaml_loaded[key]
        print(key, "success")

def str_presenter(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def main():
    yaml.add_representer(str, str_presenter)

    prompts_dict = get_all_prompts()

    dump_to_yaml(prompts_dict)
    test_yaml(prompts_dict)

    print("success")


if __name__ == "__main__":
    main()