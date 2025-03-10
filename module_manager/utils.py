def check_latest_version(module):
    latest_versions = {
        "products": "1.1.0",
    }

    if module.name in latest_versions:
        module.latest_version = latest_versions[module.name]
        module.save(update_fields=["latest_version"])
