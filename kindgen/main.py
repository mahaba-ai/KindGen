"""
    Main Application Script to run for a given Workflow
"""

from kindgen.stages import (
    run_stage_1,
    run_stage_2,
    run_stage_3,
    run_stage_4,
    run_stage_5,
    run_stage_6,
)


def main():
    """
    Process must yield results where required after / in each substage.
    """
    stage_1_results = run_stage_1()

    stage_2_results = run_stage_2(stage_1_results)

    stage_3_results = run_stage_3(stage_2_results)

    stage_4_results = run_stage_4(stage_3_results)

    stage_5_results = run_stage_5(stage_4_results)

    stage_6_results = run_stage_6(stage_5_results)

    return True


if __name__ == "__main__":
    main()
