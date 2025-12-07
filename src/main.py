"""Text-based BG3 character creator command-line interface; menu, input and output logic."""

from src import data_bg3
from src.services import CharacterGenerationService
from src.storage_db import CharacterStorage
from src.exporters import (
    character_to_text,
    export_to_txt,
    export_to_json,
    export_to_html,
)
from src import point_buy
from src import utils


def _pause():
    input("\nPress Enter to continue...")

# Asking user to pick one item from a list by number
def _ask_choice(prompt, options):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"  [{i}] {option}")
    while True:
        raw = input("Enter number: ").strip()
        if not raw.isdigit():
            print("Please enter a number")
            continue
        idx = int(raw)
        if 1 <= idx <= len(options):
            return options[idx - 1]
        print("Invalid choice, try again")

# Yes/no question with default
def _ask_yes_no(prompt, default=False):
    suffix = " [y/n]: " if default else " [y/n]: "
    raw = input(prompt + suffix).strip().lower()
    if not raw:
        return default
    return raw.startswith("y")

# Asking user to input valid ability scores with point-buy
def _ask_ability_scores():
    print("\nEnter base ability scores (8–15). Must satisfy 27-point point-buy.")
    print("Costs: 8=0, 9=1, 10=2, 11=3, 12=4, 13=5, 14=7, 15=9")
    print("Total must equal 27.\n")

    while True:
        scores = {}
        for ability in data_bg3.ABILITY_SCORES:
            while True:
                raw = input(f"{ability}: ").strip()
                try:
                    value = int(raw)
                except ValueError:
                    print("Please enter a number")
                    continue
                scores[ability] = value
                break

        if point_buy.is_valid_point_buy(scores):
            total = point_buy.total_cost(scores)
            print(f"Point-buy cost: {total} (OK)")
            return scores

        total = point_buy.total_cost(scores)
        print(f"Point-buy cost is {total}, not 27 – this is invalid.")
        if not _ask_yes_no("Try again?", default=True):
            raise ValueError("User aborted ability score entry")

# Asking user to select 4 skills from the list
def _ask_skills():
    print("\nSelect 4 skills by number, separate them with commas")
    for i, skill in enumerate(data_bg3.SKILLS, start=1):
        print(f"  [{i}] {skill}")

    while True:
        raw = input("Your choices: ").strip()
        try:
            numbers = [int(x) for x in raw.replace(" ", "").split(",") if x]
        except ValueError:
            print("Please enter comma-separated numbers")
            continue

        if len(numbers) != 4:
            print("You must select 4 skills")
            continue

        try:
            skills = [data_bg3.SKILLS[i - 1] for i in numbers]
        except IndexError:
            print("One of those numbers is out of range")
            continue

        return skills

# Creating a random character and optionally saving to database
def create_random_character(service, storage):
    print("\n=== Create Random Character ===")
    name = input("Enter character name (default 'Tav'): ").strip() or "Tav"

    character = service.random_character(name)

    print("\n=== Generated Character ===\n")
    print(character_to_text(character))

    if _ask_yes_no("\nSave this character to database?", default=True):
        storage.save_character(character)
        print("Character saved.")

# Manual character creation from user input
def create_manual_character(service, storage):
    print("\n=== Manual Character Creation ===")
    name = input("Enter character name (default 'Tav'): ").strip() or "Tav"

    origin = _ask_choice("Choose origin:", data_bg3.ORIGINS)
    race = _ask_choice("Choose race:", data_bg3.RACES)
    character_class = _ask_choice("Choose class:", data_bg3.CLASSES)
    subclasses = data_bg3.SUBCLASSES_BY_CLASS.get(character_class, ["Base"])
    subclass = _ask_choice(f"Choose subclass for {character_class}:", subclasses)
    background = _ask_choice("Choose background:", data_bg3.BACKGROUNDS)

    try:
        base_scores = _ask_ability_scores()
    except ValueError:
        print("Cancelled manual character creation (no ability scores)")
        return

    print("\nChoose +2 ability bonus:")
    plus_two = _ask_choice("Ability for +2:", data_bg3.ABILITY_SCORES)
    print("\nChoose +1 ability bonus:")
    plus_one = _ask_choice("Ability for +1:", data_bg3.ABILITY_SCORES)

    skills = _ask_skills()

    print("\nChoose a feat:")
    feat_choice = _ask_choice("Choose feat:", data_bg3.FEATS)
    feats = [feat_choice]

    try:
        character = service.build_character_from_choices(
            name=name,
            origin=origin,
            race=race,
            character_class=character_class,
            subclass=subclass,
            background=background,
            base_scores=base_scores,
            plus_two_ability=plus_two,
            plus_one_ability=plus_one,
            skills=skills,
            feats=feats,
        )
    except ValueError as e:
        print(f"\nError: {e}")
        return

    print("\n=== Created Character ===\n")
    print(character_to_text(character))

    if _ask_yes_no("\nSave this character to database?", default=True):
        storage.save_character(character)
        print("Character saved.")

