"""Application logic for BG3 character creation; random and manual generation with validation"""

import random

from src import data_bg3
from src.models import AbilityScores, Character
from src import point_buy

# Converting dict to AbilityScores object
def build_ability_scores_from_dict(scores):
    return AbilityScores(
        STR=scores["STR"],
        DEX=scores["DEX"],
        CON=scores["CON"],
        INT=scores["INT"],
        WIS=scores["WIS"],
        CHA=scores["CHA"]
    )

# Applying +2 and +1 ability bonuses
def apply_ability_bonuses(base_scores, plus_two_ability, plus_one_ability):
    if plus_two_ability == plus_one_ability:
        raise ValueError("+2 and +1 bonuses must be applied to different abilities")

    scores = dict(base_scores)

    for ability in (plus_two_ability, plus_one_ability):
        if ability not in data_bg3.ABILITY_SCORES:
            raise ValueError(f"Unknown ability code: {ability}")

    scores[plus_two_ability] += 2
    scores[plus_one_ability] += 1

    bonuses = {
        plus_two_ability: 2,
        plus_one_ability: 1
    }

    return build_ability_scores_from_dict(scores), bonuses

# Character-creation logic

class CharacterGenerationService:
    def __init__(self, rng=None):
        self.random = rng or random.Random()

    def random_character(self, name):   # Generating a random character; skills, feats, abilities, etc.
        origin = self.random.choice(data_bg3.ORIGINS)
        race = self.random.choice(data_bg3.RACES)
        char_class = self.random.choice(data_bg3.CLASSES)

        subclasses = data_bg3.SUBCLASSES_BY_CLASS.get(char_class, ["Base"])
        subclass = self.random.choice(subclasses)

        background = self.random.choice(data_bg3.BACKGROUNDS)

        # One random feat
        feats = [self.random.choice(data_bg3.FEATS)]

        # 27-point buy
        base_scores = point_buy.random_point_buy(data_bg3.ABILITY_SCORES, rng=self.random)

        # Random +2/+1 abilities
        plus_two, plus_one = self.random.sample(data_bg3.ABILITY_SCORES, 2)
        ability_scores, ability_bonuses = apply_ability_bonuses(base_scores, plus_two, plus_one)

        # 4 random skills
        skills = self.random.sample(data_bg3.SKILLS, 4)

        return Character.create_new(
            name=name,
            origin=origin,
            race=race,
            character_class=char_class,
            subclass=subclass,
            background=background,
            ability_scores=ability_scores,
            ability_bonuses=ability_bonuses,
            skills=skills,
            feats=feats
        )


    def build_character_from_choices(
        self,
        name,
        origin,
        race,
        character_class,
        subclass,
        background,
        base_scores,
        plus_two_ability,
        plus_one_ability,
        skills,
        feats=None
    ):  # Manual creation from user choices

        # Basic validation of string choices
        if origin not in data_bg3.ORIGINS:
            raise ValueError(f"Invalid origin: {origin}")
        if race not in data_bg3.RACES:
            raise ValueError(f"Invalid race: {race}")
        if character_class not in data_bg3.CLASSES:
            raise ValueError(f"Invalid class: {character_class}")

        valid_subclasses = data_bg3.SUBCLASSES_BY_CLASS.get(character_class, [])
        if valid_subclasses and subclass not in valid_subclasses:
            raise ValueError(f"Invalid subclass {subclass!r} for class {character_class!r}")

        if background not in data_bg3.BACKGROUNDS:
            raise ValueError(f"Invalid background: {background}")

        # Validating base scores with point-buy rules
        if set(base_scores.keys()) != set(data_bg3.ABILITY_SCORES):
            raise ValueError("Base scores must include all abilities: " + ", ".join(data_bg3.ABILITY_SCORES))

        if not point_buy.is_valid_point_buy(base_scores):
            raise ValueError("Ability scores do not satisfy 27-point point-buy rules")

        # Applying +2/+1 bonuses
        ability_scores, ability_bonuses = apply_ability_bonuses(
            base_scores,
            plus_two_ability,
            plus_one_ability
        )

        # Validating skills; exactly 4 and all must be valid
        if len(skills) != 4:
            raise ValueError("You must select 4 skills")
        for skill in skills:
            if skill not in data_bg3.SKILLS:
                raise ValueError(f"Unknown skill: {skill}")

        # Validating feats
        feats = feats or []
        for feat in feats:
            if feat not in data_bg3.FEATS:
                raise ValueError(f"Unknown feat: {feat}")

        return Character.create_new(
            name=name,
            origin=origin,
            race=race,
            character_class=character_class,
            subclass=subclass,
            background=background,
            ability_scores=ability_scores,
            ability_bonuses=ability_bonuses,
            skills=skills,
            feats=feats
        )

# Returning a copy of character with new skills
    def with_new_skills(self, character, skills):
        if len(skills) != 4:
            raise ValueError("You must select 4 skills")
        for skill in skills:
            if skill not in data_bg3.SKILLS:
                raise ValueError(f"Unknown skill: {skill}")

        new_data = character.to_dict()
        new_data["skills"] = list(skills)
        return Character.from_dict(new_data)
