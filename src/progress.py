from src.db import get_connection

# -------------------------
# SAVE NOTES COMPLETION
# -------------------------
def mark_notes_completed(email, main_topic, chapter, subtopic):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO user_progress
        (email, main_topic, chapter, subtopic, notes_completed)
        VALUES (%s, %s, %s, %s, TRUE)
        ON DUPLICATE KEY UPDATE notes_completed = TRUE
    """, (email, main_topic, chapter, subtopic))

    conn.commit()
    conn.close()


# -------------------------
# SAVE SUBTOPIC QUIZ SCORE
# -------------------------
def save_subtopic_quiz_score(email, main_topic, chapter, subtopic, score):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO user_progress
        (email, main_topic, chapter, subtopic, subtopic_quiz_score)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE subtopic_quiz_score = %s
    """, (email, main_topic, chapter, subtopic, score, score))

    conn.commit()
    conn.close()


# -------------------------
# SAVE CHAPTER QUIZ SCORE
# -------------------------
def save_chapter_quiz_score(email, main_topic, chapter, score):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        UPDATE user_progress
        SET chapter_quiz_score = %s
        WHERE email = %s AND main_topic = %s AND chapter = %s
    """, (score, email, main_topic, chapter))

    conn.commit()
    conn.close()
