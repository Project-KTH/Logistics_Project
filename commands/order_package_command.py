from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.package import Package


class OrderPackageCommand:
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        self._params = params
        self._app_data = app_data

    def execute(self):
        user_id, start_location, end_location, weight = self._params
        weight = float(weight)

        user = self._app_data.find_user_by_id(user_id)

        if not user:
            return f'User {user_id} not found!'

        package = Package(start_location=start_location, end_location=end_location, weight=weight,
                          customer_info=user.contact_info)

        self._app_data.packages.append(package)

        user.ordered_packages.append(package)

        return f'Package {package.id} was ordered by user {user_id} successfully!'
