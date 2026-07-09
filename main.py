import argparse
import re
import tomllib
from enum import StrEnum, auto
from pathlib import Path
from typing import Iterator


# package manager
class PM(StrEnum):
    # termux: pkg(apt)
    termux = auto()
    # debian, ubuntu
    apt = auto()
    # redhat, fedora
    dnf = auto()
    # archlinux manjaro
    pacman = auto()
    # windows
    scoop = auto()


PKG_FILE_PATH = Path(__file__).parent / "pkgs.toml"
type PKG_STRUCT = dict[str, dict[str, str]]
MARK_SAME = "."


def sort_pkgs() -> None:
    text = PKG_FILE_PATH.read_text().strip()
    text = re.sub("\n{2,}", "\n", text)
    name_iter = re.finditer(r"^\[[A-Za-z0-9_-]+\]$", text, re.MULTILINE)

    chunks = []
    start = 0
    for name in name_iter:
        end = name.start()
        chunks.append(text[start:end])
        start = end
    chunks.append(text[start:])

    chunks.sort()
    # print(chunks)
    # append an empty string to have an EOL
    chunks.append("")

    PKG_FILE_PATH.write_text("\n".join(chunks))


def parse_pkgs(pm: str) -> Iterator[str]:
    if pm not in PM:
        print(f"ERROR: not found {pm}")
        yield from ()
        return

    text = PKG_FILE_PATH.read_text()
    data: PKG_STRUCT = tomllib.loads(text)
    for pkg_name in data:
        pd = data[pkg_name]
        if pm in pd:
            val = pd[pm]
            if val == MARK_SAME:
                yield pkg_name
            else:
                yield val


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort", action="store_true", help="sort pkgs.toml")
    parser.add_argument("--pm", help="package manager")

    args = parser.parse_args()

    if args.sort:
        sort_pkgs()
    elif args.pm is not None:
        pkgs = parse_pkgs(args.pm)
        print(" ".join(pkgs))
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