# Listing all saved characters in the database
def list_characters(storage):
    print("\n=== Saved Characters ===")
    characters = storage.load_all_characters()
    if not characters:
        print("No characters saved yet.")
        return

    for i, ch in enumerate(characters, start=1):
        print(f"[{i}] {ch.name} (ID: {ch.id})")

# User can select a character from the database by number
def _select_character_from_db(storage):
    characters = storage.load_all_characters()
    if not characters:
        print("No characters saved yet")
        return None

    print("\nSelect a character:")
    for i, ch in enumerate(characters, start=1):
        print(f"  [{i}] {ch.name} (ID: {ch.id})")

    while True:
        raw = input("Enter number (or nothing to cancel): ").strip()
        if not raw:
            return None
        if not raw.isdigit():
            print("Please enter a number")
            continue
        idx = int(raw)
        if 1 <= idx <= len(characters):
            return characters[idx - 1]
        print("Invalid index")

# Viewing a saved character from the database
def view_character(storage):
    print("\n=== View Character ===")
    ch = _select_character_from_db(storage)
    if not ch:
        print("Cancelled.")
        return

    print("\n=== Character Sheet ===\n")
    print(character_to_text(ch))

# Deleting a saved character from the database
def delete_character(storage):
    print("\n=== Delete Character ===")
    ch = _select_character_from_db(storage)
    if not ch:
        print("Cancelled")
        return

    if _ask_yes_no(f"Really delete '{ch.name}'?", default=False):
        storage.delete_character(ch.id)
        print("Character deleted")
    else:
        print("Deletion cancelled")

# Exporting a saved character to TXT, JSON, or HTML file
def export_character(storage):
    print("\n=== Export Character ===")
    ch = _select_character_from_db(storage)
    if not ch:
        print("Cancelled")
        return

    export_type = _ask_choice(
        "Choose export format:",
        ["Text (.txt)", "JSON (.json)", "HTML (.html)"],
    )

    default_name_txt = utils.default_export_filename(ch.name, "txt")
    default_name_json = utils.default_export_filename(ch.name, "json")
    default_name_html = utils.default_export_filename(ch.name, "html")

    if export_type.startswith("Text"):
        default_path = default_name_txt
        path = input(f"Enter TXT filename [{default_path}]: ").strip() or default_path
        export_to_txt(ch, path)
        print(f"Exported to {path}")
    elif export_type.startswith("JSON"):
        default_path = default_name_json
        path = input(f"Enter JSON filename [{default_path}]: ").strip() or default_path
        export_to_json(ch, path)
        print(f"Exported to {path}")
    else:
        default_path = default_name_html
        path = input(f"Enter HTML filename [{default_path}]: ").strip() or default_path
        export_to_html(ch, path)
        print(f"Exported to {path}")

# Main menu loop for the command-line interface
def main_menu():
    service = CharacterGenerationService()
    storage = CharacterStorage()

    while True:
        print("\n==============================")
        print("  BG3 Character Creator")
        print("==============================")
        print("1) Create a random character")
        print("2) Create a manual character")
        print("3) List saved characters")
        print("4) View saved character")
        print("5) Export saved character (TXT/JSON/HTML)")
        print("6) Delete saved character")
        print("7) Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_random_character(service, storage)
            _pause()
        elif choice == "2":
            create_manual_character(service, storage)
            _pause()
        elif choice == "3":
            list_characters(storage)
            _pause()
        elif choice == "4":
            view_character(storage)
            _pause()
        elif choice == "5":
            export_character(storage)
            _pause()
        elif choice == "6":
            delete_character(storage)
            _pause()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Unknown option, please try again")


if __name__ == "__main__":
    main_menu()
