# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyyaml",
# ]
# ///
import re
import yaml

def extract_aphorisms(all_aphorisms_file):
    """Extracts aphorisms from the APHORISMS_ALL.md file.

    Args:
        all_aphorisms_file (str): Path to the APHORISMS_ALL.md file.

    Returns:
        list: A list of dictionaries, where each dictionary represents an aphorism
              and contains its title, description, and references.
    """
    with open(all_aphorisms_file, 'r') as f:
        content = f.read()

    aphorisms = []
    matches = re.findall(r"### (.*?)(?:\s+\{#(.*?)\})?\n\n(.*?)(?=\n###|\Z)", content, re.DOTALL)
    for title, anchor, text in matches:
        description = text.strip()
        references_match = re.findall(r"References:\n\n(.*?)(?=\n\n|$)", description, re.DOTALL)
        references = []
        if references_match:
            references_text = references_match[0]
            for ref_line in references_text.split("\n"):
                if ref_line.strip() and ref_line.startswith("1. "):
                    parts = ref_line[3:].split(":")
                    if len(parts) == 2:  # URL and Title
                        ref_title = parts[0].strip()
                        ref_url = parts[1].strip()
                        references.append({"title": ref_title, "url": ref_url})
                    elif len(parts) > 2:  # URL, Title, and Author (assuming format "Title - Author: URL")
                        ref_title = ":".join(parts[:-1]).strip()
                        if " - " in ref_title:
                            ref_title, ref_author = ref_title.rsplit(" - ", 1)
                            ref_title = ref_title.strip()
                            ref_author = ref_author.strip()
                        else:
                            ref_author = None
                        ref_url = parts[-1].strip()
                        ref = {"title": ref_title, "url": ref_url}
                        if ref_author:
                            ref["author"] = ref_author
                        references.append(ref)
                    else:
                        print(f"Skipping malformed reference: {ref_line}")

            description = description.replace(f"References:\n\n{references_text}", "").strip()

        aphorisms.append({
            "title": title,
            "description": description,
            "references": references if references else None,
        })
    return aphorisms

def create_markdown_file(aphorism, order, output_dir):
    """Creates a markdown file for a given aphorism.

    Args:
        aphorism (dict): Dictionary containing aphorism data.
        order (int): Order of the aphorism.
        output_dir (str): Directory to save the markdown file.
    """
    title = aphorism["title"]
    file_name = f"{str(order).zfill(2)}-{title.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(',', '').replace('?', '').replace('!', '').replace(':', '').replace(';', '')}.md"
    file_path = f"{output_dir}/{file_name}"

    frontmatter = {
        "title": title,
        "order": order,
        "icon": "💡",  # Default icon
        "description": aphorism["description"],
        "references": aphorism["references"]
    }

    with open(file_path, "w") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, sort_keys=False)
        f.write("---\n\n")
        f.write(f"# {title}\n\n")
        f.write(f"{aphorism['description']}\n")

if __name__ == "__main__":
    all_aphorisms_file = "/Users/zollman/src/personal-astro/astro_academia/src/content/APHORISMS_ALL.md"
    output_directory = "aphorisms/"  # Set your desired output directory

    aphorisms_data = extract_aphorisms(all_aphorisms_file)

    for i, aphorism_data in enumerate(aphorisms_data):
        create_markdown_file(aphorism_data, i + 1, output_directory)

    print(f"Converted {len(aphorisms_data)} aphorisms to individual files in {output_directory}")

