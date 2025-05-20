import tiktoken


def estimate_token_count(prompt: str, response: str | None) -> dict[str, int]:
    tokenizer = tiktoken.encoding_for_model("gpt-4")
    input_tokens = len(tokenizer.encode(prompt))
    output_tokens = 0 if response is None else len(tokenizer.encode(response))
    return {"input_tokens": input_tokens, "output_tokens": output_tokens} 