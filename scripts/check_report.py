#!/usr/bin/env python3
# MIT License（このリポジトリの LICENSE）。自走スターター（自走キットの無料版）に置く写しで、この行のほかは、キット v1.5（jisou-kit-v1.5.zip。2026-10-26 から note で配布）の scripts/check_report.py と同じ。下の「作者のテストは配布物に入れていない」は有料版の配布物のことで、このリポジトリには tests/check_report_cases/ に9件を入れた。
"""人間への報告の文を、CLAUDE.md の「報告の型」の長さ・見出し・前日比と、報告に書くパスで確かめる。
使い方: python3 scripts/check_report.py <<'EOF'
        （報告の全文）
        EOF                                     （標準入力で渡す。一時ファイルを作らない）
        python3 scripts/check_report.py report.md   （ファイルで渡す）
        python3 scripts/check_report.py --cases <cases.tsv のあるフォルダ>   （回帰テスト。下の「--cases の書式」。作者のテストは配布物に入れていない）
字の数え方: 空白（半角・全角）・タブ・改行を除いた文字を1字ずつ数える。記号・数字・英字・見出しの「#」・箇条書きの「-」も1字。
  上限は LIMIT（600字）。空白と改行は画面の区切りで、読む字ではないので数えない（行を分けて読みやすくしても字数は増えない）。
見ること（[ ] は種類）:
- [長さ] 上の数え方で LIMIT 字以内か
- [見出し] 「結論」「やったこと」「お前がやること」「数字」の4つが、この語のまま、この順で1回ずつあるか。
  見出しとして読む行は、「## 結論」のような # の行、「**結論**」のような太字だけの行、「【結論】」のような【】だけの行、
  「結論」だけの行（後ろの「:」「：」は可）。コードブロック（``` か ~~~ で囲んだ行）の中は見出しとして読まない（字数には数える）
- [型に無い見出し] # の行・太字だけの行・【】だけの行が、4つの語のどれかか（例: 「## 未確認・申し送り」「## 持ち主がやること」で止める）
- [前日比] 「数字」の見出しの下に「前日比」の行があり、その1行に ITEMS（投稿数・imp・フォロワー・購入）が1つずつ値つきであるか
  （値は「+3」「＋3」「-39」「0」のような数か、前日が「-」の項目の「-」。項目名のあとの「数」〔例: フォロワー数〕は可。
  前日の行が無い日は「前日比: -」だけでよい〔「-」を「」で囲んでも可〕）。「数字」の見出しが無ければ見ない
- [パス] OS のユーザー名かフォルダの名前が入るフルパスが無いか（コードブロックの中も見る）。止めるのは /Users/・/home/・~/ で始まるパス、
  C:\\Users\\ のパス、Claude Code の一時フォルダや記録の場所の名前に入る「/-Users-名前-…」の形（どれも OS のユーザー名かフォルダの名前が入る）。
  プロジェクトのフォルダからの相対パスで書く
見ないこと: 印（#・**・【】）の無い行に書いた型に無い見出し（例: 「■未確認」。ふつうの文と見分けられない）、「数字」の順（定型行 → 前日比 → 目標までの差）、
  前日比の値が台帳と合うか（前日比の値の代わりに当日の値を書いても通る）、上に挙げた形のほかのフルパス（例: /Volumes/…）、書いた中身が事実か。
  これらは CLAUDE.md の「報告の型」と「やってはいけないこと」を見て自分で確かめる。
問題があれば「行: [種類] 理由」を出し、1件でもあれば終了コード1。問題が無ければ字数を出して終了コード0。
引数の誤り・読めないファイル・空の文・端末から標準入力を渡していないときは終了コード2。
--cases の書式: フォルダの cases.tsv に1行1件で「OK<TAB>ファイル」か「NG<TAB>ファイル<TAB>種類,種類」（ファイルは cases.tsv のあるフォルダから見た場所）。
NG は、出た種類の組が書いた組と同じときだけ期待どおり。# で始まる行と空行は飛ばす。
"""
import os, re, sys

