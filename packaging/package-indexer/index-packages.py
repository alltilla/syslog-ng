#!/bin/env python3
#############################################################################
# Copyright (c) 2022 One Identity
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################

import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import List

from indexer import Indexer, NightlyDebIndexer, ReleaseDebIndexer
from config import Config


def add_required_arguments(parser: ArgumentParser) -> None:
    required_argument_group = parser.add_argument_group("required arguments")
    required_argument_group.add_argument(
        "--config",
        type=str,
        required=True,
        help="The path of the config file in yaml format.",
    )
    required_argument_group.add_argument(
        "--run-id",
        type=str,
        required=True,
        help='The "run-id" of the "draft-release" or "nightly-packages" GitHub Actions job.',
    )
    required_argument_group.add_argument(
        "--suite",
        type=str,
        required=True,
        metavar="SUITE",
        choices=["stable", "nightly"],
        help='"stable" or "nightly".',
    )


def add_optional_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--log-file",
        type=str,
        help="Also log more verbosely into this file.",
    )


def parse_args() -> dict:
    parser = ArgumentParser()
    add_required_arguments(parser)
    add_optional_arguments(parser)

    return vars(parser.parse_args())


def init_logging(args: dict) -> None:
    handlers: List[logging.Handler] = []

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    handlers.append(stream_handler)

    if "log_file" in args.keys() and args["log_file"] is not None:
        file_handler = logging.FileHandler(args["log_file"])
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)

    logging.basicConfig(
        format="%(asctime)s\t[%(name)s]\t%(message)s",
        handlers=handlers,
    )


def construct_indexers(cfg: Config, args: dict) -> List[Indexer]:
    suite = args["suite"]

    incoming_remote_storage_synchronizer = cfg.create_incoming_remote_storage_synchronizer(suite)
    indexed_remote_storage_synchronizer = cfg.create_indexed_remote_storage_synchronizer(suite)
    cdn = cfg.create_cdn(suite)

    indexers: List[Indexer] = []

    if suite == "nightly":
        indexers.append(
            NightlyDebIndexer(
                incoming_remote_storage_synchronizer=incoming_remote_storage_synchronizer,
                indexed_remote_storage_synchronizer=indexed_remote_storage_synchronizer,
                cdn=cdn,
            )
        )
    elif suite == "stable":
        indexers.append(
            ReleaseDebIndexer(
                incoming_remote_storage_synchronizer=incoming_remote_storage_synchronizer,
                indexed_remote_storage_synchronizer=indexed_remote_storage_synchronizer,
                cdn=cdn,
                run_id=args["run_id"],
                gpg_key_path=Path(cfg.get_gpg_key_path()),
            )
        )
    else:
        raise NotImplementedError("Unexpected suite: {}".format(suite))

    return indexers


def main() -> None:
    args = parse_args()
    init_logging(args)

    cfg = Config(Path(args["config"]))

    indexers = construct_indexers(cfg, args)
    for indexer in indexers:
        indexer.index()


if __name__ == "__main__":
    main()
