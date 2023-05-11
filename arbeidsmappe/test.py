from hello import load_inventory
import json

def test_load_inventory():
    with open('test-event.json') as f:
        event = json.loads(f.read())
        result = load_inventory(event, None)
        print(result)

if __name__ == '__main__':
    test_load_inventory()