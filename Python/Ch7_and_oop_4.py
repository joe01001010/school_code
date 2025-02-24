def main():
    correct_string = "The soccer game is a team sport played between 2 teams of 11\nplayers each, who almost exclusively use their feet to propel a\nball around a rectangular field. The objective of the game is\nto score more goals than the opposing team by moving the ball\nbeyond the goal line into a rectangular framed goal defended by\nthe opposing team. Traditionally, the game has been played over\ntwo 45 minute halves, for a total match time of 90 minutes."
    file = open("data.txt", "r")
    contents = file.read()
    file.close()
    if contents != correct_string:
        file = open("data.txt", "w")
        print("File was not correct. Writing correct string to file.")
        file.write(correct_string)
        file.close()
    else:
        print("File was already correct.")
    file.close()

if __name__ == "__main__":
    main()