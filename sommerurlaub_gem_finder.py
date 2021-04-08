import os
import os.path
import random
import time
import pyautogui
from termcolor import colored
from datetime import datetime
import time
import csv


result_list = history = []
j = show_info = gems_counter = 0
last_counter = -1
sorting = "Random"
filepath = path = ""
username = ""


def main():
  os.system("clear")
  print(colored("Started Sommerurlaub Gem Finder v0.4", 'yellow'))
  print(colored("- features: paths, csv support, search, randomized, gopro sort, picture support, phone sort, move to trash", 'yellow'))
  print(colored("\nTo be added: reading timestamp automatically", 'yellow'))

  global filepath, history, result_list, j, last_counter, sorting, show_info, gems_counter, username, path

  file_exists = os.path.isfile("sommerurlaub_gems.csv")
  if not file_exists:
    username = input(colored("\nEnter initials (will be printed to excel) > ", 'green'))
  else:
    with open('sommerurlaub_gems.csv', 'r', newline='') as csvfile:
      name_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
      next(name_reader)
      username = next(name_reader)[0]
  path, search = choose_path()

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
    print("\nGems added this session:", colored(gems_counter, 'green'))

    if filepath != "":
      print("\nCurrent video:", colored(filepath[12:], 'magenta'))

    if show_info == 1:
      print("\nNext 5:")
      for i in range(j, min(len(result_list), j+5)):
        print(colored(datetime.fromtimestamp(os.path.getmtime(result_list[i])).strftime(
            '%Y-%m-%d %H:%M:%S'), 'cyan'), result_list[i][12:])

    print(colored("\nenter: next\nl: last\ng: add to gems\nskip: skip 5 videos\np: change path\nh: print history\ns: search\nn: sort by date/random\ngopro: gopro sort\nphone: phone sort\nm: move to trash and show next\ni: info\nx: stop\nq: quit\n", 'yellow'))
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
        time.sleep(.5)
        j = j-2
        execute()
        # filepath = history[last_counter]
        # last_counter = last_counter - 1
        # command = "tmux new -d 'vlc "+'"'+filepath+'"'+" --fullscreen'"
        # os.system(command)
        # time.sleep(.5)
        # pyautogui.keyDown('alt')
        # time.sleep(.2)
        # pyautogui.press('tab')
        # pyautogui.keyUp('alt')
      except:
        os.system("tmux kill-server")
        # last_counter = - 1

    elif choice == "p":
      path, search = choose_path()
      result_list = []
      sorting = "(random):"

    elif choice == "h":
      history = list(set(history))
      print(*history, sep="\n")
      input(colored("\nPress any key to continue > ", 'green'))

    elif choice == "skip":
      j += 5

    elif choice == "g":
      add_to_gems()

    elif choice == "s":
      search = input(colored("\nInput search string > ", 'green'))
      result_list = []
      j = 0
      path = 'search'

    elif choice == "n":
      if len(result_list) == 0:
        generate(path, search)
      if sorting == "Sorted":
        random.shuffle(result_list)
        sorting = "Random"
      else:
        result_list.sort(key=os.path.getmtime, reverse=False)
        sorting = "Sorted"
      j = 0

    elif choice == "gopro":
      if len(result_list) == 0:
        generate(path, search)
      gopro_sort()
      sorting = "gopro"
      j = 0

    elif choice == "phone":
      if len(result_list) == 0:
        generate(path, search)
      phone_sort()
      sorting = "gopro"
      j = 0

    if choice == "m":
      if move_to_trash():
        result_list.remove(filepath)
        j = j-1
      if len(result_list) == 0:
        generate(path, search)
      os.system("tmux kill-server")
      time.sleep(.5)
      execute()
      last_counter = -1

    elif choice == "i":
      show_info = 1 - show_info

    elif choice == "x":
      os.system("tmux kill-server")

    elif choice == "q":
      os.system("tmux kill-server")
      print("")
      print("# gems added: ", colored(gems_counter, 'green'))
      print("")
      print("History:")
      history = list(set(history))
      print(*history, sep="\n")
      print("")
      return 0


