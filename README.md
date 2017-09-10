enert
=====

miyagaw61's python library.

install
=======

```bash
mkdir /hoge  
git clone https://github.com/miyagaw61/enert /hoge/enert    
export PYTHONPATH=$PYTHONPATH:/hoge
```

Usage
=====

* import 
```python
from enert import *
```

## fileクラス
```python
file_name = "a.out"
f = file(file_name)
```
- f.edit()
```
編集
```

- f.lines()
```
行数取得
```

- f.data()
```
データ読み込み
```

- f.linedata()
```
行ごとに読み込み
```

- f.write("hoge\n")
```
書き込み
```

- f.add("hoge\n")
```
追記
```

- f.exist()
```
存在するかどうか調査
```

- f.rm()
```
削除
```

- f.binary()
```
バイナリとして読み込み
```

- f.binary(n)
```
バイナリをn文字ごとにsplitしてリスト化して読み込み
```

## shellクラス
```python
cmd = shell("ls | grep *.txt")
```
- cmd.call()
```
コマンド実行
```

- stdout_str, stderr_str = cmd.get()
```
コマンドの出力を取得
```

## menuクラス
手軽にmenuが作成できる。
```python
lst = ["1. hogehoge", "2. fugafuga", "3. piyopiyo"]
def function(i):
    m.menu_exit()
    print(lst[i])
    exit()
m = menu(lst, function)

print('Please input "j" or "k" or "Enter".')
m.menu_start()
```

## 制御関数群
ターミナルを制御する関数群
* up(n)
```
カーソルをn文字上へ移動
```

* down(n)
```
カーソルをn文字下へ移動
```

* to(n)
```
カーソルをn桁目へ移動
```

* save()
```
現在のカーソルの位置を保存
```

* restore()
```
保存したカーソルの位置を復元
```

* all_delete()
```
現在の行をすべてクリア
```

* head2n_delete(n)
```
現在の行の先頭からn桁目までをクリア
```

* n2tail_delete()
```
現在の行のn桁目から行末までをクリア
```

* lines_delete(n)
```
現在の行からn行下までクリア
```

* clear()
```
clear(Ctrl+l)する
```

## screenクラス
制御関数と組み合わせて独自のmenuを作成する際に便利です。
```python
from enert import *

lst = ["hogehoge", "fugafugafugafuga", "piyopiyopiyo"]
sys.stdout.write("Your Choise : ")
s = screen()
print("\n====================")
print(black_red("> ", "bold") + black_white(lst[0], "bold"))
print("  " + lst[1])
print("  " + lst[2])
print("====================")
i = 0
header = 2
footer = 1
up(header+len(lst)+footer)
sys.stdout.write("Your Choise : ")
save()
while 1:
    key = getch()
    if (key == "j" or ord(key) == DOWN) and i < len(lst)-1:
        old = i
        i = i + 1
        s.print(1, header+old, "  " + lst[old])
        s.print(1, header+i, black_red("> ", "bold") + black_white(lst[i], "bold"))
    elif (key == "k" or ord(key) == UP) and i > 0:
        old = i
        i = i - 1
        s.print(1, header+old, "  " + lst[old])
        s.print(1, header+i, black_red("> ", "bold") + black_white(lst[i], "bold"))
    elif ord(key) == ENTER:
        restore()
        all_delete()
        sys.stdout.write("Your Choise : ")
        sys.stdout.write(lst[i])
        save()
        sys.stdout.flush()
    elif key == "q" or ord(key) == CTRL_C or ord(key) == CTRL_D:
        lines_delete(100)
        exit()
```

## その他
* 文字に色を付与
```python
red_hoge = red("hoge")
bold_green_fuga = green("hoge", "bold")
background_black_fontcolor_white = black_white("hoge", "bold")
```

* valueをn桁の2の補数表現で表現
```python
complement(value, n)
```

* 文字列strをn文字ごとにsplit
```python
str = "hogefugapiyo"
n = 4
list = splitn(str, n)
print(list) # -> ["hoge", "fuga", "piyo"]
```

* ターミナルのサイズを取得
```python
size_y, size_x = get_term_size()
```

* 文字列をファイルに書き込む
```python
buf = "hoge"
writefile(buf, "buf.txt")
```

* リアルタイムで文字を読み込む
```python
while 1:
    key = getch()
    if key:
        if key == "q":
            exit()
        if ord(key) == 13:
            print("ENTER!!!")
        else:
            print("hoge")

```
