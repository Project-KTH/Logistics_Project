from core.command_factory import CommandFactory
from core.command_factory import CommandFactory
from models.manager import Manager
from models.user import User


class Engine:
    def __init__(self, factory: CommandFactory):
        self._command_factory = factory
        self._role = None
        self._user = None
        self.show_logo()

    def show_logo(self):
        logo = """
         *************************************************************
         *                                                            *
         *                /$$                             /$$         *
         *               | $$                            | $$         *
         *   /$$$$$$     | $$   /$$  /$$$$$$  /$$$$$$$  /$$$$$$       *
         *  /$$__  $$    | $$  /$$/ /$$__  $$| $$__  $$|_  $$_/       *
         * | $$$$$$$$    | $$$$$$/ | $$  \\ $$| $$  \\ $$  | $$         *
         * | $$_____/    | $$_  $$ | $$  | $$| $$  | $$  | $$ /$$     *
         * |  $$$$$$$    | $$ \\  $$|  $$$$$$/| $$  | $$  |  $$$$/     *
         *  \\_______/    |__/  \\__/ \\______/ |__/  |__/   \\___/       *
         *                                                            *
         *         Efficient Delivery Management                      *
         *                                                            *
         **************************************************************
         """
        print(logo)
    def start(self):
        print("Welcome to the Logistic App Terminal!")
        print("Please register before using the app.")
        self.registration()
        self.main_menu()

    def registration(self):
        while True:
            print("\nAre you a 'Manager' or 'User'? Type 'exit' to quit.")
            role = input("Enter role: ").strip().lower()

            if role == 'manager':
                self._role = 'manager'
                name = input("Enter your name: ")
                contact_info = input("Enter your email: ")
                password = input("Create a password: ")
                self._user = Manager(name, contact_info, password, self._command_factory._app_data)
                print(f"\nManager {self._user.name} registered successfully!")
                break
            elif role == 'user':
                self._role = 'user'
                name = input("Enter your name: ")
                contact_info = input("Enter your email: ")
                password = input("Create a password: ")
                self._user = User(name, contact_info, password)
                print(f"\nUser {self._user.name} registered successfully!")
                break
            elif role == 'exit':
                print("Exiting the application. Goodbye!")
                exit()
            else:
                print("Invalid role. Please choose 'Manager' or 'User'.")

    def main_menu(self):
        print("\nType 'help' to see the list of available commands.")
        while True:
            input_line = input(f"{self._role.title()} {self._user.name}: ")
            if input_line.lower() == 'end':
                print("Exiting the application. Goodbye!")
                break
            elif input_line.lower() == 'help':
                self.show_help()
            else:
                try:
                    command, art_type = self._command_factory.create(input_line)
                    result = command.execute()
                    if art_type == "package":
                        result += f"\n{self._command_factory.display_box_art()}"
                    elif art_type == "route":
                        result += f"\n{self._command_factory.display_simulation_art()}"
                    elif art_type == "truck":
                        result += f"\n{self._command_factory.display_truck_art()}"
                    elif art_type == "user":
                        result += f"\n{self._command_factory.display_user_art()}"
                    elif art_type == "manager":
                        result += f"\n{self._command_factory.display_manager_art()}"

                    print(result)
                except ValueError as err:
                    print(f"Error: {err}")

    def show_help(self):
        if self._role == 'manager':
            print("""
    Available Commands for Manager:
        createpackage <start_location> <end_location> <weight> <customer_info> - Create a new package
        deletepackage <package_id> - Delete an existing package
        adduser <name> <email> <password> - Add a new user
        removeuser <user_id> - Remove an existing user
        createroute <locations> <departure_time> - Create a new route
        assignroutetotruck <truck_id> <route_id> - Assign a route to a truck
        createmanager <name> <contact_info> <password> - Create a new manager
        orderpackage <start_location> <end_location> <weight> - Order a new package
        trackpackage <package_id> - Track an existing package
        simulate <route_id> - Simulate the delivery of a route
                """)
        elif self._role == 'user':
            print("""
    Available Commands for User:
        orderpackage <start_location> <end_location> <weight> - Order a new package
        trackpackage <package_id> - Track an existing package
                """)