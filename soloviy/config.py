import pathlib
from dynaconf import Dynaconf
from xdg import XDG_CONFIG_HOME, XDG_DATA_HOME

xdg_config_dir = pathlib.Path(XDG_CONFIG_HOME) / "soloviy"
xdg_data_dir = pathlib.Path(XDG_DATA_HOME) / "soloviy"
setings_file = str(xdg_config_dir / "setings.toml")
default_config = str(pathlib.Path("./setings.default.toml"))

settings = Dynaconf(
    setings_file = setings_file,
    xdg_config_dir = xdg_config_dir,
    xdg_data_dir = xdg_data_dir,
    includes = default_config,
    environments = True,
    env = "dev",
)