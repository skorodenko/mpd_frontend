import pathlib
from dynaconf import Dynaconf
from xdg import xdg_config_home, xdg_data_home, xdg_state_home, xdg_cache_home

xdg_config_dir = pathlib.Path(xdg_config_home()) / "soloviy"
xdg_data_dir = pathlib.Path(xdg_data_home()) / "soloviy"
xdg_state_dir = pathlib.Path(xdg_state_home()) / "soloviy"
xdg_cache_dir = pathlib.Path(xdg_cache_home()) / "soloviy"
settings_file = str(xdg_config_dir / "settings.toml")
log_file = str(xdg_state_dir / "soloviy.log")
default_config = str(pathlib.Path("./settings.default.toml"))
sqlite_db = str(xdg_data_dir / "soloviy.db")
state_db = str(xdg_state_dir / "state.db")

settings = Dynaconf(
    settings_file = settings_file,
    log_file = log_file,
    xdg_config_dir = str(xdg_config_dir),
    xdg_data_dir = str(xdg_data_dir),
    xdg_state_dir = str(xdg_state_dir),
    xdg_cache_home = str(xdg_cache_dir),
    preload = default_config,
    merge_enable = True,
)