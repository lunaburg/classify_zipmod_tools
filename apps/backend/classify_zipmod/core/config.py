import json
import sys
from pathlib import Path


class ConfigDataList:
    ZIPMOD_MODE_COPY = "copy"
    ZIPMOD_MODE_MOVE = "move"
    CONFIG_DIR_NAME = "config"
    CONFIG_FILE_NAME = "settings.json"

    def __init__(self, config_path=None):
        self.mod_names = set()
        self.missing_mods = set()
        self.missing_abdata = set()
        self.card_path = set()
        self.game_dir = ""
        self.input_dir = ""
        self.output_dir = ""
        self.zipmod_extract_mode = self.ZIPMOD_MODE_COPY
        self.config_path = Path(config_path) if config_path else self.default_config_path()
        self.load_or_create()

    @classmethod
    def default_config_path(cls):
        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).resolve().parent
        else:
            base_dir = Path(__file__).resolve().parents[3]
        return base_dir / cls.CONFIG_DIR_NAME / cls.CONFIG_FILE_NAME

    def to_dict(self):
        return {
            "game_dir": self.game_dir,
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
            "zipmod_extract_mode": self.zipmod_extract_mode,
        }

    def load_or_create(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.save()
            return

        try:
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.save()
            return

        self.game_dir = str(data.get("game_dir") or "")
        self.input_dir = str(data.get("input_dir") or "")
        self.output_dir = str(data.get("output_dir") or "")
        mode = data.get("zipmod_extract_mode") or self.ZIPMOD_MODE_COPY
        if mode in {self.ZIPMOD_MODE_COPY, self.ZIPMOD_MODE_MOVE}:
            self.zipmod_extract_mode = mode
        else:
            self.zipmod_extract_mode = self.ZIPMOD_MODE_COPY
            self.save()

    def save(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def set_game_dir(self, game_dir, save=True):
        self.game_dir = game_dir
        if save:
            self.save()

    def set_input_dir(self, input_dir, save=True):
        self.input_dir = input_dir
        if save:
            self.save()

    def set_output_dir(self, output_dir, save=True):
        self.output_dir = output_dir
        if save:
            self.save()

    def set_zipmod_extract_mode(self, mode, save=True):
        if mode not in {self.ZIPMOD_MODE_COPY, self.ZIPMOD_MODE_MOVE}:
            raise ValueError(f"Unsupported zipmod extract mode: {mode}")
        self.zipmod_extract_mode = mode
        if save:
            self.save()

    def set_dir(self, game_dir, input_dir, output_dir):
        self.set_game_dir(game_dir, save=False)
        self.set_input_dir(input_dir, save=False)
        self.set_output_dir(output_dir, save=False)
        self.save()
