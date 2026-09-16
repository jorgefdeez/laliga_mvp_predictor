import json

with open("web_scraping/data_cleaning.ipynb", "r") as f:
    nb = json.load(f)

# The second cell has the mappings. We'll just keep the team mapping logic and remove the player mapping.
# It's easier to just replace the whole source of the second cell.
new_cell_2_source = [
    "_TEAM_MAP = {\n",
    "    \"FC Barcelona\": \"Barcelona\",\n",
    "    \"RCD Espanyol de Barcelona\": \"Espanyol\",\n",
    "    \"Espanyol\": \"Espanyol\",\n",
    "    \"Atlético de Madrid\": \"Atlético Madrid\",\n",
    "    \"Atletico\": \"Atlético Madrid\",\n",
    "    \"Athletic Bilbao\": \"Athletic Club\",\n",
    "    \"CA Osasuna\": \"Osasuna\",\n",
    "    \"Sevilla FC\": \"Sevilla\",\n",
    "    \"Cádiz CF\": \"Cádiz\",\n",
    "    \"Cadiz\": \"Cádiz\",\n",
    "    \"Elche CF\": \"Elche\",\n",
    "    \"Getafe CF\": \"Getafe\",\n",
    "    \"Girona FC\": \"Girona\",\n",
    "    \"Granada CF\": \"Granada\",\n",
    "    \"Levante UD\": \"Levante\",\n",
    "    \"RCD Mallorca\": \"Mallorca\",\n",
    "    \"RC Celta\": \"Celta de Vigo\",\n",
    "    \"Celta Vigo\": \"Celta de Vigo\",\n",
    "    \"UD Almería\": \"Almería\",\n",
    "    \"Almeria\": \"Almería\",\n",
    "    \"UD Las Palmas\": \"Las Palmas\",\n",
    "    \"Deportivo Alavés\": \"Alavés\",\n",
    "    \"Real Valladolid CF\": \"Valladolid\",\n",
    "    \"Real Valladolid\": \"Valladolid\",\n",
    "    \"Valencia CF\": \"Valencia\",\n",
    "    \"Villarreal CF\": \"Villarreal\",\n",
    "    \"CD Leganés\": \"Leganés\",\n",
    "    \"AD Alcorcón\": \"Alcorcón\",\n",
    "    \"CD Mirandés\": \"Mirandés\",\n",
    "    \"CD Tenerife\": \"Tenerife\",\n",
    "    \"CF Fuenlabrada\": \"Fuenlabrada\",\n",
    "    \"Málaga CF\": \"Málaga\",\n",
    "    \"SD Amorebieta\": \"Amorebieta\",\n",
    "    \"SD Eibar\": \"Eibar\",\n",
    "    \"SD Huesca\": \"Huesca\",\n",
    "    \"SD Ponferradina\": \"Ponferradina\",\n",
    "    \"UD Ibiza\": \"Ibiza\",\n",
    "    \"Real Zaragoza\": \"Zaragoza\",\n",
    "    \"R. Sociedad B\": \"Real Sociedad B\",\n",
    "}\n",
    "\n",
    "_NON_LALIGA_TEAMS = frozenset({\n",
    "    \"A Villa\",\n",
    "    \"Brighton\",\n",
    "    \"Chelsea\",\n",
    "    \"Fiorentina\",\n",
    "    \"LOSC\",\n",
    "    \"Newcastle\",\n",
    "    \"Spezia\",\n",
    "    \"Spurs\",\n",
    "    \"Udinese\",\n",
    "})\n",
    "\n",
    "def normalize_team_names(series: pd.Series) -> pd.Series:\n",
    "    result = series.astype(\"string\").str.strip()\n",
    "    return result.replace(_TEAM_MAP)\n",
    "\n",
    "def drop_non_laliga_rows(data: pd.DataFrame, team_column: str = \"team\") -> pd.DataFrame:\n",
    "    normalized_teams = normalize_team_names(data[team_column])\n",
    "    mask = ~normalized_teams.isin(_NON_LALIGA_TEAMS)\n",
    "    return data.loc[mask].copy()\n"
]

nb["cells"][1]["source"] = new_cell_2_source

# Cell 3
cell_3_source = [
    "data = pd.read_csv(PROCESSED_DIR / \"datos_combinados.csv\")\n",
    "data = data.replace(r\"^\\s*$\", np.nan, regex=True)\n",
    "data[\"player_name\"] = data[\"player_name\"].astype(\"string\").str.strip()\n",
    "data = data.dropna(subset=[\"player_name\"])\n",
    "\n",
    "for column in NUMERIC_COLUMNS:\n",
    "    data[column] = pd.to_numeric(data[column], errors=\"coerce\").fillna(0.0)\n",
    "\n",
    "for column in (\"team\", \"position\", \"season\"):\n",
    "    data[column] = data[column].astype(\"string\").fillna(\"Unknown\").replace(\"\", \"Unknown\")\n",
    "\n",
    "data[\"team\"] = normalize_team_names(data[\"team\"])\n",
    "data = drop_non_laliga_rows(data)\n"
]

nb["cells"][2]["source"] = cell_3_source

# Save it back
with open("web_scraping/data_cleaning.ipynb", "w") as f:
    json.dump(nb, f, indent=1)
