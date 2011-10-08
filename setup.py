from setuptools import setup, find_packages

setup(
    name="popcorn",
    version="0.1",
    long_description=__doc__,
    packages=find_packages(exclude=["*.test", "test", "*.test.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'jinja2', 'redis'],
    test_suite="popcorn.test"
    )
