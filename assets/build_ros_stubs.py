import argparse
import logging
import pathlib

from buildtool import builder, context

REPO_ROOT = pathlib.Path(__file__).absolute().parents[1]


def setup_logger() -> None:
    handler = logging.StreamHandler()

    buildtool_logger = logging.getLogger("buildtool")
    buildtool_logger.setLevel(logging.INFO)
    buildtool_logger.addHandler(handler)


def main() -> None:
    setup_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src",
        help="Source directory to find stub packages",
        type=str,
        default=str(REPO_ROOT / "src"),
    )
    parser.add_argument(
        "--build",
        help="Build directory to generate built packages",
        type=str,
        default=str(REPO_ROOT / "build"),
    )
    parser.add_argument(
        "--out",
        help="Output directory to store build artifacts",
        type=str,
        default=str(REPO_ROOT / "artifacts"),
    )
    args = parser.parse_args()

    ctx = context.BuilderContext(
        source_dir=pathlib.Path(args.src),
        build_dir=pathlib.Path(args.build),
        artifacts_dir=pathlib.Path(args.out),
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


if __name__ == "__main__":
    main()
