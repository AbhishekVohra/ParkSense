import pickle

users = {
    "Aashutosh": "hey@123A",
    "Rohan": "hey@123",
    "Vaibhav": "hey@123"
    # Add more users here
}

with open('users.pkl', 'wb') as f:
    pickle.dump(users, f)

print("Users created.")
