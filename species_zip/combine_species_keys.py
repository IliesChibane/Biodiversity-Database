import glob

def combine_species_keys():
    # Find all species_keys txt files
    txt_files = glob.glob("species_zip/species_keys_*.txt")
    
    # Use a set to automatically handle duplicates
    all_species_keys = set()
    
    # Read each file and add keys to the set
    for txt_file in txt_files:
        print(f"Reading {txt_file}...")
        with open(txt_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    all_species_keys.add(line)
    
    # Sort the keys for consistent output
    sorted_keys = sorted(all_species_keys, key=lambda x: int(x) if x.isdigit() else 0)
    
    # Write to combined file
    output_file = "species_zip/whitelist.txt"
    with open(output_file, "w") as f:
        for key in sorted_keys:
            f.write(f"{key}\n")
    
    print(f"\nCombined {len(all_species_keys)} unique species keys from {len(txt_files)} files")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    combine_species_keys()
