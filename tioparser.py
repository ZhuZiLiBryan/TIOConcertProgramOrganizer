import csv

# TODO: Refactor to take user input
FILENAME = "sp24.csv"

 # Map section/committee -> people in section
section_map = {}

# column 2 is the "names"
# column 4 is the "sections"
with open(FILENAME, encoding="utf-8") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        member_name = row[2]
        sections = row[4]

        # If in multiple sections, seperate sections using comma as delimiter
        sections = sections.split(",")
        sections = [s.strip() for s in sections]

        # Add member to sections they've listed
        for s in sections:
            if "Voice" in s:
                s = "Voice"
            section_map[s] = section_map.get(s, [])
            section_map[s].append(member_name)
    

with open("output.txt", "w") as output:
    for k, v in section_map.items():
            output.write("**" + k + "**" + ": " +  ', '.join(v))
            output.write("\n")

