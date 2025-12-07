"""Functions to export character data to text, JSON and HTML formats."""

from pathlib import Path
import json

# Returning a plain text representation of the character
def character_to_text(character):
    lines = []

    lines.append(f"Name: {character.name}")
    lines.append(f"Origin: {character.origin}")
    lines.append(f"Race: {character.race}")
    lines.append(f"Class: {character.character_class} ({character.subclass})")
    lines.append(f"Background: {character.background}")
    lines.append("")

    lines.append("Ability Scores:")
    ability_scores = character.ability_scores.as_dict()
    for ability, value in ability_scores.items():
        bonus = character.ability_bonuses.get(ability, 0)
        if bonus:
            lines.append(f"  {ability}: {value} (includes +{bonus})")
        else:
            lines.append(f"  {ability}: {value}")
    lines.append("")

    lines.append("Skills:")
    if character.skills:
        lines.append(f"  {', '.join(character.skills)}")
    else:
        lines.append("  None")

    lines.append("Feats:")
    if character.feats:
        lines.append(f"  {', '.join(character.feats)}")
    else:
        lines.append("  None")

    return "\n".join(lines)

# Writing a plain text character to a file
def export_to_txt(character, path):
    path = Path(path)
    path.write_text(character_to_text(character), encoding="utf-8")

# Writing character as JSON to a file
def export_to_json(character, path):
    path = Path(path)
    data = character.to_dict()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

# Returning an HTML representation of the character
def character_to_html(character):
    ab = character.ability_scores.as_dict()
    skills = ", ".join(character.skills) if character.skills else "None"
    feats = ", ".join(character.feats) if character.feats else "None"

    rows = ""
    for ability, value in ab.items():
        bonus = character.ability_bonuses.get(ability, 0)
        rows += f"<tr><td>{ability}</td><td>{value}</td><td>{bonus}</td></tr>"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>BG3 Character: {character.name}</title>
</head>
<body>
    <h1>{character.name}</h1>
    <p><strong>Origin:</strong> {character.origin}</p>
    <p><strong>Race:</strong> {character.race}</p>
    <p><strong>Class:</strong> {character.character_class} ({character.subclass})</p>
    <p><strong>Background:</strong> {character.background}</p>

    <h2>Ability Scores</h2>
    <table border="1" cellpadding="4">
        <thead>
            <tr><th>Ability</th><th>Score</th><th>Bonus</th></tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>

    <h2>Skills</h2>
    <p>{skills}</p>

    <h2>Feats</h2>
    <p>{feats}</p>
</body>
</html>
"""
    return html

# Writing character as HTML to a file
def export_to_html(character, path):
    path = Path(path)
    path.write_text(character_to_html(character), encoding="utf-8")
