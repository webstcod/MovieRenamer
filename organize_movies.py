import os
import imdb
import time
import winshell
from imdbpie import Imdb
from win32com.client import Dispatch

# https://github.com/richardasaurus/imdb-pie
# https://imdbpy.sourceforge.io/support.html#documentation
t_start = time.time()

ib = imdb.IMDb()

# Import the imdb package.
ia = Imdb()

del_ext = ["txt", "nfo", "png", "jpg", "url"]
ign_ext = ["exe", "zip", "part", "srt", "pdf", "iso", "txt", "nfo", "png", "jpg", "url", "ini"]
ign_key = []
repl_key = dict()
repl_key["Æ"] = 'ae'
error_list = list()

library = "Z:\Downloaded\Video(s)"
# library = "Z:\Ripped\Movies"
os.chdir(library)
with open("movie_management.log", 'w') as log:
    for root, subdirs, files in os.walk(os.path.join(library, 'Library')):
        for f in sorted(files):
            # ---------------------------------------------
            # Filter and define search
            # ---------------------------------------------
            if any(ext == f[(-len(ext)):] for ext in ign_ext):
                continue

            # movie = '.'.join(f.split('.')[:-1]).split(")")[0] + ")"
            if ")" in f:
                yr = f.split(")")[0].split("(")[1].split()[0]
                mov = f.split(")")[0].split("(")[0]
                movie = "{0} ({1})".format(mov, yr)
            else:
                movie = '.'.join(f.split('.')[:-1])
            if any(key in movie for key in ign_key):
                for key in ign_key:
                    temp = f.split(key)
                    if temp[0] == '':
                        movie = ''.join(temp[1:])
                    else:
                        movie = temp[0]
            if any(key in movie for key in repl_key.keys()):
                for key in repl_key.keys():
                    temp = f.split(key)
                    movie = repl_key[key].join(temp)
            print(movie)
            # log.write(movie+"\n")

            # ---------------------------------------------
            # Search for movie data
            # ---------------------------------------------
            res = ia.search_for_title(movie)
            if len(res) < 1:
                res = ia.search_for_title(movie.split("(")[0])
                if len(res) < 1:
                    print("Nothing found: {0}".format(f))
                    log.write("Nothing found: {0}\n".format(f))
                    error_list.append(os.path.join(root, f))
                    continue

            n = 0
            Cont = False
            attempt = 0
            while res[n]['type'] == None:
                n += 1
                if n >= len(res) and attempt == 0:
                    n = 0
                    attempt = 1
                    res = ia.search_for_title(movie.split("(")[0])
                elif n >= len(res):
                    Cont = True
                    break
            if Cont:
                print("Failed: {0}".format(movie))
                log.write("Failed: {0}\n".format(movie))
                error_list.append(os.path.join(root, f))
                continue
            while "TV" in res[n]['type'] and not "movie" in res[n]['type'].lower() and not "special" in res[n]['type'].lower():
                n += 1
                if n >= len(res) and attempt == 0:
                    n = 0
                    attempt = 1
                    res = ia.search_for_title(movie.split("(")[0])
                elif n >= len(res):
                    Cont = True
                    break
                while res[n]['type'] == None:
                    n += 1
                    if n >= len(res) and attempt == 0:
                        n = 0
                        attempt = 1
                        res = ia.search_for_title(movie.split("(")[0])
                    elif n >= len(res):
                        Cont = True
                        break
                if n >= len(res) and attempt == 0:
                    n = 0
                    attempt = 1
                    res = ia.search_for_title(movie.split("(")[0])
                elif n >= len(res):
                    Cont = True
                    break
            if Cont:
                print("Failed: {0}".format(movie))
                log.write("Failed: {0}\n".format(movie))
                error_list.append(os.path.join(root, f))
                continue

            # ---------------------------------------------
            # Create a shortcut to the file based on genre
            # ---------------------------------------------
            desktop = winshell.desktop()
            try:
                genres = ia.get_title_genres(res[n]['imdb_id'])['genres']
            except:
                genres = []
                log.write('No Genres: {0}\n'.format(f))
                error_list.append(os.path.join(root, f))

            f_name = '.'.join(f.split('.')[:-1])
            f_path = os.path.join(root,f)
            for genre in genres:
                genre_dir = os.path.join(library, "Genres", genre)
                if not os.path.exists(genre_dir):
                    os.mkdir(genre_dir)
                s_path = os.path.join(genre_dir, f_name+".lnk")
                if os.path.exists(s_path):
                    os.remove(s_path)
                target = f_path
                wDir = root
                icon = f_path

                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(s_path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = wDir
                shortcut.IconLocation = icon
                shortcut.save()


# ---------------------------------------------
# Added movies with an error into and unknown genre directory
# ---------------------------------------------
for f_err in error_list:
    f_name = '.'.join(os.path.split(f_err)[-1].split('.')[:-1])
    f_path = f_err
    genre_dir = os.path.join(library, "Genres", "Unknown")
    if not os.path.exists(genre_dir):
        os.mkdir(genre_dir)
    s_path = os.path.join(genre_dir, f_name+".lnk")
    if os.path.exists(s_path):
        os.remove(s_path)
    target = f_path
    wDir = os.path.split(f_err)[0]
    icon = f_path

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(s_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()

print("Elapsed time: {0}".format(time.time()-t_start))
