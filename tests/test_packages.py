import pathlib

from buildtool import stub_package


def test_packages(repo_root: pathlib.Path) -> None:
    src_dir = repo_root / "src"
    package_dirs = list(src_dir.iterdir())

    for package_dir in package_dirs:
        # `src` directory should have only packages
        assert package_dir.is_dir()
        assert package_dir.name.endswith("-stubs")

        # check if the package have package.yaml
        package_file = package_dir / "_package.yaml"
        assert package_file.exists()
        assert package_file.is_file()

        # validate package.yaml by loading config
        stub_package.load_stub_package(package_file)
