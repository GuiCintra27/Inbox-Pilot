from __future__ import annotations

from app.core.redaction import redact_provider_input


def test_redaction_masks_sensitive_identifiers_with_stable_tokens() -> None:
    result = redact_provider_input(
        (
            "Contato maria@example.com, telefone +55 11 99999-1234, "
            "CPF 123.456.789-09, CNPJ 12.345.678/0001-90, pedido 9981 e ticket ABC-123."
        ),
        enabled=True,
    )

    assert "[EMAIL]" in result.text
    assert "[PHONE]" in result.text
    assert "[CPF]" in result.text
    assert "[CNPJ]" in result.text
    assert "[OP_ID]" in result.text
    assert result.counts["email"] == 1
    assert result.counts["phone"] == 1
    assert result.counts["cpf"] == 1
    assert result.counts["cnpj"] == 1
    assert result.counts["op_id"] == 2


def test_redaction_can_be_disabled() -> None:
    original = "contato maria@example.com e pedido 9981"
    result = redact_provider_input(original, enabled=False)

    assert result.text == original
    assert result.counts == {}

