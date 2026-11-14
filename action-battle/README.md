# アクションバトル（試作 v0.1）

見下ろし視点で円形の草原を自由に動き、通常攻撃とスキルを組み合わせて、敵の群れと戦う試作です。
武器は md-forge の鍛造で作ったものを持ち込みます。武器・スキル・動作は、QR コードか文字列で別の端末へ渡せます。

- 本体：`index.html`（単体で動きます）
- 定義：`definitions.md`（主人公・通常攻撃・武器種・スキル・敵・ウェーブ）
- QR の生成：`lib/qrcode.js`（qrcode-generator 1.4.4、MIT）

## 遊び方

1. `action-battle/index.html` を開くと「持ち込み」の画面が出ます。
2. 武器を選びます。
   - **鍛造のセーブから読む**：同じ端末・同じアドレス（オリジン）で md-forge を遊んでいれば、装備中の武器を持ち込みます。md-forge のセーブ（`mdforge.save.v1`）は読むだけで、書き込みません。
   - 持ち込みが無いときは、仮の「見習いの大剣」で遊べます。
3. スキル枠 1・枠 2 と、通常攻撃の動作を選んで「戦う」を押します。
4. 3 ウェーブの敵をすべて倒すとクリアです。HP が 0 になると負けです。どちらからも、その場でやり直せます。

## 操作

| | パソコン | スマートフォン |
| --- | --- | --- |
| 移動 | WASD・矢印キー | 左下の仮想ジョイスティック（画面の左側をさわる） |
| 通常攻撃（3 段） | J・Z・マウスのクリック | 右下の「攻撃」 |
| スキル枠 1 | K・X | 右下の小さいボタン（名前は装備中のスキル） |
| スキル枠 2 | L・C | 右下の小さいボタン |
| 最初から | R・右上「最初から」 | 右上「最初から」 |
| 持ち込みを開く | 右上「持ち込み」 | 右上「持ち込み」 |

- 攻撃を続けて押すと、1 段目 → 2 段目 → 3 段目と進みます。3 段目は重く、ノックバックが大きくなります。
- 攻撃するときは、射程の中で一番近い敵のほうを向きます。いなければ、今の向きへ振ります。
- 敵に当てるたびにコンボが増えます。「コンボ継続秒数」のあいだ当てないと 0 に戻ります。

## definitions.md の書き方

`## 見出し` の下の Markdown の表を読みます。見出しと列の名前は変えずに、数値だけ書き換えてください。
再読み込みすると反映されます。読めないとき（ファイルを直接開いたときなど）は、`index.html` の中の同じ初期値で動きます。

| 見出し | 内容 |
| --- | --- |
| 主人公 | 体力・移動速度・コンボ継続秒数・被弾後の無敵秒数 |
| 通常攻撃 | 段ごとの倍率（武器の実効攻撃力に掛ける）・射程・角度・ノックバック・ヒットストップ秒 |
| 武器種 | 長剣・大剣・短剣・斧・槍の射程倍率・角度倍率・間隔倍率 |
| スキル | 名前・形（扇形／円形／飛び道具）・範囲・角度・ダメージ倍率・クールダウン秒・ノックバック・追加効果（「なし」か「N秒間速度半分」）・色。上の 2 行が、はじめの枠 1・枠 2 |
| 敵 | 名前・形（スライム／けもの／ゴーレム）・色・体力・移動速度・攻撃・射程・攻撃間隔秒・大きさ |
| ウェーブ | 「ぷるん×2・きばけもの×2」のように、敵の名前と数を「・」でつなぐ |

通常攻撃 1 回の長さは、`0.34 秒 × 武器種の間隔倍率 ÷ 武器の速度 × 動作の秒数`（3 段目だけ 1.25 倍）です。
会心は武器の会心率で判定し、当たるとダメージが 1.5 倍になります。

## QR の部品（WPN・SKL・MOT）

### 共通の形

1. データを JSON にします。
2. CompressionStream の gzip で圧縮し、Base64URL（`+`→`-`、`/`→`_`、`=` なし）の文字列にします。
3. 700 文字ずつに分けて、`種類:番号/総数:データ片` にします（例：`WPN:1/2:H4sI…`）。1 枚でも `WPN:1/1:…` と書きます。分けるのは 8 枚までです。
4. 読み取る側は、順番がばらばらでも受け取ります。そろったら結合して戻します。

取り込むときは、決まった項目だけを取り出し、数値を安全な範囲に丸めます。おかしいデータはエラーを出して取り込みません。
取り込んだものは、この試作の保存領域（localStorage の `mdforge.actionbattle.v1`）に残るので、再読み込みしても使えます。

カメラでの読み取りは、ブラウザが BarcodeDetector に対応しているときだけ使えます（Android の Chrome など。https か localhost が必要）。
対応していないときは、文字列を「取り込む」の欄に貼り付けてください。

### WPN：武器

md-forge の武器と同じ名前の項目です。

| 項目 | 内容 |
| --- | --- |
| v | 形式の版（1） |
| name・type・rarity・match | 名前・武器種（長剣／大剣／短剣／斧／槍）・レアリティ・完成度 |
| atk・spd・crit | 攻撃力・速度・会心率 |
| elem・elemLv | 属性（無／炎／氷／雷／風）と、そのレベル |
| skill・skillVal | パッシブスキルの名前と値（v0.1 では表示だけ） |
| f | 合成で足した値 `{atk, crit, def, skill, count}` |
| outline | 鍛造でできた輪郭 `[[x, y], …]`（48×128 マスの座標） |
| grip | 握る位置 `[x, y]` |
| matColor・hiltColors・kimyaku | 材料の色・持ち手の色 `{guard, grip, wrap}`・輝脈の剣か |

