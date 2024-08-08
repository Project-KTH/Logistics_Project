from models.location import Location



class Node:
    def __init__(self, location: str):
        self.location = location  # Ensure this is a string
        self.next = None

