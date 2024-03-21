import pickle

# booked_slots = {
#     # Example: "slot1": "user1"
#     "slot1": "Rohan",
# }

booked_slots = {
    "slot1": "Rohan",
    "slot11": "user",
    "slot12": "user",
    "slot13": "user",
    "slot15": "user",
    "slot30": "user",
    "slot31": "user",
    "slot16": "user",
    "slot27": "user",
    "slot17": "user",
    "slot24": "user",
    "slot25": "user",
    "slot26": "user",
    "slot21": "user",
    
    # Additional entries
    
    
    

    
    
}

# Note: The above dictionary manually adds entries for each slot number you provided.
# If you need to handle this programmatically for a larger range or different set of numbers, 
# you might want to use a loop or other logic to populate the dictionary.


with open('booked_slots.pkl', 'wb') as f:
    pickle.dump(booked_slots, f)

print("Booked slots created.")

