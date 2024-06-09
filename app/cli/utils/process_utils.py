import sys


class ProcessManager:
    api_process = None
    cli_process = None

    @staticmethod
    def set_api_process(process):
        ProcessManager.api_process = process

    @staticmethod
    def set_cli_process(process):
        ProcessManager.cli_process = process

    @staticmethod
    def terminate_processes():
        
        # ProcessManager.cli_process.terminate()
        # ProcessManager.api_process.terminate()
        sys.exit(0)