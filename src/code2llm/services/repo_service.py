import subprocess
from pathlib import Path
from git import Repo


class RepomixProcessor:
    def __init__(self, repo_url: str, output_dir: str = "data"):
        self.repo_url = repo_url
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.output_dir = Path(output_dir)
        self.md_path = self.output_dir / f"{self.repo_name}.md"

    def clone_repository(self):
        """克隆 Git 仓库"""
        if not (self.output_dir / self.repo_name).exists():
            Repo.clone_from(self.repo_url, self.output_dir / self.repo_name)

    def generate_markdown(self, compress: bool = True):
        """调用 Repomix 生成 Markdown"""
        cmd = [
            "npx", "repomix",
            "--remote", self.repo_url,
            "--style", "markdown",
            "--output", str(self.md_path)
        ]
        if compress:
            cmd.append("--compress")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Repomix failed: {result.stderr}")

        return self.md_path
