import sys
from apply import apply_script

if __name__ == '__main__':
    print(len(sys.argv))
    print("autoApply")
    if len(sys.argv) == 1:
        apply_script()
    elif len(sys.argv) == 2 and sys.argv[1].lower() == "--questions":
        apply_script(True)
    else:
        apply_script()