import tkinter as tk
from tkinter import messagebox
import random

# Define the Token class for demo
class Token:
    def __init__(self, name, symbol, supply):
        self.name = name
        self.symbol = symbol
        self.supply = supply
        self.balances = {}

    def mint(self, address, amount):
        self.balances[address] = self.balances.get(address, 0) + amount
        self.supply += amount

    def transfer(self, sender, receiver, amount):
        if self.balances.get(sender, 0) >= amount:
            self.balances[sender] -= amount
            self.balances[receiver] = self.balances.get(receiver, 0) + amount
            return True
        return False

    def balance_of(self, address):
        return self.balances.get(address, 0)

# Define staking and rewards logic
class HazoEcosystem:
    def __init__(self, hazo_token, rav_token):
        self.hazo_token = hazo_token
        self.rav_token = rav_token
        self.stakers = {}

    def stake_hazo(self, address, amount):
        if self.hazo_token.balances.get(address, 0) >= amount:
            self.hazo_token.balances[address] -= amount
            self.stakers[address] = self.stakers.get(address, 0) + amount
            return True
        return False

    def distribute_rav_rewards(self, velocity=0.01):
        for address, staked_amount in self.stakers.items():
            reward = staked_amount * velocity
            self.rav_token.mint(address, reward)

    def simulate_block_confirmation(self):
        if self.stakers:
            random_staker = random.choice(list(self.stakers.keys()))
            self.rav_token.balances[random_staker] += 2  # Demo reward amount

# Initialize tokens
hazo = Token(name="Hazo Token", symbol="HAZO", supply=420_420_420)
rav = Token(name="Ravina Token", symbol="RAV", supply=0)
ecosystem = HazoEcosystem(hazo, rav)

# GUI functions
def update_balances():
    user1_hazo.set(f"{hazo.balance_of('user1')} HAZO")
    user2_hazo.set(f"{hazo.balance_of('user2')} HAZO")
    user1_rav.set(f"{rav.balance_of('user1')} RAV")
    user2_rav.set(f"{rav.balance_of('user2')} RAV")

def mint_tokens():
    hazo.mint("user1", 1000)
    hazo.mint("user2", 1500)
    update_balances()

def transfer_tokens():
    success = hazo.transfer("user1", "user2", 500)
    if success:
        messagebox.showinfo("Success", "Transfer successful!")
    else:
        messagebox.showerror("Error", "Insufficient balance for transfer!")
    update_balances()

def stake_tokens():
    success1 = ecosystem.stake_hazo("user1", 200)
    success2 = ecosystem.stake_hazo("user2", 300)
    if success1 and success2:
        messagebox.showinfo("Success", "Staking successful!")
    else:
        messagebox.showerror("Error", "Insufficient HAZO balance for staking!")
    update_balances()

def distribute_rewards():
    ecosystem.distribute_rav_rewards()
    update_balances()
    messagebox.showinfo("Rewards Distributed", "RAV rewards have been distributed.")

def simulate_block():
    ecosystem.simulate_block_confirmation()
    update_balances()
    messagebox.showinfo("Block Confirmed", "Block confirmation simulated with RAV rewards.")

# Initialize UI
root = tk.Tk()
root.title("Hazo Solutions Demo")
root.geometry("400x400")
root.configure(bg="white")

# Variables to display balances
user1_hazo = tk.StringVar(value="0 HAZO")
user2_hazo = tk.StringVar(value="0 HAZO")
user1_rav = tk.StringVar(value="0 RAV")
user2_rav = tk.StringVar(value="0 RAV")

# Layout
tk.Label(root, text="Hazo Solutions Demo", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

# User balances
balance_frame = tk.Frame(root, bg="white")
balance_frame.pack(pady=10)
tk.Label(balance_frame, text="User Balances", font=("Helvetica", 14, "bold"), bg="white").grid(row=0, columnspan=2)

tk.Label(balance_frame, text="User 1 HAZO:", bg="white").grid(row=1, column=0, sticky="e")
tk.Label(balance_frame, textvariable=user1_hazo, bg="white").grid(row=1, column=1, sticky="w")

tk.Label(balance_frame, text="User 2 HAZO:", bg="white").grid(row=2, column=0, sticky="e")
tk.Label(balance_frame, textvariable=user2_hazo, bg="white").grid(row=2, column=1, sticky="w")

tk.Label(balance_frame, text="User 1 RAV:", bg="white").grid(row=3, column=0, sticky="e")
tk.Label(balance_frame, textvariable=user1_rav, bg="white").grid(row=3, column=1, sticky="w")

tk.Label(balance_frame, text="User 2 RAV:", bg="white").grid(row=4, column=0, sticky="e")
tk.Label(balance_frame, textvariable=user2_rav, bg="white").grid(row=4, column=1, sticky="w")

# Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

tk.Button(button_frame, text="Mint Tokens", command=mint_tokens, font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Transfer HAZO", command=transfer_tokens, font=("Helvetica", 12)).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Stake HAZO", command=stake_tokens, font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Distribute RAV Rewards", command=distribute_rewards, font=("Helvetica", 12)).grid(row=1, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Simulate Block", command=simulate_block, font=("Helvetica", 12)).grid(row=2, columnspan=2, pady=10)

# Start UI loop
update_balances()
root.mainloop()
