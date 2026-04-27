import subprocess
import sys


def test_mini_case():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/mini.tsv"],
        capture_output=True,
        text=True
    )

    # 1. it finished without crashing
    assert result.returncode == 0    

    expected = """Q 2.1
Mutated from G
Mutated to allele A: 2
Mutated from T
Mutated to allele G: 1
Mutated from C
Mutated to allele T: 2
Mutated to allele G: 1

Q 2.2:
icgc_sample_id with highest unique icgc_mutation_id is SA514847 with 6 mutation count
icgc_sample_id with lowest unique icgc_mutation_id is SA514847 with 6 mutation count
"""

    assert result.returncode == 0
    assert result.stdout == expected


def test_run_50_lines_finishes():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/top50.tsv"],
        capture_output=True,
        text=True
    )

    # 1. it finished without crashing
    assert result.returncode == 0

    # 2. it produced output
    assert result.stdout != ""

def test_run_1_line():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/top1.tsv"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Mutated from G" in result.stdout
    assert "Mutated to allele A: 1" in result.stdout

def test_run_no_data():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/no_data.tsv"],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert "No data rows found in file" in result.stderr

def test_missing_file():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "does_not_exist.txt"],
        capture_output=True,
        text=True
    )

    # should fail
    assert result.returncode != 0

    # should show your error message
    assert "ERROR: File not found:" in result.stderr

def test_missing_column():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/bad_column.tsv"],
        capture_output=True,
        text=True
    )

     # should fail
    assert result.returncode != 0

    # should show your error message
    assert "Missing required columns: {'icgc_sample_id'}" in result.stderr

def test_bad_dna():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/bad_dna.tsv"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Invalid DNA (Z -> A)" in result.stdout
    assert "skipping line" in result.stdout

def test_bad_sample():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/bad_sample.tsv"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Icgc_sample_id is not in the form of SA and a digit" in result.stdout
    assert "skipping line" in result.stdout

def test_missing_mutation_id():
    result = subprocess.run(
        [sys.executable, "parse_mutations_updated.py", "--file", "test_files/missing_mutation.tsv"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Missing value in input" in result.stdout
    assert "skipping line" in result.stdout