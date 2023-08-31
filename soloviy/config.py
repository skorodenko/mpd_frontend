import pathlib
from dynaconf import Dynaconf
from xdg import XDG_CONFIG_HOME, XDG_DATA_HOME

xdg_config_dir = pathlib.Path(XDG_CONFIG_HOME) / "soloviy"
xdg_data_dir = pathlib.Path(XDG_DATA_HOME) / "soloviy"
settings_file = str(xdg_config_dir / "settings.toml")
default_config = str(pathlib.Path("./settings.default.toml"))

settings = Dynaconf(
    settings_file = settings_file,
    xdg_config_dir = str(xdg_config_dir),
    xdg_data_dir = str(xdg_data_dir),
    preload = default_config,
)