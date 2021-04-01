import os
import random
import time
import pyautogui
from termcolor import colored
from datetime import datetime
import time


result_list = history = []
j = show_info = gems_counter = 0
last_counter = -1
sorting = "Random"
filepath = ""
username = ""


def main():
  os.system("clear")
  print(colored("Started Sommerurlaub Gem Finder v0.1", 'yellow'))
  print(colored("- features: x", 'yellow'))
  print(colored("\n to be added: csv support", 'yellow'))

  global filepath, history, result_list, j, last_counter, sorting, show_info, gems_counter, username

  path, search = choose_path()

  username = input(colored("\n Enter initials (will be printed to excel) > ", 'yellow'))

  while True:
    os.system("clear")

    print("Username: ", username)

    if search != "":
      if len(result_list) != 0:
        print("Current search string:", colored(search, 'green'), "\n -", sorting, "match", j, "/", len(result_list))
      else:
        print("Current search string:", colored(search, 'green'))
    else:
      if len(result_list) != 0:
        print("Current path:", path, "\n -", sorting, "file", j, "/", len(result_list))
      else:
        print("Current path:", path)

    if filepath != "":
      print("\nCurrent video:", colored(filepath[12:], 'magenta'))

    if show_info == 1:
      print("\nNext 5:")
      for i in range(j, min(len(result_list), j+5)):
        print(colored(datetime.fromtimestamp(os.path.getmtime(result_list[i])).strftime(
            '%Y-%m-%d %H:%M:%S'), 'cyan'), result_list[i][12:])

    print(colored("\nenter: next\nl: last\nf: add to favorites\ng: add to gems\nd: delete file\np: change path\nh: print history\ns: search\nn: sort new/random\ni: info\nx: stop\nq: quit\n", 'yellow'))
    choice = input(colored("> ", 'green'))

    if choice == "":
      if len(result_list) == 0:
        generate(path, search)
      os.system("tmux kill-server")
      time.sleep(.5)
      execute()
      last_counter = -1

    elif choice == "l":
      try:
        os.system("tmux kill-server")
        filepath = history[last_counter]
        last_counter = last_counter - 1
        command = "tmux new -d 'vlc "+'"'+filepath+'"'+" --fullscreen'"
        os.system(command)
        time.sleep(.5)
        pyautogui.keyDown('alt')
        time.sleep(.2)
        pyautogui.press('tab')
        pyautogui.keyUp('alt')
      except:
        os.system("tmux kill-server")
        last_counter = - 1

    elif choice == "d":
      os.system("tmux kill-server")
      if delete():
        result_list.remove(filepath)
        j = j-1
        deleted_counter = deleted_counter + 1

    elif choice == "p":
      path, search = choose_path()
      result_list = []
      sorting = "(random):"

    elif choice == "h":
      history = list(set(history))
      print(*history, sep="\n")
      input(colored("\nPress any key to continue > ", 'green'))

    elif choice == "f":
      add_to_favorites()

    elif choice == "g":
      add_to_gems()

    elif choice == "s":
      search = input(colored("\nInput search string > ", 'green'))
      result_list = []
      j = 0
      path = 'search'

    elif choice == "n":
      if sorting == "Sorted":
        random.shuffle(result_list)
        sorting = "Random"
      else:
        result_list.sort(key=os.path.getmtime, reverse=True)
        sorting = "Sorted"
      j = 0

    elif choice == "i":
      show_info = 1 - show_info

    elif choice == "x":
      os.system("tmux kill-server")

    elif choice == "q":
      os.system("tmux kill-server")
      print("")
      print("# gems added: ", gems_counter)
      print("")
      print("History:")
      history = list(set(history))
      print(*history, sep="\n")
      print("")
      return 0


def choose_path():
  print(colored("\n1: Sommerurlaub 1\n2: Sommerurlaub 2.0\n3: Sommerurlaub Reunion\n4: Sommerurlaub 1.1\n5: Sommerurlaub 5\na: all\ncp: custom path\nf: favorites\ns: search\nq: quit\n", 'cyan'))
  choice = input(colored("> ", 'green'))
  search = ''

  if choice == "1":
    path = '/mnt/ntfs_F/Sommerurlaub_footage/1_Sommerurlaub_1'

  elif choice == "2":
    path = '/mnt/ntfs_F/Sommerurlaub_footage/2_Sommerurlaub_2.0'

  elif choice == "3":
    path = '/mnt/ntfs_F/Sommerurlaub_footage/3_Sommerurlaub_reunion'

  elif choice == "4":
    path = '/mnt/ntfs_F/Sommerurlaub_footage/4_Sommerurlaub_1.1'

  elif choice == "5":
    path = '/mnt/ntfs_F/Sommerurlaub_footage/3_Sommerurlaub_5'

  elif choice == "a":
    path = 'all'

  elif choice == "cp":
    path = input("  Custom path: ")

  elif choice == "f":
    path = 'favs'

  elif choice == "s":
    search = input(colored("\nInput search string > ", 'green'))
    path = 'search'

  elif choice == "q":
    os.system("tmux kill-server")
    exit()

  else:
    path = '/mnt/ntfs_F/--'

  return path, search


def generate(path, search):
  global result_list, j

  result_list = []
  j = 0
  random.seed()

  if path == 'favs':
    file = open('favs.txt', 'r')
    result_list = file.readlines()
    for x in range(len(result_list)):
      result_list[x] = result_list[x][:-1]
    file.close()
    random.shuffle(result_list)

  elif path == 'all':
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/1_Sommerurlaub_1'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/2_Sommerurlaub_2.0'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/3_Sommerurlaub_reunion'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/4_Sommerurlaub_1.1'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/5_Sommerurlaub_5'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    random.shuffle(result_list)

  elif search == "":
    for root, dirs, files in os.walk(path):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    random.shuffle(result_list)

  else:
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage'):
      for name in files:
        if name.endswith((".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
          if all(x in os.path.join(root, name).lower() for x in search.split()):
            filepath = os.path.join(root, name)
            result_list.append(filepath)
    random.shuffle(result_list)

  return


def execute():
  # print(*result_list, sep="\n")
  global result_list, j, filepath

  try:
    if j == len(result_list):
      j = 0
    filepath = result_list[j]
    j = j+1
    command = "tmux new -d 'vlc "+'"'+filepath+'"'+" --fullscreen'"
    os.system(command)
    time.sleep(.5)
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    history.append(filepath)
    return
  except:
    filepath = "Error - No file found"
    j = 0
  return


def add_to_favorites():
  global filepath

  print(colored("\nFunction inactive:", 'green'), filepath)
  choice = input(colored("\n> ", 'green'))

  # if choice == "y":
  #   f = open('favs.txt', 'a+')
  #   f.write(filepath)
  #   f.write('\n')
  return


def add_to_gems():
  global filepath, username, gems_counter
  # Columns: comment, situation, timestamp, current datetime, username, current video name

  print(colored("\nWhat is the current situation?:", 'green'), filepath)
  # Kategorien vorgeben?
  situation = input(colored("\n> ", 'green'))

  print(colored("\nAdditional Comment:", 'green'), filepath)
  comment = input(colored("\n> ", 'green'))

  # write to csv
  gems_counter = gems_counter + 1
  print("gem added")

  return


def delete():
  global filepath

  print(colored("\nFunction inactive:", 'red'), filepath)
  choice = input(colored("\n> ", 'red'))

  # if choice == "yes":
  #   command = "rm "+'"'+filepath+'"'
  #   os.system(command)
  #   return True
  return False


if __name__ == '__main__':
  main()
