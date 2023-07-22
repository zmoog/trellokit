from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="trellokit",
    description="CLI tool and Python library to access and use Trello API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Maurizio Branca",
    url="https://github.com/zmoog/trellokit",
    project_urls={
        "Issues": "https://github.com/zmoog/trellokit/issues",
        "CI": "https://github.com/zmoog/trellokit/actions",
        "Changelog": "https://github.com/zmoog/trellokit/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["trellokit"],
    entry_points="""
        [console_scripts]
        trellokit=trellokit.cli:cli
    """,
    install_requires=["click"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.7",
)
