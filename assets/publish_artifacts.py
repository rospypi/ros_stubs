import argparse
import pathlib
import sys
import tempfile
from typing import List

import build_ros_stubs
import git
from buildtool.builder import ArtifactInfo

DEFAULT_ROSPYPI_SIMPLE_URL = "git@github.com:rospypi/simple.git"
DEFAULT_ARTIFACT_BRANCH = "any_stubs"


def clone_rospypi_simple(remote_url: str, dst: pathlib.Path, branch: str) -> git.Repo:
    repo = git.Repo.clone_from(remote_url, dst, branch=branch)
    return repo


def build_artifacts(rospypi: pathlib.Path) -> List[ArtifactInfo]:
    build_ros_stubs.setup_logger()
    return build_ros_stubs.run(None, None, out=rospypi)


def has_new_artifacts(artifacts: List[ArtifactInfo], repo: git.Repo) -> bool:
    has_change = any(a.previous_version != a.generated_version for a in artifacts)
    if has_change:
        assert repo.is_dirty()
        return True

    return False


def commit_artifacts(repo: git.Repo) -> None:
    repo.index.add("**/*.tar.gz")
    repo.index.add("**/*.whl")
    repo.index.commit(
        "Release ros_stubs: {}",
        author=git.Actor("ros_stubs", "ros_stubs@noreply.github.com"),
    )

    assert not repo.is_dirty()


def push_artifacts(repo: git.Repo) -> None:
    repo.remote().push()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--simple-url",
        help="Url of rospypi/simple",
        default=DEFAULT_ROSPYPI_SIMPLE_URL,
    )
    parser.add_argument(
        "--branch",
        help="Target branch to push artifacts",
        default=DEFAULT_ARTIFACT_BRANCH,
    )
    args = parser.parse_args()

    build_ros_stubs.setup_logger()
    with tempfile.TemporaryDirectory() as td:
        tempdir = pathlib.Path(td)
        rospypi_dir = tempdir / "rospypi"
        rospypi_dir.mkdir()

        print("Cloning rospypi")
        repo = clone_rospypi_simple(args.simple_url, rospypi_dir, args.branch)
        print("Building artifacts")
        artifacts = build_artifacts(rospypi_dir)

        if not has_new_artifacts(artifacts, repo):
            print("Nothing has been changed, exit")
            sys.exit(0)

        print("Creating commit")
        commit_artifacts(repo)
        print("Push to remote")
        push_artifacts(repo)

        print("Done")


if __name__ == "__main__":
    main()
