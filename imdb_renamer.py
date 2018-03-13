import os
import imdb
import winshell
from imdbpie import Imdb
from win32com.client import Dispatch


ib = imdb.IMDb()

# Import the imdb package.
ia = Imdb()

del_ext = ["txt" "nfo"  "png"  "jpg"  "url"]
ign_ext = ["exe"  "zip" "part"]
ign_key = []

# res = ia.search_for_title('Deadpool')
# genre = ia.get_title_genres(res[0]['imdb_id'])
# print(genre['genres'])

base = "F:\Ripped\Movies"
os.chdir(base)
for root, subdirs, files in os.walk(os.getcwd()):
    for f in files:
        if root == base:
            continue
        if any(ext == f[:(-1*len(ext))] for ext in ign_ext):
            continue
        if any(ext == f[:(-1*len(ext))] for ext in del_ext):
            os.remove(os.path.join(root, f))

        movie = '.'.join(f.split('.')[:-1]).split(")")[0] + ")"
        if any(key in movie for key in ign_key):
            for key in ign_key:
                temp = f.split(key)
                if temp[0] == '':
                    movie = ''.join(temp[1:])
                else:
                    movie = temp[0]

        res = ia.search_for_title(movie)
        if len(res) < 1:
            res = ia.search_for_title(movie.split("(")[0])
            if len(res) < 1:
                print("Nothing found: {0}".format(f))
                continue

        n = 0
        while "TV" in res[n]['type']:
            n += 1

        title = res[n]['title']
        yr = res[n]['year']
        id = res[n]['imdb_id'][2:]
        mov = ib.get_movie(id)
        ratings = mov.get('certificates')
        mpaa = ''
        for r in sorted(ratings, reverse=True):
            if "USA" in r or "United States" in r:
                mpaa = r.split(':')[1]

        f_name = "{0} ({1} {2})".format(title, yr, mpaa)
        banned_char = [':','?','!']
        if any(b in f_name for b in banned_char):
            for b in banned_char:
                if b == ':':
                    f_name = '-'.join(f_name.split(b))
                else:
                    f_name = ''.join(f_name.split(b))
        print(f_name)
        new_path = os.path.join(base,f_name+f[-4:])
        if os.path.exists(new_path):
            print("File already exists: {0} : {1}".format(f,new_path))
            continue
        os.rename(os.path.join(root,f), new_path)
        if len(os.listdir(root)) < 1:
            try:
                os.rmdir(root)
            except:
                pass

        # ---------------------------------------------
        # Create a shortcut to the file based on genre
        # ---------------------------------------------
        desktop = winshell.desktop()
        genres = ia.get_title_genres(res[n]['imdb_id'])

        library = "Z:\Ripped\Movies"
        for genre in genres:
            genre_dir = os.path.join(library, "Genres", genre)
            if not os.path.exists(genre_dir):
                os.mkdir(genre_dir)
            s_path = os.path.join(genre_dir, f_name+".lnk")
            if os.path.exists(s_path):
                os.remove(s_path)
            target = new_path
            wDir = base
            icon = new_path

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(s_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()

