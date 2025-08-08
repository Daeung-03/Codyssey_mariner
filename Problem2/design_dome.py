def loading():
    with open("mars_base/Mars_Base_Inventory_List.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
    [print(row) for row in lines]

def main():
    loading()

if __name__ == "__main__":
    main()