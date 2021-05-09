from setuptools import find_packages, setup

setup(
    name="buildtool",
    version="0.0.1",
    packages=find_packages(),
    description="A Python stub generator from genmsg specs",
    author="Yuki Igarashi",
    author_email="me@bonprosoft.com",
    install_requires=[
        "PyYAML>=5.4,<6.0",
        "build>=0.3.0,<0.4.0",
        "genmypy>=0.3.1,<0.4.0",
        "pydantic>=1.8.0,<2.0.0",
    ],
    package_data={"buildtool": ["py.typed"]},
)
