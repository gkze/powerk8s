from __future__ import annotations

import logging
import sys
from io import TextIOBase
from logging import Logger
from pathlib import Path
from typing import Any, Callable, Mapping, NewType, Optional, Sequence, TextIO

import black
import click
import toml
from autoflake import _main as autoflake_main
from black import main as black_main
from isort.main import main as isort_main

FILE_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = FILE_DIR.parent
PROJECT_CONFIG_FILE: str = "pyproject.toml"

AUTOFLAKE: str = "autoflake"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(msg)s"
)
LOGGER: logging.Logger = logging.getLogger(__name__)
LogLevel = NewType("LogLevel", int)


class TextIOLogger(TextIOBase):
    def __init__(
        self: TextIOLogger,
        logger: Logger,
        level: LogLevel,
        prefix: Optional[str] = None,
    ) -> None:
        self._logger: Logger = logger
        self._level: LogLevel = level
        self._prefix = prefix

    def write(self: TextIOLogger, s: str) -> None:
        if s == "\n":
            return

        lvlstrlower: str = logging.getLevelName(self._level).lower()
        lvl: Callable[...] = getattr(self._logger, lvlstrlower)
        msg: str = s.replace("\n", "")

        if self._prefix is not None:
            msg = f"({self._prefix}) {msg}"

        lvl(msg)


def get_autoflake_args(
    config_path: Path = ROOT_DIR / PROJECT_CONFIG_FILE,
) -> Sequence[str]:
    config: Mapping[str, Any] = {}
    autoflake_args: Sequence[str] = []

    with config_path.open() as f:
        config = toml.load(f)

    autoflake_opts: Mapping[str, Any] = config["tool"][AUTOFLAKE]
    for opt, val in autoflake_opts.items():
        opt_as_arg: str = f"--{opt.replace('_', '-')}"

        if opt == "src":
            autoflake_args.append(val)
            continue

        if isinstance(val, bool):
            autoflake_args.append(opt_as_arg)

        else:
            autoflake_args.append(f'{opt_as_arg}="{val}"')

    return autoflake_args


def main() -> None:
    autoflake_info_logger: TextIOLogger = TextIOLogger(
        logging.getLogger(f"linter.{AUTOFLAKE}"), logging.INFO
    )
    autoflake_warn_logger: TextIOLogger = TextIOLogger(
        logging.getLogger(f"linter.{AUTOFLAKE}"), logging.INFO
    )
    isort_logger: TextIOLogger = TextIOLogger(
        logging.getLogger("linter.isort"), logging.INFO
    )
    black_logger: Logger = logging.getLogger("linter.black")

    def click_secho_logger_shim(
        s: str, *args: Sequence[str], **kwargs: Mapping[str, Any]
    ) -> None:
        black_logger.info(s)

    LOGGER.info("Running autoflake...")
    autoflake_retcode: int = autoflake_main(
        [AUTOFLAKE, *get_autoflake_args()], autoflake_info_logger, autoflake_warn_logger
    )
    LOGGER.info(f"Autoflake exited with code {autoflake_retcode}")

    LOGGER.info("Running isort...")
    sys_stdout_orig: TextIO = sys.stdout
    sys.stdout = isort_logger
    isort_main(["."])
    sys.stdout = sys_stdout_orig
    LOGGER.info("Isort ran successfully")

    LOGGER.info("Running black...")
    click_secho_orig = click.secho
    click.secho = click_secho_logger_shim
    black.out = black_logger.info
    black.err = black_logger.warn

    try:
        black_main((".",))
    except SystemExit as e:
        LOGGER.info(f"Black exited with code {e}")

    click.secho = click_secho_orig

    LOGGER.info("Finished running all linters.")


if __name__ == "__main__":
    main()
