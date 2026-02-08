import pyautogui
import time
import sys
from pynput import keyboard  # pynputライブラリを使用

# --- 設定項目 ---

# ▼ クリックしたい座標 (X, Y) を指定してください
CLICK_X = 500
CLICK_Y = 500

# ▼ クリック間隔（秒）
INTERVAL = 0.2

# ▼ プログラムを終了するためのキー（'q' などの単一の文字）
STOP_KEY = 'q'

# -----------------

# 終了フラグ（グローバル変数）
stop_program = False

def on_press(key):
    """ キーが押された時に呼び出される関数 """
    global stop_program
    try:
        # 押されたキーが設定したSTOP_KEYかチェック
        if key.char == STOP_KEY:
            print(f"\n'{STOP_KEY}' キーが検出されました。プログラムを終了します。")
            stop_program = True
            # リスナーを停止して、プログラムが終了できるようにする
            return False
    except AttributeError:
        # 'q' 以外（Shiftキーなど）の特殊キーが押された場合は無視
        pass

def main():
    print("--- クリック自動化プログラム開始 ---")
    print(f"座標 ({CLICK_X}, {CLICK_Y}) を {INTERVAL} 秒ごとにクリックします。")
    print(f"（どのウィンドウがアクティブでも）'{STOP_KEY}' キーを押すと終了します。")
    print("---------------------------------")
    
    # フェイルセーフ機能（画面左上隅にマウスを移動で強制停止）
    pyautogui.FAILSAFE = True

    # キーボードリスナーを別スレッド（バックグラウンド）で開始
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        # 終了フラグ（stop_program）が True になるまでループ
        while not stop_program:
            
            # 指定した座標で左クリックを実行
            pyautogui.click(CLICK_X, CLICK_Y)
            
            # 終了フラグをチェックしながら待機
            wait_time = INTERVAL
            while wait_time > 0 and not stop_program:
                time.sleep(0.1)
                wait_time -= 0.1

    except pyautogui.FailSafeException:
        print("\n緊急停止（フェイルセーフ）が作動しました。プログラムを終了します。")
    except KeyboardInterrupt:
        print("\nプログラムが手動で中断されました。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    finally:
        if listener.is_alive():
            listener.stop()
        print("--- プログラム終了 ---")

if __name__ == "__main__":
    main()