import sys

from appeals import AppealsPipeline

if __name__ == "__main__":
    AppealsPipeline().run(
        max_dt=int(sys.argv[1]) if len(sys.argv) > 1 else None
    )
