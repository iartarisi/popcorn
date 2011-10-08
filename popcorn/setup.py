from setuptools import setup

setup(
    name="Popcorn",
    version="0.1",
    long_description=__doc__,
    packages=["popcorn"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask", "jinja2", "redis"]
