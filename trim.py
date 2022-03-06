import tkinter
from matplotlib.pyplot import title
import pyautogui  # 外部ライブラリ
from PIL import Image, ImageTk  # 外部ライブラリ
import pprint

from sympy import root
from torch import tile

RESIZE_RETIO = 1.25 # 縮小倍率の規定

g_canvas1 = ""
g_img_resized = ""
g_ctr = 0
g_tag = "rect_0"
g_rtn_inf = []

# メイン処理
def main():
	global g_canvas1
	global g_img_resized
	global g_ctr
	global g_rtn_inf
	global root
	# 初期化
	g_ctr = 0
	g_tag = "rect_0"
	g_rtn_inf = []

	# 表示する画像の取得（スクリーンショット）
	img = pyautogui.screenshot()

	# スクリーンショットした画像は表示しきれないので画像リサイズ
	g_img_resized = img.resize(size=(int(img.width / RESIZE_RETIO),
								   int(img.height / RESIZE_RETIO)),
							 resample=Image.BILINEAR)

	root = tkinter.Toplevel()
	root.attributes("-topmost", True) # tkinterウィンドウを常に最前面に表示
	root.protocol("WM_DELETE_WINDOW", on_closing)
	root.title(u"翻訳領域をドラッグ。ドラッグ完了後は「×」ボタンで閉じる。")


	# tkinterで表示できるように画像変換
	img_tk = ImageTk.PhotoImage(g_img_resized)

	# Canvasウィジェットの描画
	g_canvas1 = tkinter.Canvas(root,
							 bg="black",
							 width=g_img_resized.width,
							 height=g_img_resized.height)
	# Canvasウィジェットに取得した画像を描画
	g_canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)

	# Canvasウィジェットを配置し、各種イベントを設定
	g_canvas1.pack()
	g_canvas1.bind("<ButtonPress-1>", start_point_get)
	g_canvas1.bind("<Button1-Motion>", rect_drawing)
	g_canvas1.bind("<ButtonRelease-1>", release_action)

	root.mainloop()
	print("ループ終了")
	pprint.pprint(g_rtn_inf)

	return g_rtn_inf


# ドラッグ開始した時のイベント
def start_point_get(event):
	global start_x, start_y # グローバル変数に書き込みを行なうため宣言
	# g_canvas1上に四角形を描画（rectangleは矩形の意味）
	g_canvas1.create_rectangle(event.x,
							 event.y,
							 event.x + 1,
							 event.y + 1,
							 outline="red",
							 tag=g_tag)
	# グローバル変数に座標を格納
	start_x, start_y = event.x, event.y


# ドラッグ中のイベント
def rect_drawing(event):
	# ドラッグ中のマウスポインタが領域外に出た時の処理
	if event.x < 0:
		end_x = 0
	else:
		end_x = min(g_img_resized.width, event.x)
	if event.y < 0:
		end_y = 0
	else:
		end_y = min(g_img_resized.height, event.y)

	# g_tagの画像を再描画
	g_canvas1.coords(g_tag, start_x, start_y, end_x, end_y)


# ドラッグを離したときのイベント
def release_action(event):
	global g_rtn_inf
	global g_ctr
	global g_tag
	# g_tagの画像の座標を元の縮尺に戻して取得
	start_x, start_y, end_x, end_y = [
		round(n * RESIZE_RETIO) for n in g_canvas1.coords(g_tag)
	]

	# 開始位置、終了位置の幅確認
	if 10 > abs(start_x - end_x):
		g_canvas1.delete(g_tag)
		return
	if 10 > abs(start_y - end_y):
		g_canvas1.delete(g_tag)
		return

	# 取得した座標を保持
	get_coordinate = { "start_x":start_x , "start_y":start_y , "end_x":end_x , "end_y":end_y }
	g_rtn_inf.append(get_coordinate)
	g_ctr += 1
	g_tag = "rect_"+str(g_ctr)


# 終了処理
def on_closing():
	root.destroy()
	root.quit()


# メイン処理 -
if __name__ == "__main__":
	main()