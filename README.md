enert
=====

miyagaw61's python library.

install
=======

```bash
pip install "git+https://github.com/miyagaw61/enert.git#egg=enert"
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
- 編集
```python
f.edit()
```

- 行数取得
```python
f.lines()
```

- データ読み込み
```python
f.data()
```

- 行ごとに読み込み
```python
f.linedata()
```

- 書き込み
```python
f.write("hoge\n")
```

- 追記
```python
f.add("hoge\n")
```

- 存在するかどうか調査
```python
f.exist()
```

- 削除
```python
f.rm()
```

- バイナリとして読み込み
```python
f.binary()
```

- バイナリをn文字ごとにsplitしてリスト化して読み込み
```python
f.binary(n)
```

## shellクラス
```python
cmd = shell("ls | grep *.txt")
```
- コマンド実行
```python
cmd.call()
```

- コマンドの出力を取得
```python
stdout_str, stderr_str = cmd.get()
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
* カーソルをn文字上へ移動
```python
up(n)
```

* カーソルをn文字下へ移動
```python
down(n)
```

* カーソルをn桁目へ移動
```python
to(n)
```

* 現在のカーソルの位置を保存
```python
save()
```

* 保存したカーソルの位置を復元
```python
restore()
```

* 現在の行をすべてクリア
```python
all_delete()
```

* 現在の行の先頭からn桁目までをクリア
```python
head2n_delete(n)
```

* 現在の行のn桁目から行末までをクリア
```python
n2tail_delete()
```

* 現在の行からn行下までクリア
```python
lines_delete(n)
```

* clear(Ctrl+l)する
```python
clear()
```

## screenクラス
制御関数と組み合わせて独自のmenuを作成する際に便利です。

* 原点を作成
```python
s = screen()
```

* 原点を更新
```python
save()
```

* 原点を元にした座標に出力
```python
s.addstr(x, y, strings)
```

* example
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
        s.addstr(1, header+old, "  " + lst[old])
        s.addstr(1, header+i, black_red("> ", "bold") + black_white(lst[i], "bold"))
    elif (key == "k" or ord(key) == UP) and i > 0:
        old = i
        i = i - 1
        s.addstr(1, header+old, "  " + lst[old])
        s.addstr(1, header+i, black_red("> ", "bold") + black_white(lst[i], "bold"))
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
    if key == "q":
        print("Exit.")
        exit()
    elif ord(key) == ENTER:
        print("ENTER!!!")
    elif key:
        print(key)

```
