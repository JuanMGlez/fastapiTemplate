from pydantic import BaseModel
from datetime import datetime

# Schema para los settings
class SettingBase(BaseModel):
    config_name: str
    config_value: str

class SettingCreate(SettingBase):
    pass

class Setting(SettingBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True