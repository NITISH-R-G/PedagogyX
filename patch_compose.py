import sys
# Just clear Docker images to avoid the overlayfs bug
import subprocess

subprocess.run(["docker", "system", "prune", "-a", "-f"], check=True)
