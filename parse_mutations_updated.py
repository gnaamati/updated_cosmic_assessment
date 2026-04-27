from collections import defaultdict
import pandas as pd
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Parse a File")
    parser.add_argument("--file", required=True, help="input file")
    args = parser.parse_args()
    return args

def read_file(file):
    try:
        df = pd.read_csv(file, sep="\t")
    except FileNotFoundError:
        exit(f"ERROR: File not found: {file}")
    except Exception as e:
        exit(f"ERROR: Failed to read {file}: {e}")
    if df.empty:
        exit(f"No data rows found in file")
    
    return df

def check_columns(df):
    required = {"mutated_from_allele", "mutated_to_allele", "icgc_mutation_id", "icgc_sample_id"}
    missing = required - set(df.columns)

    if missing:
        raise SystemExit(f"Missing required columns: {missing}")
    
def get_data(mutation):
    valid_dna = {"A", "C", "G", "T"} ##Assuming DNA is uppercase
    
    mut_from    = mutation.get('mutated_from_allele')
    mut_to      = mutation.get('mutated_to_allele')
    mutation_id = mutation.get('icgc_mutation_id')
    sample_id   = mutation.get('icgc_sample_id')

    # Check for missing or empty values
    for val in (mut_from, mut_to, mutation_id, sample_id):
        if pd.isna(val) or str(val).strip() == "":
            print("Missing value in input")
            return None
    
    ##Check data looks OK 
    if mut_from not in valid_dna or mut_to not in valid_dna:
        print(f"Invalid DNA ({mut_from} -> {mut_to})")
        return None
    elif not mutation_id.startswith("MU") or not mutation_id[2:].isdigit():
        print(f"Icgc_mutation_id is not in the form of MU and a digit")
        return None
    elif not sample_id.startswith("SA") or not sample_id[2:].isdigit():
        print(f"Icgc_sample_id is not in the form of SA and a digit")
        return None
    
    return (mut_from,mut_to,mutation_id,sample_id)

def display_patterns(patterns):
    ##Go over dict and print all the patterns and their unique mutation count
    print(f"Q 2.1") 
    for allele in patterns:
        print(f"Mutated from {allele}")
        for mut_allele in patterns[allele]:
            print(f"Mutated to allele {mut_allele}: {patterns[allele][mut_allele]}") 

def print_high_low(sample_mutation_count):
    lowest     = float('inf')
    highest    = 0 
    lowest_id  =  highest_id =  ''
   
    ##Go over all the 
    for sample in sample_mutation_count:
        ##count how many unique mutations per sample_id
        count = len(sample_mutation_count[sample])
        if count < lowest:
            lowest = count
            lowest_id = sample
        if count > highest:
            highest = count
            highest_id = sample
    
    ##Print out the sample ids with the most and least mutation counts
    print(f"\nQ 2.2:")
    print(f"icgc_sample_id with highest unique icgc_mutation_id is {highest_id} with {highest} mutation count")
    print(f"icgc_sample_id with lowest unique icgc_mutation_id is {lowest_id} with {lowest} mutation count")


def parse_data(df):
    patterns = defaultdict(lambda: defaultdict(int))
    sample_mutation_count = defaultdict(lambda: defaultdict(int))
    uniq_counter = defaultdict(int)

    ##Go over each line as a dict and count relevant info
    for i, mutation in enumerate(df.to_dict("records"), start=2):
        
        ##Get relevant data and check validity - skip if not valid       
        mutation_data = get_data(mutation)
        if mutation_data is None:
            print(f"skipping line {i}")
            continue 
          
        mut_from,mut_to,mutation_id,sample_id = mutation_data
    
        ##Count mutation patterns once for each mutation_id 
        if uniq_counter[mutation_id] == 0:
            patterns[mut_from][mut_to] +=1
            uniq_counter[mutation_id] = 1

        ##Count unique mutations per sample
        sample_mutation_count[sample_id][mutation_id] += 1

    return patterns, sample_mutation_count



#=========================================#
def main():
    args = parse_args()
    
    df = read_file(args.file)
    
    check_columns(df)

    patterns, sample_mutation_count = parse_data(df)

    display_patterns(patterns)
    
    print_high_low(sample_mutation_count)    
    
if __name__ == "__main__":
    main()
