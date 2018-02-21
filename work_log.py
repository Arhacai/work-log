import csv
import task
import task_search
import utils


class WorkLog():
    """WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them aswell several ways to search through the tasks. It reads and
    save all information in a csv file.
    """
    TASKS = []

    def __init__(self, file):
        """Initialize the app by reading the csv file and adding all task to a
        list. If there is no file, the app runs and creates it when the user
        save an entry. When imported, the tasks are sorted by date in the list.
        """
        logs = []
        try:
            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    logs.append(row)
        except FileNotFoundError:
            logs = []
        else:
            for log in logs:
                self.TASKS.append(task.Task(log))
                self.sort_tasks()

    def sort_tasks(self):
        """Takes the list of tasks imported from csv file and sort them by
        date, from the oldest to the newest one.
        """
        for i in range(1, len(self.TASKS)):
            j = i-1
            key = self.TASKS[i]
            while (self.TASKS[j].date > key.date) and (j >= 0):
                self.TASKS[j+1] = self.TASKS[j]
                j -= 1
            self.TASKS[j+1] = key

    def show_tasks(self, tasks):
        """Takes a list of tasks and shows them on screen one at a time. It
        also displays a set of options to page through tasks, edit and remove
        them.
        """
        index = 0

        while True:
            # If all taks are deleted a message is prompt to advice us.
            if len(tasks) == 0:
                utils.clear_screen()
                print("There are no more tasks to show.\n")
                input("Press enter to return to search menu.")
                break
            else:
                tasks[index].show_task()
                print("\nResult {} of {}\n".format(index+1, len(tasks)))

                # Menu displayed if only one task is found.
                if index == 0 and len(tasks) == 1:
                    print("[E]dit, [D]elete, [R]eturn to search menu")
                    option = input("\n> ")
                    if option.upper() == 'E':
                        tasks[index] = self.edit_task(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index = 0
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

                # Menu displayed to the first task if there is more than one.
                elif index == 0:
                    print("""
[N]ext, [E]dit, [D]elete, [R]eturn to search menu""")
                    option = input("\n> ")
                    if option.upper() == 'N':
                        index += 1
                    elif option.upper() == 'E':
                        tasks[index] = self.edit_task(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index = 0
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

                # Menu displayed to any task but the first and last one.
                elif index > 0 and index < len(tasks)-1:
                    print("""
[P]revious, [N]ext, [E]dit, [D]elete, [R]eturn to search menu""")
                    option = input("\n> ")
                    if option.upper() == 'P':
                        index -= 1
                    elif option.upper() == 'N':
                        index += 1
                    elif option.upper() == 'E':
                        tasks[index] = self.edit_task(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index -= 1
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

                # Menu displayed for the last tasks if there are more than one.
                elif index == len(tasks)-1:
                    print("""
[P]revious, [E]dit, [D]elete, [R]eturn to search menu""")
                    option = input("\n> ")
                    if option.upper() == 'P':
                        index -= 1
                    elif option.upper() == 'E':
                        tasks[index] = self.edit_task(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index -= 1
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

    def edit_task(self, entry):
        """Edit a task by creating one new and overriding its attributed when
        needed. It replaces the original task and then the tasks are saved
        to file. It returns the task to being able to see it on screen.
        """
        new_task = task.Task.edit_task(entry)
        self.TASKS[self.TASKS.index(entry)] = new_task
        self.save_file('log.csv')
        return new_task

    def delete_task(self, entry):
        """Let the user to delete an entry. User must confirm this action
        because it can't be undone. Once the entry is deleted, the file is
        saved with the changes made.
        """
        answer = input("\n Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            del self.TASKS[self.TASKS.index(entry)]
            self.save_file('log.csv')
            return True
        else:
            return False

    def save_file(self, file):
        """Saves the file in a csvfile."""
        with open(file, 'w') as csvfile:
            fieldnames = ["Date", "Title", "Time", "Notes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.TASKS:
                writer.writerow(entry.log)

    def add_entry(self):
        """Let the user to create and save a new task. Once is created, the
        file is saved and the user is prompted with the new task to review
        its content. The tasks are sorted before being saved to file to keep
        them ordered.
        """
        entry = task.Task.create_new_task()
        self.TASKS.append(entry)
        self.sort_tasks()
        self.save_file('log.csv')
        entry.show_task()
        input("The entry has been add. Press enter to return to the menu")

    def main_menu(self):
        """Displays on screen the main menu of the application and let the user
        to choose an option or quit program.
        """
        while True:
            utils.clear_screen()
            print("""WORK LOG
What would you like to do?
a) Add new entry
b) Search in existing entries
c) Quit program
""")
            option = input("> ")
            if option == 'a':
                self.add_entry()
            elif option == 'b':
                self.search_menu()
            elif option == 'c':
                break
            else:
                print("Sorry, you must choose a valid option.")
                input()

    def search_menu(self):
        """Displays on screen que search menu of the application and let the
        user to choose a search method or return to main menu.
        """
        while True:
            utils.clear_screen()
            print("""Do you want to search by:
a) Exact Date
b) Range of Dates
c) Time Spent
d) Exact Search
e) Regex Pattern
f) Return to menu
""")
            option = input("> ")

            if option == 'a':
                found = task_search.TaskSearch.search_date(self.TASKS)
                self.show_tasks(found)
            elif option == 'b':
                found = task_search.TaskSearch.search_by_range(self.TASKS)
                self.show_tasks(found)
            elif option == 'c':
                found = task_search.TaskSearch.search_time(self.TASKS)
                self.show_tasks(found)
            elif option == 'd':
                found = task_search.TaskSearch.search_exact(self.TASKS)
                self.show_tasks(found)
            elif option == 'e':
                found = task_search.TaskSearch.search_regex(self.TASKS)
                self.show_tasks(found)
            elif option == 'f':
                break
            else:
                print("Sorry, you must choose a valid option")
                input()


if __name__ == '__main__':
    WorkLog('log.csv').main_menu()
