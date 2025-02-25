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
