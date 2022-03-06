# coding: utf -8
import PySimpleGUI as sg  # ライブラリの読み込み
from googletrans import Translator
import trim
import ocr

# テーマの設定
# sg.theme("Dark Blue 3 ")

# ドメイン設定
L1 = [
	# 暗号利用モード
	[sg.Button("実行", border_width=4, size=(30, 2), key="trans_start")]
	]
L2 = [
	# 翻訳前
	[sg.Multiline(default_text="",
				  text_color="#000000",
				  background_color="#ffffff",
				  size=(80, 50),
				  key="-INPUT_TXT-")]
	]
L3 = [
	# 翻訳後
	[sg.Multiline(default_text="",
				  text_color="#000000",
				  # background_color="#ffff00",
				  size=(80, 50),
				  key="-OUTPUT_TXT-")]
	]

L = [[sg.Frame("翻訳処理の開始",L1)],
	[sg.Frame("翻訳前",L2),sg.Frame("翻訳後",L3)]]


# ウィンドウ作成
window = sg.Window("AES_TOOL ", L)


def main():
	# イベントループ
	while True:
		# イベントの読み取り（イベント待ち）
		event, values = window.read()
		all_input_txt = ""
		all_output_txt = ""
		if event == "trans_start":
			# ドラッグ領域の取得
			rtn_inf = trim.main()
			print("終了")
			for i , capture_inf in enumerate(rtn_inf):
				# ドラッグした領域の数だけキャプチャ、文字抽出
				ocr.ScreenShot(capture_inf['start_x'],
							capture_inf['start_y'],
							capture_inf['end_x'] - capture_inf['start_x'],
							capture_inf['end_y'] - capture_inf['start_y'])
				# 抽出した文字列の翻訳
				input_txt = ocr.TranslationActors()
				output_txt = translation(input_txt)
				# 出力データ更新
				all_input_txt += "/* ドラッグ領域(" + str(i + 1) + ") */\n" + input_txt + "\n\n"
				all_output_txt += "/* ドラッグ領域(" + str(i + 1) + ") */\n" + output_txt + "\n\n"
			# 画面上の表示を更新
			window["-INPUT_TXT-"].Update(all_input_txt)
			window["-OUTPUT_TXT-"].Update(all_output_txt)
		# 終了条件（ None: クローズボタン）
		elif event is None:
			break
	# 終了処理
	window.close()


def translation(trans_data):
	tr = Translator()
	result = tr.translate(trans_data, src="en", dest="ja").text
	return result


if __name__ == "__main__":
	main()