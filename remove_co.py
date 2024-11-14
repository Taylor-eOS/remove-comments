from pathlib import Path

def remove_python_comments():
    filename = input("Enter PY file path: ")
    file_path = Path(filename).expanduser().resolve()
    if not file_path.is_file():
        print(f"File not found: {file_path}")
        return
    with file_path.open('r') as file:
        content = file.read()
    final_text = []
    i = 0
    inside_block_comment = False
    inside_string = False
    string_char = ''
    while i < len(content):
        if inside_block_comment:
            if content[i:i+3] == "'''":
                inside_block_comment = False
                i += 3
                continue
            i += 1
        elif content[i:i+3] == "'''":
            inside_block_comment = True
            i += 3
        elif inside_string:
            if content[i] == string_char and (i == 0 or content[i-1] != '\\'):
                inside_string = False
            final_text.append(content[i])
            i += 1
        elif content[i] in ('"', "'"):
            inside_string = True
            string_char = content[i]
            final_text.append(content[i])
            i += 1
        elif content[i] == '#':
            while i < len(content) and content[i] != '\n':
                i += 1
        else:
            final_text.append(content[i])
            i += 1
    lines = ''.join(final_text).splitlines()
    cleaned_lines = []
    prev_line_empty = False
    for i, line in enumerate(lines):
        if line.strip() == '':
            if prev_line_empty or (i + 1 < len(lines) and lines[i + 1].lstrip().startswith(('def ', 'class '))):
                cleaned_lines.append(line)
            prev_line_empty = True
        else:
            cleaned_lines.append(line)
            prev_line_empty = False
    final_output = '\n'.join(cleaned_lines)
    output_filename = f"{file_path.name}_cleaned"
    with open(file_path.parent / output_filename, 'w') as output_file:
        output_file.write(final_output)
    print(f"Saved as {output_filename}")

if __name__ == "__main__":
    remove_python_comments()
