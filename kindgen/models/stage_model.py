from typing import Generator, Dict, Callable, ClassVar

from pydantic import BaseModel

from kindgen.stages import (
    run_stage_1_substage_1,
    run_stage_1_substage_3,
    run_stage_1_substage_4,
    run_stage_1_substage_6,
    run_stage_1_substage_8,
)


class Stage(BaseModel):
    stage: int
    substage: int

    stage_function_map: ClassVar[Dict[int, Callable]] = {
        (1, 1): run_stage_1_substage_1,
        (1, 3): run_stage_1_substage_3,
        (1, 4): run_stage_1_substage_4,
        (1, 6): run_stage_1_substage_6,
        (1, 8): run_stage_1_substage_8,
    }

    def next_substage(self):
        """Increment the substage."""
        self.substage += 1

    def reset_substage(self):
        """Reset the substage to 1."""
        self.substage = 1

    def next_stage(self):
        """Move to the next stage and reset the substage."""
        self.stage += 1
        self.reset_substage()

    def reset(self):
        """Reset to default"""
        self.stage = 1
        self.substage = 1

    def to_tuple(self) -> tuple[int, int]:
        """Return the stage and substage as a tuple."""
        return self.stage, self.substage

    def run(self, *args, **kwargs) -> Generator:
        """
        Execute the function corresponding to the current stage and substage.

        This method routes to the correct function and yields the results.
        """
        stage_function = self.stage_function_map.get((self.stage, self.substage))

        if not stage_function:
            raise ValueError(f"No function defined for stage {self.stage}")

        yield from stage_function(substage=self.substage, *args, **kwargs)