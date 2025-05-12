import random

# def generate_dna_sequence(length):
#     nucleotides = ['A', 'C', 'G', 'T']
#     return ''.join(random.choice(nucleotides) for _ in range(length))

#(shortened name, used random.choices for performance):
def make_sequence(size):
    return ''.join(random.choices("ACGT", k=size))


# insert_position = random.randint(0, len(sequence))
# final_sequence = sequence[:insert_position] + name + sequence[insert_position:]

#(moved to a separate function for modularity):
def insert_name(seq, name):
    pos = random.randint(0, len(seq))
    return seq[:pos] + name + seq[pos:]

# fasta_file.write(sequence_with_name + "\n")

#(FASTA format: split into lines of 70 characters):
def format_fasta(sequence, line_width=70):
    return '\n'.join(sequence[i:i+line_width] for i in range(0, len(sequence), line_width))


# Validation function for sequence ID (filename safety)
def validate_id(seq_id):
    return ''.join(c for c in seq_id if c.isalnum() or c in "_-")


# Stats calculation function (ignores inserted name)
def calculate_stats(sequence):
    total = len(sequence)
    stats = {base: round(sequence.count(base)/total*100, 1) for base in "ACGT"}
    cg = stats["C"] + stats["G"]
    at = stats["A"] + stats["T"]
    cg_at_ratio = round(cg / at * 100, 1) if at else 0
    return stats, cg_at_ratio


try:
    length = int(input("Enter sequence length: "))
    if length < 1:
        raise ValueError("Length must be positive.")

    seq_id = input("Enter sequence ID: ")
    desc = input("Enter description: ")
    user_name = input("Enter your name: ")

    # Generate DNA
    dna = make_sequence(length)

    # Insert name (not counted in stats)
    dna_with_name = insert_name(dna, user_name)

    # Sanitize filename
    safe_id = validate_id(seq_id)
    filename = f"{safe_id}.fasta"

    # Write to FASTA file
    with open(filename, "w") as file:
        file.write(f">{safe_id} {desc}\n")
        file.write(format_fasta(dna_with_name) + "\n")

    print(f"FASTA file saved as: {filename}")

    # Calculate statistics on raw sequence
    stats, ratio = calculate_stats(dna)

    print("Base frequencies:")
    for base, value in stats.items():
        print(f"{base}: {value}%")
    print(f"CG/AT ratio: {ratio}")

except Exception as e:
    print(f"Error: {e}")