輪郭の点が多いときは、160 点以下に間引きます（形のずれが小さくなるよう、ダグラス・ポイカー法で間引きます）。それでも 8 枚を超えるときは、120 点 → 80 点 → 48 点と減らします。

戦闘への反映：

- 形：輪郭を厚みのある立体にして、右手に持たせます（md-forge の `buildWeaponMesh` と同じ作り方）。
- 通常攻撃のダメージ：実効攻撃力（atk＋f.atk）×段の倍率。
- 振りの間隔：速度と武器種で変わります。
- 会心：crit（＋f.crit）で判定します。
- 属性：通常攻撃の斬撃の色になります。

### SKL：魔法とスキル

| 項目 | 内容 |
| --- | --- |
| v・name・elem | 形式の版・名前・属性 |
| shape | `fan`（前方の扇形）・`circle`（自分のまわり）・`projectile`（飛び道具） |
| range・angle | 範囲（飛び道具は飛ぶ距離）・角度 |
| damage | 武器の実効攻撃力への倍率 |
| cooldown・knockback・color | クールダウン秒・ノックバック・色（`#rrggbb`） |
| duration・slow | 速度を下げる秒数と、下げる割合（0〜0.9。無ければ 0） |
| speed・radius・count | 飛び道具だけ：速さ・当たった所で広がる半径・数（1〜5） |

サンプルの魔法「火球」の文字列：

```
SKL:1/1:H4sIAAAAAAAAEz2NQQ6CQBRD71K3P8YhRpN_my_zQWSYTwaQhXGh7o338GBcw4wm7tq-tL3gDHaEKJ2Csdzey-sBggbtsr8_QRiO0mfaJztpOTZBQUgSawW7giCxDgreELx08k3XO0JpFrzNEbwltNHK9iBl-4fBEhirqtpLISD4KcnYWPwODcHmn-hVPdi5_Oibacj9IvenOILd9QPyxJ27wgAAAA
```

### MOT：動作

VRMA のファイルそのものは大きくて QR に載らないため、短いキーフレームのレシピで表します。

| 項目 | 内容 |
| --- | --- |
| v・name | 形式の版・名前 |
| target | 使う所。v0.1 では `normal`（通常攻撃）だけ |
| duration | 全体の秒数（実際の振りの長さに合わせて伸び縮みします） |
| frames | `[{t: 秒, 骨の名前: [X, Y, Z]（度）}, …]`。骨は hips・spine・rightUpperArm・rightLowerArm・rightHand の 5 つまで |
| hit | 当たる時刻（秒）。無ければ全体の 45% の所 |

キーフレームの間は、なめらかに補います。モデルに無い骨は飛ばします。

サンプルの動作「大振り」の文字列：

```
MOT:1/1:H4sIAAAAAAAAE73RsU7DMBAG4Hf553Nkm9ih3tgYujJVHSzVtJGIE7kuDFUXRsRjIDHyUAieAxkojZtkZTyf7v9s3x73MILgbeNg8PHy-vn89v74BEK0Ye0iDHwbGnsHwmoXbKxbDyMKSdjUEYYXWhNug23cFmaxRzpLvS6VnDjxJWHb1d716lCvN_Gm61y4Cg3Mgs2Ik54dO_P24djhxER5mrm2fvWXc6AfrlA9kInLjEzjTJbjrKgUcZJ8HC7VAGbyjNYys-WZfbrPiJ2ipJqw-dAWKrersmcLndFS0sXEX3_HVFPugM1f_Lv5_9ju8vAFOCDp1J4CAAA
```

「持ち込み」の画面の「サンプル『火球』を入れる」「サンプル『大振り』を入れる」でも、同じ文字列が入ります。

## 主人公

- 既定はサンプル VRM（`../models/VRM1_Constraint_Twist_Sample.vrm`）です。
- 「ミューズさん」は `../models/muse.vrm` を読みます。ファイルが無いときは簡易モデルになります。
- 自分の VRM ファイルを選ぶと、その場で差し替わります（保存はしません）。
- VRM が読めないときは、図形で作った簡易モデルで遊べます。

## クレジット

| もの | 作者 | ライセンス |
| --- | --- | --- |
| three.js 0.160.0 | three.js authors | MIT |
| @pixiv/three-vrm 2.1.0 | pixiv Inc. | MIT |
| qrcode-generator 1.4.4（`lib/qrcode.js`） | Kazuhiko Arase | MIT（`lib/LICENSE-qrcode-generator.txt`） |
| サンプル VRM「VRM1_Constraint_Twist_Sample」 | (c) 2022 pixiv Inc. | VRM Public License 1.0（`../models/README.md`） |
| フォント「でんきチップ」x8y12pxDenkiChip | 作者表記は `../fonts/README.md` | SIL Open Font License 1.1（`../fonts/OFL.txt`） |

「QR コード」は株式会社デンソーウェーブの登録商標です。
敵・地面・木・岩・武器・演出は、すべて three.js の図形で作ったオリジナルです。
