import csv

# TODO: Refactor to take user input for input file name
FILENAME = "sp24.csv"
NAME_COL = 2
SECTION_COL = 4

 # Map section/committee -> people in section
section_map = {}

# column 2 is the "names"
# column 4 is the "sections"
with open(FILENAME, encoding="utf-8") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')

    # Skip header line
    next(csv_reader)

    # Iterate through CSV and member to sections they've listed
    for row in csv_reader:
        member_name = row[NAME_COL]
        sections = row[SECTION_COL]

        # If in multiple sections, seperate sections using comma as delimiter
        sections = sections.split(",")
        sections = [s.strip() for s in sections]

        # Add member to sections they've listed
        for s in sections:

            # ! All voice parts listed under "Voice"
            if "Voice" in s:
                s = "Voice"
            section_map[s] = section_map.get(s, set())
            section_map[s].add(member_name.title())
    

# Write to .md file
with open("output.md", "w") as output:
    for k, v in section_map.items():
            # Handle the edge cases at end
            if k == "None":
                continue

            # Heading of each section is section name
            output.write("## " + k + "\n\n")

            # Names are written in sorted order
            for name in sorted(v):
                output.write("* " + name + "\n")

            output.write("\n")
    
    # Handle any names that were not in any section at the end
    if "None" in section_map:
        k = "TO SORT MANUALLY"
        v = section_map["None"]
        # Heading of each section is section name
        output.write("## " + k + "\n\n")

        for name in sorted(v):
            output.write("* " + name + "\n")

        output.write("\n")

