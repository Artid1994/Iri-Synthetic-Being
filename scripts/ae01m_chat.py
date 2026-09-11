from runtime.runtime import TranscendingRuntime

runtime = TranscendingRuntime()

print("AE01M v0.1")
print("พิมพ์ exit เพื่อออก")

while True:
    try:
        user_input = input("\nคุณ: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        result = runtime.cognitive.think(user_input)
        print(f"AE01M: {result}")

    except KeyboardInterrupt:
        print("\nหยุดการทำงาน")
        break
