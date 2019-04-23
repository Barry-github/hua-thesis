from tools.utils import start_experiments,print_data_generation
from loguru import logger
import sys
logger.add("logs/log{time:MM-DD_HH:mm}.log", format="{time:DD-MM-YY at hh:mm:s} <level>{message}</level>")
start_experiments(real_data=False)
