ORIGINS = [
    "Custom",
    "Astarion",
    "Gale",
    "Karlach",
    "Lae'zel",
    "Shadowheart",
    "Wyll",
    "The Dark Urge"
]

RACES = [
    "Human",
    "Elf",
    "Drow",
    "Half-Elf",
    "Half-Orc",
    "Halfling",
    "Dwarf",
    "Gnome",
    "Tiefling",
    "Githyanki",
    "Dragonborn"
]

CLASSES = [
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard"
]

SUBCLASSES_BY_CLASS = {
    "Barbarian": ["Berserker", "Wildheart", "Wild Magic", "Path of Giants"],
    "Bard": ["College of Lore", "College of Valour", "College of Swords", "College of Glamour"],
    "Cleric": ["Life Domain", "Light Domain", "Trickery Domain", "War Domain", "Nature Domain", "Tempest Domain"],
    "Druid": ["Circle of the Land", "Circle of the Moon", "Circle of Spores"],
    "Fighter": ["Battle Master", "Champion", "Eldritch Knight"],
    "Monk": ["Way of the Open Hand", "Way of Shadow", "Way of the Four Elements", "Drunken Master"],
    "Paladin": ["Oath of Devotion", "Oath of the Ancients", "Oath of Vengeance", "Oathbreaker"],
    "Ranger": ["Hunter", "Beast Master", "Gloom Stalker"],
    "Rogue": ["Thief", "Assassin", "Arcane Trickster"],
    "Sorcerer": ["Draconic Bloodline", "Wild Magic", "Storm Sorcery"],
    "Warlock": ["The Fiend", "The Great Old One", "The Archfey"],
    "Wizard": ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
}

BACKGROUNDS = [
    "Acolyte",
    "Charlatan",
    "Criminal",
    "Entertainer",
    "Folk Hero",
    "Guild Artisan",
    "Haunted One",
    "Noble",
    "Outlander",
    "Sage",
    "Soldier",
    "Urchin"
]

# BG3 ability names
ABILITY_SCORES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

# Skills as per BG3 skills list
SKILLS = [
    "Athletics",         # STR
    "Acrobatics",        # DEX
    "Sleight of Hand",   # DEX
    "Stealth",           # DEX
    "Arcana",            # INT
    "History",           # INT
    "Investigation",     # INT
    "Nature",            # INT
    "Religion",          # INT
    "Animal Handling",   # WIS
    "Insight",           # WIS
    "Medicine",          # WIS
    "Perception",        # WIS
    "Survival",          # WIS
    "Deception",         # CHA
    "Intimidation",      # CHA
    "Performance",       # CHA
    "Persuasion"         # CHA
]

SKILLS_BY_ABILITY = {
    "STR": ["Athletics"],
    "DEX": ["Acrobatics", "Sleight of Hand", "Stealth"],
    "CON": [],
    "INT": ["Arcana", "History", "Investigation", "Nature", "Religion"],
    "WIS": ["Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
    "CHA": ["Deception", "Intimidation", "Performance", "Persuasion"]
}

# List of feats from BG3
FEATS = [
    "Ability Improvement", "Actor", "Alert", "Athlete",
    "Charger", "Crossbow Expert", "Defensive Duelist",
    "Dual Wielder", "Dungeon Delver", "Durable",
    "Elemental Adept", "Great Weapon Master", "Heavily Armored",
    "Heavy Armor Master", "Inspiring Leader", "Keen Mind",
    "Lightly Armored", "Linguist", "Lucky", "Mage Slayer",
    "Magic Initiate", "Martial Adept", "Medium Armor Master",
    "Mobile", "Moderately Armored", "Mounted Combatant",
    "Observant", "Polearm Master", "Resilient", "Ritual Caster",
    "Savage Attacker", "Sentinel", "Sharpshooter", "Shield Master",
    "Skilled", "Spell Sniper", "Tavern Brawler", "Tough", "War Caster",
    "Weapon Master"
]
