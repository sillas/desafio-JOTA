import json
import sys


def validate_json(json_data: dict[str, str]) -> tuple[bool, str]:
    """
    Função que valida o artigo recebido,
    verificando tamanho do pacote e campos obrigatórios.

    Args:
        json_data (dict): O artigo a ser validado.

    Returns:
        tuple (bool, str): O primeiro elemento indica se houve um erro na validação, e o segundo explica o resultado.
    """

    # 1. Verificar o tamanho do JSON
    try:
        json_string = json.dumps(json_data, ensure_ascii=False)
        json_size_kb = sys.getsizeof(json_string) / 1024
        if json_size_kb > 255:
            return True, f"O JSON excede o tamanho máximo permitido de 255 KB. Tamanho atual: {json_size_kb:.2f} KB."

    except TypeError:
        return True, "Erro ao serializar o JSON. Verifique se o objeto é serializável."

    # 2. Verificar campos obrigatórios
    required_fields = {
        "title": {"type": str, "max_length": 150},
        "subtitle": {"type": str, "max_length": 300},
        "article": {"type": str}
    }

    for field, rules in required_fields.items():
        if field not in json_data:
            return True, f"Campo obrigatório '{field}' não encontrado."

        field_value = json_data[field]

        if (not isinstance(field_value, rules["type"])):
            return True, f"Campo '{field}' deve ser do tipo {rules['type'].__name__}."

        if ("max_length" in rules and len(field_value) > rules["max_length"]):
            return True, f"Campo '{field}' excede o comprimento máximo de {rules['max_length']} caracteres."

    return False, "success"
