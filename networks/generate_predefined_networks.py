import json
from string import ascii_lowercase


def generate_predefined_networks(agent_sizes, n_variants=10, output_file="networks.json"):
    """
    Generate multiple networks for different agent sizes and random seeds.
    Allows for a quick lookup rather than generating at runtime.

    Parameters:
    - agent_sizes: list of agent counts to generate
    - n_variants: number of random seeds (set to ten networks)
    - output_file: name of json file containing outputs
    """

    all_networks = {}

    for size in agent_sizes:
        print(f"\nGenerating networks for N={size}")

        #build agent names
        agents = ["AG" + str(i).zfill(3) for i in range(size)]

        for i in range(n_variants):
            letter = ascii_lowercase[i]
            key = f"{size}{letter}"
            seed = i + 1

            print(f"  Doing: {key} (seed={seed})")

            net = make_network(
                agents,
                link_density=0.08,
                degree_heterogeneity=1.5,
                clustering_coef=0.25,
                random_state=seed
            )

            all_networks[key] = net

    #save to JSON
    with open(output_file, "w") as f:
        json.dump(all_networks, f)

    print(f"\nSaved to {output_file}")

generate_predefined_networks(
    agent_sizes=[50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 750, 800, 850, 900, 950, 1000],    
    n_variants=10
    )
