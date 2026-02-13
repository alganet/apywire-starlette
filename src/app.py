# SPDX-FileCopyrightText: 2026 Alexandre Gomes Gaigalas <alganet@gmail.com>
#
# SPDX-License-Identifier: ISC

import sys
import yaml
import uvicorn
from apywire import WiringCompiler
from container import compiled


def create_app():
    return compiled.app()


if __name__ == "__main__":
    if "--compile" in sys.argv:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        with open("src/container.py", "w") as f:
            f.write(WiringCompiler(config).compile())
    elif "--migrate" in sys.argv:
        compiled.migrations().run()
    elif "--run" in sys.argv:
        uvicorn.run("app:create_app", factory=True)
    else:
        print("Usage:")
        print("  python src/app.py --migrate  - Migrate the database")
        print("  python src/app.py --compile  - Compile the container")
        print("  python src/app.py --run      - Run the application")
