
from setuptools import setup, find_packages

setup(
    name = "TorSpiders",
    description="Spiders a website using the darknet via Tor.",
    author="Travis Hoppe",
    author_email="travis.hoppe+github.tor_spiders@gmail.com",
    url="https://github.com/thoppe/tor_spiders",
    version = "1.0",
    packages = find_packages(),
    install_requires = [
        'certifi>=2015.4.28',
        'chardet>=2.3.0',
        'requesocks>=0.10.8',
        'stem>=1.4.0',
        'wheel>=0.24.0',
    ]
)
