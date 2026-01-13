import zipfile
import csv
import sys
import argparse

csv.field_size_limit(sys.maxsize)


def extract_species_keys(zip_path, output_file):
    species_keys = set()

    with open(output_file, "w") as out_f:
        with zipfile.ZipFile(zip_path) as z:
            with z.open("occurrence.txt") as f:
                reader = csv.DictReader(
                    (line.decode("utf-8", errors="ignore") for line in f),
                    delimiter="\t"
                )

                for row in reader:
                    sk = row.get("speciesKey")
                    if sk:
                        key = int(sk) if sk.isdigit() else str(sk)
                        if key not in species_keys:
                            print(key)
                            species_keys.add(key)
                            out_f.write(f"{key}\n")
                            out_f.flush()  # Ensure data is written to disk

    return species_keys


def main():
    parser = argparse.ArgumentParser(
        description="Extract unique species keys from a GBIF occurrence zip file."
    )
    parser.add_argument(
        "zip_path",
        nargs="?",
        default="species_zip/<country>_<specie>.zip",
        help="Path to the input zip file (default: species_zip/<country>_<specie>.zip)",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="species_zip/species_keys_<specie>.txt",
        help="Path to the output text file (default: species_zip/species_keys_<specie>.txt)",
    )
    args = parser.parse_args()

    keys = extract_species_keys(args.zip_path, args.output_file)
    print(f"Extracted {len(keys)} species keys")


if __name__ == "__main__":
    main()