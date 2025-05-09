#!/usr/bin/env python

# python modules
import configparser
import logging
import os
from pathlib import Path
import sys
import traceback

# internal modules
from util import settings
from app_logic.PSG_controller import multiple_directory_run, single_psg_run


def read_config():
    try:
        config_path = Path(os.getcwd(), 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            # Signal names of EMG channels in EDF files to be evaluated for RSWA
            config_signals_to_evaluate = config.get('Settings', 'SIGNALS_TO_EVALUATE', fallback=None)
            if config_signals_to_evaluate:
                settings.SIGNALS_TO_EVALUATE = [x.strip() for x in config_signals_to_evaluate.split(',')]

            # Index of chin channel(s) in SIGNALS_TO_EVALUATE
            config_chin = config.get('Settings', 'CHIN', fallback=None)
            if config_chin:
                settings.CHIN = [int(x.strip()) for x in config_chin.split(',')]

            # Index of leg channel(s) in SIGNALS_TO_EVALUATE
            config_legs = config.get('Settings', 'LEGS', fallback=None)
            if config_legs:
                settings.LEGS = [int(x.strip()) for x in config_legs.split(',')]

            # Index of arm channel(s) in SIGNALS_TO_EVALUATE
            config_arms = config.get('Settings', 'ARMS', fallback=None)
            if config_arms:
                settings.ARMS = [int(x.strip()) for x in config_arms.split(',')]

            # Artifact types to be excluded from evaluation
            settings.FLOW = config.getboolean('Settings', 'FLOW', fallback=settings.FLOW)
            settings.HUMAN_ARTIFACTS = config.getboolean('Settings', 'HUMAN_ARTIFACTS',
                                                         fallback=settings.HUMAN_ARTIFACTS)
            settings.SNORE = config.getboolean('Settings', 'SNORE', fallback=settings.SNORE)

            # Use manually defined static baselines from a baseline file instead of calculating adaptive baseline levels
            settings.HUMAN_BASELINE = config.getboolean('Settings', 'HUMAN_BASELINE',
                                                        fallback=settings.HUMAN_BASELINE)
        except configparser.NoSectionError:
            logging.info("Section [Settings] not found in config file.")

    except EnvironmentError:
        logging.info('No config file found. Default settings are used.')

def run_single_psg_cmdline():
    error_messages = 'GUI error - please contact developer.'
    test_input_path = r'C:\Users\sajoz\My Drive\Work\Grants & Studies 2024-2025\RSWA normative project\Datasets\STAGES\MSMI00001'
    error_messages = single_psg_run(test_input_path)

    if not error_messages:
        logging.info(f'All PSGs of {test_input_path} were processed without errors.')
        error_messages = error_messages + f'All PSGs of {test_input_path} were processed without errors.'

#            self.processing_variable.set("")
if __name__ == "__main__":
    logging.basicConfig(
        filename='logfile.txt',
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='### %d.%m.%Y %I:%M:%S ###  '
    )
    logging.info('\n----------- START -----------')

    try:
        read_config()

        logging.info('Starting GUI')

        run_single_psg_cmdline()
        #rbd_gui = gui.Gui()
        #rbd_gui.mainloop()

    except BaseException as e:
        logging.error(f'Program terminated with unexpected error:\n {e}')
        logging.error(traceback.format_exc())
        print(f'An unexpected error occurred. Error message can be found in log file. '
              f'Please contact the developer.')
        sys.exit(1)


