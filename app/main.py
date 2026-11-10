
import argparse
import logging
import shutil
from pathlib import Path

# Create logs directory relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def check_disk_space(path="/"):
    """Return disk usage information for the given path."""
    total, used, free = shutil.disk_usage(path)

    usage_percent = (used / total) * 100 if total else 0

    result = {
        "path": path,
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "usage_percent": round(usage_percent, 2),
    }

    logging.info("Disk check completed for %s", path)
    return result


def is_disk_usage_critical(usage_percent, threshold=90):
    """Check whether disk usage has reached the configured threshold."""
    return usage_percent >= threshold


def main(threshold=90):
    print("=== Py_devops System Health Checker ===")
    print(f"Warning threshold: {threshold}%")

    disk = check_disk_space()

    print(f"Disk path: {disk['path']}")
    print(f"Total space: {disk['total_gb']} GB")
    print(f"Used space: {disk['used_gb']} GB")
    print(f"Free space: {disk['free_gb']} GB")
    print(f"Disk usage: {disk['usage_percent']}%")

    if is_disk_usage_critical(disk["usage_percent"], threshold):
        print("WARNING: Disk usage is critically high!")
        logging.warning("Disk usage is critically high")
    else:
        print("Disk status: OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Py_devops System Health Checker"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=90,
        help="Disk usage warning threshold (0-100, default: 90)",
    )

    args = parser.parse_args()

    if not 0 <= args.threshold <= 100:
        parser.error("Threshold must be between 0 and 100")

    main(args.threshold)

