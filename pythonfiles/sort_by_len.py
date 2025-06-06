import sys
import shutil

# Get command line arguments
library = sys.argv[1]
min_len = int(sys.argv[2])

input_fasta = f"files/{library}_all.fasta"
good_file = f"files/{library}_len_pass.fasta"
bad_file = f"files/{library}_len_fail.fasta"

# If threshold is 0, rename the input file to the good file and create an empty bad file
if min_len == 0:
    shutil.move(input_fasta, good_file)
    open(bad_file, 'w').close()
    print(f"Renamed {input_fasta} to {good_file} and created empty {bad_file}")
    sys.exit(0)

# Sort reads based on length
with open(input_fasta, 'r') as infile, open(good_file, 'w') as good_out, open(bad_file, 'w') as bad_out:
    seq = ""
    header = ""
    
    for line in infile:
        line = line.strip()
        if line.startswith(">"):
            if seq and len(seq) >= min_len:
                good_out.write(header + "\n" + seq + "\n")
            elif seq:
                bad_out.write(header + "\n" + seq + "\n")
            header = line
            seq = ""
        else:
            seq += line
    
    # Handle last sequence
    if seq and len(seq) >= min_len:
        good_out.write(header + "\n" + seq + "\n")
    elif seq:
        bad_out.write(header + "\n" + seq + "\n")

print(f"Sequences sorted into {good_file} (pass) and {bad_file} (fail)")