LIMIT = 600
HEADINGS = ('結論', 'やったこと', 'お前がやること', '数字')
KINDS = ('長さ', '見出し', '型に無い見出し', '前日比', 'パス')
ITEMS = ('投稿数', 'imp', 'フォロワー', '購入')   # 前日比に1つずつ書く項目（CLAUDE.md の「報告の型」）
VALUE = r'数?\s*[:：=]?\s*(?:[+＋\-−－±]?\s*\d[\d,]*|[-−－](?!\s*\d))'   # 項目名のあとの値（「+3」「-39」「0」か、前日が「-」の「-」）
PARENS = re.compile(r'[（(][^（）()]*[）)]')                            # 「（5→6）」のような括弧書き
DASH_ONLY = re.compile(r'[「『"`]?[-−－][」』"`]?')                       # 前日の行が無い日の「-」（「」で囲んだ形も）
HOME = re.compile(r'(?<![\w.~-])(?:/(?:Users|home)/[^\s/]+|~/)'           # OS のユーザー名かフォルダの名前が入るパス
                  r'|(?<![\w.-])-(?:Users|home)-[^\s/]+'                    # 一時フォルダや記録の場所の名前（/private/tmp/claude-NNN/-Users-名前-…）
                  r'|\b[A-Za-z]:\\(?:Users|home)\\')                        # C:\Users\…
MD_HEAD = re.compile(r'^#{1,6}\s+(.*?)\s*#*\s*$')        # 「## 結論」
BOLD_ONLY = re.compile(r'^\*\*([^*]+)\*\*\s*[:：]?\s*$')   # 「**結論**」
BRACKET = re.compile(r'^【([^】]+)】\s*[:：]?\s*$')          # 「【結論】」
FENCE = re.compile(r'^\s*(```|~~~)')                           # コードブロックの囲み


def count(text):
    """空白（半角・全角）・タブ・改行を除いた字数"""
    return sum(1 for c in text.lstrip('\ufeff') if not c.isspace())


def heading(line):
    """見出しの行なら (語, 印があるか)。見出しでなければ None"""
    s = line.strip()
    m = MD_HEAD.match(s)
    if m:
        return re.sub(r'^\*\*(.*)\*\*$', r'\1', m[1]).strip().rstrip(':：').strip(), True
    m = BOLD_ONLY.match(s) or BRACKET.match(s)
    if m:
        return m[1].strip().rstrip(':：').strip(), True
    w = s.rstrip(':：').strip()
    if w in HEADINGS:
        return w, False
    return None


def diff_line(rows, num):
    """「数字」の項の行 rows から前日比の行を見て、ITEMS が値つきで1つずつあるか"""
    # 行頭（「- 」「**」のあと）が「前日比」の行を先に選ぶ（定型行などの文中の「前日比」と取り違えない）
    hit = (next(((i, l) for i, l in rows if re.match(r'\s*(?:[-*・]\s+)?(?:\*\*)?前日比', l)), None)
           or next(((i, l) for i, l in rows if '前日比' in l), None))
    if hit is None:
        return [(num, '前日比', f'「数字」に前日比の行が無い。定型行の次に「前日比: {"、".join(x + " +N" for x in ITEMS)}」の1行を置く（前日の行が無い日は「前日比: -」）')]
    i, l = hit
    rest = PARENS.sub('', l.split('前日比', 1)[1]).strip().strip('*').strip().lstrip(':：').strip()
    if DASH_ONLY.fullmatch(rest.rstrip('。').strip()):
        return []   # 前日の行が無い日
    miss = [x for x in ITEMS if not re.search(re.escape(x) + VALUE, rest, re.I)]
    if miss:
        return [(i, '前日比', f'前日比に「{"」「".join(miss)}」の値が無い。{"・".join(ITEMS)}の4つを、減った項目も0の項目も省かずに書く（例: 投稿数 -1、imp -39、フォロワー +1、購入 0。前日が「-」の項目は「-」。前日の行が無い日は「前日比: -」の1行）')]
    return []


