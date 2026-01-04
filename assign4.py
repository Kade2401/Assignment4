class Event:
    def __init__(self, name, date, capacity):
        self.name = name
        self.date = date
        self.capacity = capacity
        self.attendees = []

    def edit_event(self, new_name=None, new_date=None, new_capacity=None):
        if new_name:
            self.name = new_name
        if new_date:
            self.date = new_date
        if new_capacity:
            if new_capacity < len(self.attendees):
                print("Cannot reduce capacity below current number of attendees!")
            else:
                self.capacity = new_capacity

    def add_attendee(self, user):
        if len(self.attendees) >= self.capacity:
            print(f"Cannot add {user}. Event is full!")
        elif user in self.attendees:
            print(f"{user} is already registered.")
        else:
            self.attendees.append(user)
            print(f"{user} successfully registered for {self.name}.")

    def remove_attendee(self, user):
        if user in self.attendees:
            self.attendees.remove(user)
            print(f"{user} removed from {self.name}.")
        else:
            print(f"{user} is not registered for this event.")

    def show_info(self):
        print(f"\nEvent: {self.name}")
        print(f"Date: {self.date}")
        print(f"Capacity: {self.capacity}")
        print(f"Registered attendees ({len(self.attendees)}): {', '.join(self.attendees)}\n")

events = []

def create_event():
    name = input("Event name: ")
    date = input("Event date (YYYY-MM-DD): ")
    capacity = int(input("Event capacity: "))
    event = Event(name, date, capacity)
    events.append(event)
    print(f"Event '{name}' created successfully!")

def edit_event():
    if not list_events(): 
        return
    try:
        idx = int(input("Select event number to edit: ")) - 1
        if 0 <= idx < len(events):
            event = events[idx]
            print("\nCurrent event details:")
            event.show_info()
            
            new_name = input("New name (leave blank to keep current): ")
            new_date = input("New date (leave blank to keep current): ")
            new_capacity_input = input("New capacity (leave blank to keep current): ")
            new_capacity = int(new_capacity_input) if new_capacity_input else None
            
            event.edit_event(new_name or None, new_date or None, new_capacity)
            print("Event updated!")
        else:
            print("Invalid event number.")
    except ValueError:
        print("Please enter a valid number.")


def list_events():
    if not events:
        print("No events available.")
        return False
    print("\nAvailable events:")
    for i, event in enumerate(events, start=1):
        print(f"{i}. {event.name}")
    return True

def show_event_details():
    if not list_events():
        return
    try:
        idx = int(input("Select event number to view details: ")) - 1
        if 0 <= idx < len(events):
            events[idx].show_info()
        else:
            print("Invalid event number.")
    except ValueError:
        print("Please enter a valid number.")

def register_user():
    if not list_events():
        return
    try:
        idx = int(input("Select event number to register: ")) - 1
        if 0 <= idx < len(events):
            event = events[idx]
            if len(event.attendees) >= event.capacity:
                print(f"Cannot register. Event '{event.name}' is already full!")
                return
            user = input("Enter your name: ")
            event.add_attendee(user)
        else:
            print("Invalid event number.")
    except ValueError:
        print("Please enter a valid number.")

def show_attendees(event):
    if not event.attendees:
        print("No attendees registered for this event.")
    else:
        print("\nRegistered attendees:")
        for i, user in enumerate(event.attendees, start=1):
            print(f"{i}. {user}")

def remove_user():
    if not list_events():
        return
    try:
        idx = int(input("Select event number to remove attendee from: ")) - 1
        if 0 <= idx < len(events):
            event = events[idx]
            show_attendees(event)
            user_name = input("Enter the name of attendee to remove: ")
            event.remove_attendee(user_name)
        else:
            print("Invalid event number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    while True:
        print("\n--- Event Management System ---")
        print("1. Create Event")
        print("2. Edit Event")
        print("3. Register User")
        print("4. Remove User")
        print("5. Show Event Info")
        print("6. Exit")

        choice = input("Select an option: ")
        if choice == '1':
            create_event()
        elif choice == '2':
            edit_event()
        elif choice == '3':
            register_user()
        elif choice == '4':
            remove_user()
        elif choice == '5':
            show_event_details()
        elif choice == '6':
            print("Exiting system.")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()