import argparse
import pathlib
import sys
import tempfile
from typing import List

import build_ros_stubs
import git
from buildtool.builder import ArtifactInfo

DEFAULT_ROSPYPI_SIMPLE_URL = "https://github.com/rospypi/simple.git"
DEFAULT_ARTIFACT_BRANCH = "any_stubs"

GIT_ATTRIBUTES_CONTENT = """*.whl filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
"""


def clone_rospypi_simple(remote_url: str, dst: pathlib.Path, branch: str) -> git.Repo:
    repo = git.Repo.clone_from(remote_url, dst, branch=branch)
    return repo


def build_artifacts(rospypi: pathlib.Path) -> List[ArtifactInfo]:
    build_ros_stubs.setup_logger()
    return build_ros_stubs.run(None, None, out=rospypi)


def has_new_artifacts(artifacts: List[ArtifactInfo], repo: git.Repo) -> bool:
    has_change = any(a.previous_version != a.generated_version for a in artifacts)
    if has_change:
        return True

    return False


def commit_artifacts(repo_dir: pathlib.Path, repo: git.Repo) -> None:
    repo.head.reset(index=True, working_tree=True)

    (repo_dir / ".gitattributes").write_text(GIT_ATTRIBUTES_CONTENT)
    repo.index.add(".gitattributes")
    repo.index.add("**/*.tar.gz")
    repo.index.add("**/*.whl")
    # NOTE: Use parent_commits=[] to create an orphan commit,
    # then update current head to refer to the commit by head=True
    repo.index.commit(
        "Release ros_stubs: {}",
        author=git.Actor("ros_stubs", "ros_stubs@noreply.github.com"),
        head=True,
        parent_commits=[],
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
    parser.add_argument(
        "--no-push",
        help="Do not push artifacts to remote repository",
        action="store_true",
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
        commit_artifacts(rospypi_dir, repo)
        if not args.no_push:
            print("Push to remote")
            push_artifacts(repo)

        print("Done")


if __name__ == "__main__":
    main()
