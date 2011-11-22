from setuptools import setup, find_packages
import tinkerer

setup(
    name="Tinkerer",
    version=tinkerer.__version__,
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "tinker = tinkerer.cmdline:main"
        ]
    }
)
