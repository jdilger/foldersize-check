# filesize.py

# import module
import os
from typing import Tuple
from itertools import islice
import typer

app = typer.Typer()

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def iterate_folder_size(folderpath:str,all:dict):
     for path, dirs, files in os.walk(folderpath):
        for f in files:
            fp = os.path.join(path, f)
            f_size = os.path.getsize(fp)
            size += f_size
            all[f"{fp}"] = f"{round(f_size*0.000000001,2)} GB, {round(f_size*0.000001, 2)} MB"   
def folder_size(folderpath:str)->Tuple[dict,int]:
    # assign size
    size = 0 
    # assign folder path
    all = {}
    # # get size
    for path, dirs, files in os.walk(folderpath):
        for f in files:
            fp = os.path.join(path, f)
            f_size = os.path.getsize(fp)
            size += f_size
            all[f"{fp}"] = f"{round(f_size*0.000000001,2)} GB, {round(f_size*0.000001, 2)} MB"


    return all, size

def sortSliceDict(dictionary:dict,num_take:int)->list:
    dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    sliced = take(num_take, dictionary.items())
    return sliced

@app.command()
def dir_size(folderpath:str, top10 : bool = typer.Option(False,help="Bool to display the top10 largest files. Defaults to False.")):
    '''quickly check a folders file size, and optionally export the top 10 largest files.
    '''
    files, size = folder_size(folderpath)
    bts = typer.style(str(size),fg="cyan")
    mbs = typer.style(str(round(size*0.000001, 2)),fg="cyan")
    gbs = typer.style(str(round(size*0.000000001,2)),fg="cyan")
    typer.echo(f"Folder size bytes: {bts}")
    typer.echo(f"Folder size megabytes: {mbs}")
    typer.echo(f"Folder size gigabytes: {gbs}")
    if top10:
        sorted_files = sortSliceDict(files, 10)
        for f in sorted_files:
            typer.secho(f"{f[0]}",fg="green")
            typer.secho(f"... {f[1]}",fg="blue")

if __name__ == "__main__":
    app()