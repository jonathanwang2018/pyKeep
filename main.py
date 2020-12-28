import os
import colorama
from colorama import Fore
import sqlite3

colorama.init()


def start():
    os.system('cls' if os.name == 'nt' else 'clear')

    user_option = input(
        Fore.WHITE +
        "Welcome to pyKeep! \nEnter 1 to create a note.\nEnter 2 to manage your notes\nChoose an option: "
    )

    def repeat():
        repeat_option = str.lower(
            input(Fore.RED + "Do you want to execute another action? (Y/N) "))

        if repeat_option == "y":
            # os.system('python "main.py"')
            start();
        else:
            pass

    def create():

        title = input("What is the name of the note you want to create? ")

        conn = sqlite3.connect([DATABASE_URL])
        c = conn.cursor()

        exist = c.execute("SELECT * FROM pyNotes WHERE title=:title", {
            "title": title
        }).fetchall()

        if len(exist) != 0:
            print("That note already exists! Pick a different name.")
            repeat()

        else:
            text = input("Start writing on your note called " + Fore.GREEN +
                         title + ": " + Fore.BLUE)

            c.execute("INSERT INTO pyNotes (title, note) VALUES (?,?)",
                      (title, text))
            conn.commit()

        conn.close()

        print(Fore.GREEN + "Note was successfully saved to pyNotes database: " +
              title + "\n")
        repeat()

    def manage():

        conn = sqlite3.connect([DATABASE_URL])
        c = conn.cursor()

        c.execute("SELECT title FROM pyNotes")
        file_list = list(c.fetchall())
        counter = 0

        for items in file_list:
            counter += 1

        if counter == 0:
            print(Fore.WHITE + "-----------------------------------")
            print(
                Fore.RED +
                "You currently have no notes stored in pyKeep. To create a note, click 1. "
            )
            print(Fore.WHITE + "-----------------------------------")
            nn = str.lower(input("Do you want to create a new note (Y/N) "))
            if nn == "y":
                create()
            else:
                exit()
        else:
            counter = 0
            pass

        print("---------------------------")
        print(Fore.GREEN + "Here are the files we found in our pyNotes database: ")
        print(Fore.WHITE + "---------------------------")

        for items in file_list:
            items = str(items)
            items = items[:-3]
            items = items[2:]
            print(counter, items)

            counter += 1

        print("----------------------------")
        number = int(input("Select a note above with its corresponding number: "))

        try:
            select_file = str(file_list[number])
            remove_chars = ['(', ')', ',', '\'']
            for i in remove_chars:
                select_file = select_file.replace(i, '')
            print("-----------------------------------------")
            file_option = str.lower(
                input("What do you want to do with " + select_file +
                      "? (view/delete): "))
        except IndexError:
            print("-----------------------------------------")
            print(Fore.RED + "That file does not exist!")
            print(Fore.WHITE + "-----------------------------------------")
            exit()
        except ValueError:
            print("-----------------------------------------")
            print(
                Fore.RED +
                "File could not be indexed. Please enter a number, not the title of the note!"
            )
            print(Fore.WHITE + "-----------------------------------------")
            exit()

        if file_option == "delete":
            print("")
            dc = str.lower(
                input(
                    Fore.RED +
                    "Deleting a file will lead to permanent deletion. \nYou can not recover this file later. This is your only chance to change your mind. \nDo you wish to delete "
                    + select_file + "? (Y/N): "))

            print(Fore.WHITE + "-----------------------------------------")

            if dc == "y":

                print(Fore.RED + "File deletion in progress...")
                print("File has been deleted.")
                print(Fore.WHITE + "")
                c.execute("DELETE FROM pyNotes WHERE title=:select_file",
                          {"select_file": select_file})
                conn.commit()

            else:
                print(Fore.GREEN + "File deletion process was cancelled.")
                print(Fore.WHITE + "-----------------------------------------")
        elif file_option == "view":
            c.execute("SELECT note FROM pyNotes WHERE title=:select_file",
                      {"select_file": select_file})
            print_this = str(list(c.fetchall()))

            print("Here are the contents of " + Fore.RED + select_file)
            print(Fore.WHITE + "-----------------------------------------")

            print_this = print_this[:-4]
            print_this = print_this[3:]
            print(Fore.GREEN + print_this)

        else:
            print("That is not a valid action")

        conn.close()
        repeat()

    if user_option == "1":
        create()
    elif user_option == "2":
        manage()
    else:
        print(Fore.RED + "That is not a valid option.")
        pass


start()