def choose_path():
  print(colored("\n1: Sommerurlaub 1\n2: Sommerurlaub 2.0\n3: Sommerurlaub Reunion\n4: Sommerurlaub 1.1\n5: Sommerurlaub 5\na: all\nf: Frankfurt Footage\ncp: custom path\nf: favorites\ns: search\nq: quit\n", 'cyan'))
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
    path = '/mnt/ntfs_F/Sommerurlaub_footage/5_Sommerurlaub_5'

  elif choice == "a":
    path = 'all'

  elif choice == "f":
    path = '/mnt/ntfs_F/Frankfurt_footage'

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
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/2_Sommerurlaub_2.0'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/3_Sommerurlaub_reunion'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/4_Sommerurlaub_1.1'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage/5_Sommerurlaub_5'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    random.shuffle(result_list)

  elif search == "":
    for root, dirs, files in os.walk(path):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          filepath = os.path.join(root, name)
          result_list.append(filepath)
    random.shuffle(result_list)

  else:
    for root, dirs, files in os.walk('/mnt/ntfs_F/Sommerurlaub_footage'):
      for name in files:
        if name.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".JPG", ".jpg", "jpeg")):
          if all(x in os.path.join(root, name).lower() for x in search.split()):
            filepath = os.path.join(root, name)
            result_list.append(filepath)
    random.shuffle(result_list)

  return


def gopro_sort():
  # sorts gopro videos chronologically
  global result_list
  path_file_dict = {}
  files = []
  for path in result_list:
    filename = path.split('/')[-1:]
    # print(filename)
    if filename[0][1] == "H":
      filename = filename[0][2:8]
      # print('filename[2:8] = ', filename)
      files.append(filename)
      path_file_dict[filename] = path
  result_list = []
  for i in range(1, 600):
    for j in range(1, 7):
      for name in files:
        if int(name[-3:]) == i and int(name[1]) == j:
          # print('added ', path_file_dict[name])
          result_list.append(path_file_dict[name])


def phone_sort():
  global result_list
  path_file_dict = {}
  files = []
  for path in result_list:
    filename = path.split('/')[-1:]
    # print("filepath before if:", filename)
    if filename[0][0] == "I" or filename[0][0] == "V":
      filename = filename[0][4:12]+"99"+filename[0][15:19]
      # print("filename whatsapp:", filename)
    else:
      filename = filename[0][0:8]+filename[0][9:15]
      # print("filename:", filename)
    path_file_dict[filename] = path
    files.append(int(filename))
  files.sort()
  result_list = []
  for file in files:
    result_list.append(path_file_dict[str(file)])


def execute():
  # print(*result_list, sep="\n")
  global result_list, j, filepath

  try:
    if j == len(result_list):
      j = 0
    filepath = result_list[j]
    j = j+1
    if filepath.endswith((".MP4", ".mp4", ".mkv", ".wmv", ".flv", ".webm", ".mov")):
      command = "tmux new -d 'vlc "+'"'+filepath+'"'+" --fullscreen'"
      os.system(command)
      time.sleep(.5)
      pyautogui.keyDown('alt')
      time.sleep(.2)
    else:
      # command = "tmux new -d 'feh --scale-down --auto-zoom --geometry 2560x1440+2560+0 " + filepath+"'"
      command = "tmux new -d 'vlc "+'"'+filepath+'"'+" --fullscreen'"
      # command = "xdg-open " + filepath
      # print("command: ", command)
      os.system(command)
      time.sleep(.2)
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


def add_to_gems():
  global filepath, username, gems_counter, path
  # Columns: comment, situation, timestamp, current datetime, username, current video name
  current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  file_exists = os.path.isfile("sommerurlaub_gems.csv")

  print(colored("\nTimestamp of gem start ('XX:XX'):", 'green'))
  timestamp = input(colored("> ", 'green'))

  print(colored("\nWhat is the current situation?:", 'green'))
  print(colored("1: Draußen unterwegs\n2: Buffen\n3: Zocken\n4: Bauen\n5: Jamaican Shower\n6: Random\n7: Zuhause\n8: Feiern", 'green'))
  situations = {
      "1": "Draußen unterwegs",
      "2": "Buffen",
      "3": "Zocken",
      "4": "Bauen",
      "5": "Jamaican Shower",
      "6": "Random",
      "7": "Zuhause",
      "8": "Feiern",
  }
  situation = situations[input(colored("> ", 'green'))]

  print(colored("\nAdditional Comment:", 'green'))
  comment = input(colored("> ", 'green'))

  # write to csv
  with open('sommerurlaub_gems.csv', 'a', newline='') as csvfile:
    gem_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    if not file_exists:
      gem_writer.writerow(['Username', 'path', 'Datetime added', 'Relevant Filepath', 'timestamp', 'Situation', 'Comment'])
    gem_writer.writerow([username, path, current_datetime, filepath.split('/')[-2:], timestamp, situation, comment])

  gems_counter = gems_counter + 1

  return


def move_to_trash():
  global filepath

  # print(colored("\nAre you sure:", 'red'), filepath)
  # choice = input(colored("yes: yes\nn: no \n\n> ", 'red'))
  command = "mv "+filepath+" /mnt/ntfs_F/_trash"
  os.system(command)
  return True

  # if choice == "yes":
  #   command = "rm "+'"'+filepath+'"'
  #   os.system(command)
  #   return True
  # return False


if __name__ == '__main__':
  main()
