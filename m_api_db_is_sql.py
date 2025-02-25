import sqlite3
import requests

# Database file constant
DB_FILE = "pokemon.db"


def init_db():
    """
    Initialize the SQLite database.
    WARNING: This will drop any existing 'pokemon' table to ensure the correct schema.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Drop the table if it exists to avoid schema mismatch issues
    cursor.execute("DROP TABLE IF EXISTS pokemon")
    create_table_query = """
    CREATE TABLE pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        height REAL,
        weight REAL,
        types TEXT,
        abilities TEXT,
        weaknesses TEXT,
        strengths TEXT,
        evolutions TEXT,
        strength_level INTEGER
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


# Modular CRUD Functions
def create_record(data):
    """Insert or update Pokémon data into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    insert_query = """
    INSERT OR REPLACE INTO pokemon 
    (id, name, height, weight, types, abilities, weaknesses, strengths, evolutions, strength_level)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (
        data.get("id"),
        data.get("name"),
        data.get("height"),
        data.get("weight"),
        data.get("types"),
        data.get("abilities"),
        data.get("weaknesses"),
        data.get("strengths"),
        data.get("evolutions"),
        data.get("strength_level")
    ))
    conn.commit()
    conn.close()
    print(f"\nRecord for {data.get('name').capitalize()} (ID: {data.get('id')}) added/updated successfully.\n")


def read_all_records():
    """Retrieve and return all Pokémon records from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon")
    records = cursor.fetchall()
    conn.close()
    return records


def read_record_by_id(pokemon_id):
    """Retrieve a Pokémon record by its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,))
    record = cursor.fetchone()
    conn.close()
    return record


def search_by_name(name):
    """Search for Pokémon records by name (case-insensitive)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon WHERE LOWER(name) = LOWER(?)", (name,))
    records = cursor.fetchall()
    conn.close()
    return records


def update_record(pokemon_id, field, new_value):
    """Update a specific field of a Pokémon record identified by its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = f"UPDATE pokemon SET {field} = ? WHERE id = ?"
    cursor.execute(query, (new_value, pokemon_id))
    conn.commit()
    conn.close()
    print(f"\nRecord with ID {pokemon_id} updated: set {field} to {new_value}.\n")


