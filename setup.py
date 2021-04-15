import codecs
from os.path import abspath, dirname, join

from setuptools import find_packages, setup


TEST_DEPS = ["coverage[toml]", "pytest", "pytest-cov"]
DOCS_DEPS = [
    "sphinx",
    "sphinx-rtd-theme",
    "sphinx-autoapi",
    "recommonmark",
    "sphinxcontrib-runcmd",
]
CHECK_DEPS = [
    "isort[colors]",
    "flake8",
    "flake8-quotes",
    "pep8-naming",
    "mypy",
    "black",
]
REQUIREMENTS = ["pyyaml", "spotipy"]

EXTRAS = {
    "test": TEST_DEPS,
    "docs": DOCS_DEPS,
    "check": CHECK_DEPS,
    "dev": TEST_DEPS + DOCS_DEPS + CHECK_DEPS,
}

# Read in the version
with open(join(dirname(abspath(__file__)), "VERSION")) as version_file:
    version = version_file.read().strip()


setup(
    name="stream-tools",
    version=version,
    description="Collection of scripts/tools for streaming",
    long_description=codecs.open("README.md", "r", "utf-8").read(),
    long_description_content_type="text/markdown",
    author="Fernando Chorney",
    author_email="github@djsbx.com",
    url="https://github.com/fchorney/stream_tools",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=["any"],
    include_package_data=True,
    tests_require=TEST_DEPS,
    extras_require=EXTRAS,
    entry_points={
        "console_scripts": ["spotify-title = stream_tools.spotify.track_title:main"]
    },
)
