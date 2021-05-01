import argparse
import contextlib
import pathlib
import sys
import tempfile
from datetime import datetime
from typing import ContextManager, Iterator, List

import build_ros_stubs
import git
from buildtool.builder import ArtifactInfo

DEFAULT_ROSPYPI_SIMPLE_URL = "https://github.com/rospypi/simple.git"
DEFAULT_ARTIFACT_BRANCH = "stubs"

GIT_ATTRIBUTES_CONTENT = """*.whl filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
"""


@contextlib.contextmanager
def load_remote_repository(remote_url: str, branch: str) -> Iterator[git.Repo]:
    with tempfile.TemporaryDirectory() as tempdir:
        print("* Cloning rospypi repository")
        repo = git.Repo.clone_from(remote_url, tempdir, branch=branch, depth=1)
        yield repo


@contextlib.contextmanager
def load_local_repository(path: pathlib.Path, branch: str) -> Iterator[git.Repo]:
    print("* Loading local rospypi repository")
    repo = git.Repo(path, search_parent_directories=True)
    head = repo.heads[branch]
    repo.head.reference = head
    repo.head.reset(index=True, working_tree=True)
    yield repo


def build_artifacts(rospypi: pathlib.Path) -> List[ArtifactInfo]:
    build_ros_stubs.setup_logger()
    return build_ros_stubs.run(None, None, out=rospypi)


def has_new_artifacts(artifacts: List[ArtifactInfo], repo: git.Repo) -> bool:
    has_change = any(a.previous_version != a.generated_version for a in artifacts)
    if has_change:
        return True

    return False


def reset_hard_branch(repo: git.Repo, new_branch: str) -> git.Head:
    try:
        head = repo.heads[new_branch]
        print("Head: {branch} exists in local repository -> Removed")
        git.Head.delete(repo, head, force=True)
    except IndexError:
        pass

    head = repo.create_head(new_branch)
    return head


def commit_artifacts(repo: git.Repo) -> None:
    (pathlib.Path(repo.working_dir) / ".gitattributes").write_text(
        GIT_ATTRIBUTES_CONTENT
    )
    repo.index.add(".gitattributes")

    # NOTE: As GitPython doesn't support git-lfs,
    # use low-level API to track the following files as lfs objects
    repo.git.add("**/*.tar.gz")
    repo.git.add("**/*.whl")

    # NOTE: Use parent_commits=[] to create an orphan commit,
    # then update current head to refer to the commit by head=True
    repo.index.commit(
        "Release ros_stubs: {}".format(datetime.now().isoformat()),
        author=git.Actor("ros_stubs", "ros_stubs@noreply.github.com"),
        head=True,
        parent_commits=[],
    )

    assert not repo.is_dirty()


def push_artifacts(repo: git.Repo) -> None:
    repo.remote().push(force=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        help="Url of rospypi/simple",
        default=None,
    )
    parser.add_argument(
        "--repository",
        type=pathlib.Path,
        help="Local path of rospypi/simple",
        default=None,
    )
    parser.add_argument(
        "--branch",
        help="Target branch to push artifacts",
        default=DEFAULT_ARTIFACT_BRANCH,
    )
    parser.add_argument(
        "--ref-branch",
        help=(
            "Target branch to compare artifacts with."
            "If this option is unset, use the same branch as --branch"
        ),
        default=None,
    )
    parser.add_argument(
        "--push",
        help="Push artifacts to remote repository",
        action="store_true",
    )
    args = parser.parse_args()

    build_ros_stubs.setup_logger()
    ref_branch = args.ref_branch or args.branch

    if args.url is not None and args.repository is not None:
        parser.error("cannot set both --url and --repository options")

    context: ContextManager[git.Repo]
    if args.repository is not None:
        context = load_local_repository(args.repository, ref_branch)
    else:
        context = load_remote_repository(
            args.url or DEFAULT_ROSPYPI_SIMPLE_URL, ref_branch
        )

    with context as repo:  # type: git.Repo
        print("* Building artifacts")
        artifacts = build_artifacts(pathlib.Path(repo.working_dir))

        if not has_new_artifacts(artifacts, repo):
            print("=> Nothing has been changed, exit")
            sys.exit(0)

        print("* Creating commit")
        if ref_branch != args.branch:
            # args.branch needs to be reset --hard with ref_branch
            head = reset_hard_branch(repo, args.branch)
        else:
            head = repo.heads[args.branch]

        # swicth current head to the branch
        repo.head.reference = head

        commit_artifacts(repo)
        if args.push:
            print("* Force push to remote")
            push_artifacts(repo)

        print("=> Done")


if __name__ == "__main__":
    main()
