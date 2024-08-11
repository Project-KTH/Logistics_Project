from commands.add_user_command import AddUserCommand
from commands.assign_rout_to_truck_command import AssignRouteToTruckCommand
from commands.base_command import BaseCommand
from commands.create_manager_command import CreateManagerCommand
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.delete_package_command import DeletePackageCommand
from commands.order_package_command import OrderPackageCommand
from core.application_data import ApplicationData




class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line):
        cmd, *params = input_line.split()

        if cmd.lower() == "createpackage":
            return CreatePackageCommand(params, self._app_data)
        elif cmd.lower() == "deletepackage":
            return DeletePackageCommand(params, self._app_data)
        elif cmd.lower() == "adduser":
            return AddUserCommand(params, self._app_data)
        elif cmd.lower() == "removeuser":
        #     return RemoveUserCommand(params, self._app_data)
        # elif cmd.lower() == "assignrole": TODO
        #     return AssignRoleCommand(params, self._app_data)
        # elif cmd.lower() == "createroute":TODO
            return CreateRouteCommand(params, self._app_data)
        elif cmd.lower() == "assignroutetotruck":
            return AssignRouteToTruckCommand(params, self._app_data)
        elif cmd.lower() == "createmanager":
            return CreateManagerCommand(params, self._app_data)
        elif cmd.lower() == "orderpackage":
            return OrderPackageCommand(params, self._app_data)

        raise ValueError(f'Invalid command name: {cmd}!')