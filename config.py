import yaml
import pydantic as pyd


class ConfigMeter(pyd.BaseModel):
    # run_type: str = pyd.Field(validation_alias=pyd.AliasChoices('RUN_TYPE', 'RUN TYPE', 'run type'))
    run_type: str
    meter_uuid: pyd.UUID4
    # meter_uuid: pyd.UUID4 = pyd.Field(validation_alias=pyd.AliasChoices('METER_UUID', 'METER UUID', 'meter uuid'))

    # @pyd.field_validator('run_type')
    # @classmethod
    # def check_run_type(cls, v: str) -> str:
    #     supported_run_types = ("dry run", "run")
    #     if v.lower() not in supported_run_types:
    #         raise ValueError(f"run type:'{v}' not supported. Use of of the following: {supported_run_types}")
    #     return v.lower()


def open_config_meter(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_config_meter(file_path="./data/config_meter.yaml") -> ConfigMeter:
    config_raw = open_config_meter(file_path)
    config_parsed = ConfigMeter(**config_raw)
    return config_parsed

