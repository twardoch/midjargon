"""
Constants for Midjourney engine.
"""

# Parameter ranges and constraints
STYLIZE_RANGE = (0, 1000)
CHAOS_RANGE = (0, 100)
WEIRD_RANGE = (0, 3000)
IMAGE_WEIGHT_RANGE = (0.0, 3.0)
SEED_RANGE = (0, 4294967295)
STOP_RANGE = (10, 100)

# New parameter ranges (lenient)
QUALITY_RANGE = (0.1, 2.0)  # More lenient than spec
CHARACTER_WEIGHT_RANGE = (0, 200)  # More lenient than spec
STYLE_WEIGHT_RANGE = (0, 2000)  # More lenient than spec
STYLE_VERSION_RANGE = (1, 10)  # More lenient than spec
REPEAT_RANGE = (1, 100)  # More lenient than spec

# File extensions
ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

# Mode flags
VALID_STYLES = {"raw", "expressive", "cute", "scenic", "original"}  # Extensible
VALID_VERSIONS = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "5.0",
    "5.1",
    "5.2",
    "6",
    "6.1",
}  # Extensible
VALID_NIJI_VERSIONS = {"4", "5", "6"}  # Extensible
