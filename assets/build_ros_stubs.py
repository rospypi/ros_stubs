import argparse
import logging
import pathlib
from typing import List, Optional

from buildtool import builder, context

REPO_ROOT = pathlib.Path(__file__).absolute().parents[1]


def setup_logger() -> None:
    handler = logging.StreamHandler()

    buildtool_logger = logging.getLogger("buildtool")
    buildtool_logger.setLevel(logging.INFO)
    buildtool_logger.addHandler(handler)


def run(
    src: Optional[pathlib.Path],
    build: Optional[pathlib.Path],
    out: Optional[pathlib.Path],
) -> List[builder.ArtifactInfo]:
    source_dir = src or REPO_ROOT / "src"
    build_dir = build or REPO_ROOT / "build"
    artifacts_dir = out or REPO_ROOT / "artifacts"

    ctx = context.BuilderContext(
        source_dir=source_dir,
        build_dir=build_dir,
        artifacts_dir=artifacts_dir,
    )
    ctx.variables["ROS_SHARE_DIR"] = "/opt/ros/melodic/share"

    artifacts = builder.build(ctx)
    print(" ===== Build Result =====")
    for artifact in artifacts:
        previous_version = "-"
        footer = ""
        if artifact.previous_version is not None:
            previous_version = artifact.previous_version.version
            if artifact.previous_version != artifact.generated_version:
                footer = " (updated)"

        print(
            " - {}: {} -> {}{}".format(
                artifact.name,
                previous_version,
                artifact.generated_version.version,
                footer,
            )
        )

    return artifacts


def main() -> None:
    setup_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src",
        help="Source directory to find stub packages",
        type=pathlib.Path,
        default=None,
    )
    parser.add_argument(
        "--build",
        help="Build directory to generate built packages",
        type=pathlib.Path,
        default=None,
    )
    parser.add_argument(
        "--out",
        help="Output directory to store build artifacts",
        type=pathlib.Path,
        default=None,
    )
    args = parser.parse_args()

    run(args.src, args.build, args.out)


if __name__ == "__main__":
    main()
