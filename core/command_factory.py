from commands.add_user_command import AddUserCommand
from commands.assign_route_to_truck_command import AssignRouteToTruckCommand
from commands.create_manager_command import CreateManagerCommand
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.delete_package_command import DeletePackageCommand
from commands.order_package_command import OrderPackageCommand
from commands.simulation_command import SimulateRouteCommand
from commands.view_all_vehicles import ViewAllVehicles
from commands.find_route_for_package import FindRouteForPackage
from commands.view_available_vehicles_for_route import ViewAvailableVehicles
from core.application_data import ApplicationData



import shlex

class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line: str):
        cmd, *params = input_line.split(maxsplit=1)

        if params:
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
        elif cmd.lower() == "viewallvehicles":
            return self.create_with_art(ViewAllVehicles(params, self._app_data), "truck")
        elif cmd.lower() == "findrouteforpackage":
            return self.create_with_art(FindRouteForPackage(params, self._app_data), "route")
        elif cmd.lower() == "viewavailablevehicles":
            return self.create_with_art(ViewAvailableVehicles(params, self._app_data), "truck")
        elif cmd.lower() == 'simulate':
            return self.create_with_art(SimulateRouteCommand(params, self._app_data), "route")
        else:
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

    def display_simulation_art(self):
        return """
           ______
         /|_||_\\__.
        (   _    _ _|
         =`(_)--(_)

         ~~~~~~~~~~~~~~~
         ||   ROUTE   || 
         ~~~~~~~~~~~~~~~
         """