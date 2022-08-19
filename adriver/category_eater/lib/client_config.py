#from __future__ import annotations
import json
import re



class Access(object):
    """
    Whitelist + Blacklist
    """

    ALL = 'all'

    @classmethod
    def from_dict(cls, value):
        allowed = value["allowed"]
        disallowed = value["disallowed"]
        return cls(allowed, disallowed)

    def __new__(cls, allowed, disallowed):
        if allowed == cls.ALL and not disallowed:
            return ConstAccess(True)

        if disallowed == cls.ALL:
            return ConstAccess(False)

        return super(Access, cls).__new__(cls)

    def __init__(self, allowed, disallowed):
        self.allowed = self.ALL if allowed == self.ALL else \
            self.prepare_items(allowed)
        self.disallowed = self.ALL if disallowed == self.ALL else \
            self.prepare_items(disallowed)

    def prepare_items(self, items):
        return set(items)

    def check(self, item):
        return (self.allowed == self.ALL or item in self.allowed) and \
               self.disallowed != self.ALL and item not in self.disallowed

    def filter(self, items):
        return [i for i in items if self.check(i)]


class PydanticAccess(Access):
    @classmethod
    def __get_validators__(cls):
        yield cls.from_dict


class ConstAccess(object):
    def __init__(self, value):
        self.is_true = value

    def check(self, item):
        return self.is_true

    def filter(self, items):
        return items if self.is_true else []


class CategoryAccess(Access):

    def prepare_items(self, items):
        return super(CategoryAccess, self).prepare_items(
            int(category_id) for category_id in items
        )


class DomainAccess(Access):
    def __init__(self, allowed, disallowed):
        self.allowed = [re.compile(r) for r in allowed]
        self.disallowed = [re.compile(r) for r in disallowed]

    def check(self, item):
        return any(r.match(item) for r in self.allowed) and \
               not any(r.match(item) for r in self.disallowed)


class ClientsConfigLoader:

    def create_config(self, data):
        return data

    def create_many_configs(self, data):

        configs = dict()
        parsed_config = dict()
        allowed_common, disallowed_common = self.create_default_config(data)
        try:
            for site in data["sites"]:
                cfg = site["site_id"]
                configs[cfg] = self.create_config(site)

        except KeyError:
            raise ("Config scheme is not valid")
        try:
            for _, sid in configs.items():

                cfg_allowed = sid.get("categories", {}).get("allowed", [])
                cfg_disallowed = sid.get("categories", {}).get("disallowed", [])
                if "all" in cfg_allowed:
                    pass
                else:
                    cfg_allowed.extend(allowed_common)

                    cfg_disallowed.extend(disallowed_common)
                conf = sid.get("site_id", {})
                parsed_config[conf] = self.create_config(sid)
            return parsed_config
        except KeyError:
            raise ("Config schema is broken")

    def create_default_config(self, data):
        try:
	    print(data)
            default_cfg = data.get("common", {}).get("categories", {})
            allowed_common = default_cfg.get("allowed", [])
            disallowed_common = default_cfg.get("disallowed", [])
            return allowed_common, disallowed_common
        except KeyError:
            raise ("Config scheme is not valid")


class LoadParsedConfig(object):

    @classmethod
    def create_parsed(cls, config_data):
        return cls(config_data)

    @classmethod
    def create_multi_parsed(cls, config_data):
        configs = dict()
        for _, params in config_data.items():
            site_id = params["site_id"]
            configs[site_id] = cls.create_parsed(params)
        # print configs
        return configs

    def __init__(self, config_data):
        self._config_data = config_data
        self.enabled = self._config_data.get("enabled", True)
        referers = self._config_data.get("referers", {})
        self.referers_access = Access(
            referers.get("allowed", []),
            referers.get("disallowed", [])
        )

        categories = self._config_data.get("categories", {})
        self.categories_access = Access(
            categories.get("allowed", []),
            categories.get("disallowed", [])
        )


class ConfigBuilder:

    @classmethod
    def build_config(cls, config_data):
        cls.load_config = ClientsConfigLoader()
        parsed_config = cls.load_config.create_many_configs(config_data)
        config = LoadParsedConfig.create_multi_parsed(parsed_config)
        return config

# def load_clients_config(source_config):
#     data_source = source_config.get("data_source")
#     if data_source == "acc":
#         acc_config = source_config["acc"]
#         config_data = ACCClient(
#             host=acc_config["url"],
#             auth_token=acc_config["auth_token"],
#         ).get_config(
#             app_id=acc_config["app_id"],
#             config_name="publishers"
#         )
#     elif data_source == "file":
#         file_path = source_config["file"]
#         with open(file_path) as _config_file:
#             config_data = json.load(_config_file)
#     else:
#         raise ValueError(
#             "Invalid clients config data source: \"{source}\"".format(
#                 source=data_source
#             )
#         )
#
#    return ClientConfig.create_many_configs(config_data)
