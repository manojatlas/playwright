import os

from features.environment import PROJECT_ROOT


def set_output_file(context, filename):
    output_directory = PROJECT_ROOT / "screenshot_test"
    baseline_directory = PROJECT_ROOT / "screenshot_baseline"
    if ("baseline" in context.feature.tags) or ("baseline" in context.scenario.tags):
        os.makedirs(baseline_directory, exist_ok=True)
        outfile = os.path.join(baseline_directory, f"{filename}.png")
    else:
        os.makedirs(output_directory, exist_ok=True)
        outfile = os.path.join(output_directory, f"{filename}.png")
    return output_directory, baseline_directory, outfile
