# [PyLint](https://www.pylint.org) plugins

Plugins wrote during my internship on the optimization of the energy
consumption of programs written in [Python](https://www.python.org).

It features two plugins :

* One to prevent from using a while loop for the iteration in a list
* One to prevent from using this kind of line : `list|set(map(\ldots))`

## How to launch

* [Install PyLint](https://www.pylint.org/#install)
* Clone this repository
* Add this repository to your `PYTHONPATH`

If you are using a GNU/Linux distribution, follow these instructions:

+ open your `~/.bashrc` file with your favorite text editor ([GNU
EMACS](https://www.gnu.org/software/emacs/) for example)

+ if the name of the directory is /path/to/your/directory/, then add
this line at the end of your `~/bashrc` :

```
export PYTHONPATH=/path/to/your/directory/
```

+ then open a new terminal window and run this command below (exapmle with whlie_plugin):
```
pylint --load-plugins=while_plugin --disable=all --enable=while-iteration test.py
```

with test.py the file to test