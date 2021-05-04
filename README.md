# ros\_stubs

Collection of typing stubs for ROS1 Python libraries

## Installation

```sh
# Install the stub package including all stubs
$ pip install --extra-index-url https://rospypi.github.io/simple/ ros-stubs-all
# Or install each stub package individually
$ pip install --extra-index-url https://rospypi.github.io/simple/ std-msgs-stub
```

Please refer to `src` directory to see the list of available packages.

## Usage

All packages are marked as [stub-only packages](https://www.python.org/dev/peps/pep-0561/#stub-only-packages),
so you don't have to do anything other than installing packages in your Python environment.

## Contributing

All your contributions are always welcome!
Please keep in mind that some directories like `msg`, `srv` are generated at build time.
You can see the build actions for building each package in `_pacakge.yaml`.

We are happy to have typing stubs for third-party ROS libraries.
If you find this repository doesn't have the stub package you want to contribute, please feel free to create.

To create a new stub package, add a directory ending with name ending with `-stubs` under `src` directory.
Also, please add `_package.yaml` in the directory to define the stub information.

### Tips: Generate stub files automatically using stubgen

You can automatically generate the stub file for either a package or a module using [`stubgen`](https://mypy.readthedocs.io/en/stable/stubgen.html).
```sh
$ pip install mypy  # make sure that mypy is installed
$ stubgen -p [package] -o out  # generate stub files for a package
$ stubgen -m [module] -o out  # generate the stub file for a module
```

As stubgen generates draft stubs; generated files may contain wrong definitions, many `Any` types, unnecessary re-exports, etc.
As such, before make a PR, you need to either
- Update generated stubs manually
- Add a warning message as a note in the head of the file.

You will also need to fix stub files to pass the lint CI.
But you can temporarily add them into the ignore list of lint targets only when you choose the latter option.

### Testing

Install `tox` and run `tox` command in the root of this repository.

### Building stubs

All the stub packages are built and published using GitHub actions,
but of course you can build them in your local environment.

Install Python 3.8 and `pipenv==2020.11.15`, and run the following commands:
```sh
$ cd assets
$ pipenv sync --dev
$ pipenv run python build_ros_stubs.py
```

Then, you will get artifacts in `artifacts` in the root of this repository.
