import sys

def number_lines(input_stream):
    counter = 1
    for line in input_stream:
        line_content = line.rstrip('\n')
        sys.stdout.write(f"{counter}  {line_content}\n")
        counter += 1

def main():
    if len(sys.argv) > 2:
        print(f"Использование: {sys.argv[0]} [ФАЙЛ]", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r') as file:
                number_lines(file)
        except IOError as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        number_lines(sys.stdin)

if __name__ == "__main__":
    main()