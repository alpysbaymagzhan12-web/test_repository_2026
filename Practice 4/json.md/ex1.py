import json


with open('sample-data.json') as f:
    data = json.load(f)
    print("Файл бар")


print("Interface Status")
print("=" * 70)
print(f"{'DN':<50} {'Speed':<8} {'MTU':<6}")
print("-" * 70)


for item in data['imdata']:
    attr = item['l1PhysIf']['attributes']
    print(f"{attr['dn']:<50} {attr['speed']:<8} {attr['mtu']:<6}")