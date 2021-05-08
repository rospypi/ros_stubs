import argparse
import logging
import pathlib
from typing import List, Optional

from buildtool import build_env, builder, context

_logger = logging.getLogger(__name__)

ASSETS_DIR = pathlib.Path(__file__).absolute().parent
REPO_ROOT = ASSETS_DIR.parent


def setup_logger() -> None:
    loggers = [
        logging.getLogger("buildtool"),
        _logger,
    ]

    handler = logging.StreamHandler()
    for logger in loggers:
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)


def run(
    src: Optional[pathlib.Path],
    env_manifest: Optional[pathlib.Path],
    build: Optional[pathlib.Path],
    out: Optional[pathlib.Path],
) -> List[builder.ArtifactInfo]:
    source_dir = src or REPO_ROOT / "src"
    build_dir = build or REPO_ROOT / "build"
    artifacts_dir = out or REPO_ROOT / "artifacts"
    env_manifest = env_manifest or ASSETS_DIR / "build_env_manifest.yaml"

    build_env_dir = build_dir / ".build_env"
    build_env.clean_build_env_dir(build_env_dir)

    _logger.info("Loading env-manifest")
    env_packages = build_env.load_env_package_yaml(env_manifest)
    _logger.info("Preparing build environment")
    build_env.setup_build_env(env_packages, build_env_dir)

    ctx = context.BuilderContext(
        source_dir=source_dir,
        build_dir=build_dir,
        artifacts_dir=artifacts_dir,
    )
    ctx.variables["ROS_SHARE_DIR"] = "/opt/ros/noetic/share"
    ctx.variables["BUILD_ENV_DIR"] = str(build_env_dir)

    _logger.info("Running buildtool")
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
        "--env-manifest",
        help="Path to a yaml file which defines the environment to build packages",
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

    run(args.src, args.env_manifest, args.build, args.out)


if __name__ == "__main__":
    main()
