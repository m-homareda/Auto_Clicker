import pyautogui
import time
import sys
import tkinter as tk
from pynput import keyboard

# --- 設定項目 ---

# ▼ クリック間隔（秒）
INTERVAL = 0.1

# ▼ プログラムを終了するためのキー
STOP_KEY = 'q'

# -----------------

stop_program = False
target_pos = (0, 0) # 座標保存用

def get_target_coordinates():
    """
    半透明の全画面ウィンドウを表示し、クリックされた座標を取得する関数
    """
    print("座標設定モード: クリックしたい場所をクリックしてください...")
    
    # tkinterのルートウィンドウ作成
    root = tk.Tk()
    
    # 全画面表示設定
    root.attributes('-fullscreen', True) # フルスクリーン
    root.attributes('-alpha', 0.3)       # 透明度 (0.1~1.0)
    root.configure(bg='black')           # 背景色
    root.lift()                          # 最前面へ
    
    # 説明ラベル
    label = tk.Label(root, text="連打したい場所をクリックしてください", 
                     font=("Helvetica", 30), fg="white", bg="black")
    label.pack(expand=True)

    # クリック時の処理
    def on_click(event):
        global target_pos
        target_pos = (event.x_root, event.y_root)
        root.destroy() # ウィンドウを閉じる

    # マウス左クリック (<Button-1>) をバインド
    root.bind('<Button-1>', on_click)
    
    # 閉じるボタン等で強制終了された場合
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit())

    root.mainloop()
    return target_pos

def on_press(key):
    global stop_program
    try:
        if hasattr(key, 'char') and key.char == STOP_KEY:
            print(f"\n'{STOP_KEY}' キーが検出されました。終了します。")
            stop_program = True
            return False
    except:
        pass

def main():
    # 1. 最初に座標を取得する
    x, y = get_target_coordinates()
    
    print("---------------------------------")
    print(f"設定完了！ 座標 ({x}, {y}) を連打します。")
    print("3秒後に開始します...")
    print(f"中断するには '{STOP_KEY}' キーを押してください。")
    print("---------------------------------")
    
    time.sleep(3) # ユーザーが準備する時間

    # フェイルセーフ（マウスを左上にやると止まる機能）
    pyautogui.FAILSAFE = True

    # キーボード監視開始
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while not stop_program:
            pyautogui.click(x, y)
            
            # 待機処理（終了フラグをこまめにチェック）
            end_time = time.time() + INTERVAL
            while time.time() < end_time:
                if stop_program:
                    break
                time.sleep(0.01) # 短いスリープでCPU負荷を下げる

    except pyautogui.FailSafeException:
        print("\nフェイルセーフ作動（マウス左上）により停止しました。")
    except KeyboardInterrupt:
        print("\n手動停止されました。")
    except Exception as e:
        print(f"\nエラー: {e}")
    finally:
        if listener.is_alive():
            listener.stop()
        print("--- 終了 ---")

if __name__ == "__main__":
    main()