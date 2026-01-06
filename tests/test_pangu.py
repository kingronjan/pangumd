from pathlib import Path

import pangu
from tests.utils import get_fixture_path


class TestPangu:
    pass


class TestSpacing(TestPangu):
    # 略過

    def test_skip_underscore(self):
        assert pangu.spacing('前面_後面') == '前面_後面'
        assert pangu.spacing('前面 _ 後面') == '前面 _ 後面'
        assert pangu.spacing('Vinta_Mollie') == 'Vinta_Mollie'
        assert pangu.spacing('Vinta _ Mollie') == 'Vinta _ Mollie'

    # 兩邊都加空格

    def test_alphabets(self):
        assert pangu.spacing('中文abc') == '中文 abc'
        assert pangu.spacing('abc中文') == 'abc 中文'

    def test_numbers(self):
        assert pangu.spacing('中文123') == '中文 123'
        assert pangu.spacing('123中文') == '123 中文'

    def test_latin1_supplement(self):
        assert pangu.spacing('中文Ø漢字') == '中文 Ø 漢字'
        assert pangu.spacing('中文 Ø 漢字') == '中文 Ø 漢字'

    def test_greek_and_coptic(self):
        assert pangu.spacing('中文β漢字') == '中文 β 漢字'
        assert pangu.spacing('中文 β 漢字') == '中文 β 漢字'
        assert pangu.spacing('我是α，我是Ω') == '我是 α，我是 Ω'

    def test_number_forms(self):
        assert pangu.spacing('中文Ⅶ漢字') == '中文 Ⅶ 漢字'
        assert pangu.spacing('中文 Ⅶ 漢字') == '中文 Ⅶ 漢字'

    def test_cjk_radicals_supplement(self):
        assert pangu.spacing('abc⻤123') == 'abc ⻤ 123'
        assert pangu.spacing('abc ⻤ 123') == 'abc ⻤ 123'

    def test_kangxi_radicals(self):
        assert pangu.spacing('abc⾗123') == 'abc ⾗ 123'
        assert pangu.spacing('abc ⾗ 123') == 'abc ⾗ 123'

    def test_hiragana(self):
        assert pangu.spacing('abcあ123') == 'abc あ 123'
        assert pangu.spacing('abc あ 123') == 'abc あ 123'

    def test_katakana(self):
        assert pangu.spacing('abcア123') == 'abc ア 123'
        assert pangu.spacing('abc ア 123') == 'abc ア 123'

    def test_bopomofo(self):
        assert pangu.spacing('abcㄅ123') == 'abc ㄅ 123'
        assert pangu.spacing('abc ㄅ 123') == 'abc ㄅ 123'

    def test_enclosed_cjk_letters_and_months(self):
        assert pangu.spacing('abc㈱123') == 'abc ㈱ 123'
        assert pangu.spacing('abc ㈱ 123') == 'abc ㈱ 123'

    def test_cjk_unified_ideographs_extension_a(self):
        assert pangu.spacing('abc㐂123') == 'abc 㐂 123'
        assert pangu.spacing('abc 㐂 123') == 'abc 㐂 123'

    def test_cjk_unified_ideographs(self):
        assert pangu.spacing('abc丁123') == 'abc 丁 123'
        assert pangu.spacing('abc 丁 123') == 'abc 丁 123'

    def test_cjk_compatibility_ideographs(self):
        assert pangu.spacing('abc車123') == 'abc 車 123'
        assert pangu.spacing('abc 車 123') == 'abc 車 123'

    def test_dollar(self):
        assert pangu.spacing('前面$後面') == '前面 $ 後面'
        assert pangu.spacing('前面 $ 後面') == '前面 $ 後面'
        assert pangu.spacing('前面$100後面') == '前面 $100 後面'

    def test_percent(self):
        assert pangu.spacing('前面%後面') == '前面 % 後面'
        assert pangu.spacing('前面 % 後面') == '前面 % 後面'
        assert pangu.spacing('前面100%後面') == '前面 100% 後面'
        assert pangu.spacing('新八的構造成分有95%是眼鏡、3%是水、2%是垃圾') == '新八的構造成分有 95% 是眼鏡、3% 是水、2% 是垃圾'

    def test_caret(self):
        assert pangu.spacing('前面^後面') == '前面 ^ 後面'
        assert pangu.spacing('前面 ^ 後面') == '前面 ^ 後面'

    def test_ampersand(self):
        assert pangu.spacing('前面&後面') == '前面 & 後面'
        assert pangu.spacing('前面 & 後面') == '前面 & 後面'
        assert pangu.spacing('Vinta&Mollie') == 'Vinta&Mollie'
        assert pangu.spacing('Vinta&陳上進') == 'Vinta & 陳上進'
        assert pangu.spacing('陳上進&Vinta') == '陳上進 & Vinta'
        assert pangu.spacing('得到一個A&B的結果') == '得到一個 A&B 的結果'

    def test_asterisk(self):
        assert pangu.spacing('前面*後面') == '前面 * 後面'
        assert pangu.spacing('前面 * 後面') == '前面 * 後面'
        assert pangu.spacing('Vinta*Mollie') == 'Vinta*Mollie'
        assert pangu.spacing('Vinta*陳上進') == 'Vinta * 陳上進'
        assert pangu.spacing('陳上進*Vinta') == '陳上進 * Vinta'
        assert pangu.spacing('得到一個A*B的結果') == '得到一個 A*B 的結果'

    def test_minus(self):
        assert pangu.spacing('前面-後面') == '前面 - 後面'
        assert pangu.spacing('前面 - 後面') == '前面 - 後面'
        assert pangu.spacing('Vinta-Mollie') == 'Vinta-Mollie'
        assert pangu.spacing('Vinta-陳上進') == 'Vinta - 陳上進'
        assert pangu.spacing('陳上進-Vinta') == '陳上進 - Vinta'
        assert pangu.spacing('得到一個A-B的結果') == '得到一個 A-B 的結果'
        assert pangu.spacing('长者的智慧和复杂的维斯特洛- 文章') == '长者的智慧和复杂的维斯特洛 - 文章'

    def test_equal(self):
        assert pangu.spacing('前面=後面') == '前面 = 後面'
        assert pangu.spacing('前面 = 後面') == '前面 = 後面'
        assert pangu.spacing('Vinta=Mollie') == 'Vinta=Mollie'
        assert pangu.spacing('Vinta=陳上進') == 'Vinta = 陳上進'
        assert pangu.spacing('陳上進=Vinta') == '陳上進 = Vinta'
        assert pangu.spacing('得到一個A=B的結果') == '得到一個 A=B 的結果'

    def test_plus(self):
        assert pangu.spacing('前面+後面') == '前面 + 後面'
        assert pangu.spacing('前面 + 後面') == '前面 + 後面'
        assert pangu.spacing('Vinta+Mollie') == 'Vinta+Mollie'
        assert pangu.spacing('Vinta+陳上進') == 'Vinta + 陳上進'
        assert pangu.spacing('陳上進+Vinta') == '陳上進 + Vinta'
        assert pangu.spacing('得到一個A+B的結果') == '得到一個 A+B 的結果'
        assert pangu.spacing('得到一個C++的結果') == '得到一個 C++ 的結果'

    def test_pipe(self):
        assert pangu.spacing('前面|後面') == '前面 | 後面'
        assert pangu.spacing('前面 | 後面') == '前面 | 後面'
        assert pangu.spacing('Vinta|Mollie') == 'Vinta|Mollie'
        assert pangu.spacing('Vinta|陳上進') == 'Vinta | 陳上進'
        assert pangu.spacing('陳上進|Vinta') == '陳上進 | Vinta'
        assert pangu.spacing('得到一個A|B的結果') == '得到一個 A|B 的結果'

    def test_backslash(self):
        assert pangu.spacing('前面\\後面') == '前面 \\ 後面'
        assert pangu.spacing('前面 \\ 後面') == '前面 \\ 後面'

    def test_slash(self):
        assert pangu.spacing('前面/後面') == '前面 / 後面'
        assert pangu.spacing('前面 / 後面') == '前面 / 後面'
        assert pangu.spacing('Vinta/Mollie') == 'Vinta/Mollie'
        assert pangu.spacing('Vinta/陳上進') == 'Vinta / 陳上進'
        assert pangu.spacing('陳上進/Vinta') == '陳上進 / Vinta'
        assert pangu.spacing('Mollie/陳上進/Vinta') == 'Mollie / 陳上進 / Vinta'

        assert pangu.spacing('得到一個A/B的結果') == '得到一個 A/B 的結果'
        assert pangu.spacing('2016-12-26(奇幻电影节) / 2017-01-20(美国) / 詹姆斯麦卡沃伊') == '2016-12-26 (奇幻电影节) / 2017-01-20 (美国) / 詹姆斯麦卡沃伊'
        assert pangu.spacing('/home/和/root是Linux中的頂級目錄') == '/home/ 和 /root 是 Linux 中的頂級目錄'
        assert pangu.spacing('當你用cat和od指令查看/dev/random和/dev/urandom的內容時') == '當你用 cat 和 od 指令查看 /dev/random 和 /dev/urandom 的內容時'

    def test_less_than(self):
        assert pangu.spacing('前面<後面') == '前面 < 後面'
        assert pangu.spacing('前面 < 後面') == '前面 < 後面'
        assert pangu.spacing('Vinta<Mollie') == 'Vinta<Mollie'
        assert pangu.spacing('Vinta<陳上進') == 'Vinta < 陳上進'
        assert pangu.spacing('陳上進<Vinta') == '陳上進 < Vinta'

        assert pangu.spacing('得到一個A<B的結果') == '得到一個 A<B 的結果'

    def test_greater_than(self):
        assert pangu.spacing('前面>後面') == '前面 > 後面'
        assert pangu.spacing('前面 > 後面') == '前面 > 後面'
        assert pangu.spacing('Vinta>Mollie') == 'Vinta>Mollie'
        assert pangu.spacing('Vinta>陳上進') == 'Vinta > 陳上進'
        assert pangu.spacing('陳上進>Vinta') == '陳上進 > Vinta'
        assert pangu.spacing('得到一個A>B的結果') == '得到一個 A>B 的結果'

        assert pangu.spacing('得到一個A>B的結果') == '得到一個 A>B 的結果'

    # 只加左空格

    def test_at(self):
        # https://twitter.com/vinta
        # https://www.weibo.com/vintalines
        assert pangu.spacing('請@vinta吃大便') == '請 @vinta 吃大便'
        assert pangu.spacing('請@陳上進 吃大便') == '請 @陳上進 吃大便'

    def test_hash(self):
        assert pangu.spacing('前面#後面') == '前面 #後面'
        assert pangu.spacing('前面C#後面') == '前面 C# 後面'
        assert pangu.spacing('前面#H2G2後面') == '前面 #H2G2 後面'
        assert pangu.spacing('前面 #銀河便車指南 後面') == '前面 #銀河便車指南 後面'
        assert pangu.spacing('前面#銀河便車指南 後面') == '前面 #銀河便車指南 後面'
        assert pangu.spacing('前面#銀河公車指南 #銀河拖吊車指南 後面') == '前面 #銀河公車指南 #銀河拖吊車指南 後面'

    # 只加右空格

    def test_triple_dot(self):
        assert pangu.spacing('前面...後面') == '前面... 後面'
        assert pangu.spacing('前面..後面') == '前面.. 後面'

    def test_u2026(self):
        assert pangu.spacing('前面…後面') == '前面… 後面'
        assert pangu.spacing('前面……後面') == '前面…… 後面'

    # 換成全形符號

    def test_tilde(self):
        assert pangu.spacing('前面~後面') == '前面～後面'
        assert pangu.spacing('前面 ~ 後面') == '前面～後面'
        assert pangu.spacing('前面~ 後面') == '前面～後面'
        assert pangu.spacing('前面 ~後面') == '前面～後面'

    def test_exclamation_mark(self):
        assert pangu.spacing('前面!後面') == '前面！後面'
        assert pangu.spacing('前面 ! 後面') == '前面！後面'
        assert pangu.spacing('前面! 後面') == '前面！後面'
        assert pangu.spacing('前面 !後面') == '前面！後面'

    def test_semicolon(self):
        assert pangu.spacing('前面;後面') == '前面；後面'
        assert pangu.spacing('前面 ; 後面') == '前面；後面'
        assert pangu.spacing('前面; 後面') == '前面；後面'
        assert pangu.spacing('前面 ;後面') == '前面；後面'

    def test_colon(self):
        assert pangu.spacing('前面:後面') == '前面：後面'
        assert pangu.spacing('前面 : 後面') == '前面：後面'
        assert pangu.spacing('前面: 後面') == '前面：後面'
        assert pangu.spacing('前面 :後面') == '前面：後面'
        assert pangu.spacing('電話:123456789') == '電話：123456789'
        assert pangu.spacing('前面:)後面') == '前面：) 後面'
        assert pangu.spacing('前面:I have no idea後面') == '前面：I have no idea 後面'
        assert pangu.spacing('前面: I have no idea後面') == '前面: I have no idea 後面'

    def test_comma(self):
        assert pangu.spacing('前面,後面') == '前面，後面'
        assert pangu.spacing('前面 , 後面') == '前面，後面'
        assert pangu.spacing('前面, 後面') == '前面，後面'
        assert pangu.spacing('前面 ,後面') == '前面，後面'
        assert pangu.spacing('前面,') == '前面，'
        assert pangu.spacing('前面, ') == '前面，'

    def test_period(self):
        assert pangu.spacing('前面.後面') == '前面。後面'
        assert pangu.spacing('前面 . 後面') == '前面。後面'
        assert pangu.spacing('前面. 後面') == '前面。後面'
        assert pangu.spacing('前面 .後面') == '前面。後面'
        assert pangu.spacing('黑人問號.jpg 後面') == '黑人問號.jpg 後面'

    def test_question_mark(self):
        assert pangu.spacing('前面?後面') == '前面？後面'
        assert pangu.spacing('前面 ? 後面') == '前面？後面'
        assert pangu.spacing('前面? 後面') == '前面？後面'
        assert pangu.spacing('前面 ?後面') == '前面？後面'
        assert pangu.spacing('所以，請問Jackey的鼻子有幾個?3.14個') == '所以，請問 Jackey 的鼻子有幾個？3.14 個'

    def test_u00b7(self):
        assert pangu.spacing('前面·後面') == '前面・後面'
        assert pangu.spacing('喬治·R·R·馬丁') == '喬治・R・R・馬丁'
        assert pangu.spacing('M·奈特·沙马兰') == 'M・奈特・沙马兰'

    def test_u2022(self):
        assert pangu.spacing('前面•後面') == '前面・後面'
        assert pangu.spacing('喬治•R•R•馬丁') == '喬治・R・R・馬丁'
        assert pangu.spacing('M•奈特•沙马兰') == 'M・奈特・沙马兰'

    def test_u2027(self):
        assert pangu.spacing('前面‧後面') == '前面・後面'
        assert pangu.spacing('喬治‧R‧R‧馬丁') == '喬治・R・R・馬丁'
        assert pangu.spacing('M‧奈特‧沙马兰') == 'M・奈特・沙马兰'

    # 成對符號：相異

    def test_less_than_and_greater_than(self):
        assert pangu.spacing('前面<中文123漢字>後面') == '前面 <中文 123 漢字> 後面'
        assert pangu.spacing('前面<中文123>後面') == '前面 <中文 123> 後面'
        assert pangu.spacing('前面<123漢字>後面') == '前面 <123 漢字> 後面'
        assert pangu.spacing('前面<中文123漢字> tail') == '前面 <中文 123 漢字> tail'
        assert pangu.spacing('head <中文123漢字>後面') == 'head <中文 123 漢字> 後面'
        assert pangu.spacing('head <中文123漢字> tail') == 'head <中文 123 漢字> tail'

    def test_parentheses(self):
        assert pangu.spacing('前面(中文123漢字)後面') == '前面 (中文 123 漢字) 後面'
        assert pangu.spacing('前面(中文123)後面') == '前面 (中文 123) 後面'
        assert pangu.spacing('前面(123漢字)後面') == '前面 (123 漢字) 後面'
        assert pangu.spacing('前面(中文123) tail') == '前面 (中文 123) tail'
        assert pangu.spacing('head (中文123漢字)後面') == 'head (中文 123 漢字) 後面'
        assert pangu.spacing('head (中文123漢字) tail') == 'head (中文 123 漢字) tail'
        assert pangu.spacing('(or simply "React")') == '(or simply "React")'
        assert pangu.spacing("OperationalError: (2006, 'MySQL server has gone away')") == "OperationalError: (2006, 'MySQL server has gone away')"
        assert pangu.spacing('我看过的电影(1404)') == '我看过的电影 (1404)'
        assert pangu.spacing('Chang Stream(变更记录流)是指collection(数据库集合)的变更事件流') == 'Chang Stream (变更记录流) 是指 collection (数据库集合) 的变更事件流'

    def test_braces(self):
        assert pangu.spacing('前面{中文123漢字}後面') == '前面 {中文 123 漢字} 後面'
        assert pangu.spacing('前面{中文123}後面') == '前面 {中文 123} 後面'
        assert pangu.spacing('前面{123漢字}後面') == '前面 {123 漢字} 後面'
        assert pangu.spacing('前面{中文123漢字} tail') == '前面 {中文 123 漢字} tail'
        assert pangu.spacing('head {中文123漢字}後面') == 'head {中文 123 漢字} 後面'
        assert pangu.spacing('head {中文123漢字} tail') == 'head {中文 123 漢字} tail'

    def test_brackets(self):
        assert pangu.spacing('前面[中文123漢字]後面') == '前面 [中文 123 漢字] 後面'
        assert pangu.spacing('前面[中文123]後面') == '前面 [中文 123] 後面'
        assert pangu.spacing('前面[123漢字]後面') == '前面 [123 漢字] 後面'
        assert pangu.spacing('前面[中文123漢字] tail') == '前面 [中文 123 漢字] tail'
        assert pangu.spacing('head [中文123漢字]後面') == 'head [中文 123 漢字] 後面'
        assert pangu.spacing('head [中文123漢字] tail') == 'head [中文 123 漢字] tail'

    def test_u201c_u201d(self):
        assert pangu.spacing('前面“中文123漢字”後面') == '前面 “中文 123 漢字” 後面'

    # 成對符號：相同

    def test_back_quote_back_quote(self):
        assert pangu.spacing('前面`中間`後面') == '前面 `中間` 後面'

    def test_hash_hash(self):
        assert pangu.spacing('前面#H2G2#後面') == '前面 #H2G2# 後面'
        assert pangu.spacing('前面#銀河閃電霹靂車指南#後面') == '前面 #銀河閃電霹靂車指南# 後面'

    def test_quote_quote(self):
        assert pangu.spacing('前面"中文123漢字"後面') == '前面 "中文 123 漢字" 後面'
        assert pangu.spacing('前面"中文123"後面') == '前面 "中文 123" 後面'
        assert pangu.spacing('前面"123漢字"後面') == '前面 "123 漢字" 後面'
        assert pangu.spacing('前面"中文123" tail') == '前面 "中文 123" tail'
        assert pangu.spacing('head "中文123漢字"後面') == 'head "中文 123 漢字" 後面'
        assert pangu.spacing('head "中文123漢字" tail') == 'head "中文 123 漢字" tail'

    def test_single_quote_single_quote(self):
        assert pangu.spacing("Why are Python's 'private' methods not actually private?") == "Why are Python's 'private' methods not actually private?"
        assert pangu.spacing("陳上進 likes 林依諾's status.") == "陳上進 likes 林依諾's status."
        assert pangu.spacing("举个栗子，如果一道题只包含'A' ~ 'Z'意味着字符集大小是") == "举个栗子，如果一道题只包含 'A' ~ 'Z' 意味着字符集大小是"

    def test_u05f4_u05f4(self):
        assert pangu.spacing('前面״中間״後面') == '前面 ״中間״ 後面'

    # 英文與符號

    def test_alphabets_u201c_u201d(self):
        assert pangu.spacing('阿里云开源“计算王牌”Blink，实时计算时代已来') == '阿里云开源 “计算王牌” Blink，实时计算时代已来'
        assert pangu.spacing('苹果撤销Facebook“企业证书”后者股价一度短线走低') == '苹果撤销 Facebook “企业证书” 后者股价一度短线走低'
        assert pangu.spacing('【UCG中字】“數毛社”DF的《戰神4》全新演示解析') == '【UCG 中字】“數毛社” DF 的《戰神 4》全新演示解析'

    def test_parentheses_percent(self):
        assert pangu.spacing("丹寧控注意Levi's全館任2件25%OFF滿額再享85折！") == "丹寧控注意 Levi's 全館任 2 件 25% OFF 滿額再享 85 折！"


class TestSpacingText(TestPangu):

    def test_spacing_text(self):
        assert pangu.spacing_text('請使用uname -m指令來檢查你的Linux作業系統是32位元或是[敏感词已被屏蔽]位元') == '請使用 uname -m 指令來檢查你的 Linux 作業系統是 32 位元或是 [敏感词已被屏蔽] 位元'


class TestSpacingFile(TestPangu):

    def test_spacing_file(self):
        filepath = get_fixture_path('test_file.txt')
        assert pangu.spacing_file(filepath) == '老婆餅裡面沒有老婆，JavaScript 裡面也沒有 Java'
