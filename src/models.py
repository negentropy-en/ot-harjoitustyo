from dataclasses import dataclass, asdict, field
from uuid import uuid4  # For generating unique IDs for characters


@dataclass
class AbilityScores:    # Ability scores for a character
    STR: int
    DEX: int
    CON: int
    INT: int
    WIS: int
    CHA: int

    def as_dict(self):  # Converting ability scores to a dictionary
        return asdict(self)


@dataclass
class Character:    # A BG3 character with all relevant data
    id: str
    name: str
    origin: str
    race: str
    character_class: str
    subclass: str
    background: str
    ability_scores: AbilityScores
    ability_bonuses: dict = field(default_factory=dict)
    skills: list = field(default_factory=list)
    feats: list = field(default_factory=list)

    @classmethod
    def create_new(
        cls,
        name,
        origin,
        race,
        character_class,
        subclass,
        background,
        ability_scores,
        ability_bonuses,
        skills,
        feats=None,
    ):
        # Creating a new character with new UUID; unique identifier
        return cls(
            id=str(uuid4()),
            name=name,
            origin=origin,
            race=race,
            character_class=character_class,
            subclass=subclass,
            background=background,
            ability_scores=ability_scores,
            ability_bonuses=ability_bonuses,
            skills=list(skills),
            feats=list(feats) if feats else [],
        )

    def to_dict(self):
        # Turning this character into a plain dict for JSON / DB
        return {
            "id": self.id,
            "name": self.name,
            "origin": self.origin,
            "race": self.race,
            "character_class": self.character_class,
            "subclass": self.subclass,
            "background": self.background,
            "ability_scores": self.ability_scores.as_dict(),
            "ability_bonuses": dict(self.ability_bonuses),
            "skills": list(self.skills),
            "feats": list(self.feats),
        }

    @classmethod
    def from_dict(cls, data):
        # Creating a character from a dict for JSON / DB
        ability_scores = AbilityScores(**data["ability_scores"])
        return cls(
            id=data["id"],
            name=data["name"],
            origin=data["origin"],
            race=data["race"],
            character_class=data["character_class"],
            subclass=data["subclass"],
            background=data["background"],
            ability_scores=ability_scores,
            ability_bonuses=data.get("ability_bonuses", {}),
            skills=data.get("skills", []),
            feats=data.get("feats", []),
        )
