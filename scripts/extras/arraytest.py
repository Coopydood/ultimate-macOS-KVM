
path = "/home/cooper/Documents/GitHub/ultimate-macOS-KVM/boot.sh"

print(path[0])

if path[0] == "/":
    print("TRUE")
    path = path.replace("/","",1)
print("\n-------------------------------------------")
print(path)
print("-------------------------------------------")