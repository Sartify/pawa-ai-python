from pawa_ai.models.chat import ChatCompletion, ChatMessage, Usage
from pawa_ai.models.embeddings import EmbeddingResponse
from pawa_ai.models.models import ModelList


def test_chat_completion_text_from_string_content():
    completion = ChatCompletion.from_dict(
        {
            "success": True,
            "message": "ok",
            "data": {
                "request": [
                    {"finish_reason": "stop", "message": {"role": "assistant", "content": "Jambo"}}
                ],
                "created": "1",
                "model": "pawa-v1-ember-20240924",
                "object": "chat.request",
            },
        }
    )
    assert completion.text == "Jambo"


def test_chat_message_text_from_parts():
    message = ChatMessage.from_dict(
        {
            "role": "assistant",
            "content": [{"type": "text", "text": "Habari "}, {"type": "text", "text": "yako"}],
        }
    )
    assert message.text == "Habari yako"


def test_embedding_response_parser():
    response = EmbeddingResponse.from_dict(
        {
            "success": True,
            "message": "Embeddings created successfully",
            "data": {"embeddings": [[0.1, 0.2], [0.3, 0.4]]},
        }
    )
    assert response.success is True
    assert len(response.embeddings) == 2


def test_model_list_parser():
    response = ModelList.from_dict(
        {
            "success": True,
            "message": "Models fetched successfully",
            "data": [
                {"id": 1, "name": "pawa-v1-ember-20240924", "modelType": "chat"},
                {"id": 2, "name": "pawa-v1-blaze-20250318", "modelType": "chat"},
            ],
        }
    )
    assert len(response.models) == 2
    assert response.models[0].name == "pawa-v1-ember-20240924"


def test_usage_parser():
    usage = Usage.from_dict({"tokens_in": 12, "tokens_out": 34})
    assert usage is not None
    assert usage.tokens_in == 12
    assert usage.tokens_out == 34
