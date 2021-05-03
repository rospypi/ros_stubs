import pathlib
from typing import List, Literal, Tuple, cast

from .build_action import BuildAction
from .context import BuilderContext

ACTIONLIB_EXTENSION = ".action"


def parse_actionlib(contents: str) -> Tuple[str, str, str]:
    parts: List[List[str]] = []
    for line in contents.splitlines():
        if line.startswith("---"):
            parts.append([])
            continue

        parts[-1].append(line)

    assert len(parts) == 3, "Invalid actionlib file"
    return cast(Tuple[str, str, str], tuple("\n".join(p) for p in parts))


def generate_msgs_from_actionlib(path: pathlib.Path, out_dir: pathlib.Path) -> None:
    assert path.name.endswith(ACTIONLIB_EXTENSION)
    action_name = path.name[: -len(ACTIONLIB_EXTENSION)]

    contents = path.read_text()
    goal, result, feedback = parse_actionlib(contents)

    (out_dir / f"{action_name}Goal.msg").write_text(goal)
    (out_dir / f"{action_name}Result.msg").write_text(result)
    (out_dir / f"{action_name}Feedback.msg").write_text(feedback)
    (out_dir / f"{action_name}Action.msg").write_text(
        f"""{action_name}ActionGoal action_goal
{action_name}ActionResult action_result
{action_name}ActionFeedback action_feedback
"""
    )
    (out_dir / f"{action_name}ActionGoal.msg").write_text(
        f"""Header header
actionlib_msgs/GoalID goal_id
{action_name}Goal goal
"""
    )
    (out_dir / f"{action_name}ActionResult.msg").write_text(
        f"""Header header
actionlib_msgs/GoalStatus status
{action_name}Result result
"""
    )
    (out_dir / f"{action_name}ActionFeedback.msg").write_text(
        f"""Header header
actionlib_msgs/GoalStatus status
{action_name}Feedback feedback
"""
    )


class ActionlibBuild(BuildAction):
    type: Literal["actionlib_build"]

    source_dir: str
    message_dir: str

    def build(
        self, package_name: str, package_dir: pathlib.Path, context: BuilderContext
    ) -> None:
        source_dir = context.format_path(self.source_dir, package_dir)
        message_dir = context.format_path(self.message_dir, package_dir)
        action_files = list(source_dir.glob(f"*{ACTIONLIB_EXTENSION}"))

        for action in action_files:
            generate_msgs_from_actionlib(action, message_dir)
