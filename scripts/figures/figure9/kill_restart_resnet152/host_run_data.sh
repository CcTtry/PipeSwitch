# Get current work dir
WORK_DIR=$(pwd)

# Import global variables
source $WORK_DIR/scripts/config/env.sh

PYTHONPATH=$PYTHONPATH:$WORK_DIR python scripts/figures/figure9/kill_restart_resnet152/host_run_data.py $WORK_DIR/scripts/config/servers.txt