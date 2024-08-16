from commands.add_user_command import AddUserCommand
from commands.assign_rout_to_truck_command import AssignRouteToTruckCommand
from commands.base_command import BaseCommand
from commands.create_manager_command import CreateManagerCommand
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.delete_package_command import DeletePackageCommand
from commands.order_package_command import OrderPackageCommand
from core.application_data import ApplicationData


import shlex

class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line):
        cmd, *params = input_line.split(maxsplit=1)

        if not params:
            raise ValueError(f'Invalid number of arguments for {cmd}. Expected more parameters.')

        params = shlex.split(params[0])

        # Creating the command based on input
        if cmd.lower() == "createpackage":
            return self.create_with_art(CreatePackageCommand(params, self._app_data), "package")
        elif cmd.lower() == "deletepackage":
            return DeletePackageCommand(params, self._app_data)
        elif cmd.lower() == "adduser":
            return self.create_with_art(AddUserCommand(params, self._app_data), "user")
        elif cmd.lower() == "assignroutetotruck":
            return self.create_with_art(AssignRouteToTruckCommand(params, self._app_data), "truck")
        elif cmd.lower() == "createmanager":
            return self.create_with_art(CreateManagerCommand(params, self._app_data), "manager")
        elif cmd.lower() == "createroute":
            return self.create_with_art(CreateRouteCommand(params, self._app_data), "route")
        elif cmd.lower() == "orderpackage":
            return OrderPackageCommand(params, self._app_data)

        raise ValueError(f'Invalid command name: {cmd}!')

    def create_with_art(self, command, art_type):
        return command, art_type
    def display_box_art(self):
        return """
         +---------+
         |         |
         | PACKAGE |
         |         |
         +---------+
         """

    def display_route_art(self):
        return """
         ~~~~~~~~~~~~~~~
         ||   ROUTE   || 
         ~~~~~~~~~~~~~~~
         """

    def display_truck_art(self):
        return """
           ______
         |      |_____
         | Truck|     |
         |______|_____|
            O     O
         """

    def display_user_art(self):
        return """
         +-------+
         | USER  |
         +-------+
         """

    def display_manager_art(self):
        return """
         +-----------+
         | MANAGER   |
         +-----------+
         """