# enert - Python Utils Library.

[![Twitter](https://imgur.com/Ibo0Twr.png)](https://twitter.com/miyagaw61)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

# install

```bash
pip install git+https://github.com/miyagaw61/enert
```

# Usage

* import 

```python
from enert import *
```

## Fileクラス

```python
file_name = "a.out"
f = File(file_name)
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
失敗した時はbytes型になります
```python
f.read()
```

- データを行ごとに読み込み

```python
f.readlines()
```

- 制御文字を削除してデータ読み込み
```python
f.white_read()
```

- 制御文字を削除してデータを行ごとに読み込み
```python
f.white_readlines()
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

## Shellクラス

```python
cmd = Shell("ls | grep *.txt")
```
- コマンド実行

```python
cmd.call()
```

- コマンドの出力を取得

```python
stdout_str, stderr_str = cmd.get()
```

## Menuクラス

手軽にmenuが作成できる。

```python
lst = ["1. hogehoge", "2. fugafuga", "3. piyopiyo"]
def function(i):
    m.menu_exit()
    print(lst[i])
    exit()
m = Menu(lst, function)

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

## Screenクラス

制御関数と組み合わせて独自のmenuを作成する際に便利です。

* 原点を作成

```python
s = Screen()
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
s = Screen()
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

## enerdict型

dict型(辞書型)を継承して作成したdict型の上位互換です

* 宣言

```python
dct = enerdict(one='1', two='2', three='3')
```

* キーのリストをビュー型ではなく完全なリスト型で返却

```python
dct.keys
```

* 値のリストをビュー型ではなく完全なリスト型で返却

```python
dct.values
```

* n番めのキーを取得

```python
dct.keys[n]
```

* n番めの値を取得

```python
dct.values[n]
```

* リストのような形で返却

```python
dct.list
```

* 要素追加

```python
dct['four'] = '4' #Please use this.
#dct.append(five='5')   #You can use this, BUT don't use this!
#dct.append('six', '6') #You can use this, BUT don't use this!
```

* example

```python
dct = enerdict(zero="0", one="1", two="2", three="3")

#>>> dct
#>>> {'zero': '0', 'one': '1', 'two': '2', 'three': '3'}
#>>> dct.keys[1]
#>>> "one"
#>>> dct.values[3]
#>>> "3"
#>>> dct.list
#>>> [['zero', '0'], ['one', '1'], ['two', '2'], ['three', '3']]

for key in dct:
    print(key)
#>>> zero
#>>> one
#>>> two
#>>> three

for key,value in dct.list:
    print("key is " + key + ", value is " + value)
#>>> key is zero, value is 0
#>>> key is one, value is 1
#>>> key is two, value is 2
#>>> key is three, value is 3

dct['four'] = '4'

for key,value in dct.list:
    print("key is " + key + ", value is " + value)
#>>> key is zero, value is 0
#>>> key is one, value is 1
#>>> key is two, value is 2
#>>> key is three, value is 3
#>>> key is four, value is 4
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
strings = "hogefugapiyo"
n = 4
lst = splitn(strings, n)
print(lst) # -> ["hoge", "fuga", "piyo"]
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

* Usageをパースして表示

これを使えば、サブコマンド形式とオプション形式をどちらも採用しているスクリプトを簡単に作ることができる。(サブコマンド形式のルーチンのみこのコマンドを使用)
```python
Usage: parse_usage(str usage, list args)
Example usage: 'git [commit <-m>] [push <branch>]'
Example args: ['commit [-m <comment>]:commit to local repository', 'push [branch]:push to remote repository']
```

* parserの基本骨格を作成

これを使えば、簡単にパーサーの基本骨格を作成することが可能

```python
parser_A = mkparser(usage)
parser_B = mkparser(usage, ['add', 'commit'])
parser_A.add_argument('-a', '--all', action='store_true')
```

* リスト二つを比較して、一致するものが一つでもあるかどうかを調査

一致するものが一つでもあれば1を返す。
```python
list_check(listA, listB)
```

* helpを表示すべきかどうか調査

lstの中に-hもしくは--helpが存在すれば1を返す。また、argc < idxを満たせば1を返す。
```python
help() -> help(lst=argv, idx=None)
help(lst=lstA) -> help(lst=lstA, idx=None)
help(idx=3) -> help(lst=argv, idx=3)
```

* search()

* search_binary()

* to_ascii()

* get_now()

* to_binary()

* split_byte()

* int2bins()

* int2bin()

* bin2ints()

* bin2int()

* bin2hexes()

* bin2hex()

* hex2bins()

* hex2bin()

* hex2ints()

* hex2int()

* int2hexes()

* int2hex()

* sanitize()

* pad()

* unpad()

* Ssl
