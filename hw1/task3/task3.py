import sys

def get_file_stats(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            lines = data.count(b'\n')
            content = data.decode('utf-8', errors='replace')
            words = len(content.split())
            return (lines, words, len(data), filename)
    except IOError as e:
        print(f"wc: {filename}: {e.strerror}", file=sys.stderr)
        return None

def main():
    total = [0, 0, 0]
    results = [] 
    
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            stats = get_file_stats(filename)
            if stats:
                results.append(stats)
                for i in range(3):
                    total[i] += stats[i]
        
        for lines, words, bytes_count, name in results:
            print(f"{lines:7}{words:7}{bytes_count:7} {name}")
        
        if len(results) > 1:
            print(f"{total[0]:7}{total[1]:7}{total[2]:7} total")
    
    else:
        data = sys.stdin.buffer.read()
        lines = data.count(b'\n')
        content = data.decode('utf-8', errors='replace')
        words = len(content.split())
        print(f"{lines:7}{words:7}{len(data):7}")

if __name__ == "__main__":
    main()