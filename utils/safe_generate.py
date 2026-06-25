def safe_generate(func, *args):
    try:
        return func(*args)

    except Exception as e:
        return f"""
# ❌ Agent Error

{str(e)}
"""