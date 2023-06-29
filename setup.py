from setuptools import setup, find_packages
import glob

setup(
    name='metal_library',
    version='1.0.0',
    packages=find_packages(),
    python_requires=">=3.9",
    include_package_data=True,
)