def check(text):
    """問題を (行, 種類, 理由) の並びで返す。行は全体のときは 0"""
    out = []
    n = count(text)
    if n > LIMIT:
        out.append((0, '長さ', f'{n}字。空白・改行を除いて{LIMIT}字以内にする（{n - LIMIT}字多い）。伝えることは4つの見出しのどれかに入れて削る'))
    seen = []   # (行, 語)。型の4つの見出し
    heads = []   # 見出しの行（型に無いものも）。「数字」の項の終わりを決める
    body = []    # コードブロックの外の行 (行, 文)
    fence = None   # コードブロックの中なら、開いた囲み（``` か ~~~）
    lines = text.lstrip('\ufeff').replace('\r\n', '\n').split('\n')
    for i, l in enumerate(lines, 1):
        if HOME.search(l):
            out.append((i, 'パス', 'OS のユーザー名かフォルダの名前が入るフルパス（/Users/…・/home/…・~/…・C:\\Users\\…・一時フォルダの /-Users-…）。プロジェクトのフォルダからの相対パス（例: ops/day02.md）で書き、フォルダの外のファイルは書かない'))
        f = FENCE.match(l)
        if f and fence in (None, f[1]):
            fence = None if fence else f[1]
            continue
        if fence:
            continue
        body.append((i, l))
        h = heading(l)
        if h is None:
            continue
        word, marked = h
        heads.append(i)
        if word in HEADINGS:
            seen.append((i, word))
        elif marked:
            out.append((i, '型に無い見出し', f'「{word}」は報告の型に無い見出し。見出しは「{"」「".join(HEADINGS)}」の4つだけを、この語のまま使い、伝えることはそのどれかに入れる'))
    num = next((i for i, w in seen if w == '数字'), None)
    if num:
        end = next((i for i in heads if i > num), len(lines) + 1)
        out += diff_line([(i, l) for i, l in body if num < i < end], num)
    words = [w for _, w in seen]
    for w in HEADINGS:
        if w not in words:
            out.append((0, '見出し', f'見出し「{w}」が無い。「{"」→「".join(HEADINGS)}」の順に、この語のまま置く'))
    for k, (i, w) in enumerate(seen):
        if w in words[:k]:
            out.append((i, '見出し', f'見出し「{w}」が2回ある。4つの見出しは1回ずつ'))
    first = [w for k, w in enumerate(words) if w not in words[:k]]   # 1回目に出た順
    want = [w for w in HEADINGS if w in first]
    if first != want:
        k = next(k for k in range(len(first)) if first[k] != want[k])
        i = next(i for i, w in seen if w == first[k])
        out.append((i, '見出し', f'見出しの順が「{"」→「".join(first)}」。「{"」→「".join(HEADINGS)}」の順にする'))
    return sorted(out, key=lambda z: z[0])


def read(path):
    try:
        return open(path, encoding='utf-8').read(), None
    except (OSError, UnicodeDecodeError) as e:
        return None, f"{path}: 読めません（{getattr(e, 'strerror', None) or e}）"


def cases(d):
    tsv = os.path.join(d, 'cases.tsv')
    rows, err = read(tsv)
    if err:
        print(err); return 2
    n = fail = 0
    for i, row in enumerate(rows.split('\n'), 1):
        row = row.rstrip('\r')
        if not row.strip() or row.startswith('#'):
            continue
        cols = row.split('\t')
        want = {k.strip() for k in cols[2].split(',') if k.strip()} if len(cols) == 3 else set()
        if not ((cols[0] == 'OK' and len(cols) == 2) or (cols[0] == 'NG' and want)) or not want <= set(KINDS):
            print(f'{tsv}:{i}: 書式が違う（OK<TAB>ファイル か NG<TAB>ファイル<TAB>種類,種類。種類は {"・".join(KINDS)}）'); return 2
        text, err = read(os.path.join(d, cols[1]))
        if err:
            print(err); return 2
        got = {k for _, k, _ in check(text)}
        n += 1
        if got != want:
            fail += 1
            exp = 'NG ' + '・'.join(sorted(want)) if want else 'OK'
            act = 'NG ' + '・'.join(sorted(got)) if got else 'OK'
            print(f'{tsv}:{i}: 期待 {exp} → 実際 {act} … {cols[1]}')
    print(f'{n} 件中 {n - fail} 件が期待どおり')
    return 1 if fail else 0


def main(argv):
    args = argv[1:]
    if args[:1] == ['--cases']:
        if len(args) != 2:
            print(__doc__.strip()); return 2
        return cases(args[1])
    if len(args) > 1 or (args and args[0].startswith('-') and args[0] != '-'):
        print(__doc__.strip()); return 2
    if args and args[0] != '-':
        text, err = read(args[0])
        if err:
            print(err); return 2
        name = args[0]
    else:
        if sys.stdin.isatty():
            print(__doc__.strip()); return 2
        try:
            text = sys.stdin.buffer.read().decode('utf-8')
        except UnicodeDecodeError as e:
            print(f'標準入力: 読めません（{e}）'); return 2
        name = '標準入力'
    if not text.lstrip('\ufeff').strip():
        print(f'{name}: 報告の文が空（全文を標準入力かファイルで渡す）'); return 2
    found = check(text)
    for i, k, msg in found:
        print(f'{name}:{i}: [{k}] {msg}' if i else f'{name}: [{k}] {msg}')
    n = count(text)
    print(f'{n}字（空白・改行を除く。上限{LIMIT}）。' + ('問題なし' if not found else f'問題 {len(found)} 件'))
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
