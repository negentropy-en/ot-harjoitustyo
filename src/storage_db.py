"""SQLite-based storage for BG3 character objects"""

import sqlite3
import json
from pathlib import Path

from src.models import Character


class CharacterStorage:
    def __init__(self, db_path="bg3_characters.db"):
        self.db_path = Path(db_path)
        self._ensure_tables()

    def _connect(self): # Opening a new SQLite connection
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):   # Creating tables if they don't exist
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS characters (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    origin TEXT,
                    race TEXT,
                    character_class TEXT,
                    subclass TEXT,
                    background TEXT,
                    ability_scores TEXT,
                    ability_bonuses TEXT,
                    skills TEXT,
                    feats TEXT
                );
                """
            )
            conn.commit()

    def save_character(self, character):    # Inserting or updating a character in the database
        data = character.to_dict()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO characters (
                    id, name, origin, race, character_class, subclass, background,
                    ability_scores, ability_bonuses, skills, feats
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["id"],
                    data["name"],
                    data["origin"],
                    data["race"],
                    data["character_class"],
                    data["subclass"],
                    data["background"],
                    json.dumps(data["ability_scores"]),
                    json.dumps(data["ability_bonuses"]),
                    json.dumps(data["skills"]),
                    json.dumps(data["feats"])
                )
            )
            conn.commit()

    def load_character(self, char_id):  # Loading a character by id
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT id, name, origin, race, character_class, subclass, background, "
                "ability_scores, ability_bonuses, skills, feats "
                "FROM characters WHERE id = ?",
                (char_id,),
            )
            row = cur.fetchone()

        if not row:
            return None

        (
            id_,
            name,
            origin,
            race,
            character_class,
            subclass,
            background,
            ability_scores_json,
            ability_bonuses_json,
            skills_json,
            feats_json,
        ) = row

        data = {
            "id": id_,
            "name": name,
            "origin": origin,
            "race": race,
            "character_class": character_class,
            "subclass": subclass,
            "background": background,
            "ability_scores": json.loads(ability_scores_json),
            "ability_bonuses": json.loads(ability_bonuses_json),
            "skills": json.loads(skills_json),
            "feats": json.loads(feats_json)
        }
        return Character.from_dict(data)

    def load_all_characters(self):  # Returning a list of all saved characters
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT id, name, origin, race, character_class, subclass, background, "
                "ability_scores, ability_bonuses, skills, feats FROM characters "
                "ORDER BY name COLLATE NOCASE"
            )
            rows = cur.fetchall()

        characters = []
        for row in rows:
            (
                id_,
                name,
                origin,
                race,
                character_class,
                subclass,
                background,
                ability_scores_json,
                ability_bonuses_json,
                skills_json,
                feats_json
            ) = row

            data = {
                "id": id_,
                "name": name,
                "origin": origin,
                "race": race,
                "character_class": character_class,
                "subclass": subclass,
                "background": background,
                "ability_scores": json.loads(ability_scores_json),
                "ability_bonuses": json.loads(ability_bonuses_json),
                "skills": json.loads(skills_json),
                "feats": json.loads(feats_json)
            }
            characters.append(Character.from_dict(data))

        return characters

    def delete_character(self, char_id):    # Deleting a character by id
        with self._connect() as conn:
            conn.execute("DELETE FROM characters WHERE id = ?", (char_id,))
            conn.commit()
