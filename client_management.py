import json

def load_clients():
    """Load client data from JSON."""
    with open("data/clients.json", "r") as file:
        return json.load(file)

def save_clients(clients):
    """Save client data to JSON."""
    with open("data/clients.json", "w") as file:
        json.dump(clients, file, indent=4)

def get_next_client(clients):
    """Get the client whose policy expires soonest."""
    clients = sorted(clients, key=lambda c: c["policyEndDate"])
    for client in clients:
        if client["policyEndDate"] >= "2023-12-01":  # Replace with current date logic
            return client
    return None

def update_client_policy(client_id, new_policy_end_date):
    """Update the client's policy end date."""
    clients = load_clients()
    for client in clients:
        if client["id"] == client_id:
            client["policyEndDate"] = new_policy_end_date
            client["outstandingBalance"] = 0
            break
    save_clients(clients)
