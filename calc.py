def run(args):
    if not args:
        print("Usage: calc <expression>")
        print("Example: calc (5 * 5) / 2")
        return 1

    expression = "".join(args)
    
    # Simple security: block common dangerous keywords
    forbidden = ["import", "os", "sys", "eval", "exec", "open", "write"]
    for word in forbidden:
        if word in expression:
            print("Error: Dangerous keyword detected in expression.")
            return 1

    try:
        # Calculate
        result = eval(expression)
        print(f"\033[96mResult:\033[0m {result}")
        return 0
    except Exception as e:
        print(f"Math Error: {e}")
        return 1
