import streamlit as st


# -----------------------------------------------------------------------------
# セッション状態の初期化
# -----------------------------------------------------------------------------

def init_session_state():
    """ウィザード進行と入力値のための初期化."""
    if "step" not in st.session_state:
        st.session_state.step = 1

    # 各質問の回答を session_state に確保しておく
    for key in [
        # ウィジェットの生の値
        "habit",
        "start_small",
        "confirm_size",
        "anchor_habit",
        "time_fixed",
        "place_fixed",
        "prep",
        "reward",
        # 「次へ進む」を押したタイミングで確定させた値
        "habit_saved",
        "start_small_saved",
        "anchor_saved",
        "time_fixed_saved",
        "place_fixed_saved",
        "prep_saved",
        "reward_saved",
        # 表示用フラグ
        "show_example_2",
        "show_example_4",
        "show_example_7",
    ]:
        st.session_state.setdefault(key, None)


def go_to_step(step_num: int) -> None:
    """ステップを更新し、即座に画面を切り替える（1クリックで次へ進むため）。"""
    st.session_state.step = step_num
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


# -----------------------------------------------------------------------------
# ステップ描画用のヘルパー
# -----------------------------------------------------------------------------

def show_step_1():
    st.header("① 習慣化したいことを入力してください")
    habit = st.text_input("習慣化したいこと", key="habit", placeholder="例：筋トレを習慣にしたい")

    if st.button("次へ進む", key="next_1"):
        if habit and habit.strip():
            st.session_state.habit_saved = habit.strip()
            go_to_step(2)
        else:
            st.warning("まずは、習慣化したいことを一言で書いてみましょう。")


def show_step_2():
    st.header("② 小さく始めるのがコツですが、どこからなら始められそうですか？")
    st.write("「こんなの意味ある？」くらい小さくて大丈夫です。")

    start_small = st.text_input(
        "どこから始められそうですか？",
        key="start_small",
        placeholder="例：腕立て1回だけ、5分だけ本を開く など",
    )

    # 例を見るボタン
    if st.button("例を見る", key="example_2_button"):
        st.session_state.show_example_2 = not bool(st.session_state.get("show_example_2"))

    if st.session_state.get("show_example_2"):
        st.info(
            "例：\n"
            "・ランニング → ランニングウェアに着替えるだけ\n"
            "・ランニング → 外に出て3歩だけ歩く"
        )

    if st.button("次へ進む", key="next_2"):
        if start_small and start_small.strip():
            st.session_state.start_small_saved = start_small.strip()
            go_to_step(3)
        else:
            st.warning("「これならできそう」という小さな一歩を書いてみましょう。")


def show_step_3():
    st.header("③ ここからなら始められそうですか？")

    current = (
        st.session_state.get("start_small_saved")
        or st.session_state.get("start_small")
        or "（まだ入力されていません）"
    )
    st.write("いま考えている一歩：")
    st.info(current)

    st.write("ここからなら始められそうですか？もっと小さくできますか？")
    choice = st.radio(
        "感覚に近い方を選んでください",
        ["このくらいなら始められそう", "もっと小さくしたい"],
        key="confirm_size",
    )

    if st.button("次へ進む", key="next_3"):
        if choice == "このくらいなら始められそう":
            go_to_step(7)
        else:
            st.info("とても良い感覚です。もう一段、小さく優しくしてみましょう。")
            go_to_step(2)


def show_step_4():
    st.header("④ 20秒以内に始めるために、できる準備はありますか？")
    st.write("「始めるまでのハードル」をできるだけ下げておきましょう。")

    prep = st.text_input(
        "20秒以内でできる準備",
        key="prep",
        placeholder="例：前日にウェアを出しておく、道具を机の上に置いておく など",
    )

    if st.button("例を見る", key="example_7_button"):
        st.session_state.show_example_7 = not bool(st.session_state.get("show_example_7"))

    if st.session_state.get("show_example_7"):
        st.info("例：\n・前日にウェアを出しておく\n・道具を机の上に置いておく")

    if st.button("次へ進む", key="next_7"):
        st.session_state.prep_saved = (prep or "").strip()
        go_to_step(8)


def show_step_5():
    st.header("⑤ 実際に行動できた時のご褒美を決めましょう")
    st.write("お金がかからない、小さなご褒美でOKです。")

    reward = st.text_input(
        "ご褒美",
        key="reward",
        placeholder="例：チェックを付ける、好きな音楽を1分聴く など",
    )

    if st.button("次へ進む", key="next_8"):
        st.session_state.reward_saved = (reward or "").strip()
        go_to_step(9)


def show_step_6_summary():
    st.header("⑥ これまでの回答を振り返りましょう")

    # 冒頭にメッセージを表示
    st.write(
        "サボってしまっても、再開すればそれも『継続』です。\n"
        "自分を責めずに、無理なく習慣化していきましょうね。"
    )

    habit = st.session_state.get("habit_saved") or st.session_state.get("habit") or ""
    start_small = (
        st.session_state.get("start_small_saved")
        or st.session_state.get("start_small")
        or ""
    )
    prep = (
        st.session_state.get("prep_saved")
        or st.session_state.get("prep")
        or "（特になし）"
    )
    reward = (
        st.session_state.get("reward_saved")
        or st.session_state.get("reward")
        or "（特になし）"
    )

    st.subheader("今回のテーマとなる習慣")
    st.info(habit or "まだ入力されていません")

    st.subheader("最初の一歩（できるだけ小さく）")
    st.info(start_small or "まだ入力されていません")

    st.subheader("20秒以内に始めるための準備")
    st.write(prep)

    st.subheader("行動できたときのご褒美")
    st.write(reward)

    # 最初からやり直したいときのボタン
    if st.button("もう一度はじめから考えてみる", key="restart"):
        st.session_state.step = 1
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()


# -----------------------------------------------------------------------------
# メインアプリ
# -----------------------------------------------------------------------------


def main():
    st.set_page_config(page_title="『続けられる』習慣メーカー", layout="centered")
    init_session_state()

    st.title("『続けられる』習慣メーカー")
    st.caption("習慣化が苦手な人のための、やさしい一問一答ウィザードです。")

    step = st.session_state.step

    # そのときのステップだけを表示する
    if step == 1:
        show_step_1()
    elif step == 2:
        show_step_2()
    elif step == 3:
        show_step_3()
    elif step == 7:
        show_step_7()
    elif step == 8:
        show_step_8()
    elif step == 9:
        show_step_9_summary()
    else:
        # 想定外の値になっていた場合は最初のステップに戻す
        st.session_state.step = 1
        show_step_1()


if __name__ == "__main__":
    main()
