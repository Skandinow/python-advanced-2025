import sys

def print_tail(filename, lines_count, print_header=False):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except IOError as e:
        print(f"tail: cannot open '{filename}' for reading: {e.strerror}", file=sys.stderr)
        return
    
    tail = lines[-lines_count:] if len(lines) >= lines_count else lines
    
    if print_header:
        print(f"==> {filename} <==")
    sys.stdout.write("".join(tail))

def process_stdin():
    lines = sys.stdin.readlines()      
    tail = lines[-17:] if len(lines) >= 17 else lines
    sys.stdout.write("".join(tail))

def main():
    if len(sys.argv) == 1:
        process_stdin()
        return
    
    filenames = sys.argv[1:]
    multiple_files = len(filenames) > 1
    
    for filename in filenames:
        print_tail(
            filename, 
            lines_count=10, 
            print_header=multiple_files
        )

if __name__ == "__main__":
    main()