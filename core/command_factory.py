from commands.base_command import BaseCommand
from core.application_data import ApplicationData

class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line):
        cmd, *params = input_line.split()

        if cmd.lower() == "basecommand":
            return BaseCommand(params, self._app_data)
        
        raise ValueError(f'Invalid command name: {cmd}!')