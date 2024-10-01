from pathlib import Path

from taskipy.task_runner import TaskRunner


def run():
    runner = TaskRunner(Path(__file__).parent.parent)
    print("\n====================== RUNNING CHECK TASKS... ======================")

    print("\n======================== FORMATTING CODE... ========================")
    code = runner.run("format", ["."])
    if code != 0:
        print("\nERROR: CODE FORMATTING FAILED!")
        return False

    print("\n========================= LINTING CODE... ==========================")
    code = runner.run("lint", ["src"])
    if code != 0:
        print("\nERROR: CODE LINTING FAILED!")
        return False

    print("\n=================== GENERATING COVERAGE REPORT... ==================")
    code = runner.run("cov", [])
    if code != 0:
        print("\nERROR: COVERAGE REPORT GENERATION FAILED!")
        return False

    print("\nOK!")
