from core.application_data import ApplicationData


class ViewNotAssignedPackages:
    def __init__(self, params, app_data: ApplicationData):

        self._params = params
        self._app_data = app_data

    def execute(self):
        if len(self._params) == 0:
            not_assigned = [
                str(package) for package in self._app_data.packages if not package.route
            ]
            if not_assigned:
                weight_not_assigned = [
                    package.weight
                    for package in self._app_data.packages
                    if not package.route
                ]
                result = (
                    "\n----------------------\n".join(
                        f"   {ind}. {n}" for ind, n in enumerate(not_assigned, 1)
                    )
                    + f"\nTotal weight of not assigned packages: {sum(weight_not_assigned):_}kg."
                )
            else:
                result = "Not assigned packages not found."

            return result

        elif len(self._params) == 1:
            location_package = self._params[0].upper()
            not_assigned = [
                str(package)
                for package in self._app_data.packages
                if not package.route and str(package.start_location) == location_package
            ]
            if not_assigned:
                weight_not_assigned = [
                    package.weight
                    for package in self._app_data.packages
                    if not package.route and str(package.start_location) == location_package
                ]

                result = (
                    "\n----------------------\n".join(
                        f"   {ind}. {n}" for ind, n in enumerate(not_assigned, 1)
                    )
                    + f"\nTotal weight of not assigned packages at location {location_package}: {sum(weight_not_assigned):_}kg."
                )

            else:
                result = f"Not assigned packages not found at location: {location_package}"

            return result

        elif len(self._params) == 2:
            start_location_package = self._params[0].upper()
            end_location_package = self._params[1].upper()

            not_assigned = [
                str(package)
                for package in self._app_data.packages
                if not package.route
                and str(package.start_location) == start_location_package
                and str(package.end_location) == end_location_package
            ]
            if not_assigned:
                weight_not_assigned = [
                    package.weight
                    for package in self._app_data.packages
                    if not package.route
                    and str(package.start_location) == start_location_package
                    and str(package.end_location) == end_location_package
                ]

                result = (
                    "\n----------------------\n".join(
                        f"   {ind}. {n}" for ind, n in enumerate(not_assigned, 1)
                    )
                    + f"\nTotal weight of not assigned packages at {start_location_package} to {end_location_package}: {sum(weight_not_assigned):_}kg."
                )

            else:
                result = f"Not assigned packages from {start_location_package} to {end_location_package} not found."

            return result
        else: 
            raise ValueError(f"Invalid number of params: {len(self._params)} params found. Params should be [0:2]")