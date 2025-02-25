Pokémon API & Database Integration System


Overview
This command-line application integrates data from the PokéAPI with a local SQLite database. Users can fetch detailed Pokémon information from the API, view stored records, search, update, or delete records—all through a user-friendly CLI.



Features

•	Fetch Pokémon Data from API:
Retrieve Pokémon details including ID, Name, Height (in m and ft), Weight (in kg and lbs), Types, Strength Level (base experience), Abilities, Battlefield weakness/strength types, and Evolutions. A Wikipedia link is provided for additional information.

•	Database Integration:
Store and manage Pokémon records in a SQLite database (pokemon.db).

•	Modular CRUD Functions:
Create, Read, Update, and Delete records with dedicated functions.


•	User-Friendly CLI:
Navigate a clear menu interface to interact with the data.



Requirements

•	Python 3.x

•	SQLite3: (Included with Python)

•	Requests Library:
Install via pip if necessary:
pip install requests


Setup

1.	Clone or Download the Repository:
Ensure you have the project files on your local machine.

2.	Install Dependencies:
If not already installed, use:
pip install requests

3.	Run the Application:
Navigate to the project directory and run:
python m_api_db_is_sql.py
(Replace m_api_db_is_sql.py with the correct filename if different.)



How to Use
When you start the application, a menu is displayed with the following options:


1.	Fetch Pokémon Data from API
   
o	Input: Pokémon name or ID (e.g., pikachu).

o	Output: Displays details in a refined format:
  
  Id: e.g., 25
  
  Name: Pikachu
  
  Height: 0.4 m (1.3 ft)
  
  Weight: 6.0 kg (13.2 lbs)
  
  Types: electric
  
  Strength Level: 112
  
  Abilities: static, lightning-rod
  
  Battlefield or Pokémon weakness against type: ground
  
  Battlefield or Pokémon strength against type: water, flying
  
  Evolutions: pichu, pikachu, raichu
  
  More info: A Wikipedia hyperlink for additional details
  
o	You will then be prompted to decide whether to store this data in the database.

3.	View All Records
Displays all Pokémon records stored in the SQLite database.

4.	Search Record by ID
Enter a Pokémon ID to view the corresponding record.

5.	Search Record by Name
Enter a Pokémon name (case-insensitive) to search for records.

6.	Update a Record
Specify the Pokémon ID, the field to update, and the new value.
Valid fields: name, height, weight, types, abilities, weaknesses, strengths, evolutions, strength_level

7.	Delete a Record
Provide a Pokémon ID to remove the record from the database.

8.	Exit
Terminates the application.



Code Structure

•	Database Initialization:

The init_db() function ensures that the SQLite database is set up with the correct schema by dropping any existing pokemon table and recreating it.

•	CRUD Functions:

o	create_record(data): 
Inserts or updates a Pokémon record.

o	read_all_records(): 
Retrieves all stored records.

o	read_record_by_id(pokemon_id): 
Retrieves a specific record by ID.

o	search_by_name(name): 
Searches for records by Pokémon name.

o	update_record(pokemon_id, field, new_value): 
Updates a field for a given record.

o	delete_record(pokemon_id): 
Deletes a record by ID.

•	API Data Parsing Functions:

o	fetch_pokemon_data(pokemon_identifier): 
Fetches Pokémon data from the PokéAPI and processes details including type damage relations and evolution chain.

o	parse_evolution_chain(chain): 
Recursively extracts the evolution chain from the API response.

•	Display Function:

o	display_fetched_data(data): 
Formats and prints the fetched Pokémon data along with a Wikipedia link.

•	CLI Menu:
The cli_menu() function loops through the available options, allowing users to interact with the database.
