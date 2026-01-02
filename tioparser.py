import csv

FILENAME = "sp24.csv"
NAME_COL = 2
SECTION_COL = 4

# Custom section order
SECTION_ORDER = [
    "Conductors", "Violin I", "Violin II", "Violas", "Violoncellos", "Contrabasses",
    "Flutes", "Oboes", "Clarinets", "Bass Clarinets", "Alto Saxophones",
    "Tenor Saxophones", "Baritone Saxophones", "Bassoons", "French Horns",
    "Trumpets", "Trombones", "Euphoniums", "Tuba", "Percussion", "Pianos",
    "Voice", "Acoustic Guitars", "Electric Guitars", "Electric Basses",
    "Harp", "EWI", "Tech Team", "Art Committee"
]

section_map = {}

def last_name_key(fullname: str):
    """Sort key extracting last name."""
    parts = fullname.split()
    return parts[-1].lower(), fullname.lower()

# Voice part priority
VOICE_ORDER = {
    "soprano": 1,
    "alto": 2,
    "tenor": 3,
    "bass": 4
}

def voice_sort_key(fullname: str):
    """Sort names in Voice section by voice part → last name."""
    # fullname will be like: "Alice Zhang (alto)"
    if "(" in fullname and ")" in fullname:
        part = fullname.split("(")[1].split(")")[0].lower()
    else:
        part = "zzz"  # fallback
        
    part_rank = VOICE_ORDER.get(part, 999)
    return (part_rank, last_name_key(fullname))


with open(FILENAME, encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    next(csv_reader)  # skip header

    for row in csv_reader:
        base_name = row[NAME_COL].title()
        sections = [s.strip() for s in row[SECTION_COL].split(",")]

        voice_part = None

        # Check if any section is Voice with part
        for s in sections:
            if "Voice" in s:
                # extract part: Voice - Soprano → "soprano"
                voice_part = s.split()[2].lower()

        for s in sections:

            if "Voice" in s:
                # Add voice with (part)
                display_name = f"{base_name} ({voice_part})"
                s = "Voice"
            else:
                # Non-voice sections: plain name
                display_name = base_name

            section_map.setdefault(s, set()).add(display_name)


# Determine leftover sections not in list
other_sections = sorted(
    [sec for sec in section_map.keys() if sec not in SECTION_ORDER and sec != "None"]
)

final_sections = SECTION_ORDER + other_sections


with open("output.md", "w") as output:
    for section in final_sections:

        if section not in section_map:
            continue
        if section == "None":
            continue

        # Write section header
        output.write(section + "\n\n")

        # Voice: sort by part first
        if section == "Voice":
            sorted_names = sorted(section_map[section], key=voice_sort_key)
        else:
            sorted_names = sorted(section_map[section], key=last_name_key)

        for name in sorted_names:
            output.write(name + "\n")

        output.write("\n")

    # Handle names not in any section
    if "None" in section_map:
        output.write("TO SORT MANUALLY\n\n")
        for name in sorted(section_map["None"], key=last_name_key):
            output.write(name + "\n")
        output.write("\n")
