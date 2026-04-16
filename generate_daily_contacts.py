import numpy as np

def generate_daily_contacts(full_network, mean_contacts = 8.0, std_contacts = 3, day_seed = 0):
    """
    Derive a daily contact sub-network from each agent's full neighbourhood.

    Mean somewhat derived from Mousa et al. (2021)
    -> The study analyzed daily contacts per person across different circumstances (Home, School, Work, Other) per age group
        -> Their mean landed around 12 contacts per person per day
        CONSIDERING:
            -> My study views househoulds as a singular agent, not considering inhabitants
            -> Talking about electricity usage is a uncommon conversation topic
        DECISION:
            -> mean set at 8 and std at 3 produces an actual mean close to 10 daily contacts influencing electricity usage per household (as seen in bottom check) with some heterogeneity
            -> this mean increases as N grows (because networks less bounding) but stabilizes at higher N's (from 250 onwards)
    
    Each day every agent talks to a subset of their full network.
    This algorithm guarantees:
      - Every agent has at least 1 daily contact.
      - Selection is mutual: if X picks Y, Y automatically includes X.
      - The mean number of daily contacts across agents estimates mean_contacts.
      - Variance in contact count is controlled by std_contacts.
      - Still works for small N (contact count is capped by actual degree).

    Parameters
    - full_network: dictionary containing agent_id: [list of neighbour agent_ids]}, given by the .json files
    - mean_contacts: Target mean number of daily contacts per agent 
    - std_contacts: Standard deviation of daily contact count (default 3).
    - day_seed: Seed for this day's RNG

    Returns a dictionary like the input, where agent_id = [list of daily contact agent_ids]
    """
    rng = np.random.default_rng(day_seed)
    agents = list(full_network.keys())

    #Sets for efficiency
    daily = {}
    for agent in agents:
        daily[agent] = set()

    #Shuffle agents, so no positional bias in who gets to pick first   
    #Agents processed later may already have contacts assigned to them by earlier agents (mutual picks), so they have fewer new picks
    
    shuffled_agents = rng.permutation(agents)

    for agent in shuffled_agents:
        neighbours = full_network.get(agent, [])

        #Sample a personal target, capped to the agent's actual degree
        raw_target = rng.normal(mean_contacts, std_contacts)
        target = int(np.clip(round(raw_target), 1, len(neighbours)))

        already_have = len(daily[agent])
        if already_have >= target:
            #Mutual picks from earlier agents already satisfied this one
            continue

        needed = target - already_have

        #Only consider neighbours not already in today's contact list
        available = [n for n in neighbours if n not in daily[agent]]
        if not available: #if not agents left to pick from, dont bother
            continue

        n_pick = min(needed, len(available))
        chosen = rng.choice(available, size=n_pick, replace=False)

        for contact in chosen:
            daily[agent].add(contact)   #add contact to self
            daily[contact].add(agent)   #mutual assignment

    #Extra pass to make sure all agents have at least one contact
    for agent in agents:
        if len(daily[agent]) == 0:
            neighbours = full_network.get(agent, [])
            if neighbours:
                picked = rng.choice(neighbours)
                daily[agent].add(picked)
                daily[picked].add(agent)


    result = {}
    for agent, contacts in daily.items():
        result[agent] = list(contacts)
    return result

"""
#Uncomment for a test
import json

with open("networkstil500.json", "r") as f:
    data = json.load(f)
    network = data["250d"]

net = generate_daily_contacts(network, day_seed = 80)
total = 0
for agent in net:
    total += len(net[agent])

print(f"Mean = {total/len(net)}")
print(net["AG003"])
print(net["AG039"])
"""

