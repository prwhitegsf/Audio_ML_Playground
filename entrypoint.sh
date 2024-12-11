#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# Enable strict mode.
#set -euo pipefail
# ... Run whatever commands ...

# Temporarily disable strict mode and activate conda:
#set +euo pipefail
conda activate ./ml_env

# Re-enable strict mode:
#set -euo pipefail

# exec the final command:
exec gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:app