import json
from typing import Dict, Any, List

from openai import OpenAI

from .config import OPENAI_API_KEY
from .preprocess import clean_text, split_into_chunks
from .prompt_template import SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)


DEFAULT_MODEL = "gpt-4.1-mini"  # or any available model in your account


def _merge_entities(results: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    merged = {
        "company": [],
        "person": [],
        "ticker": [],
        "event": [],
        "monetary_value": [],
        "date": [],
        "location": [],
        "other": [],
    }

    for r in results:
        for key in merged.keys():
            if key in r and isinstance(r[key], list):
                merged[key].extend(r[key])

    # Deduplicate while preserving order
    for key, values in merged.items():
        seen = set()
        deduped = []
        for v in values:
            if v not in seen:
                seen.add(v)
                deduped.append(v)
        merged[key] = deduped

    return merged


def _call_llm(text: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Calls the LLM and returns the parsed JSON.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
    )

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Basic recovery: try to extract JSON between {} if LLM adds text
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            data = json.loads(raw[start : end + 1])
        else:
            raise ValueError(f"Model output is not valid JSON:\n{raw}")

    return data


def extract_entities_from_text(text: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Full pipeline: clean text, chunk if needed, call LLM, merge results.
    """
    cleaned = clean_text(text)
    chunks = split_into_chunks(cleaned)

    if not chunks:
        return {
            "company": [],
            "person": [],
            "ticker": [],
            "event": [],
            "monetary_value": [],
            "date": [],
            "location": [],
            "other": [],
        }

    results = []
    for chunk in chunks:
        result = _call_llm(chunk, model=model)
        results.append(result)

    return _merge_entities(results)
