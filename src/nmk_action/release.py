from typing import List
from nmk.model.builder import NmkTaskBuilder
from nmk.utils import run_with_logs
from nmk.model.keys import NmkRootConfig

class BaseReleaseBuilder(NmkTaskBuilder):
    def git(self, args: List[str]):
        self.logger.info(self.task.emoji, f"Running git {' '.join(args)}")
        run_with_logs(["git"] + args, cwd=self.model.config[NmkRootConfig.PROJECT_DIR].value, logger=self.logger)

class ReleaseBuilder(NmkTaskBuilder):
    def build(self, tag: str, default_version: str, target_versions: List[str]):
        # Prolog: just verify we're not dirty
        assert not self.model.config["gitVersion"].value.endswith("-dirty"), "Repo is dirty, please commit before"

        # Step 1: create tag
        self.git(["tag", tag])

        # Step 2: prepare Docker file content
        with self.main_input.open() as f:
            dk_content = f.read()

        # Step 3: iterate on target versions to create all tags
        for t_v in target_versions:
            needs_update = t_v != default_version
            if needs_update:
                # Create branch
                self.git(["checkout", "-b", "temp"])

                # Update Docker file
                updated_content = dk_content.replace(default_version, t_v)
                with self.main_input.open("w") as f:
                    f.write(updated_content)

                # Commit
                self.git(["add", self.main_input.name])
                self.git(["commit", "-m", f"Update {self.main_input.name} for {tag}-{t_v}"])

            # Tag
            self.git(["tag", f"{tag}-{t_v}"])

            if needs_update:
                # Back to main branch
                self.git(["checkout", "main"])
                self.git(["branch", "-D", "temp"])


class DeleteBuilder(BaseReleaseBuilder):
    def build(self, tag: str, default_version: str, target_versions: List[str]):
        # Iterate on tags
        for t_v in [tag] + list(map(lambda v:f"{tag}-{v}", target_versions)):
            self.git(["tag", "-d", t_v])


class PushBuilder(BaseReleaseBuilder):
    def build(self, tag: str, default_version: str, target_versions: List[str]):
        # Iterate on tags
        for t_v in [tag] + list(map(lambda v:f"{tag}-{v}", target_versions)):
            self.git(["push", "origin", t_v])