def delete_record(pokemon_id):
    """Delete a Pokémon record from the database based on its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pokemon WHERE id = ?", (pokemon_id,))
    conn.commit()
    conn.close()
    print(f"\nRecord with ID {pokemon_id} deleted successfully.\n")


# API Data Parsing Functions
def parse_evolution_chain(chain):
    """
    Recursively parse the evolution chain and return a list of Pokémon names.
    The evolution chain is nested within the API response.
    """
    evolutions = []
    if chain:
        species_name = chain.get("species", {}).get("name")
        if species_name:
            evolutions.append(species_name)
        evolves_to = chain.get("evolves_to", [])
        for evo in evolves_to:
            evolutions.extend(parse_evolution_chain(evo))
    return evolutions


def fetch_pokemon_data(pokemon_identifier):
    """
    Fetch Pokémon data from the PokéAPI using the Pokémon name or ID.
    Retrieves basic info, type damage relations (for battlefield strengths and weaknesses),
    and evolution chain details.
    """
    base_url = "https://pokeapi.co/api/v2/"
    pokemon_url = f"{base_url}pokemon/{pokemon_identifier}"

    try:
        response = requests.get(pokemon_url)
        if response.status_code != 200:
            print(f"Error: Pokémon '{pokemon_identifier}' not found or API error.")
            return None
        data = response.json()
    except Exception as e:
        print("Error fetching data from PokéAPI:", e)
        return None

    # Basic Pokémon info
    poke_id = data.get("id")
    name = data.get("name")
    # Convert height (decimetres to metres) and weight (hectograms to kilograms)
    height_m = data.get("height") / 10.0
    weight_kg = data.get("weight") / 10.0
    # Calculate imperial conversions
    height_ft = round(height_m * 3.28084, 1)
    weight_lbs = round(weight_kg * 2.20462, 1)

    # Types
    types_list = [t["type"]["name"] for t in data.get("types", [])]
    types_str = ", ".join(types_list)

    # Abilities
    abilities_list = [a["ability"]["name"] for a in data.get("abilities", [])]
    abilities_str = ", ".join(abilities_list)

    # Use base_experience as the "strength level"
    strength_level = data.get("base_experience")

    # Initialize sets for weaknesses and strengths (battlefield match-ups)
    weaknesses_set = set()
    strengths_set = set()

    # For each type, fetch damage relations to determine advantages/disadvantages
    for t in data.get("types", []):
        type_url = t["type"]["url"]
        try:
            type_response = requests.get(type_url)
            if type_response.status_code == 200:
                type_data = type_response.json()
                damage_relations = type_data.get("damage_relations", {})
                # Weaknesses: types that deal double damage to this type
                weaknesses = [d["name"] for d in damage_relations.get("double_damage_from", [])]
                # Strengths: types that this type deals double damage to
                strengths = [d["name"] for d in damage_relations.get("double_damage_to", [])]
                weaknesses_set.update(weaknesses)
                strengths_set.update(strengths)
            else:
                print(f"Failed to fetch type data for {t['type']['name']}")
        except Exception as e:
            print(f"Error fetching type data: {e}")

    weaknesses_str = ", ".join(weaknesses_set) if weaknesses_set else "None"
    strengths_str = ", ".join(strengths_set) if strengths_set else "None"

    # Fetch evolution chain from the species endpoint
    species_url = f"{base_url}pokemon-species/{pokemon_identifier}"
    evolutions_str = "N/A"
    try:
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            species_data = species_response.json()
            evolution_chain_url = species_data.get("evolution_chain", {}).get("url")
            if evolution_chain_url:
                evo_response = requests.get(evolution_chain_url)
                if evo_response.status_code == 200:
                    evo_data = evo_response.json()
                    chain = evo_data.get("chain")
                    evolution_list = parse_evolution_chain(chain)
                    evolutions_str = ", ".join(evolution_list)
        else:
            evolutions_str = "N/A"
    except Exception as e:
        print("Error fetching evolution chain:", e)
        evolutions_str = "N/A"

    # Compile all data into a dictionary
    pokemon_data = {
        "id": poke_id,
        "name": name,
        "height": height_m,  # in metres
        "weight": weight_kg,  # in kilograms
        "types": types_str,
        "abilities": abilities_str,
        "weaknesses": weaknesses_str,
        "strengths": strengths_str,
        "evolutions": evolutions_str,
        "strength_level": strength_level,
        "height_ft": height_ft,
        "weight_lbs": weight_lbs
    }

    return pokemon_data


def display_fetched_data(data):
    """Display the fetched Pokémon data in a refined, elaborate format."""
    if not data:
        print("No data to display.")
        return

    print("\nFetched Pokémon Data:")
    print(f"Id: {data.get('id')}")
    print(f"Name: {data.get('name').capitalize()}")
    print(f"Height: {data.get('height')} m ({data.get('height_ft')} ft)")
    print(f"Weight: {data.get('weight')} kg ({data.get('weight_lbs')} lbs)")
    print(f"Types: {data.get('types')}")
    print(f"Strength Level: {data.get('strength_level')}")
    print(f"Abilities: {data.get('abilities')}")
    print(f"Battlefield or Pokémon weakness against type: {data.get('weaknesses')}")
    print(f"Battlefield or Pokémon strength against type: {data.get('strengths')}")
    print(f"Evolutions: {data.get('evolutions')}")
    # Provide a Wikipedia link based on the Pokémon name
    wiki_link = f"https://en.wikipedia.org/wiki/{data.get('name').capitalize()}"
    print(f"More info please go to wiki link: {wiki_link}\n")


# CLI
def cli_menu():
    """
    Command-line interface for interacting with the Pokémon database.
    Options include:
      1. Fetch Pokémon Data from API
      2. View All Records
      3. Search Record by ID
      4. Search Record by Name
      5. Update a Record
      6. Delete a Record
      7. Exit
    """
    init_db()  # Ensuring the database is set up with the correct schema
    while True:
        print("\n--- Pokémon Database CLI ---")
        print("1. Fetch Pokémon Data from API")
        print("2. View All Records")
        print("3. Search Record by ID")
        print("4. Search Record by Name")
        print("5. Update a Record")
        print("6. Delete a Record")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            identifier = input("Enter Pokémon name or ID to fetch: ").strip().lower()
            pokemon_data = fetch_pokemon_data(identifier)
            if pokemon_data:
                display_fetched_data(pokemon_data)
                store_choice = input("Do you want to store this data in the database? (y/n): ").strip().lower()
                if store_choice == "y":
                    create_record(pokemon_data)
        elif choice == "2":
            records = read_all_records()
            if records:
                for record in records:
                    print("\n--- Record ---")
                    print(f"Id: {record[0]}")
                    print(f"Name: {record[1].capitalize()}")
                    print(f"Height: {record[2]} m")
                    print(f"Weight: {record[3]} kg")
                    print(f"Types: {record[4]}")
                    print(f"Abilities: {record[5]}")
                    print(f"Battlefield or Pokémon weakness against type: {record[6]}")
                    print(f"Battlefield or Pokémon strength against type: {record[7]}")
                    print(f"Evolutions: {record[8]}")
                    print(f"Strength Level: {record[9]}")
                print("")
            else:
                print("No records found.")
        elif choice == "3":
            try:
                search_id = int(input("Enter Pokémon ID to search: "))
                record = read_record_by_id(search_id)
                if record:
                    print("\n--- Record Found ---")
                    print(f"Id: {record[0]}")
                    print(f"Name: {record[1].capitalize()}")
                    print(f"Height: {record[2]} m")
                    print(f"Weight: {record[3]} kg")
                    print(f"Types: {record[4]}")
                    print(f"Abilities: {record[5]}")
                    print(f"Battlefield or Pokémon weakness against type: {record[6]}")
                    print(f"Battlefield or Pokémon strength against type: {record[7]}")
                    print(f"Evolutions: {record[8]}")
                    print(f"Strength Level: {record[9]}\n")
                else:
                    print("Record not found.")
            except ValueError:
                print("Invalid input. Please enter a numeric ID.")
        elif choice == "4":
            name = input("Enter Pokémon name to search: ").strip().lower()
            records = search_by_name(name)
            if records:
                for record in records:
                    print("\n--- Record Found ---")
                    print(f"Id: {record[0]}")
                    print(f"Name: {record[1].capitalize()}")
                    print(f"Height: {record[2]} m")
                    print(f"Weight: {record[3]} kg")
                    print(f"Types: {record[4]}")
                    print(f"Abilities: {record[5]}")
                    print(f"Battlefield or Pokémon weakness against type: {record[6]}")
                    print(f"Battlefield or Pokémon strength against type: {record[7]}")
                    print(f"Evolutions: {record[8]}")
                    print(f"Strength Level: {record[9]}\n")
            else:
                print(f"No records found for Pokémon name '{name}'.")
        elif choice == "5":
            try:
                update_id = int(input("Enter Pokémon ID to update: "))
                field = input(
                    "Enter the field to update (name, height, weight, types, abilities, weaknesses, strengths, evolutions, strength_level): ").strip().lower()
                new_value = input("Enter the new value: ").strip()
                update_record(update_id, field, new_value)
            except ValueError:
                print("Invalid input. Please try again.")
        elif choice == "6":
            try:
                delete_id = int(input("Enter Pokémon ID to delete: "))
                delete_record(delete_id)
            except ValueError:
                print("Invalid input. Please enter a numeric ID.")
        elif choice == "7":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    cli_menu()
