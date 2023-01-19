""" generate json file """
from typing import AnyStr
import requests
from packaging import version
import json

import settings


def load_remote_instance_urls():
    try:
        response = requests.get(settings.JOIN_INSTANCES_JSON, timeout=settings.TIMEOUT)
        return response.json()
    except:
        print(
            f"Could not remote load instance urls from {settings.JOIN_INSTANCES_JSON}"
        )
        return None


def load_dev_instance_urls():
    return [settings.DEV_INSTANCE_URL]


def get_instance_info(url: AnyStr):
    try:
        response = requests.get(f"{url}api/v1/instance", timeout=settings.TIMEOUT)
        return response.json()
    except:
        print(f"Could not load instance infos from {url}")
        return None


def filter_valid_instance(info):
    if not info:
        return False

    parsed_version = version.parse(info["version"])
    if parsed_version < version.parse(settings.MINIMUM_VERSION):
        return False

    return True


if __name__ == "__main__":
    remote_instance_urls = load_remote_instance_urls() or []
    instance_urls = load_dev_instance_urls() + remote_instance_urls

    instance_infos = map(get_instance_info, instance_urls)
    available_instances = list(filter(filter_valid_instance, instance_infos))

    with open(f"data/instances.json", "w+", encoding="utf-8") as api_file:
        api_file.write(json.dumps(available_instances))
